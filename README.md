EcoTrack - API de Suivi Environnemental
EcoTrack est une interface de programmation (API REST) développée avec le framework FastAPI. Elle permet la collecte, le stockage et l'analyse d'indicateurs environnementaux locaux tels que la qualité de l'air, les conditions météorologiques et la consommation énergétique.

Ce projet a été réalisé dans un cadre pédagogique pour démontrer l'implémentation d'une architecture backend complète incluant l'authentification sécurisée, la gestion de bases de données relationnelles et l'ingestion de données externes.

Table des matières
Description du projet

Architecture technique

Fonctionnalités

Prérequis

Installation

Utilisation

Documentation de l'API

Sources de données

Auteurs et Licence

Description du projet
L'application EcoTrack agrège des séries temporelles d'indicateurs environnementaux par zone géographique. Elle expose ces données via une API documentée et fournit un tableau de bord (dashboard) pour la visualisation.

Le système est conçu pour :

Centraliser des données hétérogènes (API externes, fichiers CSV).

Fournir des statistiques agrégées (moyennes, tendances).

Gérer les droits d'accès via un système de rôles (RBAC).

Architecture technique
Le projet repose sur les technologies suivantes :

Langage : Python 3.8+

Framework Web : FastAPI

Serveur d'application : Uvicorn

Base de données : SQLite

ORM : SQLAlchemy

Authentification : JWT (JSON Web Tokens) et Passlib (Bcrypt)

Frontend : HTML5, CSS3, JavaScript (Vanilla)

Fonctionnalités
Backend (API)
Authentification : Inscription et connexion sécurisée par token JWT.

Gestion des utilisateurs : Distinction entre utilisateurs standards (lecture seule) et administrateurs (gestion des utilisateurs, import de données).

Indicateurs : Création, lecture, filtrage (par date, zone, type) et pagination des données.

Statistiques : Calcul de moyennes et analyse de la qualité de l'air sur des périodes données.

Ingestion : Scripts automatisés pour la récupération de données depuis des API tierces.

Frontend (Dashboard)
Visualisation des indicateurs sous forme de cartes.

Interface d'administration pour la gestion des comptes utilisateurs.

Déclenchement manuel de la synchronisation des données externes.

Prérequis
Python 3.8 ou version supérieure.

pip (gestionnaire de paquets Python).

Un navigateur web moderne pour l'accès au dashboard.

Installation
Suivez les étapes ci-dessous pour configurer l'environnement de développement.

Cloner le dépôt

```Bash

git clone https://github.com/votre-username/ecotrack.git
cd ecotrack
Créer un environnement virtuel
```
```Bash

# Windows
python -m venv venv
venv\Scripts\activate

# Linux / MacOS
python3 -m venv venv
source venv/bin/activate
Installer les dépendances
```
```Bash
pip install -r requirements.txt
Initialiser la base de données Ce script crée les tables nécessaires et configure le compte administrateur par défaut.
```
```Bash
python scripts/init_db.py
(Optionnel) Peupler la base de données Pour récupérer les données météorologiques et de qualité de l'air initiales :
```
```Bash
python scripts/data_ingestion.py
Utilisation
Démarrage du serveur
Lancez le serveur API avec la commande suivante :
```
```Bash
uvicorn app.main:app --reload
```
L'API sera accessible à l'adresse : http://127.0.0.1:8000

Accès au Dashboard
Ouvrez le fichier frontend/index.html dans votre navigateur.

Identifiants par défaut (Admin) :

Email : admin@ecotrack.com

Mot de passe : admin123

Ces identifiants sont générés par le script scripts/init_db.py.

Documentation de l'API
Une documentation interactive (Swagger UI) est générée automatiquement par FastAPI. Une fois le serveur lancé, elle est accessible à l'adresse suivante :

http://127.0.0.1:8000/docs

Principaux points de terminaison (Endpoints)
Auth : /auth/login, /auth/register

Indicateurs : /indicators/ (GET, POST)

Zones : /zones/ (GET)

Statistiques : /stats/air/averages

Administration : /admin/users/

Sources de données
Les données environnementales proviennent des sources suivantes, intégrées via le script d'ingestion :

Open-Meteo : Données météorologiques (Température, Vent, Humidité).

WAQI (World Air Quality Index) : Données de qualité de l'air (PM2.5, PM10, NO2).

Data.gouv.fr / ADEME : Données simulées pour la consommation énergétique et les émissions de CO2.

Structure du projet
```Plaintext
.
├── README.md                   # Documentation du projet
├── app                         # Code source principal de l'API Backend
│   ├── __init__.py
│   ├── auth.py                 # Gestion de l'authentification et tokens JWT
│   ├── core                    # Configuration du cœur de l'application
│   │   ├── __init__.py
│   │   └── config.py           # Variables d'environnement et paramètres
│   ├── crud.py                 # Opérations de base de données (Create, Read, Update, Delete)
│   ├── database.py             # Configuration de la connexion SQLAlchemy
│   ├── main.py                 # Point d'entrée de l'application FastAPI
│   ├── models.py               # Définition des modèles de données (Tables)
│   ├── routes.py               # Définition des endpoints et routeurs API
│   └── schemas.py              # Schémas Pydantic pour la validation des données
├── data
│   └── ecotrack.db             # Fichier de base de données SQLite
├── frontend                    # Interface utilisateur web
│   ├── css
│   │   └── style.css           # Feuilles de style pour le dashboard
│   ├── index.html              # Page principale unique (Single Page App)
│   └── js
│       ├── admin.js            # Logique de gestion des utilisateurs (admin)
│       ├── app.js              # Configuration globale et utilitaires JS
│       ├── auth.js             # Gestion de la connexion et inscription
│       ├── dashboard.js        # Logique d'affichage des indicateurs
│       ├── data-ingestion.js   # Gestion du déclenchement de l'ingestion
│       └── filters.js          # Logique de filtrage (dates, zones)
├── requirements.txt            # Liste des dépendances Python
└── scripts                     # Scripts utilitaires pour la gestion du projet
    ├── __init__.py
    ├── check_database.py       # Script de diagnostic de la base de données
    ├── data_ingestion.py       # Script backend de récupération des API externes
    ├── init_db.py              # Script d'initialisation (création tables + admin)
    └── test.py                 # Script de test rapide
```
Auteurs et Licence
Ce projet a été développé dans le cadre d'un cursus universitaire.

Licence : MIT License