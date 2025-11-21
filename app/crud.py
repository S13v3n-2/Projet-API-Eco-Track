from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime

from . import models, schemas, auth


# Users - FONCTIONS AJOUTÉES
def get_users(db: Session, skip: int = 0, limit: int = 100):
    """Récupère tous les utilisateurs"""
    return db.query(models.User).offset(skip).limit(limit).all()


def get_user(db: Session, user_id: int):
    """Récupère un utilisateur par son ID"""
    return db.query(models.User).filter(models.User.id == user_id).first()


def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate):
    """Met à jour un utilisateur"""
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        return None

    update_data = user_update.dict(exclude_unset=True)

    # Ne pas permettre de modifier son propre rôle si admin
    for field, value in update_data.items():
        setattr(db_user, field, value)

    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    """Supprime un utilisateur"""
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        return False

    db.delete(db_user)
    db.commit()
    return True


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# Zones
def get_zones(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Zone).offset(skip).limit(limit).all()


def create_zone(db: Session, zone: schemas.ZoneBase):
    db_zone = models.Zone(**zone.dict())
    db.add(db_zone)
    db.commit()
    db.refresh(db_zone)
    return db_zone


# Sources
def get_sources(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Source).offset(skip).limit(limit).all()


def create_source(db: Session, source: schemas.SourceBase):
    db_source = models.Source(**source.dict())
    db.add(db_source)
    db.commit()
    db.refresh(db_source)
    return db_source


# Indicators
def create_indicator(db: Session, indicator: schemas.IndicatorCreate, user_id: int):
    db_indicator = models.Indicator(
        **indicator.dict(),
        user_id=user_id,
        timestamp=indicator.timestamp if isinstance(indicator.timestamp, datetime) else datetime.fromisoformat(
            indicator.timestamp)
    )
    db.add(db_indicator)
    db.commit()
    db.refresh(db_indicator)
    return db_indicator


def get_indicators_by_type(db: Session, indicator_type: str, limit: int = 100):
    return db.query(models.Indicator).filter(
        models.Indicator.type == indicator_type
    ).order_by(models.Indicator.timestamp.desc()).limit(limit).all()


def get_indicators_by_zone(db: Session, zone_id: int, limit: int = 100):
    return db.query(models.Indicator).filter(
        models.Indicator.zone_id == zone_id
    ).order_by(models.Indicator.timestamp.desc()).limit(limit).all()


def get_indicators(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        type: str = None,
        zone_id: int = None,
        start_date: datetime = None,
        end_date: datetime = None
):
    """Récupère les indicateurs avec filtres optionnels"""
    query = db.query(models.Indicator)

    # Filtrer par type seulement si spécifié et non vide
    if type and type.strip() != "":
        query = query.filter(models.Indicator.type == type)

    if zone_id:
        query = query.filter(models.Indicator.zone_id == zone_id)

    # CORRECTION : Gestion correcte des dates
    if start_date:
        # S'assurer que start_date est au début de la journée
        start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
        query = query.filter(models.Indicator.timestamp >= start_date)

    if end_date:
        # S'assurer que end_date est à la fin de la journée
        end_date = end_date.replace(hour=23, minute=59, second=59, microsecond=999999)
        query = query.filter(models.Indicator.timestamp <= end_date)

    return query.order_by(models.Indicator.timestamp.desc()).limit(limit).all()


def get_air_quality_by_zone(
        db: Session,
        start_date: datetime,
        end_date: datetime,
        zone_id: Optional[int] = None
):
    query = db.query(
        models.Zone.name,
        func.avg(models.Indicator.value).label('average_quality'),
        func.count(models.Indicator.id).label('data_points')
    ).join(models.Zone, models.Zone.id == models.Indicator.zone_id) \
        .filter(
        models.Indicator.type == 'air_quality_pm25',
        models.Indicator.timestamp >= start_date,
        models.Indicator.timestamp <= end_date
    )

    if zone_id:
        query = query.filter(models.Indicator.zone_id == zone_id)

    result = query.group_by(models.Zone.name).all()

    return [
        {
            "zone_name": row[0],
            "average_quality": float(row[1]) if row[1] else 0,
            "period": f"{start_date.date()} to {end_date.date()}",
            "data_points": row[2]
        }
        for row in result
    ]


def get_air_quality_stats(db: Session):
    pollutants = ['air_quality_pm25', 'air_quality_pm10', 'air_quality_no2']

    stats = []
    for pollutant in pollutants:
        result = db.query(
            func.avg(models.Indicator.value).label('average'),
            func.count(models.Indicator.id).label('count'),
            func.min(models.Indicator.value).label('min'),
            func.max(models.Indicator.value).label('max')
        ).filter(
            models.Indicator.type == pollutant
        ).first()

        if result and result[0]:
            stats.append({
                "type": pollutant,
                "average": float(result.average),
                "count": result.count,
                "min": float(result.min),
                "max": float(result.max)
            })

    return stats