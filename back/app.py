from flask import Flask, jsonify, request
from sklearn.preprocessing import StandardScaler

import os
import joblib
import sqlite3
import numpy as np
import pandas as pd

app = Flask(__name__)

# model_main = joblib.load("back/models/hist.pkl")
# model_rf = joblib.load("back/models/rf.pkl")
# label_encoder = joblib.load("back/models/label_encoder.pkl")

# features_path = "back/models/feature_columns.pkl"
# feature_columns = joblib.load(features_path)

scaler = StandardScaler()
grav_map = {
    0: "Indemne",
    1: "Blessé hospitalisé",
    2: "Blessé léger",
    3: "Tué"
}

os.environ["LOKY_MAX_CPU_COUNT"] = "8"

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "bdd.db")

@app.route("/vehicule-types")
def get_vehicule_types():
    conn = sqlite3.connect(DB_PATH)
    df = conn.execute("SELECT DISTINCT catv FROM accidents").fetchall()
    conn.close()
    return jsonify([r[0] for r in df if r[0]])

@app.route('/grav-types')
def get_grav_accident_types():
    conn = sqlite3.connect(DB_PATH)
    df = conn.execute("SELECT DISTINCT grav FROM accidents").fetchall()
    conn.close()
    return jsonify([r[0] for r in df if r[0]])

@app.route("/points")
def get_filtered_points():
    catv = request.args.get("catv")
    start_year = request.args.get("start")
    end_year = request.args.get("end")
    grav = request.args.get("grav")

    if not start_year or not end_year:
        return jsonify([])

    query = """
    SELECT lat, long, atm, col, surf, manv, grav
    FROM accidents
    WHERE strftime('%Y', date) BETWEEN ? AND ?
    AND lat IS NOT NULL AND long IS NOT NULL
    """

    params = [start_year,end_year]

    if catv and catv != "all":
        query += "AND catv = ? "
        params.append(catv)
    if grav and grav != "all":
        query += " AND grav = ? "
        params.append(grav)

    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(query, params).fetchall()
    conn.close()

    results = []
    for lat, lon, atm, col, surf, manv, grav in rows:
        results.append({
            "lat": lat,
            "lon": lon,
            "atm": atm,
            "col": col,
            "surf": surf,
            "manv": manv,
            "catv": catv,
            "grav": grav
        })

    return jsonify(results)

@app.route("/prediction", methods=["POST"])
def predict_accident():
    data = request.get_json()

    features_wanted = [
        "sexe", "catu", "catv", "atm", "lum", "col", "choc",
        "manv", "plan", "surf", "nbv", "secu1", "infra", "place", "age"
    ]

    catv_mapping = {
        'Voiture': 'Voiture',
        'Véhicule utilitaire': 'Voiture',
        'Poids lourd > 7.5t': 'Poids lourd',
        'Poids lourd <= 7.5t': 'Poids lourd',
        'PL + remorque': 'Poids lourd',
        'Tracteur + semi-remorque': 'Poids lourd',
        'Tracteur routier seul': 'Poids lourd',
        'Quad lourd': 'Deux-roues motorisé',
        'Quad léger': 'Deux-roues motorisé',
        'Voiturette': 'Voiture',
        'Scooter <= 50 cm3': 'Deux-roues motorisé',
        'Scooter > 50 cm3': 'Deux-roues motorisé',
        'Scooter > 125 cm3': 'Deux-roues motorisé',
        'Scooter <= 125 cm3': 'Deux-roues motorisé',
        'Cyclomoteur <50cm3': 'Deux-roues motorisé',
        'Moto > 125 cm3': 'Deux-roues motorisé',
        'Moto <= 125 cm3': 'Deux-roues motorisé',
        '3RM > 50 cm3': 'Deux-roues motorisé',
        '3RM <= 50 cm3': 'Deux-roues motorisé',
        'Bicyclette': 'Deux-roues non motorisé',
        'EDP motorisé': 'Deux-roues motorisé',
        'EDP non motorisé': 'Deux-roues non motorisé',
        'VAE': 'Vélo',
        'Train': 'Trains',
        'Tramway': 'Transport collectif',
        'Autocar': 'Transport collectif',
        'Autobus': 'Transport collectif',
        'Engin spécial': 'Autres',
        'Indéterminable': 'Autres',
        'Non renseigné': 'Autres',
        'Autre': 'Autres'
    }

    input_df = pd.DataFrame([data])[features_wanted]
    input_df["catv"] = input_df["catv"].replace(catv_mapping)

    input_encoded = pd.get_dummies(input_df.astype(str))
    # input_encoded = input_encoded.reindex(columns=feature_columns, fill_value=0)
 
    if "age" in input_encoded.columns:
        input_encoded[["age"]] = scaler.transform(input_encoded[["age"]])

    input_encoded = input_encoded.astype(np.float32)

    # y_pred_main = model_main.predict(input_encoded)[0]
    # proba_main = model_main.predict_proba(input_encoded)[0][1]
    # proba_rf = model_rf.predict_proba(input_encoded)[0][1]
    seuil = 0.60

    # y_pred_final = 3 if (y_pred_main != 3 and proba_rf > seuil) else y_pred_main
    
    # print(y_pred_final)
    # print(label_encoder.inverse_transform([y_pred_final])[0])

    # prediction = {
    #     "prediction": grav_map[y_pred_final],
    #     "probabilité": round(float(proba_main), 3),
    #     "corrigé": bool(y_pred_main != y_pred_final),
    #     "probabilité_risque_grave": round(float(proba_rf), 3)
    # }

    # return jsonify(prediction)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
