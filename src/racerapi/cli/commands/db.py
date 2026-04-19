from __future__ import annotations

import typer

from racerapi.cli.context import CLIContext
from racerapi.cli.utils import confirm_action
from racerapi.db import get_driver


db_app = typer.Typer()


def _resolve_driver(ctx: typer.Context):
    context: CLIContext = ctx.obj
    return get_driver(context.driver, context)


@db_app.command("init")
def init(ctx: typer.Context) -> None:
    """Initialize the database driver."""
    driver = _resolve_driver(ctx)
    driver.init()


@db_app.command("migrate")
def migrate(ctx: typer.Context) -> None:
    """Create a new database migration."""
    driver = _resolve_driver(ctx)
    driver.migrate()


@db_app.command("upgrade")
def upgrade(ctx: typer.Context) -> None:
    """Apply pending database migrations."""
    driver = _resolve_driver(ctx)
    driver.upgrade()


@db_app.command("reset")
def reset(ctx: typer.Context) -> None:
    """Reset the database. Requires confirmation unless --force."""
    context: CLIContext = ctx.obj
    if not confirm_action(
        "This will reset the database and may destroy data. Continue?", context
    ):
        raise typer.Exit()
    driver = _resolve_driver(ctx)
    driver.reset()


@db_app.command("seed")
def seed(ctx: typer.Context) -> None:
    """Seed the database with initial data."""
    driver = _resolve_driver(ctx)
    driver.seed()
