from pydantic import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    APP_ENV: str = "development"
    SQL_DATABASE_URL: str = "sqlite+aiosqlite:///./dev.db"
    MONGO_DATABASE_URL: str = "mongodb://localhost:27017"
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
