from fastapi import FastAPI
from app.routers import cars, admin, favorites

from app.db.base import Base
from app.db.session import engine

from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware


Base.metadata.create_all(engine)


app = FastAPI(title="MR JAMES AFFORDABLE USED CARS API")

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

Base.metadata.create_all(engine)

app.include_router(cars.router)
app.include_router(admin.router)
app.include_router(favorites.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173","https://www.jamescarafortable.com","https://james-admin.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"welcome to:": "MR JAMES AFFORDABLE USED CARS API"}
