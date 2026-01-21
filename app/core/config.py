# app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database and app
    DATABASE_URL: str
    ADMIN_API_KEY: str
    # Cloudinary
    CLOUDINARY_CLOUD_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Create a global instance to import everywhere
settings = Settings()
