from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from pathlib import Path
import os
import uuid

from app.db.session import get_db
from app.models.car import Car
from app.models.car_image import CarImage
from app.schemas.car import CarCreate, CarOut

router = APIRouter(prefix="/admin", tags=["Admin"])

# --------------------
# Upload directory
# --------------------
UPLOAD_DIR = Path("uploads/cars")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


# --------------------
# Create car
# --------------------
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


# --------------------
# Upload car images
# --------------------
@router.post("/cars/{car_id}/images")
async def upload_car_images(
    car_id: int,
    files: list[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    car = db.query(Car).filter(Car.id == car_id).first()
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")

    if len(files) > 5:
        raise HTTPException(status_code=400, detail="Max 5 images allowed")

    for file in files:
        ext = file.filename.split(".")[-1].lower()
        filename = f"{uuid.uuid4()}.{ext}"
        file_path = UPLOAD_DIR / filename

        # save file
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        image = CarImage(
            car_id=car_id,
            image_url=f"/uploads/cars/{filename}"
        )
        db.add(image)

    db.commit()
    return {"message": "Images uploaded successfully"}


# --------------------
# Delete car
# --------------------
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
