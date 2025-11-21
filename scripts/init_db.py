import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import User, Zone, Source, Indicator
from app.auth import get_password_hash
from datetime import datetime

def init_database():
    # Créer les tables
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        print("🔄 Initialisation de la base de données EcoTrack...")

        # Vérifier si l'admin existe déjà
        admin_exists = db.query(User).filter(User.email == "admin@ecotrack.com").first()
        if not admin_exists:
            # Créer admin
            admin = User(
                email="admin@ecotrack.com",
                hashed_password=get_password_hash("admin123"),
                full_name="Administrateur EcoTrack",
                role="admin"
            )
            db.add(admin)
            db.commit()
            db.refresh(admin)
            print("✅ Admin créé")
        else:
            admin = admin_exists
            print("✅ Admin existe déjà")

        # Vérifier si les zones existent
        zones_count = db.query(Zone).count()
        if zones_count == 0:
            # Créer zones
            zones = [
                Zone(name="Paris Centre", postal_code="75001"),
                Zone(name="Lyon Centre", postal_code="69001"),
                Zone(name="Marseille Centre", postal_code="13001"),
                Zone(name="Bordeaux Centre", postal_code="33000"),
                Zone(name="Lille Centre", postal_code="59000"),
            ]
            for zone in zones:
                db.add(zone)
            db.commit()
            print("✅ Zones créées")
        else:
            print(f"✅ {zones_count} zones existent déjà")

        # Vérifier si les sources existent
        sources_count = db.query(Source).count()
        if sources_count == 0:
            # Créer sources
            sources = [
                Source(name="OpenAQ", description="Données qualité de l'air ouvertes", url="https://openaq.org"),
                Source(name="ADEME", description="Agence de la transition écologique", url="https://data.ademe.fr"),
                Source(name="data.gouv.fr", description="Plateforme ouverte des données publiques françaises",
                       url="https://data.gouv.fr"),
            ]
            for source in sources:
                db.add(source)
            db.commit()
            print("✅ Sources créées")
        else:
            print(f"✅ {sources_count} sources existent déjà")

        # Récupérer les IDs
        zones = db.query(Zone).all()
        sources = db.query(Source).all()

        # Créer quelques indicateurs d'exemple
        indicators_count = db.query(Indicator).count()
        if indicators_count == 0 and zones and sources and admin:
            indicators = [
                Indicator(
                    type="air_quality",
                    value=45.2,
                    unit="AQI",
                    timestamp=datetime.utcnow(),
                    zone_id=zones[0].id,
                    source_id=sources[0].id,
                    additional_data='{"pollutant": "PM2.5", "level": "moderate"}',
                    user_id=admin.id
                ),
                Indicator(
                    type="co2",
                    value=420.5,
                    unit="ppm",
                    timestamp=datetime.utcnow(),
                    zone_id=zones[1].id,
                    source_id=sources[1].id,
                    additional_data='{"source": "traffic", "season": "winter"}',
                    user_id=admin.id
                ),
                Indicator(
                    type="energy",
                    value=1250.8,
                    unit="kWh",
                    timestamp=datetime.utcnow(),
                    zone_id=zones[2].id,
                    source_id=sources[2].id,
                    additional_data='{"sector": "residential", "renewable": false}',
                    user_id=admin.id
                ),
                Indicator(
                    type="waste",
                    value=250.3,
                    unit="kg",
                    timestamp=datetime.utcnow(),
                    zone_id=zones[3].id,
                    source_id=sources[0].id,
                    additional_data='{"category": "plastic", "recycled": true}',
                    user_id=admin.id
                ),
            ]
            for indicator in indicators:
                db.add(indicator)
            db.commit()
            print("✅ Indicateurs d'exemple créés")
        else:
            print(f"✅ {indicators_count} indicateurs existent déjà")

        print("🎉 Base de données initialisée avec succès!")
        print("📁 Fichier: data/ecotrack.db")

    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_database()