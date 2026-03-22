from typing import Literal

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    env: Literal["dev", "test", "prod"] = "dev"
    app_name: str = "RacerAPI"
    debug: bool = False
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    database_url: str = "sqlite:///./racerapi.db"

    @model_validator(mode="after")
    def validate_production_safety(self) -> "Settings":
        if self.env == "prod" and self.database_url.startswith("sqlite"):
            raise ValueError("RACERAPI_DATABASE_URL must not use sqlite in prod")
        if self.env == "prod" and self.debug:
            raise ValueError("RACERAPI_DEBUG must be false in prod")
        return self

    model_config = SettingsConfigDict(env_file=".env", env_prefix="RACERAPI_")


settings = Settings()
