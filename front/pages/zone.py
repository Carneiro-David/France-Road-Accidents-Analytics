import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
import pandas as pd
import os
from back.zone_analysis import *

dash.register_page(__name__, path="/zones")

base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
# df = pd.read_csv(os.path.join(base_path, "data", "dataset_simplify.csv"), dtype=str)
df = pd.read_csv(
    os.path.join(base_path, "data", "dataset_simplify_v2.csv"),
    dtype=str
)
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['heure'] = df['date'].dt.hour

layout = html.Div([
    html.H3("Visualisations pertinentes"),

    html.Div([
        dcc.Graph(figure=plot_agg_pie(df)),
        # accordion_stats("Âge moyen et écart-type par gravité", age_moyen_gravite_stats(df), is_percent=False)
    ], className="card-dark"),  

    html.Div([
        dcc.Graph(figure=plot_route_zone_count(df)),
        # accordion_stats("Pourcentage de gravité par sexe", gravite_sexe_stats(df), is_percent=True)
    ], className="card-dark"),

    html.Div([
        dcc.Graph(figure=plot_route_zone_gravity(df)),
        # accordion_stats("Pourcentage de type de véhicules par gravité", gravite_catv_stats(df), is_percent=True)
    ], className="card-dark"),  
])