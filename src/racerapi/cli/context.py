from dataclasses import dataclass
from enum import Enum


class Env(str, Enum):
    dev = "dev"
    test = "test"
    prod = "prod"


class Driver(str, Enum):
    sql = "sql"
    mongo = "mongo"
    auto = "auto"


class ProjectDB(str, Enum):
    sql = "sql"
    mongo = "mongo"
    none = "none"


@dataclass
class CLIContext:
    env: Env = Env.dev
    driver: Driver = Driver.auto
    verbose: bool = False
    dry_run: bool = False
    force: bool = False

    def resolve_driver(self) -> Driver:
        if self.driver != Driver.auto:
            return self.driver
        return Driver.sql
