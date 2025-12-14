from pathlib import Path
import typer
from racerapi.utils.copy_tree import copy_tree

BASE_DIR = Path(__file__).resolve().parent.parent  # racerapi/
TEMPLATES_DIR = BASE_DIR / "templates"
PROJECT_TEMPLATE_DIR = TEMPLATES_DIR / "project"


def new_cmd(name: str):
    """Create a new RacerAPI project from templates."""

    project_root = Path(name)

    if project_root.exists():
        typer.echo(f"Directory '{name}' already exists.")
        raise typer.Exit(1)

    if not PROJECT_TEMPLATE_DIR.exists():
        typer.echo(
            f"[ERROR] Project template directory not found: {PROJECT_TEMPLATE_DIR}"
        )
        raise typer.Exit(1)

    typer.echo(f"Creating RacerAPI project in '{name}'...")

    copy_tree(
        PROJECT_TEMPLATE_DIR,
        project_root,
        {
            "project_name": name,
            "project_slug": name.replace("-", "_"),
        },
    )

    typer.echo("✅ RacerAPI project created")
    typer.echo(f"👉 cd {name}")
    typer.echo("👉 racerapi dev")
