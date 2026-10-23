import pandas as pd
import os
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from config import DATASET_PATH, DASH_PORT, START_YEAR, END_YEAR

base_path = os.path.dirname(__file__)
# df = pd.read_csv(os.path.join(base_path, "data", "dataset_simplify.csv"), dtype=str)
df = pd.read_csv(
    os.path.join(base_path, "data", "dataset_simplify_v2.csv"),
    dtype=str
)
app = dash.Dash(
    __name__,
    use_pages=True,
    pages_folder="front/pages",
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
)
server = app.server

header = dbc.Navbar(
    dbc.Container([
        html.Div("Accidents de la route en France (2019–2023)", className="navbar-title"),
        dbc.Nav(
            [
                dbc.NavItem(
                    dcc.Link(
                        page["name"],
                        href=page["relative_path"],
                        className="navbar-link"
                    )
                )
                for page in dash.page_registry.values()
            ],
            className="navbar-nav"
        ),
    ]),
    className="navbar-container"
)

app.layout = dbc.Container([
    header,
    html.Br(),
    dash.page_container
], fluid=True)

if __name__ == "__main__":
    app.run(debug=True)
