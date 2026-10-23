import pandas as pd
import plotly.express as px

def plot_gravite_meteo(df):

    grav_mapping = {
        'Indemne': 1,
        'Blessé léger': 2,
        'Blessé hospitalisé': 3,
        'Tué': 4
    }
    df['grav_num'] = df['grav'].map(grav_mapping)


    gravite_par_atm = df.dropna(subset=['grav_num', 'atm'])
    gravite_par_atm = gravite_par_atm.groupby('atm', as_index=False)['grav_num'].mean()
    gravite_par_atm = gravite_par_atm.sort_values(by='grav_num', ascending=False)

    fig = px.bar(
        gravite_par_atm,
        x='atm',
        y='grav_num',
        title="Gravité moyenne des accidents par condition météo",
        labels={'atm': 'Condition météo', 'grav_num': 'Gravité moyenne'},
        color='grav_num',
        color_continuous_scale='Viridis'
    )
    fig.update_layout(xaxis_tickangle=-45, template="plotly_dark")
    return fig


def plot_nombre_accidents_meteo_sans_normale(df):
    df_unique = df.drop_duplicates("Num_Acc")
    # df_filtered = df_unique[df_unique['atm'] != 'Normale']
    df_atm = df_unique['atm'].value_counts().reset_index()
    df_atm.columns = ['atm', 'nb_accidents']

    fig = px.bar(
        df_atm,
        x='atm',
        y='nb_accidents',
        title="Nombre d'accidents selon les conditions météorologiques",
        labels={'atm': 'Conditions météo', 'nb_accidents': 'Nombre d\'accidents'},
        color='nb_accidents'
    )
    fig.update_layout(xaxis_tickangle=-30, template="plotly_dark")
    return fig


def plot_nombre_accidents_meteo(df):
    df_unique = df.drop_duplicates("Num_Acc")
    # df_filtered = df_unique[df_unique['atm'] != 'Normale']
    df_atm = df_unique['atm'].value_counts().reset_index()
    df_atm.columns = ['atm', 'nb_accidents']

    fig = px.bar(
        df_atm,
        x='atm',
        y='nb_accidents',
        title="Nombre d'accidents selon les conditions météorologiques",
        labels={'atm': 'Conditions météo', 'nb_accidents': 'Nombre d\'accidents'},
        color='nb_accidents'
    )
    fig.update_layout(xaxis_tickangle=-30, template="plotly_dark")
    return fig

def plot_catr_atm(df):
    df_unique = df.drop_duplicates("Num_Acc")

    df_grouped = df_unique.groupby(['catr', 'atm']).size().reset_index(name='nb_accidents')
    # df_grouped = df_grouped[df_grouped['atm'] != 'Normale']

    fig = px.bar(
        df_grouped,
        x='catr',
        y='nb_accidents',
        color='atm',
        title="Nombre d'accidents par type de route et conditions météorologiques",
        labels={'catr': 'Type de route', 'nb_accidents': 'Nombre d\'accidents', 'atm': 'Météo'},
        barmode='group'
    )
    fig.update_layout(xaxis_tickangle=-70, template="plotly_dark")
    return fig
