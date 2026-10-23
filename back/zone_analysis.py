import pandas as pd
import plotly.express as px

def plot_agg_pie(df):
    grav_mapping = {
        'Indemne': 1,
        'Blessé léger': 2,
        'Blessé hospitalisé': 3,
        'Tué': 4
    }
    df['grav_num'] = df['grav'].map(grav_mapping)

    df_unique = df.drop_duplicates("Num_Acc")
    agg_counts = df_unique['agg'].value_counts().reset_index()
    agg_counts.columns = ['agg', 'count']
    agg_counts['percent'] = agg_counts['count'] / agg_counts['count'].sum()
    
    fig = px.pie(
        agg_counts,
        names='agg',
        values='count',
        title="Répartition des accidents : en ville vs hors ville",
        color_discrete_sequence=['skyblue', 'orange'],
        hole=0.3
    )

    fig.update_traces(
        textinfo='percent',
        textposition='inside',
        insidetextorientation='radial',
        hovertemplate='%{label}<br>%{value} accidents<br>%{percent}',
        showlegend=True
    )

    fig.update_layout(
        legend_title_text="Zone",
        title_x=0.5
    )
    
    return fig

def plot_route_zone_count(df):

    grav_mapping = {
        'Indemne': 1,
        'Blessé léger': 2,
        'Blessé hospitalisé': 3,
        'Tué': 4
    }
    df['grav_num'] = df['grav'].map(grav_mapping)

    df_unique = df.drop_duplicates("Num_Acc")
    df_grouped = df_unique.groupby(['catr', 'agg']).size().reset_index(name='nb_accidents')
    fig = px.bar(
        df_grouped,
        x='catr',
        y='nb_accidents',
        color='agg',
        barmode='group',
        title="Nombre d'accidents par type de route et zone (agg)",
        labels={'catr': 'Type de route', 'nb_accidents': "Nombre d'accidents", 'agg': 'Zone'}
    )
    fig.update_layout(xaxis_tickangle=-45)
    return fig

def plot_route_zone_gravity(df):
        
    grav_mapping = {
        'Indemne': 1,
        'Blessé léger': 2,
        'Blessé hospitalisé': 3,
        'Tué': 4
    }
    df['grav_num'] = df['grav'].map(grav_mapping)

    df_gravite = df.groupby(['catr', 'agg'])['grav_num'].mean().reset_index(name='grav_moyenne')
    fig = px.bar(
        df_gravite,
        x='catr',
        y='grav_moyenne',
        color='agg',
        barmode='group',
        title="Gravité moyenne des accidents par type de route et zone",
        labels={'catr': 'Type de route', 'grav_moyenne': 'Gravité moyenne', 'agg': 'Zone'}
    )
    fig.update_layout(xaxis_tickangle=-45)
    return fig