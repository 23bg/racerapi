from pydantic import BaseSettings

class Settings(BaseSettings):
    APP_ENV: str = "dev"
    SQL_DATABASE_URL: str = "sqlite:///./hello3.db"
    MONGO_DATABASE_URL: str = "mongodb://localhost:27017/hello3"
    LOG_LEVEL: str = "INFO"


settings = Settings()
