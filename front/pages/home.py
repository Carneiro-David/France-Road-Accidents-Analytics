import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__, name="Accueil", path="/", order=0)

layout = dbc.Container([
    html.H2("Bienvenue sur l'observatoire des accidents de la route en France", className="title-main"),
    html.P("""
        Cette application permet d'explorer les données d'accidents de la route entre 2019 et 2023. 
        Vous y trouverez des statistiques, des visualisations interactives et un outil de prédiction.
    """, style={"marginBottom":"40px"}),
    html.P("Utilisez le menu de navigation ci-dessus pour accéder aux différentes sections."),
], className="home-container")
