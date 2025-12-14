import typer
import os
import sys
from pathlib import Path


def env_cmd():
    """
    Inspect and validate environment variables required
    to run a RacerAPI project safely.
    """

    typer.echo("")
    typer.secho("RacerAPI Environment Check", bold=True)
    typer.echo("──────────────────────────────")
    typer.echo("")

    errors = False

    def ok(msg):
        typer.secho(f"  ✓ {msg}", fg="green")

    def warn(msg):
        typer.secho(f"  ⚠ {msg}", fg="yellow")

    def fail(msg):
        nonlocal errors
        errors = True
        typer.secho(f"  ✗ {msg}", fg="red")

    project_root = Path.cwd()

    # --------------------------------------------------
    # A. .env File
    # --------------------------------------------------
    typer.secho("Environment Files:", bold=True)

    env_file = project_root / ".env"
    if env_file.exists():
        ok(".env file found")
    else:
        warn(".env file not found (using system env vars only)")

    typer.echo("")

    # --------------------------------------------------
    # B. Core Environment Variables
    # --------------------------------------------------
    typer.secho("Core Environment Variables:", bold=True)

    core_vars = [
        "ENV",  # dev / staging / prod
        "PROFILE",  # standard / ai / full
    ]

    for var in core_vars:
        if os.getenv(var):
            ok(f"{var}={os.getenv(var)}")
        else:
            warn(f"{var} not set (default behavior may apply)")

    typer.echo("")

    # --------------------------------------------------
    # C. AI Environment Variables (conditional)
    # --------------------------------------------------
    typer.secho("AI Environment Variables:", bold=True)

    ai_dir = project_root / "app" / "ai"
    if ai_dir.exists():
        ok("AI layer detected")

        # v1: support one provider only (example: OpenAI)
        ai_required = [
            "OPENAI_API_KEY",
        ]

        for var in ai_required:
            if os.getenv(var):
                ok(f"{var} is set")
            else:
                fail(f"{var} is missing")
    else:
        warn("AI layer not present (AI env vars not required)")

    typer.echo("")

    # --------------------------------------------------
    # Result
    # --------------------------------------------------
    typer.secho("Result:", bold=True)

    if errors:
        typer.secho(
            "  ✗ Environment is NOT ready",
            fg="red",
            bold=True,
        )
        typer.echo("  Fix missing variables above.")
        sys.exit(1)
    else:
        typer.secho(
            "  ✓ Environment looks good",
            fg="green",
            bold=True,
        )
        sys.exit(0)
