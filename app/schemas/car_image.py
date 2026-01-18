from pydantic import BaseModel

class CarImageOut(BaseModel):
    id: int
    image_path: str

    class Config:
        from_attributes = True
