import sys
import typer
from fastapi.routing import APIRoute

from racerapi.cli.utils import get_version
from racerapi.cli.context import CLIContext


def routes(ctx: typer.Context = typer.Context) -> None:
    """Inspect registered FastAPI routes."""
    context: CLIContext = ctx.obj
    if context.dry_run:
        typer.echo("[dry-run] inspect routes")
        return

    from racerapi.main import app

    route_list = [route for route in app.routes if isinstance(route, APIRoute)]
    if not route_list:
        typer.echo("No routes detected.")
        raise typer.Exit()

    max_path = max(len(route.path) for route in route_list)
    for route in route_list:
        methods = ",".join(sorted(route.methods - {"HEAD", "OPTIONS"}))
        typer.echo(f"{methods:10s} {route.path.ljust(max_path)} {route.name}")


def doctor(ctx: typer.Context = typer.Context) -> None:
    """Validate Python, dependencies, and database connectivity."""
    context: CLIContext = ctx.obj
    if context.dry_run:
        typer.echo("[dry-run] run doctor checks")
        return

    errors: list[str] = []
    if sys.version_info < (3, 10):
        errors.append("Python 3.10+ is required.")

    dependencies = ["fastapi", "uvicorn", "sqlalchemy", "pydantic", "typer", "alembic"]
    for dep in dependencies:
        try:
            __import__(dep)
        except Exception as exc:
            errors.append(f"Missing dependency: {dep} ({exc})")

    from racerapi.db import get_driver

    try:
        driver = get_driver(context.driver, context)
        driver.check_connection()
    except Exception as exc:
        errors.append(str(exc))

    if errors:
        typer.echo("Doctor found issues:")
        for err in errors:
            typer.secho(f"- {err}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    typer.secho("Doctor checks passed.", fg=typer.colors.GREEN)


def version(ctx: typer.Context = typer.Context) -> None:
    """Print the RacerAPI package version."""
    typer.echo(get_version())
