# app/routers/admin.py
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import cloudinary.uploader  # Import the actual uploader

from app.db.session import get_db
from app.models.car import Car
from app.models.car_image import CarImage
from app.schemas.car import CarCreate, CarOut
from app.core.config import settings
from app.core import cloudinary_config  # This just runs the config

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
def create_car(car_in: CarCreate, db: Session = Depends(get_db)):
    """
    Create a new car.
    """
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
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload images for a car to Cloudinary.
    """
    car = db.query(Car).filter(Car.id == car_id).first()
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")

    if len(files) > 5:
        raise HTTPException(status_code=400, detail="Max 5 images allowed")

    uploaded_images = []

    for file in files:
        # Upload the file directly to Cloudinary
        result = cloudinary.uploader.upload(
            file.file,
            folder=f"cars/{car_id}"
        )

        image = CarImage(
            car_id=car_id,
            image_url=result["secure_url"],
            public_id=result["public_id"]
        )
        db.add(image)
        uploaded_images.append(image)

    db.commit()

    return {
        "message": "Images uploaded successfully",
        "images": [img.image_url for img in uploaded_images]
    }

# --------------------
# Delete car
# --------------------
@router.delete("/cars/{car_id}")
def delete_car(car_id: int, db: Session = Depends(get_db)):
    """
    Delete a car and all its images from Cloudinary.
    """
    car = db.query(Car).filter(Car.id == car_id).first()
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")

    # Delete images from Cloudinary
    for image in car.images:
        if getattr(image, "public_id", None):
            cloudinary.uploader.destroy(image.public_id)

    db.delete(car)
    db.commit()

    return {"message": "Car and its images deleted successfully"}
