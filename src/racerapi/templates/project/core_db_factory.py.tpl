from .drivers.base_driver import BaseDriver
from .drivers.sql_driver import SQLDriver
from .drivers.mongo_driver import MongoDriver


def init_drivers(settings) -> dict[str, BaseDriver]:
    drivers: dict[str, BaseDriver] = {}
    drivers["sql"] = SQLDriver(settings.SQL_DATABASE_URL)
    drivers["mongo"] = MongoDriver(settings.MONGO_DATABASE_URL)
    return drivers
