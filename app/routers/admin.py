from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.car import Car
from app.schemas.car import CarCreate, CarOut

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.post("/cars", response_model=CarOut)
def create_car(
    car_in: CarCreate,
    db: Session = Depends(get_db)
):
    car = Car(**car_in.dict())
    db.add(car)
    db.commit()
    db.refresh(car)
    return car


@router.delete("/cars/{car_id}")
def delete_car(
    car_id: int,
    db: Session = Depends(get_db)
):
    car = db.query(Car).filter(Car.id == car_id).first()

    if not car:
        raise HTTPException(status_code=404, detail="Car not found")

    db.delete(car)
    db.commit()

    return {"message": "Car deleted successfully"}
