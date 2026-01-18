from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.favorite import Favorite
from app.schemas.favorite import FavoriteCreate
from app.utils.identifier import get_identifier

router = APIRouter(prefix="/favorites", tags=["Favorites"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def add_favorite(
    data: FavoriteCreate,
    identifier: str = Depends(get_identifier),
    db: Session = Depends(get_db)
):
    favorite = Favorite(
        car_id=data.car_id,
        identifier=identifier
    )
    db.add(favorite)
    db.commit()
    return {"message": "Added to favorites"}

@router.get("/")
def get_favorites(
    identifier: str = Depends(get_identifier),
    db: Session = Depends(get_db)
):
    return db.query(Favorite).filter(
        Favorite.identifier == identifier
    ).all()
