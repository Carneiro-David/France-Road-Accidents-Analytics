
import pandas as pd
import sqlite3
from pathlib import Path
from config import DATASET_PATH, DB_PATH


# Chemins du projet
BASE_DIR = Path(__file__).resolve().parent

CSV_PATH = BASE_DIR / "dataset_simplify_v2.csv"
DB_PATH = BASE_DIR / "bdd_v2.db"

TABLE_NAME = "accidents"

# Vérifier que le CSV existe
if not CSV_PATH.exists():
    raise FileNotFoundError(f"Dataset introuvable : {CSV_PATH}")

# Charger le dataset
print("Chargement du dataset...")
df = pd.read_csv(CSV_PATH, low_memory=False)

print(f"Nombre de lignes : {len(df)}")
print(f"Nombre de colonnes : {len(df.columns)}")

# Créer la nouvelle base SQLite
print("\nCréation de la base SQLite...")

with sqlite3.connect(DB_PATH) as conn:
    df.to_sql(
        TABLE_NAME,
        conn,
        if_exists="replace",
        index=False
    )

    # Vérifier le nombre d'enregistrements
    nb_lignes = conn.execute(
        f"SELECT COUNT(*) FROM {TABLE_NAME}"
    ).fetchone()[0]

    print(f"Nombre de lignes dans SQLite : {nb_lignes}")

    print("\nExtrait de la base :")
    for row in conn.execute(
        f"SELECT Num_Acc, date, grav, catv FROM {TABLE_NAME} LIMIT 5"
    ):
        print(row)

print(f"\nBase SQLite créée : {DB_PATH}")
