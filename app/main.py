from fastapi import FastAPI
from app.routers import cars, admin, favorites

from app.db.base import Base
from app.db.session import engine

from fastapi.staticfiles import StaticFiles

from alembic.config import Config
from alembic import command

def run_migrations():
    # Load the alembic configuration from your alembic.ini file
    alembic_cfg = Config("alembic.ini")
    
    # Run the 'upgrade head' command
    command.upgrade(alembic_cfg, "head")

if __name__ == "__main__":
    run_migrations()
    # ... your app startup code here ...


from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="MR JAMES AFFORDABLE USED CARS API")

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


app.include_router(cars.router)
app.include_router(admin.router)
app.include_router(favorites.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"welcome to:": "MR JAMES AFFORDABLE USED CARS API"}
