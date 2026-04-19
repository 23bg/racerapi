from __future__ import annotations

import logging

from typer import Typer

from racerapi.core.config.settings import get_settings
from .provider import MongoProvider

logger = logging.getLogger(__name__)


def register_cli(cli: Typer) -> None:
    db_app = Typer()

    @db_app.command("ping")
    def ping() -> None:
        settings = get_settings()
        try:
            prov = MongoProvider(settings.mongo_database_url)
            prov.startup()
            print("OK")
        except Exception as exc:
            raise SystemExit(f"Mongo ping failed: {exc}")

    try:
        cli.add_typer(db_app, name="mongo")
    except Exception:
        logger.exception("failed to register CLI commands for MongoDB plugin")
