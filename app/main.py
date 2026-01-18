from fastapi import FastAPI
from app.routers import cars, admin, favorites

from app.db.base import Base
from app.db.session import engine


Base.metadata.create_all(bind=engine)

app = FastAPI(title="MR JAMES AFFORDABLE USED CARS API")

app.include_router(cars.router)
app.include_router(admin.router)
app.include_router(favorites.router)

@app.get("/")
def read_root():
    return {"welcome to:": "MR JAMES AFFORDABLE USED CARS API"}