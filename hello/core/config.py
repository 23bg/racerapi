from pydantic import BaseSettings

class Settings(BaseSettings):
    APP_ENV: str = "dev"
    SQL_DATABASE_URL: str = "sqlite:///./hello.db"
    MONGO_DATABASE_URL: str = "mongodb://localhost:27017/hello"
    LOG_LEVEL: str = "INFO"


settings = Settings()
