from pydantic import BaseModel

class CarImageOut(BaseModel):
    id: int
    image_url: str

    class Config:
        from_attributes = True
