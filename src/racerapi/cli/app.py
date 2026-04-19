import logging
import os

import typer
from typer import Context

from racerapi.cli.context import CLIContext, Driver, Env
from racerapi.cli.registry import register_commands
from racerapi.cli.commands.db import db_app
from racerapi.cli.commands.generate import generate_app
from racerapi.core.logger import configure_logging
from racerapi.core.plugins.loader import discover_plugins, register_cli_plugins
from racerapi.core.config.settings import get_settings

app = typer.Typer()
register_commands(app, generate_app, db_app)

# discover plugins (declarative via settings) and let them register CLI commands
try:
    settings = get_settings()
    cli_plugins = discover_plugins(settings)
    register_cli_plugins(app, cli_plugins)
except Exception:
    # keep CLI lightweight - plugin failures should not break core CLI
    pass


@app.callback(invoke_without_command=True)
def main(
    ctx: Context,
    env: Env = typer.Option(
        Env.dev,
        "--env",
        case_sensitive=False,
        help="Runtime environment (dev, prod, test).",
    ),
    driver: Driver = typer.Option(
        Driver.auto,
        "--driver",
        case_sensitive=False,
        help="Database driver to use for the command.",
    ),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose logging."),
    dry_run: bool = typer.Option(False, "--dry-run", help="Simulate actions without applying changes."),
    force: bool = typer.Option(False, "--force", help="Force potentially destructive actions."),
) -> None:
    if ctx.obj is None:
        ctx.obj = CLIContext(env=env, driver=driver, verbose=verbose, dry_run=dry_run, force=force)
    os.environ["RACERAPI_ENV"] = env.value
    if verbose:
        os.environ["RACERAPI_DEBUG"] = "1"
    configure_logging(logging.DEBUG if verbose else None)
