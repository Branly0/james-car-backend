from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.car import Car
from app.schemas.car import CarOut

router = APIRouter(prefix="/cars", tags=["Cars"])


@router.get("/", response_model=list[CarOut])
def get_all_cars(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    return (
        db.query(Car)
        .order_by(Car.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


@router.get("/{car_id}", response_model=CarOut)
def get_car(car_id: int, db: Session = Depends(get_db)):
    car = db.query(Car).filter(Car.id == car_id).first()

    if not car:
        raise HTTPException(status_code=404, detail="Car not found")

    car.views += 1
    db.commit()
    db.refresh(car)

    return car
