from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

from .core.config import settings

# Créer le dossier data s'il n'existe pas
os.makedirs("data", exist_ok=True)

# Configuration SQLite avec support pour les threads
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dépendance de base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()