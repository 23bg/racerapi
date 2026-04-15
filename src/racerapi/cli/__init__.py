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

# Keep backwards-compatible function names that other modules expect
def new(project_name: str, path: str | None = None) -> None:
    new_project(project_name, path)


def run(host: str = "127.0.0.1", port: int = 8000, reload: bool = False) -> None:
    run_app(host=host, port=port, reload=reload)


def generate_module(name: str, path: str | None = None) -> None:
    _generate_module(name, path)


def generate_service(name: str, path: str | None = None) -> None:
    _generate_service(name, path)


def generate_repo(name: str, path: str | None = None) -> None:
    _generate_repo(name, path)


def generate_resource(name: str, path: str | None = None) -> None:
    _generate_resource(name, path)


def db(command: str) -> None:
    db_command(command)


def main() -> None:
    app()
