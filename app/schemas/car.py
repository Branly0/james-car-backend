from pydantic import BaseModel
from datetime import datetime
from app.schemas.car_image import CarImageOut

from typing import List


class CarBase(BaseModel):
    make: str
    model: str
    year: int
    price: int
    mileage: int | None = None
    transmission: str | None = None
    fuel_type: str | None = None
    location: str | None = None
    description: str | None = None
    financing_available: bool = False
    images: List[CarImageOut] = []

    class Config:
        from_attributes = True


class CarCreate(CarBase):
    pass


class CarOut(BaseModel):
    id: int
    model: str
    make: str
    price: float
    financing_available: bool
    images: List[CarImageOut] = []

    class Config:
        from_attributes = True
