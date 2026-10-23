
from flask import Flask, jsonify, request
from config import BASE_DIR, DB_PATH, FLASK_PORT

import joblib
import sqlite3
import pandas as pd

app = Flask(__name__)

# ==========================================
# CONFIGURATION DU MACHINE LEARNING
# ==========================================

MODELS_DIR = BASE_DIR / "models"

model = joblib.load(
    MODELS_DIR / "lightgbm_gravite.joblib"
)

label_encoder = joblib.load(
    MODELS_DIR / "gravite_encoder.joblib"
)

FEATURES = [
    "sexe", "catu", "catv", "atm", "lum",
    "col", "choc", "manv", "plan", "surf",
    "nbv", "secu1", "infra", "age", "place"
]

NUMERIC_FEATURES = ["age", "nbv"]

CATEGORICAL_FEATURES = [
    col for col in FEATURES
    if col not in NUMERIC_FEATURES
]


# ==========================================
# API : TYPES DE VÉHICULES
# ==========================================

@app.route("/vehicule-types")
def get_vehicule_types():
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute(
            "SELECT DISTINCT catv FROM accidents"
        ).fetchall()

    return jsonify([row[0] for row in rows if row[0]])


# ==========================================
# API : TYPES DE GRAVITÉ
# ==========================================

@app.route("/grav-types")
def get_grav_accident_types():
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute(
            "SELECT DISTINCT grav FROM accidents"
        ).fetchall()

    return jsonify([row[0] for row in rows if row[0]])


# ==========================================
# API : POINTS POUR LA CARTOGRAPHIE
# ==========================================

@app.route("/points")
def get_filtered_points():
    catv = request.args.get("catv")
    grav = request.args.get("grav")
    start_year = request.args.get("start")
    end_year = request.args.get("end")

    if not start_year or not end_year:
        return jsonify([])

    try:
        start_year = int(start_year)
        end_year = int(end_year)

        if start_year > end_year:
            return jsonify({
                "error": "Période invalide."
            }), 400

    except ValueError:
        return jsonify({
            "error": "Les années doivent être numériques."
        }), 400

    query = """
        SELECT lat, long, atm, col, surf, manv, catv, grav
        FROM accidents
        WHERE date >= ?
          AND date < ?
          AND lat IS NOT NULL
          AND long IS NOT NULL
    """

    params = [
        f"{start_year}-01-01",
        f"{end_year + 1}-01-01"
    ]

    if catv and catv != "all":
        query += " AND catv = ?"
        params.append(catv)

    if grav and grav != "all":
        query += " AND grav = ?"
        params.append(grav)

    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute(query, params).fetchall()

    results = [
        {
            "lat": lat,
            "lon": lon,
            "atm": atm,
            "col": col,
            "surf": surf,
            "manv": manv,
            "catv": vehicle_type,
            "grav": gravity
        }
        for lat, lon, atm, col, surf, manv, vehicle_type, gravity in rows
    ]

    return jsonify(results)


# ==========================================
# API : PRÉDICTION MACHINE LEARNING
# ==========================================

@app.route("/prediction", methods=["POST"])
def predict_accident():

    data = request.get_json(silent=True)

    # Vérifier le format JSON
    if not isinstance(data, dict):
        return jsonify({
            "error": "Le corps de la requête doit être un objet JSON."
        }), 400

    # Vérifier la présence des champs obligatoires
    missing_fields = [
        col for col in FEATURES
        if col not in data
        or data[col] is None
        or data[col] == ""
    ]

    if missing_fields:
        return jsonify({
            "error": "Certains champs sont manquants.",
            "fields": missing_fields
        }), 400

    try:
        # Construire une ligne avec les 15 variables
        input_df = pd.DataFrame([
            {col: data[col] for col in FEATURES}
        ])

        # Convertir les variables numériques
        for col in NUMERIC_FEATURES:
            input_df[col] = pd.to_numeric(
                input_df[col],
                errors="raise"
            )

        # Vérifier les valeurs numériques
        age = float(input_df["age"].iloc[0])
        nbv = float(input_df["nbv"].iloc[0])

        if not (0 <= age <= 110):
            return jsonify({
                "error": "L'âge doit être compris entre 0 et 110 ans."
            }), 400

        if not (0 <= nbv <= 12):
            return jsonify({
                "error": "Le nombre de voies doit être compris entre 0 et 12."
            }), 400

        # Nettoyer les catégories
        for col in CATEGORICAL_FEATURES:
            input_df[col] = (
                input_df[col]
                .astype("string")
                .str.strip()
            )

        # Prédiction avec le pipeline complet :
        # imputation + OneHotEncoder + LightGBM
        prediction_encoded = model.predict(input_df)

        # Convertir la prédiction en gravité lisible
        prediction = label_encoder.inverse_transform(
            prediction_encoded.astype(int)
        )[0]

        return jsonify({
            "prediction": str(prediction)
        })

    except (ValueError, TypeError) as error:
        return jsonify({
            "error": "Données invalides.",
            "details": str(error)
        }), 400


# ==========================================
# DÉMARRAGE FLASK
# ==========================================

if __name__ == "__main__":
    app.run(debug=True, port=FLASK_PORT)