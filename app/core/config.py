from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # App
    APP_NAME: str = "FastAPI Auth + LLM"
    APP_VERSION: str = "1.0.0"

    # JWT
    SECRET_KEY: str = "changeme-super-secret-key"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Database
    DATABASE_URL: str = "sqlite:///./auth_app.db"

    # LLM
    GEMINI_API_KEY: str = ""  # load from .env

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()