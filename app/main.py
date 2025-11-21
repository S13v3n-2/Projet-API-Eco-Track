from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import os
import sys

# Ajouter le chemin du projet au Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import models
from app.database import engine
from app.core.config import settings
from app.auth import get_db

# Importer les routeurs
from app.routes import (
    auth_router,
    indicators_router,
    zones_router,
    sources_router,
    stats_router,
    admin_router,
    upload_router
)

# Créer les tables
try:
    models.Base.metadata.create_all(bind=engine)
    print("✅ Tables de base de données créées avec succès")
except Exception as e:
    print(f"❌ Erreur création tables: {e}")

app = FastAPI(
    title="EcoTrack API",
    description="API de suivi des indicateurs environnementaux",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclure tous les routeurs
app.include_router(auth_router)
app.include_router(indicators_router)
app.include_router(zones_router)
app.include_router(sources_router)
app.include_router(stats_router)
app.include_router(admin_router)
app.include_router(upload_router)

# Routes de base
@app.get("/")
def read_root():
    return {"message": "Bienvenue sur EcoTrack API", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "database": "SQLite"}

@app.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    """Route de test pour la base de données"""
    try:
        user_count = db.query(models.User).count()
        return {"status": "success", "user_count": user_count}
    except Exception as e:
        return {"status": "error", "message": str(e)}