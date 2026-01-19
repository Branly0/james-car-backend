from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.base import Base

class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True)
    device_id = Column(String, index=True)
    car_id = Column(Integer, ForeignKey("cars.id", ondelete="CASCADE"))
