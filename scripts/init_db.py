import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import User, Zone, Source, Indicator
from app.auth import get_password_hash
from datetime import datetime
import json


def init_database():
    """
    Script d'initialisation de la base de données EcoTrack
    Crée les tables et insère des données de base
    """
    print("🔄 Création des tables...")

    # Créer TOUTES les tables
    Base.metadata.create_all(bind=engine)
    print("✅ Tables créées avec succès")

    db = SessionLocal()

    try:
        print("🔄 Initialisation des données de base...")

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
            {"name": "Paris Centre", "postal_code": "75001", "lat": 48.8566, "lon": 2.3522},
            {"name": "Lyon Centre", "postal_code": "69001", "lat": 45.7640, "lon": 4.8357},
            {"name": "Marseille Centre", "postal_code": "13001", "lat": 43.2965, "lon": 5.3698},
            {"name": "Bordeaux Centre", "postal_code": "33000", "lat": 44.8378, "lon": -0.5792},
            {"name": "Lille Centre", "postal_code": "59000", "lat": 50.6292, "lon": 3.0573},
        ]

        zones_created = 0
        for zone_data in zones_data:
            existing_zone = db.query(Zone).filter(
                Zone.name == zone_data["name"]
            ).first()

            if not existing_zone:
                # Créer la géométrie au format GeoJSON
                geometry = {
                    "type": "Point",
                    "coordinates": [zone_data["lon"], zone_data["lat"]]
                }

                zone = Zone(
                    name=zone_data["name"],
                    postal_code=zone_data["postal_code"],
                    geometry=json.dumps(geometry)  # Stocker en tant que JSON string
                )
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
                "name": "OpenMeteo",
                "description": "API météorologique gratuite avec données historiques",
                "url": "https://open-meteo.com"
            },
            {
                "name": "WAQI",
                "description": "World Air Quality Index - Données qualité air mondiales",
                "url": "https://waqi.info"
            },
            {
                "name": "ADEME",
                "description": "Agence de la transition écologique - Données environnementales françaises",
                "url": "https://data.ademe.fr"
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
        print("\n📥 Pour ingérer des données réelles:")
        print("   python scripts/data_ingestion.py")
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