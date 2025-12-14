import typer
import subprocess
import sys
from pathlib import Path


def _run(cmd: list[str], label: str) -> bool:
    typer.secho(f"→ {label}", bold=True)
    result = subprocess.run(cmd)
    if result.returncode != 0:
        typer.secho(f"✗ {label} failed", fg="red")
        return False
    typer.secho(f"✓ {label} completed", fg="green")
    return True


def format_cmd():
    """
    Format project code using standard Python formatters:
    - black
    - isort
    - ruff (fix mode)

    Tools must already be installed.
    """

    typer.echo("")
    typer.secho("RacerAPI Code Formatter", bold=True)
    typer.echo("──────────────────────────────")
    typer.echo("")

    project_root = Path.cwd()
    app_dir = project_root / "app"

    if not app_dir.exists():
        typer.secho("✗ app/ directory not found", fg="red")
        sys.exit(1)

    tools = {
        "black": ["black", str(app_dir)],
        "isort": ["isort", str(app_dir)],
        "ruff": ["ruff", "check", str(app_dir), "--fix"],
    }

    missing = []
    for tool in tools:
        if not shutil.which(tool):
            missing.append(tool)

    if missing:
        typer.secho("✗ Missing formatting tools:", fg="red", bold=True)
        for tool in missing:
            typer.echo(f"  - {tool}")
        typer.echo("")
        typer.echo("Install them with:")
        typer.echo("  pip install black isort ruff")
        sys.exit(1)

    success = True

    success &= _run(tools["isort"], "isort (imports)")
    success &= _run(tools["black"], "black (formatting)")
    success &= _run(tools["ruff"], "ruff (auto-fix)")

    typer.echo("")

    if success:
        typer.secho("✓ Formatting completed successfully", fg="green", bold=True)
        sys.exit(0)
    else:
        typer.secho("✗ Formatting completed with errors", fg="red", bold=True)
        sys.exit(1)
