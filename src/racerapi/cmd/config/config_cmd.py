import typer
import sys
from typing import Any


def _mask(value: Any) -> str:
    """
    Mask sensitive values.
    """
    if value is None:
        return "null"

    value = str(value)

    if len(value) <= 4:
        return "****"

    return value[:2] + "****" + value[-2:]


def config_cmd():
    """
    Show effective runtime configuration for the RacerAPI application.
    """

    typer.echo("")
    typer.secho("RacerAPI Runtime Configuration", bold=True)
    typer.echo("──────────────────────────────")
    typer.echo("")

    try:
        from app.core.config import get_settings
    except Exception as e:
        typer.secho(
            f"✗ Failed to import app.core.config:get_settings\n  {e}",
            fg="red",
        )
        sys.exit(1)

    try:
        settings = get_settings()
    except Exception as e:
        typer.secho(
            f"✗ Failed to load settings\n  {e}",
            fg="red",
        )
        sys.exit(1)

    # Fields considered sensitive
    secret_keys = {
        "OPENAI_API_KEY",
        "DATABASE_URL",
        "REDIS_URL",
        "SECRET_KEY",
        "JWT_SECRET",
    }

    data = settings.model_dump()

    typer.secho("Effective Configuration:", bold=True)

    for key in sorted(data.keys()):
        value = data[key]

        if key.upper() in secret_keys:
            value = _mask(value)

        typer.echo(f"  {key:<20} = {value}")

    typer.echo("")
    typer.secho(
        "Note:",
        bold=True,
    )
    typer.echo("  Values shown are resolved from environment variables and defaults.")
    typer.echo("  Sensitive values are masked.")
    typer.echo("")
