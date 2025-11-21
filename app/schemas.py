from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    is_active: bool = True
    role: str = "user"


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
    role: Optional[str] = None


class User(UserBase):
    id: int

    class Config:
        from_attributes = True


class ZoneBase(BaseModel):
    name: str
    postal_code: str
    geometry: Optional[str] = None


class Zone(ZoneBase):
    id: int

    class Config:
        from_attributes = True


class SourceBase(BaseModel):
    name: str
    description: Optional[str] = None
    url: Optional[str] = None


class Source(SourceBase):
    id: int

    class Config:
        from_attributes = True


class IndicatorBase(BaseModel):
    type: str
    value: float
    unit: str
    timestamp: datetime
    additional_data: Optional[str] = None
    zone_id: int
    source_id: int


class IndicatorCreate(IndicatorBase):
    pass


class Indicator(IndicatorBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class AirAveragesResponse(BaseModel):
    zone_name: str
    average_quality: float
    period: str
    data_points: int


class AirQualityStats(BaseModel):
    type: str
    average: float
    count: int
    min: float
    max: float

    class Config:
        from_attributes = True