import typer
import sys
import json
import time
from pathlib import Path
from fastapi.testclient import TestClient


def eval_cmd(module: str | None = None):
    """
    Run AI evaluation scenarios against the application.

    Examples:
      racerapi eval
      racerapi eval chat
    """

    typer.echo("")
    typer.secho("RacerAPI AI Evaluation", bold=True)
    typer.echo("──────────────────────────────")
    typer.echo("")

    # --------------------------------------------------
    # Load application
    # --------------------------------------------------
    try:
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
            f"✗ Failed to create application\n  {e}",
            fg="red",
        )
        sys.exit(1)

    client = TestClient(app)

    # --------------------------------------------------
    # Locate evaluation datasets
    # --------------------------------------------------
    eval_dir = Path.cwd() / "tests" / "eval"

    if not eval_dir.exists():
        typer.secho("✗ tests/eval directory not found", fg="red")
        sys.exit(1)

    datasets = []

    if module:
        dataset = eval_dir / f"{module}.json"
        if not dataset.exists():
            typer.secho(
                f"✗ Dataset not found: tests/eval/{module}.json",
                fg="red",
            )
            sys.exit(1)
        datasets.append(dataset)
    else:
        datasets = list(eval_dir.glob("*.json"))

    if not datasets:
        typer.secho("✗ No evaluation datasets found", fg="red")
        sys.exit(1)

    # --------------------------------------------------
    # Execute evaluations
    # --------------------------------------------------
    total = 0
    failed = 0

    for dataset in datasets:
        typer.secho(f"Running {dataset.name}", bold=True)

        cases = json.loads(dataset.read_text())

        for case in cases:
            total += 1
            name = case.get("name", "unnamed")
            endpoint = case["endpoint"]
            method = case.get("method", "POST").upper()
            payload = case.get("payload", {})

            start = time.time()
            response = client.request(method, endpoint, json=payload)
            duration = (time.time() - start) * 1000

            if response.status_code >= 400:
                failed += 1
                typer.secho(
                    f"  ✗ {name} ({response.status_code}) {duration:.1f}ms",
                    fg="red",
                )
            else:
                typer.secho(
                    f"  ✓ {name} ({duration:.1f}ms)",
                    fg="green",
                )

        typer.echo("")

    # --------------------------------------------------
    # Summary
    # --------------------------------------------------
    typer.secho("Summary:", bold=True)
    typer.echo(f"  Total cases: {total}")
    typer.echo(f"  Failed: {failed}")

    if failed > 0:
        typer.secho("  ✗ Evaluation failed", fg="red", bold=True)
        sys.exit(1)
    else:
        typer.secho("  ✓ Evaluation passed", fg="green", bold=True)
        sys.exit(0)
