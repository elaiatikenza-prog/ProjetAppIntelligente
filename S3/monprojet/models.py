"""Définition des modèles candidats pour CantineAI et MaintAI."""
from sklearn.dummy import DummyClassifier, DummyRegressor
from sklearn.ensemble import (
    HistGradientBoostingClassifier,
    HistGradientBoostingRegressor,
    RandomForestClassifier,
    RandomForestRegressor,
)
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor

from . import config


def candidates() -> dict:
    """Renvoie le dictionnaire {nom: modèle scikit-learn non entraîné}.

    Contraintes pédagogiques :
    - Le PREMIER modèle est impérativement la baseline ;
    - Au moins trois modèles d'apprentissage automatique ensuite ;
    - Graine fixée (random_state=config.SEED) pour les estimateurs stochastiques.
    """
    if config.TASK == "regression":
        return {
            "baseline (moyenne)": DummyRegressor(strategy="mean"),
            "régression linéaire": LinearRegression(),
            "forêt aléatoire": RandomForestRegressor(n_estimators=100, random_state=config.SEED),
            "gradient boosting": HistGradientBoostingRegressor(random_state=config.SEED),
            "k plus proches voisins": KNeighborsRegressor(n_neighbors=5),
        }

    if config.TASK == "classification":
        return {
            "baseline (classe majoritaire)": DummyClassifier(strategy="most_frequent"),
            "régression logistique": LogisticRegression(max_iter=1000, random_state=config.SEED),
            "forêt aléatoire": RandomForestClassifier(n_estimators=100, random_state=config.SEED, class_weight="balanced"),
            "gradient boosting": HistGradientBoostingClassifier(random_state=config.SEED),
            "k plus proches voisins": KNeighborsClassifier(n_neighbors=5),
        }

    raise ValueError(f"TASK non reconnue : {config.TASK!r}. Attendu 'classification' ou 'regression'.")
