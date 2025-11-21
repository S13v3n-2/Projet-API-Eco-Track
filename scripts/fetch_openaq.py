# scripts/fetch_openaq.py
import requests
import pandas as pd
from datetime import datetime


def fetch_openaq_data(city="Paris", limit=1000):
    url = f"https://api.openaq.org/v2/measurements"
    params = {
        "city": city,
        "limit": limit,
        "parameter": ["pm25", "pm10", "no2", "o3"]
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data['results']
    return []


# Exemple de données OpenAQ :
"""
{
    "parameter": "pm25",
    "value": 12.5,
    "unit": "µg/m³",
    "location": "Paris",
    "country": "FR",
    "city": "Paris",
    "coordinates": {"latitude": 48.8566, "longitude": 2.3522},
    "date": {"utc": "2024-01-15T10:00:00Z"}
}
"""