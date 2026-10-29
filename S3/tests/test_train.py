"""Tests de l'entraînement, de l'évaluation et de la comparaison (Séance 3)."""
import json

from sklearn.dummy import DummyClassifier, DummyRegressor
from sklearn.pipeline import Pipeline

from monprojet import config
from monprojet.data import load_data, split
from monprojet.train import HIGHER_IS_BETTER, build_preprocessing, evaluate, main


def test_evaluate_renvoie_la_metrique_principale():
    X_train, X_test, y_train, y_test = split(load_data())
    dummy = DummyClassifier() if config.TASK == "classification" else DummyRegressor()
    model = Pipeline([
        ("preparation", build_preprocessing(X_train)),
        ("modele", dummy),
    ]).fit(X_train, y_train)
    scores = evaluate(model, X_test, y_test)
    assert isinstance(scores, dict), "evaluate() doit renvoyer un dictionnaire"
    assert config.MAIN_METRIC in scores, f"evaluate() doit contenir la métrique principale : {config.MAIN_METRIC}"
    assert isinstance(scores[config.MAIN_METRIC], float), "La métrique doit être un float"


def test_main_ecrit_les_resultats():
    main()
    metrics_file = config.MODELS_DIR / "metrics.json"
    assert metrics_file.exists(), "metrics.json doit exister dans models/"
    metrics = json.loads(metrics_file.read_text(encoding="utf-8"))
    assert {"main_metric", "best", "results"} <= set(metrics), \
        "metrics.json doit contenir 'main_metric', 'best' et 'results'"
    assert (config.MODELS_DIR / "model.joblib").exists(), \
        "Le meilleur modèle doit être sauvegardé dans model.joblib"


def test_le_meilleur_modele_bat_la_baseline():
    main()
    metrics = json.loads((config.MODELS_DIR / "metrics.json").read_text(encoding="utf-8"))
    results, metric = metrics["results"], metrics["main_metric"]
    baseline_name = next(iter(results))
    baseline_score = results[baseline_name][metric]
    best_score = results[metrics["best"]][metric]

    higher = HIGHER_IS_BETTER.get(metric, True)
    if higher:
        assert best_score > baseline_score, "Le meilleur modèle doit dépasser la baseline"
    else:
        assert best_score < baseline_score, "Le meilleur modèle doit avoir une erreur inférieure à la baseline"


# --- Tests complémentaires ajoutés par le groupe (Pour aller plus loin) ---

def test_evaluate_regression_metrics_complete():
    """Vérifie que pour une tâche de régression, MAE, RMSE et R2 sont toutes calculées."""
    df = load_data()
    X_train, X_test, y_train, y_test = split(df)
    dummy = DummyRegressor(strategy="mean")
    pipe = Pipeline([("prep", build_preprocessing(X_train)), ("mod", dummy)]).fit(X_train, y_train)
    scores = evaluate(pipe, X_test, y_test)
    assert "mae" in scores and "rmse" in scores and "r2" in scores
    assert scores["mae"] >= 0 and scores["rmse"] >= 0


def test_preprocessing_handles_missing_values_and_categories():
    """Vérifie que le préprocesseur gère les NaN de repas_semaine_precedente et encode les menus."""
    df = load_data()
    X_train, X_test, _, _ = split(df)
    prep = build_preprocessing(X_train)
    transformed_train = prep.fit_transform(X_train)
    transformed_test = prep.transform(X_test)
    assert transformed_train.shape[1] > 0
    assert transformed_test.shape[1] == transformed_train.shape[1]


def test_meilleur_modele_reduit_l_erreur_d_au_moins_trente_pourcent():
    """Critère d'acceptation métier : l'erreur MAE doit être réduite de plus de 30% par rapport à la baseline."""
    metrics = json.loads((config.MODELS_DIR / "metrics.json").read_text(encoding="utf-8"))
    results = metrics["results"]
    baseline_mae = results["baseline (moyenne)"]["mae"]
    best_mae = results[metrics["best"]]["mae"]
    reduction_pct = (baseline_mae - best_mae) / baseline_mae * 100
    assert reduction_pct >= 30.0, f"Réduction de {reduction_pct:.1f}% inférieure au seuil de 30%"
