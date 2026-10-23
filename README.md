# France Road Accidents Analytics

### Analyse et visualisation des accidents de la route en France (2019–2023)

**Data Analytics · Python · Dash · Flask · SQLite · Machine Learning**

France Road Accidents Analytics est une application web interactive permettant d'explorer et d'analyser les accidents corporels de la circulation routière en France entre 2019 et 2023.

Le projet combine la préparation des données, l'analyse statistique, la cartographie interactive et l'expérimentation de modèles de Machine Learning afin de mieux comprendre les facteurs associés à la gravité des accidents.

## Objectifs du projet

- Étudier l'évolution des accidents de la route entre 2019 et 2023.
- Analyser les conditions météorologiques, temporelles et environnementales.
- Explorer la répartition géographique des accidents.
- Comparer les caractéristiques des véhicules et des usagers.
- Développer un outil de prédiction de la gravité des accidents.

## Fonctionnalités

| Module | Description |
|---|---|
| Dashboard | Interface interactive développée avec Dash |
| Statistiques météorologiques | Analyse des accidents selon les conditions atmosphériques |
| Analyses temporelles | Étude des évolutions et répartitions temporelles |
| Cartographie | Visualisation géographique avec filtres |
| Filtres interactifs | Période, catégorie de véhicule et gravité |
| Prédiction ML | Prototype de prédiction de gravité, en cours de finalisation |

## Technologies utilisées

| Catégorie | Technologies |
|---|---|
| Langage | Python |
| Traitement des données | Pandas, NumPy |
| Visualisation | Plotly, Dash, Dash Leaflet |
| Interface | Dash Bootstrap Components, CSS |
| Backend | Flask |
| Base de données | SQLite |
| Machine Learning | Scikit-learn, XGBoost, LightGBM |
| Environnement | Jupyter Notebook, VS Code |
| Versionnement | Git, GitHub |

## Préparation des données

### Source des données

Le projet repose sur des données d'accidents corporels de la circulation routière en France, provenant du dispositif BAAC (Bulletins d'Analyse des Accidents Corporels).

Les données originales sont structurées autour de quatre catégories :

- Caractéristiques des accidents
- Lieux des accidents
- Véhicules impliqués
- Usagers concernés

Le jeu de données consolidé `dataset.csv` sert de point de départ au pipeline de préparation présenté dans ce dépôt.

### Nettoyage des données

Le notebook `data/01_data_preparation.ipynb` documente les transformations réalisées pour produire un dataset adapté aux analyses.

Les traitements comprennent :

1. Exploration des données et analyse des valeurs manquantes.
2. Suppression de trois colonnes particulièrement incomplètes : `lartpc`, `occutc` et `v2`.
3. Création d'une variable `date` regroupant la date et l'heure.
4. Identification et suppression de 166 doublons strictement identiques sur les 55 variables intermédiaires.
5. Sélection des 39 variables du schéma utilisé par l'application.
6. Harmonisation des catégories de véhicules selon la nomenclature BAAC.
7. Contrôles de cohérence et exportation des données.

### Résultats du pipeline

| Indicateur | Valeur |
|---|---:|
| Observations initiales | 657 865 |
| Observations après nettoyage | 657 699 |
| Variables finales | 39 |
| Accidents uniques | 273 226 |
| Catégories de véhicules | 32 |
| Dates manquantes | 0 |
| Période | 2019–2023 |

Les observations répétées après sélection des 39 variables ont été conservées lorsqu'elles correspondaient à des enregistrements distincts dans le dataset intermédiaire.

Le nouveau dataset est enregistré sous :

`data/dataset_simplify_v2.csv`

**Remarque :** les datasets volumineux ne sont pas versionnés sur GitHub. Pour exécuter le projet localement, il faut disposer de `data/dataset.csv`, puis exécuter le notebook de préparation. La récupération ou la reconstruction automatisée du fichier consolidé à partir des quatre tables BAAC reste à documenter.

## Architecture du projet

```text
France-Road-Accidents-Analytics/
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── assets/
│   └── style.css
├── back/
│   ├── app.py
│   ├── meteo_analysis.py
│   ├── temporal_graphs.py
│   ├── vehicule_analysis.py
│   └── ...
├── data/
│   ├── 01_data_preparation.ipynb
│   ├── bdd_gen.py
│   ├── dataset.csv
│   ├── dataset_simplify_v2.csv
│   └── bdd_v2.db
├── front/
│   ├── pages/
│   └── graphs/
├── prediction/
│   └── *.ipynb
└── utils/
    ├── data_loader.py
    └── helpers.py
```

Les fichiers CSV et SQLite présentés dans l'arborescence sont générés ou conservés localement et ne sont pas nécessairement inclus dans le dépôt distant.

## Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/Carneiro-David/France-Road-Accidents-Analytics.git
cd France-Road-Accidents-Analytics
```

### 2. Créer un environnement virtuel

Sous Windows :

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Sous Linux / macOS :

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Installer les dépendances

```bash
python -m pip install -r requirements.txt
```

Les dépendances supplémentaires nécessaires à l'exécution des notebooks doivent être installées selon les modèles utilisés.

### 4. Préparer le dataset

Placer le fichier consolidé `dataset.csv` dans le dossier `data/`.

Ouvrir ensuite :

```text
data/01_data_preparation.ipynb
```

Exécuter les cellules dans l'ordre afin de générer :

```text
data/dataset_simplify_v2.csv
```

### 5. Générer la base SQLite

Depuis la racine du projet :

```bash
python -m data.bdd_gen
```

Cette commande crée :

```text
data/bdd_v2.db
```

La table `accidents` contient les observations préparées à partir du CSV.

### 6. Démarrer Flask

Dans un premier terminal :

```bash
python -m back.app
```

API disponible sur :

`http://127.0.0.1:5001`

### 7. Démarrer Dash

Dans un deuxième terminal :

```bash
python app.py
```

Dashboard disponible sur :

`http://127.0.0.1:8050`

Les deux serveurs doivent être actifs pour utiliser les fonctionnalités qui reposent sur l'API Flask.

## API Flask

| Endpoint | Méthode | Fonction |
|---|---|---|
| `/vehicule-types` | GET | Liste des catégories de véhicules |
| `/grav-types` | GET | Liste des niveaux de gravité |
| `/points` | GET | Coordonnées et caractéristiques des accidents filtrés |
| `/prediction` | POST | Prototype de prédiction de la gravité |

La route `/prediction` nécessite encore la finalisation du chargement des modèles, des transformations des variables et du traitement des réponses.

## Machine Learning

Le projet contient plusieurs notebooks d'expérimentation et de comparaison de modèles de classification :

- Random Forest
- XGBoost
- LightGBM
- HistGradientBoosting

L'objectif est d'estimer la catégorie de gravité d'un accident à partir des caractéristiques disponibles.

Le module de prédiction intégré à l'application est actuellement en cours de finalisation. Les performances des modèles ne sont pas annoncées tant que les évaluations n'ont pas été vérifiées.

## Améliorations prévues

- [x] Reconstruction et documentation du dataset simplifié
- [x] Création d'une nouvelle base SQLite
- [x] Harmonisation des catégories de véhicules
- [x] Centralisation des chemins avec `config.py`
- [ ] Finalisation du module de prédiction Machine Learning
- [ ] Optimisation des requêtes SQLite et du chargement cartographique
- [ ] Amélioration du design et de l'expérience utilisateur
- [ ] Ajout de tests automatisés
- [ ] Automatisation de la récupération des données sources
- [ ] Déploiement du dashboard

## Auteur

Projet réalisé dans le cadre d'un travail d'analyse de données et de Machine Learning, puis repris et amélioré pour un portfolio professionnel.

GitHub : [Carneiro-David](https://github.com/Carneiro-David)

---

*Les analyses et prédictions présentées dans ce projet ont un objectif exploratoire et pédagogique. Elles ne constituent pas un dispositif opérationnel de prédiction du risque routier.*
