from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.favorite import Favorite

router = APIRouter()

@router.post("/{car_id}")
def add_favorite(
    car_id: int,
    device_id: str,
    db: Session = Depends(get_db)
):
    fav = Favorite(device_id=device_id, car_id=car_id)
    db.add(fav)
    db.commit()
    return {"message": "Added to favorites"}


@router.get("/")
def get_favorites(
    device_id: str,
    db: Session = Depends(get_db)
):
    return db.query(Favorite).filter(
        Favorite.device_id == device_id
    ).all()
