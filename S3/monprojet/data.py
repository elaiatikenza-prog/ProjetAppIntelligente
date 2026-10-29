"""Chargement et découpage des données pour CantineAI / MaintAI."""
import pandas as pd
from sklearn.model_selection import train_test_split

from . import config


def load_data(path=None) -> pd.DataFrame:
    """Lit le fichier CSV et renvoie un DataFrame.

    Fonctionnalités :
    - Détection automatique du séparateur (virgule ou point-virgule) et encodage ;
    - Vérification de la présence de config.TARGET (lève ValueError sinon) ;
    - Suppression des lignes où la variable cible est manquante.
    """
    csv_path = config.DATA_PATH if path is None else path
    try:
        df = pd.read_csv(csv_path, sep=None, engine="python", encoding="utf-8")
    except Exception:
        try:
            df = pd.read_csv(csv_path, sep=None, engine="python", encoding="latin-1")
        except Exception:
            df = pd.read_csv(csv_path)

    # Cas d'un séparateur ';' non détecté
    if len(df.columns) == 1 and ";" in str(df.columns[0]):
        try:
            df = pd.read_csv(csv_path, sep=";", encoding="latin-1")
        except Exception:
            df = pd.read_csv(csv_path, sep=";")

    if config.TARGET not in df.columns:
        raise ValueError(f"Colonne cible absente : {config.TARGET}")

    df = df.dropna(subset=[config.TARGET]).copy()
    if df.empty:
        raise ValueError("Aucune ligne avec une cible valide.")

    return df


def feature_columns(df: pd.DataFrame) -> list:
    """Retourne la liste des variables prédictives disponibles.

    Exclut impérativement la cible (repas_servis) et la colonne temporelle (date)
    afin d'éviter toute fuite de données (data leakage).
    """
    if config.FEATURES is not None:
        return list(config.FEATURES)
    excluded = {config.TARGET}
    if config.TIME_COLUMN:
        excluded.add(config.TIME_COLUMN)
    return [c for c in df.columns if c not in excluded]


def split(df: pd.DataFrame):
    """Sépare les données en jeu d'entraînement et jeu de test.

    Supporte :
    - 'chronologique' : tri temporel sur TIME_COLUMN, entraînement sur le passé,
      test sur le futur (les derniers 20 %).
    - 'random' : train_test_split aléatoire reproductible (SEED), stratifié si classification.
    """
    columns = feature_columns(df)
    if not columns:
        raise ValueError("Aucune variable d'entrée disponible.")

    X = df[columns].copy()
    y = df[config.TARGET].copy()

    if config.SPLIT == "chronologique":
        if not config.TIME_COLUMN or config.TIME_COLUMN not in df.columns:
            raise ValueError("TIME_COLUMN doit désigner une colonne présente pour un split chronologique.")
        order = pd.to_datetime(df[config.TIME_COLUMN]).sort_values().index
        X, y = X.loc[order], y.loc[order]
        cut = int(len(df) * (1 - config.TEST_SIZE))
        if cut < 1 or cut >= len(df):
            raise ValueError("Pas assez de lignes pour le découpage entraînement/test.")
        return X.iloc[:cut], X.iloc[cut:], y.iloc[:cut], y.iloc[cut:]

    if config.SPLIT != "random":
        raise ValueError("SPLIT doit être 'random' ou 'chronologique'.")

    stratify = y if config.TASK == "classification" and y.value_counts().min() >= 2 else None
    return train_test_split(X, y, test_size=config.TEST_SIZE, random_state=config.SEED, stratify=stratify)
