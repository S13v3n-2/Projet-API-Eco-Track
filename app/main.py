from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import csv
import io

from . import models, schemas, crud
from .auth import get_current_active_user, get_current_admin_user, get_db, authenticate_user, create_access_token
from .database import engine
from .core.config import settings

# Créer les tables
models.Base.metadata.create_all(bind=engine)

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
        skip: int = 0,
        limit: int = 100,
        type: Optional[str] = None,
        zone_id: Optional[int] = None,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_active_user)
):
    if type:
        return crud.get_indicators_by_type(db, indicator_type=type)
    elif zone_id:
        return crud.get_indicators_by_zone(db, zone_id=zone_id)
    else:
        return crud.get_indicators(db, skip=skip, limit=limit)


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
    return crud.get_air_averages(db, start_date, end_date, zone_id)


# Upload CSV
@app.post("/upload/csv/")
async def upload_csv(
        file: UploadFile = File(...),
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_admin_user)
):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Seuls les fichiers CSV sont acceptés")

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
                timestamp=row.get('timestamp'),
                zone_id=int(row['zone_id']),
                source_id=int(row['source_id']),
                additional_data=row.get('additional_data')
            )
            crud.create_indicator(db, indicator_data, current_user.id)
            indicators_created += 1
        except Exception as e:
            continue

    return {"message": f"{indicators_created} indicateurs créés avec succès"}

# Nouvelle route pour les statistiques détaillées
@app.get("/stats/air/quality")
def get_air_quality_stats(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    return crud.get_air_quality_stats(db)

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur EcoTrack API", "version": "1.0.0"}


@app.get("/health")
def health_check():
    return {"status": "healthy", "database": "SQLite"}