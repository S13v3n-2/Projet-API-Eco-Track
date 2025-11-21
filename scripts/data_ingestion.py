import requests
import pandas as pd
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import time
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models import Indicator, Zone, Source


def ingest_openaq_data():
    """Ingère les données OpenAQ avec gestion des doublons"""
    db = SessionLocal()

    try:
        cities = ["Paris", "Lyon", "Marseille", "Bordeaux", "Lille"]

        for city in cities:
            print(f"📥 Récupération données OpenAQ pour {city}...")

            data = fetch_openaq_data(city=city, limit=200)
            new_records = 0

            for measurement in data:
                # Vérifier si la donnée existe déjà
                existing = db.query(Indicator).filter(
                    Indicator.type == f"air_quality_{measurement['parameter']}",
                    Indicator.zone_id == get_zone_id(db, city),
                    Indicator.timestamp == datetime.fromisoformat(
                        measurement['date']['utc'].replace('Z', '+00:00')
                    )
                ).first()

                if not existing:
                    indicator = create_indicator_from_openaq(db, measurement, city)
                    if indicator:
                        db.add(indicator)
                        new_records += 1

            if new_records > 0:
                db.commit()
                print(f"✅ {new_records} nouvelles données pour {city}")
            else:
                print(f"ℹ️  Aucune nouvelle donnée pour {city}")

            time.sleep(2)  # Respecter les limites d'API

    except Exception as e:
        print(f"❌ Erreur ingestion OpenAQ: {e}")
        db.rollback()
    finally:
        db.close()


def ingest_weather_data():
    """Ingère les données météorologiques"""
    db = SessionLocal()

    try:
        zones = db.query(Zone).all()

        for zone in zones:
            # Coordonnées approximatives selon la ville
            coords = get_city_coordinates(zone.name)
            if coords:
                weather_data = fetch_weather_data(coords['lat'], coords['lon'])

                if weather_data:
                    # Créer indicateurs météo
                    create_weather_indicators(db, zone.id, weather_data)

        db.commit()
        print("✅ Données météo ingérées")

    except Exception as e:
        print(f"❌ Erreur ingestion météo: {e}")
        db.rollback()
    finally:
        db.close()


def fetch_openaq_data(city="Paris", limit=1000, hours_back=24):
    """Récupère les données OpenAQ des dernières 24h"""
    url = "https://api.openaq.org/v2/measurements"

    # Récupérer seulement les données récentes
    date_from = (datetime.utcnow() - timedelta(hours=hours_back)).strftime("%Y-%m-%dT%H:%M:%SZ")

    params = {
        "city": city,
        "limit": limit,
        "parameter": ["pm25", "pm10", "no2", "o3", "so2", "co"],
        "date_from": date_from,
        "sort": "desc"  # Les plus récentes d'abord
    }

    try:
        response = requests.get(url, params=params, timeout=30)
        if response.status_code == 200:
            return response.json()['results']
        else:
            print(f"⚠️ Erreur API OpenAQ: {response.status_code}")
    except Exception as e:
        print(f"⚠️ Erreur connexion OpenAQ: {e}")

    return []


# Fonctions utilitaires
def get_zone_id(db, city_name):
    """Trouve l'ID de zone correspondant à une ville"""
    zone = db.query(Zone).filter(Zone.name.ilike(f"%{city_name}%")).first()
    return zone.id if zone else None


def get_city_coordinates(city_name):
    """Retourne les coordonnées d'une ville"""
    coordinates = {
        "Paris": {"lat": 48.8566, "lon": 2.3522},
        "Lyon": {"lat": 45.7640, "lon": 4.8357},
        "Marseille": {"lat": 43.2965, "lon": 5.3698},
        "Bordeaux": {"lat": 44.8378, "lon": -0.5792},
        "Lille": {"lat": 50.6292, "lon": 3.0573}
    }

    for key, coords in coordinates.items():
        if key.lower() in city_name.lower():
            return coords
    return None


def create_indicator_from_openaq(db, measurement, city):
    """Crée un indicateur à partir des données OpenAQ"""
    zone_id = get_zone_id(db, city)
    source = db.query(Source).filter(Source.name == "OpenAQ").first()

    if not zone_id or not source:
        return None

    return Indicator(
        type=f"air_quality_{measurement['parameter']}",
        value=measurement['value'],
        unit=measurement['unit'],
        timestamp=datetime.fromisoformat(measurement['date']['utc'].replace('Z', '+00:00')),
        zone_id=zone_id,
        source_id=source.id,
        user_id=1,  # Admin user
        additional_data=str({
            "location": measurement.get('location', ''),
            "city": measurement.get('city', ''),
            "coordinates": measurement.get('coordinates', {})
        })
    )


if __name__ == "__main__":
    print("🌍 Début de l'ingestion manuelle...")
    ingest_openaq_data()
    ingest_weather_data()
    print("🎉 Ingestion terminée!")