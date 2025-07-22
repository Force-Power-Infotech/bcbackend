from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "BowlsAce API"
    
    # Environment
    ENV: str = os.getenv("ENV", "development")  # "development", "testing", or "production"
    
    # Admin settings
    ADMIN_EMAIL: str = os.getenv("ADMIN_EMAIL", "admin@bowlsace.com")
    
    # Database settings
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "bowlsace")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "supersecret")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "bowlsacedb")
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:5432/{POSTGRES_DB}"
    )
    
    # For local development, use psycopg2 if specified in environment
    if os.getenv("USE_SYNC_DB", "").lower() == "true":
        DATABASE_URL = DATABASE_URL.replace("postgresql+asyncpg", "postgresql+psycopg2")
    
    # JWT settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your_jwt_secret")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # CORS settings
    BACKEND_CORS_ORIGINS: list = ["*"]
    
    # OTP settings
    OTP_EXPIRY_SECONDS: int = int(os.getenv("OTP_EXPIRY_SECONDS", "600"))  # 10 minutes default

settings = Settings()
