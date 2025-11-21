from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import csv
import io
import os
import sys

# Ajouter le chemin du projet au Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import models, schemas, crud
from app.auth import get_current_active_user, get_current_admin_user, get_db, authenticate_user, create_access_token
from app.database import engine
from app.core.config import settings

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


# Routes d'authentification
@app.post("/auth/register", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email déjà enregistré")
    return crud.create_user(db=db, user=user)


@app.post("/auth/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = authenticate_user(db, user.email, user.password)
    if not db_user:
        raise HTTPException(status_code=400, detail="Email ou mot de passe incorrect")
    return create_access_token(data={"sub": db_user.email})


# Routes pour les indicateurs
@app.get("/indicators/", response_model=List[schemas.Indicator])
def read_indicators(
        type: Optional[str] = None,
        zone_id: Optional[int] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        limit: int = 25,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_active_user)
):
    start_dt = datetime.fromisoformat(start_date) if start_date else None
    end_dt = datetime.fromisoformat(end_date) if end_date else None

    filter_type = type if type and type.strip() != "" else None

    return crud.get_indicators(
        db,
        type=filter_type,
        zone_id=zone_id,
        start_date=start_dt,
        end_date=end_dt,
        limit=limit
    )


@app.post("/indicators/", response_model=schemas.Indicator)
def create_indicator(
        indicator: schemas.IndicatorCreate,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_active_user)
):
    return crud.create_indicator(db=db, indicator=indicator, user_id=current_user.id)


# Routes pour les zones
@app.get("/zones/", response_model=List[schemas.Zone])
def read_zones(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_active_user)
):
    return crud.get_zones(db, skip=skip, limit=limit)


# Routes pour les sources
@app.get("/sources/", response_model=List[schemas.Source])
def read_sources(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_active_user)
):
    return crud.get_sources(db, skip=skip, limit=limit)


# Routes de statistiques
@app.get("/stats/air/averages")
def get_air_averages(
        start_date: str,
        end_date: str,
        zone_id: Optional[int] = None,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_active_user)
):
    try:
        start_dt = datetime.fromisoformat(start_date)
        end_dt = datetime.fromisoformat(end_date)
        return crud.get_air_quality_by_zone(db, start_dt, end_dt, zone_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Format de date invalide: {e}")


@app.get("/stats/air/quality")
def get_air_quality_stats(
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_active_user)
):
    return crud.get_air_quality_stats(db)


# Routes ADMIN - Gestion des utilisateurs
@app.get("/admin/users/", response_model=List[schemas.User])
def get_all_users(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_admin_user)
):
    """Récupère tous les utilisateurs (admin seulement)"""
    return crud.get_users(db, skip=skip, limit=limit)


@app.get("/admin/users/{user_id}", response_model=schemas.User)
def get_user(
        user_id: int,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_admin_user)
):
    """Récupère un utilisateur par ID (admin seulement)"""
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return db_user


@app.put("/admin/users/{user_id}", response_model=schemas.User)
def update_user(
        user_id: int,
        user_update: schemas.UserUpdate,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_admin_user)
):
    """Met à jour un utilisateur (admin seulement)"""
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Vous ne pouvez pas modifier votre propre compte")

    db_user = crud.update_user(db, user_id=user_id, user_update=user_update)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return db_user


@app.delete("/admin/users/{user_id}")
def delete_user(
        user_id: int,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_admin_user)
):
    """Supprime un utilisateur (admin seulement)"""
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Vous ne pouvez pas supprimer votre propre compte")

    success = crud.delete_user(db, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return {"message": "Utilisateur supprimé avec succès"}


# Upload CSV
@app.post("/upload/csv/")
async def upload_csv(
        file: UploadFile = File(...),
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_admin_user)
):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Seuls les fichiers CSV sont acceptés")

    try:
        contents = await file.read()
        csv_data = io.StringIO(contents.decode('utf-8'))
        csv_reader = csv.DictReader(csv_data)

        indicators_created = 0
        for row in csv_reader:
            try:
                indicator_data = schemas.IndicatorCreate(
                    type=row['type'],
                    value=float(row['value']),
                    unit=row['unit'],
                    timestamp=row.get('timestamp', datetime.utcnow().isoformat()),
                    zone_id=int(row['zone_id']),
                    source_id=int(row['source_id']),
                    additional_data=row.get('additional_data')
                )
                crud.create_indicator(db, indicator_data, current_user.id)
                indicators_created += 1
            except Exception as e:
                print(f"Erreur ligne CSV: {e}")
                continue

        return {"message": f"{indicators_created} indicateurs créés avec succès"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur traitement CSV: {e}")


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