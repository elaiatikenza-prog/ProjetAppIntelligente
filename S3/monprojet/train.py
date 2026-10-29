"""Entraînement, évaluation et comparaison des modèles pour CantineAI / MaintAI.

Usage : python -m monprojet.train
"""
import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    mean_absolute_error,
    mean_squared_error,
    precision_score,
    r2_score,
    recall_score,
)
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from . import config
from .data import load_data, split
from .models import candidates

HIGHER_IS_BETTER = {
    "accuracy": True,
    "recall": True,
    "precision": True,
    "f1": True,
    "mae": False,
    "rmse": False,
    "r2": True,
}


def build_preprocessing(X: pd.DataFrame) -> ColumnTransformer:
    """Construit le pipeline de préparation des variables.

    - Nombres : imputation par la médiane (ex: repas_semaine_precedente après vacances) et standardisation ;
    - Catégories : imputation par le mode et encodage One-Hot ;
    - Texte : TF-IDF si présent.
    """
    text_cols = [config.TEXT_COLUMN] if config.TEXT_COLUMN else []
    numeric_cols = [
        c for c in X.columns
        if c not in text_cols and pd.api.types.is_numeric_dtype(X[c])
    ]
    categorical_cols = [
        c for c in X.columns
        if c not in text_cols and c not in numeric_cols
    ]

    steps = []
    if numeric_cols:
        steps.append((
            "nombres",
            make_pipeline(SimpleImputer(strategy="median"), StandardScaler()),
            numeric_cols,
        ))
    if categorical_cols:
        steps.append((
            "categories",
            make_pipeline(
                SimpleImputer(strategy="most_frequent"),
                OneHotEncoder(handle_unknown="ignore", sparse_output=False),
            ),
            categorical_cols,
        ))
    if text_cols:
        steps.append(("texte", TfidfVectorizer(), config.TEXT_COLUMN))

    return ColumnTransformer(steps, remainder="drop", sparse_threshold=0)


def evaluate(model, X_test, y_test) -> dict:
    """Évalue le modèle sur le jeu de test et renvoie un dictionnaire de métriques arrondies."""
    pred = model.predict(X_test)
    if config.TASK == "classification":
        avg = "binary" if y_test.nunique() == 2 else "macro"
        return {
            "accuracy": float(round(accuracy_score(y_test, pred), 3)),
            "recall": float(round(recall_score(y_test, pred, average=avg, zero_division=0), 3)),
            "precision": float(round(precision_score(y_test, pred, average=avg, zero_division=0), 3)),
            "f1": float(round(f1_score(y_test, pred, average=avg, zero_division=0), 3)),
        }

    # Régression
    mae = mean_absolute_error(y_test, pred)
    mse = mean_squared_error(y_test, pred)
    rmse = float(np.sqrt(mse))
    r2 = r2_score(y_test, pred)
    return {
        "mae": float(round(mae, 3)),
        "rmse": float(round(rmse, 3)),
        "r2": float(round(r2, 3)),
    }


def main():
    """Entraîne les candidats, compare sur le jeu de test et sauvegarde le meilleur modèle."""
    df = load_data()
    X_train, X_test, y_train, y_test = split(df)

    results_dict = {}
    fitted_models = {}

    for name, estimator in candidates().items():
        pipe = Pipeline([
            ("preparation", build_preprocessing(X_train)),
            ("modele", estimator),
        ])
        pipe.fit(X_train, y_train)
        scores = evaluate(pipe, X_test, y_test)
        results_dict[name] = scores
        fitted_models[name] = pipe

    results_df = pd.DataFrame(results_dict).T
    metric = config.MAIN_METRIC
    if metric not in results_df.columns:
        raise ValueError(f"Métrique principale {metric!r} non trouvée dans les résultats.")

    higher = HIGHER_IS_BETTER.get(metric, True)
    sorted_df = results_df.sort_values(by=metric, ascending=not higher)

    best_name = results_df[metric].idxmax() if higher else results_df[metric].idxmin()

    # Sauvegarde des résultats et du modèle
    config.MODELS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(fitted_models[best_name], config.MODELS_DIR / "model.joblib")

    metrics_payload = {
        "main_metric": metric,
        "best": best_name,
        "results": {name: {k: float(v) for k, v in scores.items()} for name, scores in results_dict.items()},
    }
    (config.MODELS_DIR / "metrics.json").write_text(
        json.dumps(metrics_payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    info_payload = {
        "model_name": best_name,
        "target": config.TARGET,
        "task": config.TASK,
        "main_metric": metric,
        "metrics": metrics_payload["results"][best_name],
        "feature_columns": list(X_train.columns),
        "train_samples": int(len(X_train)),
        "test_samples": int(len(X_test)),
    }
    (config.MODELS_DIR / "model_info.json").write_text(
        json.dumps(info_payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print("\n" + "=" * 65)
    print("TABLEAU DE COMPARAISON DES MODÈLES (Séance 3 - CantineAI)")
    print("=" * 65)
    print(sorted_df.to_string())
    print("-" * 65)
    print(f"Meilleur modèle retenu selon {metric.upper()} : {best_name}")
    print(f"Artefacts enregistrés dans : {config.MODELS_DIR}")
    print("=" * 65 + "\n")

    return results_df


if __name__ == "__main__":
    main()
