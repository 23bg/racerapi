import typer
import sys
from typing import List
from fastapi.routing import APIRoute


def routes_cmd():
    """
    List all registered API routes with method, path, and module ownership.
    """

    typer.echo("")
    typer.secho("RacerAPI Routes", bold=True)
    typer.echo("──────────────────────────────")
    typer.echo("")

    try:
        # Import app factory dynamically
        from app.main import create_app
    except Exception as e:
        typer.secho(
            f"✗ Failed to import app.main:create_app\n  {e}",
            fg="red",
        )
        sys.exit(1)

    try:
        app = create_app()
    except Exception as e:
        typer.secho(
            f"✗ Failed to create FastAPI app\n  {e}",
            fg="red",
        )
        sys.exit(1)

    routes: List[APIRoute] = [r for r in app.routes if isinstance(r, APIRoute)]

    if not routes:
        typer.secho("⚠ No routes registered", fg="yellow")
        sys.exit(0)

    # Table header
    typer.secho(
        f"{'METHOD':<8} {'PATH':<35} {'MODULE'}",
        bold=True,
    )
    typer.secho(f"{'-'*8} {'-'*35} {'-'*30}")

    for route in routes:
        methods = ",".join(sorted(route.methods))
        path = route.path

        # Try to infer module ownership
        endpoint = route.endpoint
        module_name = endpoint.__module__

        # Normalize module path
        if "app.modules." in module_name:
            module_name = module_name.split("app.modules.", 1)[1]
            module_name = module_name.split(".", 1)[0]
        else:
            module_name = "core / external"

        typer.echo(f"{methods:<8} {path:<35} {module_name}")

    typer.echo("")
    typer.secho(f"Total routes: {len(routes)}", bold=True)
    typer.echo("")
