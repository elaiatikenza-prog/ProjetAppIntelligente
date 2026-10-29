"""Tests des données : chargement, colonnes et découpage (Séance 3)."""
import pandas as pd
import pytest

from monprojet import config
from monprojet.data import feature_columns, load_data, split


def test_load_data_renvoie_un_tableau_avec_la_cible():
    df = load_data()
    assert isinstance(df, pd.DataFrame), "load_data() doit renvoyer un DataFrame pandas"
    assert len(df) > 0, "Le fichier de données est vide"
    assert config.TARGET in df.columns, f"La colonne cible {config.TARGET} est absente"
    assert df[config.TARGET].notna().all(), "La cible ne doit pas contenir de valeurs manquantes"


def test_load_data_drops_missing_target(tmp_path, monkeypatch):
    p = tmp_path / "test_data.csv"
    pd.DataFrame({
        "jour": ["lundi", "mardi", "mercredi"],
        config.TARGET: [350, None, 420],
    }).to_csv(p, index=False)
    df = load_data(p)
    assert len(df) == 2, "Les lignes avec une cible manquante doivent être supprimées"


def test_load_data_missing_target_raises(tmp_path):
    p = tmp_path / "bad_data.csv"
    pd.DataFrame({"invalide": [1, 2]}).to_csv(p, index=False)
    with pytest.raises(ValueError, match="cible absente"):
        load_data(p)


def test_feature_columns_excludes_time_and_target():
    df = pd.DataFrame({
        "date": ["2024-09-09"],
        "jour": ["lundi"],
        "inscrits": [620],
        config.TARGET: [380],
    })
    feats = feature_columns(df)
    assert config.TARGET not in feats, "La cible ne doit jamais être dans les features"
    if config.TIME_COLUMN:
        assert config.TIME_COLUMN not in feats, "La date ne doit pas être dans les variables prédictives"
    assert "jour" in feats and "inscrits" in feats


def test_split_separe_entrainement_et_test():
    df = load_data()
    X_train, X_test, y_train, y_test = split(df)
    assert len(X_train) == len(y_train) and len(X_test) == len(y_test)
    assert len(X_train) + len(X_test) == len(df), "Toutes les lignes doivent être utilisées"
    assert abs(len(X_test) / len(df) - config.TEST_SIZE) < 0.05, "La taille du test doit respecter TEST_SIZE"
    assert set(X_train.index).isdisjoint(X_test.index), "Aucun chevauchement entre train et test"
    assert config.TARGET not in X_train.columns, "La cible ne doit pas faire partie des variables d'entrée"


def test_split_chronologique_teste_sur_le_futur():
    if config.SPLIT != "chronologique":
        return
    df = load_data()
    X_train, X_test, _, _ = split(df)
    dates = pd.to_datetime(df[config.TIME_COLUMN])
    assert dates.loc[X_train.index].max() <= dates.loc[X_test.index].min(), \
        "En découpage chronologique, tout le test doit être postérieur à l'entraînement"
