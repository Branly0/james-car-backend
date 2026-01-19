from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import UploadFile, File
import os
import uuid

from app.db.session import get_db
from app.models.car import Car
from app.schemas.car import CarCreate, CarOut
from app.models.car_image import CarImage

UPLOAD_DIR = "uploads/cars"
os.makedirs(UPLOAD_DIR, exist_ok=True)

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


@router.post("/cars/{car_id}/images")
def upload_car_images(
    car_id: int,
    files: list[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    car = db.query(Car).filter(Car.id == car_id).first()
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")

    if len(files) > 5:
        raise HTTPException(status_code=400, detail="Max 5 images allowed")

    images = []

    for file in files:
        ext = file.filename.split(".")[-1]
        filename = f"{uuid.uuid4()}.{ext}"
        path = os.path.join(UPLOAD_DIR, filename)

        with open(path, "wb") as buffer:
            buffer.write(file.file.read())

        image = CarImage(
            car_id=car_id,
            image_url=f"/uploads/cars/{filename}"
        )
        db.add(image)
        images.append(image)

    db.commit()
    return {"message": "Images uploaded successfully"}



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
