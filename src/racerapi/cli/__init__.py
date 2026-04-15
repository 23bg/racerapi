"""RacerAPI CLI package - lightweight re-export of command entrypoints.

This package exposes functions used by the stable console script
(`racerapi.console:main`) while the real command implementations live
in `racerapi.cli.commands` modules so each command can be tested in
isolation.
"""
from .app import app
from .commands.generate import (
    generate_module as _generate_module,
    generate_service as _generate_service,
    generate_repo as _generate_repo,
    generate_resource as _generate_resource,
)
from .commands.db import db_command
from .commands.new import new_project
from .commands.run import run_app
import typer
from racerapi.core.logger import get_logger

logger = get_logger(__name__)


# Keep backwards-compatible function names that other modules expect
def new(project_name: str, path: str | None = None) -> None:
    try:
        new_project(project_name, path)
    except typer.Exit:
        raise
    except Exception as exc:
        logger.exception("new command failed")
        typer.echo(f"Error: {exc}")
        raise typer.Exit(code=2)


def run(host: str = "127.0.0.1", port: int = 8000, reload: bool = False) -> None:
    try:
        run_app(host=host, port=port, reload=reload)
    except typer.Exit:
        raise
    except Exception as exc:
        logger.exception("run command failed")
        typer.echo(f"Error: {exc}")
        raise typer.Exit(code=2)


def generate_module(name: str, path: str | None = None) -> None:
    try:
        _generate_module(name, path)
    except typer.Exit:
        raise
    except Exception as exc:
        logger.exception("generate module failed")
        typer.echo(f"Error: {exc}")
        raise typer.Exit(code=2)


def generate_service(name: str, path: str | None = None) -> None:
    try:
        _generate_service(name, path)
    except typer.Exit:
        raise
    except Exception as exc:
        logger.exception("generate service failed")
        typer.echo(f"Error: {exc}")
        raise typer.Exit(code=2)


def generate_repo(name: str, path: str | None = None) -> None:
    try:
        _generate_repo(name, path)
    except typer.Exit:
        raise
    except Exception as exc:
        logger.exception("generate repo failed")
        typer.echo(f"Error: {exc}")
        raise typer.Exit(code=2)


def generate_resource(name: str, path: str | None = None) -> None:
    try:
        _generate_resource(name, path)
    except typer.Exit:
        raise
    except Exception as exc:
        logger.exception("generate resource failed")
        typer.echo(f"Error: {exc}")
        raise typer.Exit(code=2)


def db(command: str) -> None:
    try:
        db_command(command)
    except typer.Exit:
        raise
    except Exception as exc:
        logger.exception("db command failed")
        typer.echo(f"Error: {exc}")
        raise typer.Exit(code=2)


def main() -> None:
    try:
        app()
    except Exception as exc:
        logger.exception("CLI main failed")
        typer.echo(f"Error: {exc}")
        raise typer.Exit(code=2)
