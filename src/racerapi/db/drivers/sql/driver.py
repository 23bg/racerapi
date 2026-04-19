import logging
from pathlib import Path
from typing import Any

import typer
from alembic import command as alembic_command
from alembic.config import Config

from racerapi.cli.context import CLIContext
from racerapi.db.base_driver import BaseDriver
from racerapi.db.session import get_engine

logger = logging.getLogger(__name__)


def _default_alembic_ini(database_url: str) -> str:
    return f"""[alembic]
script_location = alembic
sqlalchemy.url = {database_url}

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname = root

[logger_sqlalchemy]
level = WARN
handlers = console
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers = console
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stdout,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
"""


def _alembic_env_py() -> str:
    return """from __future__ import with_statement

import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from racerapi.core.config import settings
from racerapi.db.base import Base

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

if config.get_main_option("sqlalchemy.url") is None:
    config.set_main_option("sqlalchemy.url", settings.database_url)

target_metadata = Base.metadata


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    context.run_migrations()
else:
    run_migrations_online()
"""


class SQLDriver(BaseDriver):
    def __init__(self, context: CLIContext) -> None:
        super().__init__(context)
        self.database_url = get_engine().url.render_as_string(hide_password=False)

    @property
    def _config_path(self) -> Path:
        return Path.cwd() / "alembic.ini"

    @property
    def _alembic_dir(self) -> Path:
        return Path.cwd() / "alembic"

    def _config(self) -> Config:
        cfg = Config(str(self._config_path))
        return cfg

    def _ensure_alembic(self) -> None:
        if self._config_path.exists() and self._alembic_dir.exists():
            return

        self._alembic_dir.mkdir(parents=True, exist_ok=True)
        self._config_path.write_text(_default_alembic_ini(self.database_url), encoding="utf-8")
        (self._alembic_dir / "env.py").write_text(_alembic_env_py(), encoding="utf-8")
        (self._alembic_dir / "script.py.mako").write_text("""""", encoding="utf-8")

    def init(self) -> None:
        if self.context.dry_run:
            typer.echo("[dry-run] initialize alembic environment")
            return
        self._ensure_alembic()
        typer.echo("Alembic environment initialized")

    def migrate(self) -> None:
        self._ensure_alembic()
        typer.echo("Creating SQL migration revision")
        if self.context.dry_run:
            typer.echo("[dry-run] alembic revision --autogenerate")
            return
        alembic_command.revision(self._config(), autogenerate=True, message="auto")

    def upgrade(self) -> None:
        self._ensure_alembic()
        typer.echo("Applying SQL migrations")
        if self.context.dry_run:
            typer.echo("[dry-run] alembic upgrade head")
            return
        alembic_command.upgrade(self._config(), "head")

    def reset(self) -> None:
        self._ensure_alembic()
        typer.echo("Resetting SQL database via Alembic")
        if self.context.dry_run:
            typer.echo("[dry-run] alembic downgrade base && alembic upgrade head")
            return
        alembic_command.downgrade(self._config(), "base")
        alembic_command.upgrade(self._config(), "head")

    def seed(self) -> None:
        from racerapi.cli.utils import run_seed
        from racerapi.db.session import get_session

        seed_path = Path.cwd() / "seed.py"
        if not seed_path.exists():
            typer.echo("No seed.py found in the current project root.")
            return
        session = get_session()
        try:
            run_seed(seed_path, session, self.context)
        finally:
            session.close()

    def check_connection(self) -> None:
        if self.context.dry_run:
            typer.echo("[dry-run] checking SQL database connection")
            return
        try:
            engine = get_engine()
            with engine.connect() as connection:
                connection.execute("SELECT 1")
        except Exception as exc:
            raise typer.Exit(f"SQL connection failed: {exc}")
