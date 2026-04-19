from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central application settings loaded from environment variables."""

    app_env: Literal["dev", "prod", "test"] = Field(
        default="dev",
        validation_alias=AliasChoices("APP_ENV", "RACERAPI_ENV"),
    )
    sql_database_url: str = Field(
        default="sqlite+pysqlite:///./racerapi.db",
        validation_alias=AliasChoices("SQL_DATABASE_URL", "RACERAPI_DATABASE_URL"),
    )
    mongo_database_url: str = Field(
        default="mongodb://localhost:27017/racerapi",
        validation_alias=AliasChoices("MONGO_DATABASE_URL"),
    )
    log_level: Literal["DEBUG", "INFO", "ERROR"] = Field(
        default="INFO",
        validation_alias=AliasChoices("LOG_LEVEL", "RACERAPI_LOG_LEVEL"),
    )
    # Optional list of plugin import paths (e.g. racerapi.plugins.sqlalchemy_plugin)
    plugins: list[str] = Field(default_factory=list)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def env(self) -> Literal["dev", "prod", "test"]:
        # Backward-compatible alias used by existing code.
        return self.app_env

    @property
    def database_url(self) -> str:
        # Backward-compatible alias used by existing code.
        return self.sql_database_url


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
