from pydantic import BaseSettings

class Settings(BaseSettings):
    APP_ENV: str = "{app_env}"
    SQL_DATABASE_URL: str = "{sql_database_url}"
    MONGO_DATABASE_URL: str = "{mongo_database_url}"
    LOG_LEVEL: str = "{log_level}"


settings = Settings()
