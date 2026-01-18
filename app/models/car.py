from sqlalchemy import Column, Integer, String, Boolean, Text, TIMESTAMP
from sqlalchemy.sql import func
from app.db.base import Base

class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    make = Column(String, nullable=False)
    model = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    mileage = Column(Integer)
    transmission = Column(String)
    fuel_type = Column(String)
    location = Column(String)
    description = Column(Text)
    financing_available = Column(Boolean, default=False)
    views = Column(Integer, default=0)
    created_at = Column(TIMESTAMP, server_default=func.now())
