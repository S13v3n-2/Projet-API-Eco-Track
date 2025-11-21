import time
import threading
import logging
from datetime import datetime, timedelta
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models import Indicator

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data/ingestion.log'),
        logging.StreamHandler()
    ]
)


class DataScheduler:
    def __init__(self):
        self.running = True
        self.jobs = []

    def job_air_quality(self):
        """Récupération des données qualité de l'air"""
        logging.info("🔄 Début ingestion qualité de l'air")
        try:
            from scripts.data_ingestion import ingest_openaq_data
            ingest_openaq_data()
            logging.info("✅ Qualité de l'air ingérée avec succès")
        except Exception as e:
            logging.error(f"❌ Erreur qualité de l'air: {e}")

    def job_weather_data(self):
        """Récupération des données météo"""
        logging.info("🌤️ Début ingestion données météo")
        try:
            from scripts.data_ingestion import ingest_weather_data
            ingest_weather_data()
            logging.info("✅ Météo ingérée avec succès")
        except Exception as e:
            logging.error(f"❌ Erreur météo: {e}")

    def job_energy_waste(self):
        """Récupération données énergie/déchets"""
        logging.info("⚡ Début ingestion énergie/déchets")
        try:
            from scripts.data_ingestion import ingest_energy_data
            ingest_energy_data()
            logging.info("✅ Énergie/déchets ingérés avec succès")
        except Exception as e:
            logging.error(f"❌ Erreur énergie/déchets: {e}")

    def job_cleanup_old_data(self):
        """Nettoyage des données anciennes (garder 3 mois)"""
        logging.info("🧹 Nettoyage des données anciennes")
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=90)
            db = SessionLocal()
            # Supprimer les indicateurs de plus de 3 mois
            deleted = db.query(Indicator).filter(Indicator.timestamp < cutoff_date).delete()
            db.commit()
            logging.info(f"✅ {deleted} anciens indicateurs supprimés")
        except Exception as e:
            logging.error(f"❌ Erreur nettoyage: {e}")
        finally:
            db.close()

    def run_periodic_job(self, job_function, interval_minutes, job_name):
        """Exécute une tâche périodiquement"""

        def wrapper():
            while self.running:
                try:
                    job_function()
                except Exception as e:
                    logging.error(f"❌ Erreur dans {job_name}: {e}")

                # Attendre l'intervalle spécifié
                for _ in range(interval_minutes * 60):
                    if not self.running:
                        break
                    time.sleep(1)

        thread = threading.Thread(target=wrapper, daemon=True, name=job_name)
        thread.start()
        self.jobs.append(thread)

    def run_daily_job(self, job_function, hour, minute, job_name):
        """Exécute une tâche quotidienne à une heure spécifique"""

        def wrapper():
            while self.running:
                try:
                    now = datetime.now()
                    # Calculer le prochain exécution
                    next_run = datetime(now.year, now.month, now.day, hour, minute)
                    if now > next_run:
                        next_run += timedelta(days=1)

                    wait_seconds = (next_run - now).total_seconds()

                    # Attendre jusqu'à l'heure programmée
                    for _ in range(int(wait_seconds)):
                        if not self.running:
                            break
                        time.sleep(1)

                    if self.running:
                        job_function()

                except Exception as e:
                    logging.error(f"❌ Erreur dans {job_name}: {e}")

        thread = threading.Thread(target=wrapper, daemon=True, name=job_name)
        thread.start()
        self.jobs.append(thread)

    def start(self):
        """Démarre le planificateur"""
        logging.info("🚀 Démarrage du planificateur de données EcoTrack")

        # Qualité de l'air - toutes les heures
        self.run_periodic_job(self.job_air_quality, 60, "air_quality_job")

        # Données météo - toutes les 2 heures
        self.run_periodic_job(self.job_weather_data, 120, "weather_job")

        # Énergie et déchets - tous les jours à 6h00
        self.run_daily_job(self.job_energy_waste, 6, 0, "energy_waste_job")

        # Nettoyage - tous les jours à 2h00
        self.run_daily_job(self.job_cleanup_old_data, 2, 0, "cleanup_job")

        logging.info("📅 Planificateur configuré avec succès")

        # Exécution immédiate au démarrage
        self.job_air_quality()
        self.job_weather_data()
        self.job_energy_waste()

    def stop(self):
        """Arrête le planificateur"""
        logging.info("🛑 Arrêt du planificateur...")
        self.running = False
        for job in self.jobs:
            job.join(timeout=5)


def main():
    scheduler = DataScheduler()

    try:
        scheduler.start()

        # Boucle principale
        while True:
            time.sleep(60)

    except KeyboardInterrupt:
        print("\n🛑 Arrêt demandé par l'utilisateur")
        scheduler.stop()
    except Exception as e:
        logging.error(f"❌ Erreur critique: {e}")
        scheduler.stop()


if __name__ == "__main__":
    main()