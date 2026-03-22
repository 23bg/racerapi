import pytest

from racerapi.core.config import Settings


def test_prod_env_rejects_sqlite_database_url():
    with pytest.raises(ValueError):
        Settings(
            env="prod",
            debug=False,
            database_url="sqlite:///./prod.db",
            log_level="INFO",
            app_name="RacerAPI",
        )


def test_prod_env_rejects_debug_true():
    with pytest.raises(ValueError):
        Settings(
            env="prod",
            debug=True,
            database_url="postgresql+psycopg://user:pass@localhost/db",
            log_level="INFO",
            app_name="RacerAPI",
        )


def test_dev_env_allows_sqlite_and_debug_false_by_default():
    settings = Settings(
        env="dev", database_url="sqlite:///./dev.db", app_name="RacerAPI"
    )
    assert settings.env == "dev"
    assert settings.database_url.startswith("sqlite")
    assert settings.debug is False
