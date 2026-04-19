from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from racerapi.db.base_driver import BaseDriver
    from racerapi.cli.context import CLIContext, Driver


def _resolve_driver_name(driver) -> object:
    """Resolve driver name lazily to avoid importing `racerapi.cli` at module import time."""
    # Import Driver locally to avoid package-level side-effects
    from racerapi.cli.context import Driver as _Driver

    if driver != _Driver.auto:
        return driver

    from racerapi.core.config import settings

    database_url = getattr(settings, "database_url", "")
    if database_url.startswith("mongodb"):
        return _Driver.mongo
    return _Driver.sql


def get_driver(driver, context) -> "BaseDriver":
    # local import to prevent circular import of racerapi.cli package
    resolved = _resolve_driver_name(driver)
    if str(resolved).endswith("mongo"):
        from .mongo.driver import MongoDriver

        return MongoDriver(context)
    from .sql.driver import SQLDriver

    return SQLDriver(context)
