# -Projet-API-Eco-Track
API REST pour collecter et analyser des indicateurs écologiques (qualité de l’air, CO₂, déchets). Authentification JWT, rôles utilisateur/admin, ORM SQLAlchemy, endpoints de recherche et statistiques. Inclut scripts d’ingestion de données, tests et frontend léger. Développé dans le cadre d’un projet pédagogique.

# EcoTrack - API de Suivi Environnemental

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)](https://sqlite.org)

**Une API complète pour le suivi des indicateurs environnementaux** - Qualité de l'air, météo, énergie et déchets

## Table des matières

- [EcoTrack - API de Suivi Environnemental](#ecotrack---api-de-suivi-environnemental)
  - [Table des matières](#table-des-matières)
  - [Présentation](#présentation)
  - [Fonctionnalités](#fonctionnalités)
  - [Architecture](#architecture)
  - [Installation](#installation)
    - [Prérequis](#prérequis)
    - [Installation et démarrage](#installation-et-démarrage)
  - [Utilisation](#utilisation)
    - [Démarrage de l'API](#démarrage-de-lapi)
    - [Accès au dashboard](#accès-au-dashboard)
  - [API Endpoints](#api-endpoints)
    - [Authentification](#authentification)
    - [Indicateurs](#indicateurs)
    - [Zones](#zones)
    - [Statistiques](#statistiques)
    - [Administration](#administration)
  - [Modèle de données](#modèle-de-données)
  - [Sources de données](#sources-de-données)
  - [Développement](#développement)
    - [Structure du projet](#structure-du-projet)
    - [Tests](#tests)
    - [Scripts utiles](#scripts-utiles)
  - [Dashboard](#dashboard)
  - [Contribution](#contribution)
  - [Licence](#licence)

## Présentation

EcoTrack est une API REST complète développée avec **FastAPI** permettant de collecter, stocker et analyser des données environnementales en temps réel. Le projet répond aux exigences pédagogiques du cours API en mettant en œuvre les bonnes pratiques de développement.

**Objectifs principaux :**
- Agréger des données environnementales multiples
- Gestion sécurisée des utilisateurs et permissions
- Fournir des statistiques et analyses
- Interface web intuitive

## Fonctionnalités

### Authentification & Sécurité
- **Inscription/Connexion** avec tokens JWT
- **Rôles utilisateurs** : `user` (lecture) et `admin` (CRUD complet)
- **Protection des routes** avec dépendances FastAPI
- **Tokens d'accès** avec expiration configurable

### Gestion des Données
- **CRUD complet** pour les indicateurs environnementaux
- **Filtres avancés** : dates, zones, types d'indicateurs
- **Pagination** et limites de résultats
- **Import CSV** pour données massives

### Intégration Données Externes
- **Open-Meteo** : données météorologiques en temps réel
- **WAQI** : qualité de l'air mondiale
- **data.gouv.fr** : données énergétiques et environnementales françaises

### Analytics & Statistiques
- **Moyennes** par zone et période
- **Tendances** temporelles
- **Agrégations** pour visualisations

### Administration
- **Gestion utilisateurs** complète
- **Interface admin** sécurisée
- **Monitoring** des données

## Architecture
```python
EcoTrack/
├── app/ # Application principale
│ ├── main.py # Point d'entrée FastAPI
│ ├── routes.py # Tous les endpoints API
│ ├── models.py # Modèles SQLAlchemy
│ ├── schemas.py # Schémas Pydantic
│ ├── crud.py # Opérations base de données
│ ├── auth.py # Authentification JWT
│ ├── database.py # Configuration DB
│ └── core/
│ └── config.py # Variables d'environnement
├── data_ingestion.py # Script d'ingestion données externes
├── frontend/ # Dashboard web
│ ├── index.html
│ ├── css/style.css
│ └── js/
│ ├── app.js
│ ├── auth.js
│ ├── dashboard.js
│ ├── filters.js
│ ├── admin.js
│ └── data-ingestion.js
└── requirements.txt
```

## Installation

### Prérequis

- **Python 3.8+**
- **pip** (gestionnaire de packages Python)
- **Navigateur web moderne**

### Installation et démarrage

1. **Cloner le repository**
'''
git clone <votre-repo>
cd EcoTrack
pip install -r requirements.txt
cd Projet-API-Eco-Track
python scripts/init_db.py
python scripts/data_ingestion.py
uvicorn app.main:app --reload
'''

L'API sera accessible sur : http://localhost:8000

Connectez-vous avec :
Email : admin@ecotrack.com
Mot de passe : admin123

API Endpoints
Authentification
Method	Endpoint	Description
POST	/auth/register	Création de compte
POST	/auth/login	Connexion (JWT)
Indicateurs
Method	Endpoint	Description
GET	/indicators/	Liste avec filtres
POST	/indicators/	Création indicateur
POST	/indicators/ingest/external-data	Récupération données externes
Zones
Method	Endpoint	Description
GET	/zones/	Liste des zones
Statistiques
Method	Endpoint	Description
GET	/stats/air/averages	Moyennes qualité air
GET	/stats/air/quality	Stats globales
Administration
Method	Endpoint	Description	Accès
GET	/admin/users/	Liste utilisateurs	Admin
PUT	/admin/users/{id}	Modification	Admin
DELETE	/admin/users/{id}	Suppression	Admin
Modèle de données
User
id, email, hashed_password, full_name, is_active, role

Zone
id, name, postal_code, geometry

Source
id, name, description, url

Indicator
id, type, value, unit, timestamp, additional_data

Clés étrangères : zone_id, source_id, user_id

Sources de données
Source	Données	Fréquence	Limitations
Open-Meteo	Météo temps réel	1h	Données historiques limitées
WAQI	Qualité air	1h	Token démo limité
data.gouv.fr	Énergie, déchets	Quotidien	Données agrégées
OpenAQ	Polluants air	Temps réel	Stations limitées
