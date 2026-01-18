from pydantic import BaseModel

class FavoriteCreate(BaseModel):
    car_id: int
