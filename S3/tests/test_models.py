"""Tests des modèles candidats (Séance 3)."""
from sklearn.dummy import DummyClassifier, DummyRegressor

from monprojet import config
from monprojet.models import candidates


def test_la_baseline_est_le_premier_modele():
    first = next(iter(candidates().values()))
    assert isinstance(first, (DummyClassifier, DummyRegressor)), \
        "Le premier modèle doit être une baseline simple (DummyClassifier ou DummyRegressor)"


def test_au_moins_trois_modeles_en_plus_de_la_baseline():
    models = candidates()
    assert len(models) >= 4, "Il faut au moins 4 modèles au total (la baseline + au moins 3 modèles candidats)"
