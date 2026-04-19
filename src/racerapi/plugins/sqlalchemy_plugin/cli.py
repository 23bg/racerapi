from __future__ import annotations

import logging

from typer import Typer

from racerapi.core.config.settings import get_settings
from .provider import SQLAlchemyProvider

logger = logging.getLogger(__name__)


def register_cli(cli: Typer) -> None:
    db_app = Typer()

    @db_app.command("ping")
    def ping() -> None:
        """Ping the database via a temporary provider."""
        settings = get_settings()
        try:
            prov = SQLAlchemyProvider(settings.sql_database_url)
            prov.startup()
            with prov.get_session() as session:
                session.execute("SELECT 1")
            print("OK")
        except Exception as exc:
            raise SystemExit(f"DB ping failed: {exc}")

    try:
        cli.add_typer(db_app, name="db")
    except Exception:
        logger.exception("failed to register CLI commands for SQLAlchemy plugin")
