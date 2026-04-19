from __future__ import annotations

from racerapi.core.config.settings import Settings
from racerapi.core.db.base_driver import BaseDriver
from racerapi.core.db.drivers.mongo_driver import MongoDriver
from racerapi.core.db.drivers.sql_driver import SQLDriver


def init_drivers(settings: Settings) -> dict[str, BaseDriver]:
    return {
        "sql": SQLDriver(database_url=settings.sql_database_url),
        "mongo": MongoDriver(database_url=settings.mongo_database_url),
    }
