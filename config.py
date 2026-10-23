
from pathlib import Path

# Racine du projet
BASE_DIR = Path(__file__).resolve().parent

# Dossier contenant les données
DATA_DIR = BASE_DIR / "data"

# Dataset utilisé par l'application
DATASET_PATH = DATA_DIR / "dataset_simplify_v2.csv"

# Base SQLite utilisée par Flask
DB_PATH = DATA_DIR / "bdd_v2.db"

# Configuration des serveurs
FLASK_PORT = 5001
DASH_PORT = 8050

# Période couverte par les données
START_YEAR = 2019
END_YEAR = 2023
