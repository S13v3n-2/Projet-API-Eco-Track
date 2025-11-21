# EcoTrack - API de Suivi Environnemental

EcoTrack est une interface de programmation (API REST) développée avec
le framework FastAPI. Elle permet la collecte, le stockage et l'analyse
d'indicateurs environnementaux locaux tels que la qualité de l'air, les
conditions météorologiques et la consommation énergétique.

Ce projet a été réalisé dans un cadre pédagogique pour démontrer
l'implémentation d'une architecture backend complète incluant
l'authentification sécurisée, la gestion de bases de données
relationnelles et l'ingestion de données externes.

## Table des matières

-   Description du projet
-   Architecture technique
-   Fonctionnalités
-   Prérequis
-   Installation
-   Utilisation
-   Documentation de lAPI
-   Sources de données
-   Structure du projet
-   Auteurs et Licence

## Description du projet

L'application EcoTrack agrège des séries temporelles d'indicateurs
environnementaux par zone géographique. Elle expose ces données via une
API documentée et fournit un tableau de bord (dashboard) pour la
visualisation.

Le système est conçu pour :

-   Centraliser des données hétérogènes (API externes, fichiers CSV).
-   Fournir des statistiques agrégées (moyennes, tendances).
-   Gérer les droits d'accès via un système de rôles (RBAC).

## Architecture technique

Le projet repose sur les technologies suivantes :

-   Langage : Python 3.8+
-   Framework Web : FastAPI
-   Serveur d'application : Uvicorn
-   Base de données : SQLite
-   ORM : SQLAlchemy
-   Authentification : JWT (JSON Web Tokens) et Passlib (Bcrypt)
-   Frontend : HTML5, CSS3, JavaScript (Vanilla)

## Fonctionnalités

### Backend (API)

-   Authentification : Inscription et connexion sécurisée par token JWT.
-   Gestion des utilisateurs : Distinction entre utilisateurs standards
    (lecture seule) et administrateurs (gestion des utilisateurs, import
    de données).
-   Indicateurs : Création, lecture, filtrage (par date, zone, type) et
    pagination des données.
-   Statistiques : Calcul de moyennes et analyse de la qualité de l'air
    sur des périodes données.
-   Ingestion : Scripts automatisés pour la récupération de données
    depuis des API tierces.

### Frontend (Dashboard)

-   Visualisation des indicateurs sous forme de cartes.
-   Interface d'administration pour la gestion des comptes utilisateurs.
-   Déclenchement manuel de la synchronisation des données externes.

## Prérequis

-   Python 3.8 ou version supérieure.
-   pip (gestionnaire de paquets Python).
-   Un navigateur web moderne pour l'accès au dashboard.

## Installation

### Cloner le dépôt

``` bash
git clone [https://github.com/votre-username/ecotrack.git](https://github.com/S13v3n-2/Projet-API-Eco-Track.git)
cd Projet-API-Eco-Track
```

### Créer un environnement virtuel

``` bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / MacOS
python3 -m venv venv
source venv/bin/activate
```

### Installer les dépendances

``` bash
pip install -r requirements.txt
```

### Initialiser la base de données

``` bash
python scripts/init_db.py
```

### Peupler la base de données

``` bash
python scripts/data_ingestion.py
```

## Utilisation

### Démarrage du serveur

``` bash
uvicorn app.main:app --reload
```

API : http://127.0.0.1:8000

### Accès au Dashboard

Identifiants Admin :\
Email : admin@ecotrack.com\
Mot de passe : admin123

## Documentation de l'API

http://127.0.0.1:8000/docs

### Endpoints

-   Auth : /auth/login, /auth/register
-   Indicateurs : /indicators/ (GET, POST)
-   Zones : /zones/ (GET)
-   Statistiques : /stats/air/averages
-   Administration : /admin/users/

## Sources de données

-   Open-Meteo
-   WAQI
-   Data.gouv.fr / ADEME

## Structure du projet

    .
    ├── README.md
    ├── app
    │   ├── __init__.py
    │   ├── auth.py
    │   ├── core
    │   ├── crud.py
    │   ├── database.py
    │   ├── main.py
    │   ├── models.py
    │   ├── routes.py
    │   └── schemas.py
    ├── data
    │   └── ecotrack.db
    ├── frontend
    │   ├── css
    │   ├── index.html
    │   └── js
    ├── requirements.txt
    └── scripts

## Auteurs et Licence

Ce projet a été développé dans le cadre d'un cursus universitaire.\
Licence : MIT License
