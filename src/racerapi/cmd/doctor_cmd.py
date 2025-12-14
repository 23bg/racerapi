import sys
import typer
from pathlib import Path
import importlib.util

app = typer.Typer()


def doctor_cmd():
    typer.echo("")
    typer.secho("RacerAPI Doctor", bold=True)
    typer.echo("──────────────────────────────")
    typer.echo("")

    project_root = Path.cwd()
    errors = False

    def ok(msg):
        typer.secho(f"  ✓ {msg}", fg="green")

    def warn(msg):
        typer.secho(f"  ⚠ {msg}", fg="yellow")

    def fail(msg):
        nonlocal errors
        errors = True
        typer.secho(f"  ✗ {msg}", fg="red")

    # ==================================================
    # A. Project Structure
    # ==================================================
    typer.secho("Project Structure:", bold=True)

    required_paths = [
        project_root / "app",
        project_root / "app" / "main.py",
        project_root / "app" / "core",
        project_root / "app" / "modules",
    ]

    for path in required_paths:
        if path.exists():
            ok(path.relative_to(project_root).as_posix())
        else:
            fail(f"Missing {path.relative_to(project_root).as_posix()}")

    typer.echo("")

    # ==================================================
    # B. Module Contracts (CRITICAL)
    # ==================================================
    typer.secho("Module Contracts:", bold=True)

    modules_dir = project_root / "app" / "modules"

    if not modules_dir.exists():
        fail("app/modules directory missing")
    else:
        for module in modules_dir.iterdir():
            if not module.is_dir():
                continue

            ok(f"Module: {module.name}")

            # ---- required files ----
            controller = module / "controller.py"
            service = module / "service.py"
            schemas = module / "schema.py"

            for file in [controller, service, schemas]:
                if file.exists():
                    ok(file.relative_to(project_root).as_posix())
                else:
                    fail(f"{file.relative_to(project_root).as_posix()} missing")

            # ---- schema completeness ----
            if schemas.exists():
                content = schemas.read_text(encoding="utf-8")

                expected = [
                    f"{module.name.capitalize()}Create",
                    f"{module.name.capitalize()}Update",
                    f"{module.name.capitalize()}Out",
                ]

                for cls in expected:
                    if cls in content:
                        ok(f"{module.name}: {cls} found")
                    else:
                        fail(f"{module.name}: {cls} missing in schema.py")

            # ---- generator hygiene ----
            for py_file in module.rglob("*.py"):
                text = py_file.read_text(encoding="utf-8")
                if "{{" in text or "}}" in text:
                    fail(
                        f"Unrendered template variable in "
                        f"{py_file.relative_to(project_root).as_posix()}"
                    )

    typer.echo("")

    # ==================================================
    # C. AI Layer (OPTIONAL, NON-FATAL)
    # ==================================================
    typer.secho("AI Readiness:", bold=True)

    ai_dir = project_root / "app" / "ai"
    if ai_dir.exists():
        if (ai_dir / "models.py").exists():
            ok("app/ai/models.py")
        else:
            warn("app/ai/models.py missing")

        if not (project_root / ".env").exists():
            warn(".env file not found (AI providers may fail)")
    else:
        warn("AI layer not present")

    typer.echo("")

    # ==================================================
    # D. Runtime Dependencies
    # ==================================================
    typer.secho("Dependencies:", bold=True)

    required_pkgs = [
        "fastapi",
        "uvicorn",
        "jinja2",
        "typer",
    ]

    for pkg in required_pkgs:
        if importlib.util.find_spec(pkg):
            ok(f"{pkg} installed")
        else:
            fail(f"{pkg} NOT installed")

    typer.echo("")

    # ==================================================
    # Result
    # ==================================================
    typer.secho("Result:", bold=True)

    if errors:
        typer.secho("  ✗ Doctor found critical issues", fg="red", bold=True)
        typer.echo("  Fix errors above before continuing.")
        sys.exit(1)
    else:
        typer.secho("  ✓ Project is healthy", fg="green", bold=True)
        sys.exit(0)
