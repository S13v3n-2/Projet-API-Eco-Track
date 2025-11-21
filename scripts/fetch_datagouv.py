# scripts/fetch_datagouv.py
import requests
import pandas as pd


def fetch_french_environmental_data():
    # Qualité de l'air en France
    url = "https://www.data.gouv.fr/api/1/datasets/qualite-de-lair-mesures-temps-reel/"

    # Déchets municipaux
    waste_url = "https://www.data.gouv.fr/api/1/datasets/dechets-municipaux/"

    # Consommation énergétique
    energy_url = "https://www.data.gouv.fr/api/1/datasets/consommation-energetique/"