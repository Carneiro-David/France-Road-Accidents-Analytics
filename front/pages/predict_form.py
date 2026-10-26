import dash
import requests
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/formulaire", name="Saisie de données", order=3)

selected_cols = [
    "sexe", "catu", "catv", "atm", "lum", "col", "choc",
    "manv", "plan", "surf", "nbv", "secu1", "infra", "age","place"
]

map_cols = {
    "sexe": "Sexe",
    "catu": "Catégorie d'usager",
    "catv": "Catégorie du véhicule",
    "atm": "Conditions atmosphériques",
    "lum": "Lumière",
    "col": "Type de collision",
    "choc": "Point de choc initial",
    "manv": "Manoeuvre",
    "plan": "Tracé en plan",
    "surf": "État de la surface",
    "nbv": "Nombre de voies",
    "secu1": "Équipement de sécurité",
    "infra": "Aménagement - Infrastructure",
    "age": "Âge",
    "place": "Place occupée dans le véhicule"
}

def call_api_predict(data):
    API_URL = "http://localhost:5001/prediction"
    response = requests.post(API_URL, json=data)
    return response.json()

# Dropdown options
dropdown_options = {
    "sexe": [
        {"label": "Homme", "value": "Homme"},
        {"label": "Femme", "value": "Femme"},
    ],
    "atm": [
        {"label": "Non renseigné", "value": "Non renseigné"},
        {"label": "Normale", "value": "Normale"},
        {"label": "Pluie légère", "value": "Pluie légère"},
        {"label": "Pluie forte", "value": "Pluie forte"},
        {"label": "Neige / grêle", "value": "Neige / grêle"},
        {"label": "Brouillard / fumée", "value": "Brouillard / fumée"},
        {"label": "Vent fort / tempête", "value": "Vent fort / tempête"},
        {"label": "Temps éblouissant", "value": "Temps éblouissant"},
        {"label": "Temps couvert", "value": "Temps couvert"},
        {"label": "Autre", "value": "Autre"}
    ],
    "lum": [
        {"label": "Plein jour", "value": "Plein jour"},
        {"label": "Crépuscule ou aube", "value": "Crépuscule ou aube"},
        {"label": "Nuit sans éclairage public", "value": "Nuit sans éclairage public"},
        {"label": "Nuit avec éclairage non allumé", "value": "Nuit avec éclairage non allumé"},
        {"label": "Nuit avec éclairage allumé", "value": "Nuit avec éclairage allumé"}
    ],
    "catu": [
        {"label": "Conducteur", "value": "Conducteur"},
        {"label": "Passager", "value": "Passager"},
        {"label": "Piéton", "value": "Piéton"}
    ],
    "choc": [
        {"label": "Non renseigné", "value": "Non renseigné"},
        {"label": "Aucun", "value": "Aucun"},
        {"label": "Avant", "value": "Avant"},
        {"label": "Avant droit", "value": "Avant droit"},
        {"label": "Avant gauche", "value": "Avant gauche"},
        {"label": "Arrière", "value": "Arrière"},
        {"label": "Arrière droit", "value": "Arrière droit"},
        {"label": "Arrière gauche", "value": "Arrière gauche"},
        {"label": "Côté droit", "value": "Côté droit"},
        {"label": "Côté gauche", "value": "Côté gauche"},
        {"label": "Chocs multiple", "value": "Chocs multiples / tonneaux"}
    ],
    "plan": [
        {"label": "Non renseigné", "value": "Non renseigné"},
        {"label": "Partie rectiligne", "value": "Partie rectiligne"},
        {"label": "En courbe à gauche", "value": "Courbe à gauche"},
        {"label": "En courbe à droite", "value": "Courbe à droite"},
        {"label": "En S", "value": "En S"}
    ],
    "surf": [
        {"label": "Non renseigné", "value": "Non renseigné"},
        {"label": "Normale", "value": "Normale"},
        {"label": "Mouillé", "value": "Mouillée"},
        {"label": "Flaques", "value": "Flaques"},
        {"label": "Inondée", "value": "Inondée"},
        {"label": "Enneigée", "value": "Enneigée"},
        {"label": "Boue", "value": "Boue"},
        {"label": "Verglacée", "value": "Verglacée"},
        {"label": "Corps gras - huile", "value": "Corps gras / huile"},
        {"label": "Autre", "value": "Autre"}
    ],
    "secu1": [
        {"label": "Non renseigné", "value": "Non renseigné"},
        {"label": "Non renseigné", "value": "Aucun équipement"},
        {"label": "Ceinture", "value": "Ceinture"},
        {"label": "Casque", "value": "Casque"},
        {"label": "Dispositif enfant", "value": "Dispositif enfants"},
        {"label": "Gilet réfléchissant", "value": "Gilet réfléchissant"},
        {"label": "Airbag (2RM/3RM)", "value": "Airbag (2RM/3RM)"},
        {"label": "Gants (2RM/3RM)", "value": "Gants (2RM/3RM)"},
        {"label": "Gants + Airbag (2RM/3RM)", "value": "Gants + Airbag (2RM/3RM)"},
        {"label": "Non déterminable", "value": "Non déterminable"},
        {"label": "Autre", "value": "Autre"}
    ],
    "infra": [
        {"label": "Non renseigné", "value": "Non renseigné"},
        {"label": "Aucun", "value": "Aucun"},
        {"label": "Souterrain - tunnel", "value": "Tunnel"},
        {"label": "Pont - autopont", "value": "Pont"},
        {"label": "Bretelle d’échangeur ou de raccordement", "value": "Bretelle d’échangeur"},
        {"label": "Voie ferrée", "value": "Voie ferrée"},
        {"label": "Carrefour aménagé", "value": "Carrefour aménagé"},
        {"label": "Zone piétonne", "value": "Zone piétonne"},
        {"label": "Zone de péage", "value": "Zone de péage"},
        {"label": "Chantier", "value": "Chantier"},
        {"label": "Autre", "value": "Autre"}
    ],
    "manv": [
        {"label": "Manoeuvre principale avant l’accident : Non renseigné", "value": "Non renseigné"},
        {"label": "Manoeuvre principale avant l’accident : Inconnue", "value": "Inconnue"},
        {"label": "Manoeuvre principale avant l’accident : Sans changement de direction", "value": "Sans changement de direction"},
        {"label": "Manoeuvre principale avant l’accident : Même sens, même file", "value": "Même sens, même file"},
        {"label": "Manoeuvre principale avant l’accident : Entre 2 files", "value": "Entre 2 files"},
        {"label": "Manoeuvre principale avant l’accident : En marche arrière", "value": "En marche arrière"},
        {"label": "Manoeuvre principale avant l’accident : À contresens", "value": "À contresens"},
        {"label": "Manoeuvre principale avant l’accident : Franchissement du terre-plein", "value": "Franchissement du terre-plein"},
        {"label": "Manoeuvre principale avant l’accident : Couloir bus, même sens", "value": "Couloir bus, même sens"},
        {"label": "Manoeuvre principale avant l’accident : Couloir bus, sens inverse", "value": "Couloir bus, sens inverse"},
        {"label": "Manoeuvre principale avant l’accident : Insertion", "value": "Insertion"},
        {"label": "Manoeuvre principale avant l’accident : Demi-tour", "value": "Demi-tour"},
        {"label": "Manoeuvre principale avant l’accident : Changement file à gauche", "value": "Changement file à gauche"},
        {"label": "Manoeuvre principale avant l’accident : Changement file à droite", "value": "Changement file à droite"},
        {"label": "Manoeuvre principale avant l’accident : Déport à gauche", "value": "Déport à gauche"},
        {"label": "Manoeuvre principale avant l’accident : Déport à droite", "value": "Déport à droite"},
        {"label": "Manoeuvre principale avant l’accident : Tourne à gauche", "value": "Tourne à gauche"},
        {"label": "Manoeuvre principale avant l’accident : Tourne à droite", "value": "Tourne à droite"},
        {"label": "Manoeuvre principale avant l’accident : Dépassement gauche", "value": "Dépassement gauche"},
        {"label": "Manoeuvre principale avant l’accident : Dépassement droite", "value": "Dépassement droite"},
        {"label": "Manoeuvre principale avant l’accident : Traverse chaussée", "value": "Traverse chaussée"},
        {"label": "Manoeuvre principale avant l’accident : Stationnement", "value": "Stationnement"},
        {"label": "Manoeuvre principale avant l’accident : Évitement", "value": "Évitement"},
        {"label": "Manoeuvre principale avant l’accident : Ouverture de porte", "value": "Ouverture de porte"},
        {"label": "Manoeuvre principale avant l’accident : Arrêté", "value": "Arrêté"},
        {"label": "Manoeuvre principale avant l’accident : Stationné avec occupants", "value": "Stationné avec occupants"},
        {"label": "Manoeuvre principale avant l’accident : Sur trottoir", "value": "Sur trottoir"},
        {"label": "Manoeuvre principale avant l’accident : Autre", "value": "Autre"}
    ],
    "col": [
        {"label": "Non renseigné", "value": "Non renseigné"},
        {"label": "Deux véhicules - frontale", "value": "Frontale (2 véhicules)"},
        {"label": "Deux véhicules – par l’arrière", "value": "Par l’arrière (2 véhicules)"},
        {"label": "Deux véhicules – par le coté", "value": "Par le côté (2 véhicules)"},
        {"label": "Trois véhicules et plus – en chaîne", "value": "En chaîne (≥3 véhicules)"},
        {"label": "Trois véhicules et plus - collisions multiples", "value": "Collisions multiples (≥3 véhicules)"},
        {"label": "Autre collision", "value": "Autre collision"},
        {"label": "Sans collision", "value": "Sans collision"},

    ],
    "catv": [
        {"label": "Voiture", "value": "Voiture"},
        {"label": "Poids lourd", "value": "Poids lourd"},
        {"label": "Deux-roues motorisé", "value": "Deux-roues motorisé"},
        {"label": "Deux-roues non motorisé", "value": "Deux-roues non motorisé"},
        {"label": "Vélo", "value": "Vélo"},
        {"label": "Trains", "value": "Trains"},
        {"label": "Transport collectif", "value": "Transport collectif"},
        {"label": "Autres", "value": "Autres"}
    ]
}


def generate_input(col):
    if col in dropdown_options:
        
        default_value = None
        if col == "sexe":
            default_value = "Homme"
        elif col == "atm":
            default_value = "Pluie forte"
        elif col == "lum":
            default_value = "Nuit sans éclairage public"
        elif col == "catu":
            default_value = "Conducteur"
        elif col == "choc":
            default_value = "Avant gauche"
        elif col == "plan":
            default_value = "Non renseigné"
        elif col == "surf":
            default_value = "Normale"
        elif col == "secu1":
            default_value = "Aucun équipement"
        elif col == "infra":
            default_value = "Aucun"
        elif col == "manv":
            default_value = "Déport à gauche"
        elif col == "col":
            default_value = "Frontale (2 véhicules)"
        elif col == "catv":
            default_value = "Voiture"
            
        return dbc.Form([
            dbc.Label(map_cols.get(col, col), html_for=f"input-{col}", className="form-label-custom"),
            dcc.Dropdown(
                id=f"input-{col}",
                options=dropdown_options[col],
                value=default_value,
                placeholder=f"Choisir {col.capitalize()}",
                className="form-dropdown"
            )
        ])
    elif col == "age":
        return dbc.Form([
            dbc.Label(map_cols.get(col, col), html_for=f"input-{col}", className="form-label-custom"),
            dcc.Input(id=f"input-{col}", type="number", placeholder=f"Saisir {col}", className="form-input", value=55),
        ])
    elif col == "place":
        return dbc.Form([
            html.Img(src="/assets/aide_form_place.png", className="form-image"),
            dbc.Label(map_cols.get(col, col), html_for=f"input-{col}", className="form-label-custom"),
            dcc.Input(id=f"input-{col}", type="text", placeholder="Saisir la place", className="form-input", value="1"),
            html.Br()
        ])
    else:
        return dbc.Form([
            dbc.Label(map_cols.get(col, col).capitalize(), html_for=f"input-{col}", className="form-label-custom"),
            dcc.Input(id=f"input-{col}", type="text", placeholder=f"Saisir {col}", className="form-input")
        ])

layout = dbc.Container([
    html.H2("Saisie d'un accident", className="page-title"),

    dbc.Card([
        dbc.CardBody([
            dbc.Row([
                dbc.Col(generate_input(col), width=6) for col in selected_cols
            ], className="form-row-custom"),

            html.Div(id="form-output", className="result-output"),
            
            html.Div(className="button-wrapper", children=[
                dbc.Button("Soumettre", id="submit-button", color="primary", n_clicks=0, className="submit-button")
            ]),

            # html.Hr(),
        ])
    ])
], fluid=True)

def render_prediction_card(response):
    gravité = response.get("prediction")
    corrigé = response.get("corrigé")
    proba_grave = response.get("probabilité_risque_grave")

    couleur = {
        "Indemne": "success",
        "Blessé léger": "info",
        "Blessé hospitalisé": "warning",
        "Tué": "danger"
    }.get(gravité, "secondary")

    return dbc.Card([
        dbc.CardHeader("Résultat de la prédiction", className="text-white bg-primary"),
        dbc.CardBody([
            html.H4(f"{gravité}", className=f"text-{couleur}"),
            # html.P(f"Probabilité de risque grave : {proba_grave:.0%}"),
            # html.P("Correction manuelle appliquée" if corrigé else "Prédiction directe du modèle")
        ])
    ], color="dark", inverse=True)

@dash.callback(
    Output("form-output", "children"),
    Input("submit-button", "n_clicks"),
    [State(f"input-{col}", "value") for col in selected_cols]
)
def handle_form(n_clicks, *values):
    if n_clicks > 0:        
        data = {col: value for col, value in zip(selected_cols, values)}
        response = call_api_predict(data)
        
        if response.get("prediction") is not None:
            return render_prediction_card(response), True
        else:
            return dbc.Alert("Erreur : données invalides ou API indisponible.", color="danger"), True
        
    return "", False
