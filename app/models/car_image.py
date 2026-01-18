from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.base import Base

class CarImage(Base):
    __tablename__ = "car_images"

    id = Column(Integer, primary_key=True)
    car_id = Column(Integer, ForeignKey("cars.id", ondelete="CASCADE"))
    image_url = Column(String, nullable=False)
