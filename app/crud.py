from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime

from . import models, schemas, auth


# Users
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
def get_indicators(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Indicator).offset(skip).limit(limit).all()


def create_indicator(db: Session, indicator: schemas.IndicatorCreate, user_id: int):
    db_indicator = models.Indicator(**indicator.dict(), user_id=user_id)
    db.add(db_indicator)
    db.commit()
    db.refresh(db_indicator)
    return db_indicator


def get_indicators_by_zone(db: Session, zone_id: int):
    return db.query(models.Indicator).filter(models.Indicator.zone_id == zone_id).all()


def get_indicators_by_type(db: Session, indicator_type: str):
    return db.query(models.Indicator).filter(models.Indicator.type == indicator_type).all()


# Statistics
def get_air_averages(db: Session, start_date: str, end_date: str, zone_id: Optional[int] = None):
    query = db.query(
        models.Zone.name,
        func.avg(models.Indicator.value).label('average_value'),
        func.count(models.Indicator.id).label('data_points')
    ).join(models.Indicator.zone)

    # Filtres
    query = query.filter(models.Indicator.type == 'air_quality')
    query = query.filter(models.Indicator.timestamp >= start_date)
    query = query.filter(models.Indicator.timestamp <= end_date)

    if zone_id:
        query = query.filter(models.Indicator.zone_id == zone_id)

    result = query.group_by(models.Zone.name).all()

    return [
        {
            "zone_name": row[0],
            "average_quality": float(row[1]) if row[1] else 0,
            "period": f"{start_date} to {end_date}",
            "data_points": row[2]
        }
        for row in result
    ]