import typer
import subprocess
import sys
from pathlib import Path


def test_cmd():
    """
    Run project tests using pytest within the RacerAPI project context.
    """

    typer.echo("")
    typer.secho("RacerAPI Test Runner", bold=True)
    typer.echo("──────────────────────────────")
    typer.echo("")

    project_root = Path.cwd()
    tests_dir = project_root / "tests"

    if not tests_dir.exists():
        typer.secho("✗ tests/ directory not found", fg="red")
        typer.echo("  Create a tests/ folder before running tests.")
        sys.exit(1)

    # Check pytest availability
    try:
        import pytest  # noqa: F401
    except ImportError:
        typer.secho("✗ pytest is not installed", fg="red")
        typer.echo("  Install it with: pip install pytest")
        sys.exit(1)

    typer.secho("✓ Running tests with pytest", fg="green")
    typer.echo("")

    # Run pytest as subprocess (do NOT import pytest.main)
    result = subprocess.run(
        ["pytest", str(tests_dir)],
        cwd=project_root,
    )

    if result.returncode == 0:
        typer.secho("\n✓ Tests passed", fg="green", bold=True)
        sys.exit(0)
    else:
        typer.secho("\n✗ Tests failed", fg="red", bold=True)
        sys.exit(result.returncode)
