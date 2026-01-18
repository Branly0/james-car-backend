from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from app.db.base import Base

class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True)
    car_id = Column(Integer, ForeignKey("cars.id", ondelete="CASCADE"))
    identifier = Column(String)
    created_at = Column(TIMESTAMP, server_default=func.now())
