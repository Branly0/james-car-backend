from pydantic import BaseModel
from datetime import datetime

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


class CarCreate(CarBase):
    pass


class CarOut(CarBase):
    id: int
    views: int
    created_at: datetime

    class Config:
        from_attributes = True  # 👈 REQUIRED for SQLAlchemy (Pydantic v2)
