import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import inspect
from app.database import engine, SessionLocal
from app.models import User, Zone, Source, Indicator


def check_database():
    """Vérifie l'état de la base de données"""
    print("🔍 Vérification de la base de données...")

    # Vérifier les tables
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    required_tables = ['users', 'zones', 'sources', 'indicators']
    missing_tables = []

    print("📋 Tables trouvées:")
    for table in tables:
        print(f"  {'✅' if table in required_tables else '⚠️'} {table}")

    for table in required_tables:
        if table not in tables:
            missing_tables.append(table)

    if missing_tables:
        print(f"\n❌ Tables manquantes: {missing_tables}")
        return False

    # Vérifier les données
    db = SessionLocal()
    try:
        user_count = db.query(User).count()
        zone_count = db.query(Zone).count()
        source_count = db.query(Source).count()
        indicator_count = db.query(Indicator).count()

        print(f"\n📊 Données dans la base:")
        print(f"  👥 Utilisateurs: {user_count}")
        print(f"  🗺️ Zones: {zone_count}")
        print(f"  📚 Sources: {source_count}")
        print(f"  📈 Indicateurs: {indicator_count}")

        if zone_count == 0:
            print("\n❌ Aucune zone trouvée - la base doit être initialisée")
            return False

        return True

    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")
        return False
    finally:
        db.close()


if __name__ == "__main__":
    if check_database():
        print("\n🎉 La base de données est prête!")
    else:
        print("\n💡 Exécutez: python scripts/init_db.py")