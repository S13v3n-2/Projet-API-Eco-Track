import sys
import os

# Ajouter le chemin du projet
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import User, Zone, Source, Indicator
from app.auth import get_password_hash
from datetime import datetime


def init_database():
    """
    Script d'initialisation de la base de données EcoTrack
    Crée les tables et insère des données d'exemple
    """
    # Créer les tables
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        print("🔄 Initialisation de la base de données EcoTrack...")
        print("📁 Base de données: data/ecotrack.db")

        # === CRÉATION DE L'UTILISATEUR ADMIN ===
        admin_email = "admin@ecotrack.com"
        admin_exists = db.query(User).filter(User.email == admin_email).first()

        if not admin_exists:
            admin = User(
                email=admin_email,
                hashed_password=get_password_hash("admin123"),
                full_name="Administrateur EcoTrack",
                role="admin",
                is_active=True
            )
            db.add(admin)
            db.commit()
            db.refresh(admin)
            print("✅ Utilisateur admin créé (admin@ecotrack.com / admin123)")
        else:
            admin = admin_exists
            print("✅ Utilisateur admin existe déjà")

        # === CRÉATION DES ZONES GÉOGRAPHIQUES ===
        zones_data = [
            {"name": "Paris Centre", "postal_code": "75001"},
            {"name": "Paris Nord", "postal_code": "75018"},
            {"name": "Paris Sud", "postal_code": "75014"},
            {"name": "Lyon Centre", "postal_code": "69001"},
            {"name": "Lyon Part-Dieu", "postal_code": "69003"},
            {"name": "Marseille Centre", "postal_code": "13001"},
            {"name": "Marseille Vieux-Port", "postal_code": "13007"},
            {"name": "Bordeaux Centre", "postal_code": "33000"},
            {"name": "Lille Centre", "postal_code": "59000"},
            {"name": "Toulouse Centre", "postal_code": "31000"},
        ]

        zones_created = 0
        for zone_data in zones_data:
            existing_zone = db.query(Zone).filter(
                Zone.name == zone_data["name"]
            ).first()

            if not existing_zone:
                zone = Zone(**zone_data)
                db.add(zone)
                zones_created += 1

        if zones_created > 0:
            db.commit()
            print(f"✅ {zones_created} zones créées")
        else:
            print("✅ Zones existent déjà")

        # === CRÉATION DES SOURCES DE DONNÉES ===
        sources_data = [
            {
                "name": "OpenAQ",
                "description": "Plateforme ouverte de données sur la qualité de l'air en temps réel",
                "url": "https://openaq.org"
            },
            {
                "name": "ADEME",
                "description": "Agence de la transition écologique - Données environnementales françaises",
                "url": "https://data.ademe.fr"
            },
            {
                "name": "data.gouv.fr",
                "description": "Plateforme ouverte des données publiques françaises",
                "url": "https://data.gouv.fr"
            },
            {
                "name": "OpenMeteo",
                "description": "API météorologique gratuite avec données historiques",
                "url": "https://open-meteo.com"
            },
            {
                "name": "Capteurs Locaux",
                "description": "Réseau de capteurs environnementaux locaux",
                "url": ""
            }
        ]

        sources_created = 0
        for source_data in sources_data:
            existing_source = db.query(Source).filter(
                Source.name == source_data["name"]
            ).first()

            if not existing_source:
                source = Source(**source_data)
                db.add(source)
                sources_created += 1

        if sources_created > 0:
            db.commit()
            print(f"✅ {sources_created} sources de données créées")
        else:
            print("✅ Sources de données existent déjà")

        # === CRÉATION D'INDICATEURS ENVIRONNEMENTAUX D'EXEMPLE ===
        zones = db.query(Zone).all()
        sources = db.query(Source).all()

        if not zones or not sources:
            print("❌ Impossible de créer les indicateurs: zones ou sources manquantes")
            return

        # Types d'indicateurs environnementaux
        indicator_types = [
            {
                "type": "air_quality_pm25",
                "unit": "µg/m³",
                "description": "Particules fines PM2.5"
            },
            {
                "type": "air_quality_pm10",
                "unit": "µg/m³",
                "description": "Particules fines PM10"
            },
            {
                "type": "air_quality_no2",
                "unit": "µg/m³",
                "description": "Dioxyde d'azote"
            },
            {
                "type": "co2",
                "unit": "ppm",
                "description": "Dioxyde de carbone"
            },
            {
                "type": "temperature",
                "unit": "°C",
                "description": "Température ambiante"
            },
            {
                "type": "humidity",
                "unit": "%",
                "description": "Humidité relative"
            },
            {
                "type": "waste_production",
                "unit": "kg/jour",
                "description": "Production de déchets"
            },
            {
                "type": "energy_consumption",
                "unit": "kWh",
                "description": "Consommation énergétique"
            }
        ]

        # Créer des indicateurs réalistes pour chaque zone
        indicators_created = 0
        from datetime import timedelta

        for zone in zones:
            for i, ind_type in enumerate(indicator_types):
                # Valeurs réalistes selon le type d'indicateur
                base_values = {
                    "air_quality_pm25": (8, 25),  # µg/m³ (bon à moyen)
                    "air_quality_pm10": (12, 40),  # µg/m³
                    "air_quality_no2": (15, 60),  # µg/m³
                    "co2": (400, 450),  # ppm
                    "temperature": (5, 25),  # °C
                    "humidity": (40, 85),  # %
                    "waste_production": (200, 800),  # kg/jour
                    "energy_consumption": (1000, 5000)  # kWh
                }

                min_val, max_val = base_values.get(ind_type["type"], (0, 100))

                # Créer 3 mesures par indicateur avec des dates différentes
                for days_ago in [0, 1, 2]:
                    # Variation réaliste selon la zone et le temps
                    zone_factor = hash(zone.name) % 100 / 100  # Facteur unique par zone
                    time_factor = (days_ago * 0.1)  # Légère variation dans le temps

                    value = min_val + (max_val - min_val) * (0.5 + zone_factor * 0.5 - time_factor)
                    value = round(value, 2)

                    # Vérifier si l'indicateur existe déjà
                    existing_indicator = db.query(Indicator).filter(
                        Indicator.type == ind_type["type"],
                        Indicator.zone_id == zone.id,
                        Indicator.timestamp == datetime.utcnow() - timedelta(days=days_ago)
                    ).first()

                    if not existing_indicator:
                        indicator = Indicator(
                            type=ind_type["type"],
                            value=value,
                            unit=ind_type["unit"],
                            timestamp=datetime.utcnow() - timedelta(days=days_ago),
                            zone_id=zone.id,
                            source_id=sources[i % len(sources)].id,  # Répartir les sources
                            user_id=admin.id,
                            additional_data=f'{{"description": "{ind_type["description"]}", "quality": "good"}}'
                        )
                        db.add(indicator)
                        indicators_created += 1

        if indicators_created > 0:
            db.commit()
            print(f"✅ {indicators_created} indicateurs environnementaux créés")
        else:
            print("✅ Indicateurs environnementaux existent déjà")

        # === RÉSUMÉ FINAL ===
        print("\n" + "=" * 50)
        print("🎉 BASE DE DONNÉES INITIALISÉE AVEC SUCCÈS!")
        print("=" * 50)

        # Statistiques finales
        total_users = db.query(User).count()
        total_zones = db.query(Zone).count()
        total_sources = db.query(Source).count()
        total_indicators = db.query(Indicator).count()

        print(f"👥 Utilisateurs: {total_users}")
        print(f"🗺️ Zones géographiques: {total_zones}")
        print(f"📚 Sources de données: {total_sources}")
        print(f"📈 Indicateurs environnementaux: {total_indicators}")
        print("\n🔑 Identifiants de test:")
        print("   Email: admin@ecotrack.com")
        print("   Mot de passe: admin123")
        print("\n🌐 Pour démarrer l'API:")
        print("   uvicorn app.main:app --reload")
        print("=" * 50)

    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()

    finally:
        db.close()


if __name__ == "__main__":
    init_database()