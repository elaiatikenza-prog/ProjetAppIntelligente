"""Configuration du projet : c'est le seul fichier à adapter à votre sujet."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# --- Vos données -------------------------------------------------------------
# Supporte à la fois exemple_pannes.csv (contenant les données cantine de l'étudiante) et cantine_repas.csv
if (ROOT / "data" / "exemple_pannes.csv").exists():
    DATA_PATH = ROOT / "data" / "exemple_pannes.csv"
else:
    DATA_PATH = ROOT / "data" / "cantine_repas.csv"

TARGET = "repas_servis"           # la colonne à prédire (nombre de repas servis)
FEATURES = None                   # None = toutes les colonnes utiles sauf cible et TIME_COLUMN
TEXT_COLUMN = None                # nom d'une colonne de texte libre, sinon None

# --- Type de problème --------------------------------------------------------
TASK = "regression"               # "classification" ou "regression"
MAIN_METRIC = "mae"               # métrique principale : "mae" (Mean Absolute Error)

# --- Découpage entraînement / test -------------------------------------------
SPLIT = "chronologique"          # "random" ou "chronologique"
TIME_COLUMN = "date"              # colonne d'ordre chronologique
TEST_SIZE = 0.2                   # 20 % en test
SEED = 42                         # graine aléatoire pour la reproductibilité

# Dossier de sauvegarde des artefacts
MODELS_DIR = ROOT / "models"
OUTPUT_DIR = MODELS_DIR           # alias de compatibilité
