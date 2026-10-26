import dash
import dash_leaflet as dl
import requests

from dash import html, dcc, Input, Output

from back.meteo_analysis import (
    plot_gravite_meteo,
    plot_nombre_accidents_meteo,
    plot_nombre_accidents_meteo_sans_normale,
    plot_catr_atm
)

from utils.data_loader import get_data
from front.pages.temporal import get_temporal_content
from front.pages.autres import get_autres_content
from config import START_YEAR, END_YEAR

dash.register_page(
    __name__,
    name="Statistiques",
    path="/statistique",
    order=1
)

API_URL = "http://localhost:5001"

df = get_data()

def get_vehicule_types():
    r = requests.get(f"{API_URL}/vehicule-types")
    return r.json()
def get_grav_accident():
    r = requests.get(f"{API_URL}/grav-types")
    return r.json()

def get_filtered_points(catv,grav_type, start_year, end_year):
    params = {"catv": catv,"grav": grav_type, "start": start_year, "end": end_year}
    r = requests.get(f"{API_URL}/points", params=params)
    return r.json()

layout = html.Div([
    html.H2("Exploration des statistiques", className="text-center"),

    html.Div([
        dcc.Dropdown(
            id="section_selector",
            options=[
                {"label": "Cartographie", "value": "carto"},
                {"label": "Statistiques météo", "value": "meteo"},
                {"label": "Statistiques temporelles", "value": "temporal"},
                {"label": "Autres statistiques", "value": "autres"}
            ],
            value="meteo",
            clearable=False,
            className="custom-dropdown"
        )
    ], style={"display": "flex", "justifyContent": "center", "marginBottom": "20px"}),

    html.Div(id="section_content")
])

@dash.callback(
    Output("section_content", "children"),
    Input("section_selector", "value")
)
def update_section(selected_section):
    if selected_section == "meteo":
        return html.Div([
            html.H4("Section : Statistiques météo"),
            dcc.Graph(figure=plot_gravite_meteo(df)),
            html.Hr(),
            dcc.Graph(figure=plot_nombre_accidents_meteo(df)),
            html.Hr(),
            dcc.Graph(figure=plot_nombre_accidents_meteo_sans_normale(df)),
            html.Hr(),
            dcc.Graph(figure=plot_catr_atm(df)),
            html.P("Ici se trouveront les graphiques interactifs liés à la météo.")
        ])
    elif selected_section == "temporal":
        return html.Div([
            html.H4("Section : Statistiques temporelles", className="title-main"),
            html.Div([
                html.Label("Sélectionnez une vue :", className="radio-title"),
                dcc.RadioItems(
                    id="mode-temporal",
                    options=[
                        {"label": "Données temporelles", "value": "vue1"},
                        {"label": "Données temporelles croisées", "value": "vue2"},
                    ],
                    value="vue1",
                    className="radio-switch",
                    labelStyle={"marginRight": "30px"},
                )
            ], className="radio-container"),
            html.Div(id="contenu-graphiques-temporaux")
        ])

    elif selected_section == "autres":
        return get_autres_content(df.copy())

    elif selected_section == "carto":
        # Prépare le dropdown avec les différents types de véhicules
        vehicule_types = sorted(get_vehicule_types())

        vehicule_dropdown = html.Div([
            html.Label("Filtrer par type de véhicule :"),
            dcc.Dropdown(
                id="vehicule_selector",
                options=[
                    {"label": "Tous les véhicules", "value": "all"},
                    *[
                        {"label": v, "value": v}
                        for v in vehicule_types
                    ]
                ],
                value="all",
                clearable=False,
                className="carto_select"
            )
        ])
        ordre_gravite = ["Indemne", "Blessé léger", "Blessé hospitalisé", "Tué"]
        grav_accident = get_grav_accident()
        grav_tri = [g for g in ordre_gravite if g in grav_accident]

        grav_dropdown = html.Div([
            html.Label("Filtrer par gravité d'accident (grav) :"),
            dcc.Dropdown(
                id="grav_selector",
                options=[
                    {"label": "Toutes les gravités", "value": "all"},
                    *[
                        {"label": grav, "value": grav}
                        for grav in grav_tri
                    ]
                ],
                value="all",
                clearable=False,
                className="carto_select"
            )
        ])
        period_range = html.Div([
            html.Label("Période à afficher (années) :"),
            dcc.RangeSlider(
                id='year_range',
                min=START_YEAR,
                max=END_YEAR,
                step=1,
                value=[START_YEAR, END_YEAR],
                marks={year: str(year) for year in range(START_YEAR, END_YEAR + 1)},
                tooltip={"placement": "bottom", "always_visible": True},
                allowCross=False
            )
        ])
        return html.Div([
            html.Div([
                html.Div(vehicule_dropdown, className="filter-dropdown"),
                html.Div(grav_dropdown, className="filter-dropdown"),
            ], style={"display": "flex", "gap": "25px", "justifyContent": "center", "marginBottom": "15px"}),

            period_range,

            dl.Map(id="map", center=[46.5, 2.5], zoom=6, children=[
                dl.TileLayer(), 
                dl.GeoJSON(
                    id="geojson_cluster",
                    cluster=True,
                    zoomToBoundsOnClick=True,
                    options={"pointToLayer": None}
                )
            ], style={'height': 'calc(100vh - 200px)'}, className="carteCustom")
        ])

@dash.callback(
    Output("geojson_cluster", "data"),
    Input("vehicule_selector", "value"),
    Input("grav_selector", "value"),
    Input("year_range", "value")
)
def update_geojson(selected_type, grav_type, year_range):
    if not year_range:
        return {"type": "FeatureCollection", "features": []}

    catv = selected_type or "all"
    grav = grav_type or "all"

    points = get_filtered_points(catv,grav, year_range[0], year_range[1])

    features = []
    for p in points:
        popup_text = f"""\
            Type : {p['catv']}
            Météo : {p['atm']}
            Collision : {p['col']}
            Chaussée : {p['surf']}
            Manœuvre : {p['manv']}
            Gravité : {p['grav']}"""

        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [p["lon"], p["lat"]]
            },
            "properties": {
                "popup": popup_text
            }
        })

    return {"type": "FeatureCollection", "features": features}

@dash.callback(
    Output("contenu-graphiques-temporaux", "children"),
    Input("mode-temporal", "value")
)
def update_temporal_graphs(mode):
    return get_temporal_content(mode, df.copy())
