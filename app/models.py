from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String, default="user")

    indicators = relationship("Indicator", back_populates="owner")


class Zone(Base):
    __tablename__ = "zones"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    postal_code = Column(String)
    geometry = Column(Text)

    indicators = relationship("Indicator", back_populates="zone")


class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(Text)
    url = Column(String)

    indicators = relationship("Indicator", back_populates="source")


class Indicator(Base):
    __tablename__ = "indicators"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, index=True)
    value = Column(Float)
    unit = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    additional_data = Column(Text)

    zone_id = Column(Integer, ForeignKey("zones.id"))
    source_id = Column(Integer, ForeignKey("sources.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    zone = relationship("Zone", back_populates="indicators")
    source = relationship("Source", back_populates="indicators")
    owner = relationship("User", back_populates="indicators")