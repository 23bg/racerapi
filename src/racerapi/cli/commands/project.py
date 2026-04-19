import os
from pathlib import Path

import typer

from click import get_current_context
from racerapi.cli.context import CLIContext, ProjectDB
from racerapi.cli.utils import ensure_dir, ensure_package, write_file


def _find_templates_dir() -> Path:
    # Prefer package-local templates (`src/racerapi/templates/project`) but
    # fall back to the top-level `src/templates/project` used by older layouts.
    base = Path(__file__).resolve()
    candidate_pkg = base.parents[2] / "templates" / "project"
    candidate_src = base.parents[3] / "templates" / "project"
    if candidate_pkg.exists():
        return candidate_pkg
    return candidate_src


def _render_template_file(path: Path, **context: str) -> str:
    template = path.read_text(encoding="utf-8")
    return template.format(**context)


def _project_root(name: str, ctx: CLIContext) -> Path:
    root = Path.cwd() / name
    if root.exists() and not ctx.force and not ctx.dry_run:
        raise typer.Exit(f"Project '{name}' already exists. Use --force to overwrite.")
    return root


def _create_package(path: Path, ctx: CLIContext) -> None:
    ensure_package(path, ctx)


def _write_project_files(root: Path, name: str, db: ProjectDB, ctx: CLIContext) -> None:
    env_values = {
        "project_name": name,
        "app_env": ctx.env.value,
        "sql_database_url": f"sqlite:///./{name}.db",
        "mongo_database_url": f"mongodb://localhost:27017/{name}",
        "log_level": "INFO",
        "database_url": "",
        "dependencies": "",
    }

    dependencies = ["fastapi>=0.115.0", "uvicorn[standard]>=0.32.0", "pydantic>=2.0.0"]
    if db == ProjectDB.sql:
        dependencies.append("sqlalchemy>=2.0")
        env_values["database_url"] = env_values["sql_database_url"]
    elif db == ProjectDB.mongo:
        dependencies.append("pymongo>=4.0.0")
        env_values["database_url"] = env_values["mongo_database_url"]
    else:
        env_values["database_url"] = ""

    if ctx.dry_run:
        typer.echo(f"[dry-run] create project scaffold at {root}")
    else:
        ensure_dir(root, ctx)

    template_root = _find_templates_dir()
    if not template_root.exists():
        raise typer.Exit(f"Templates directory not found: {template_root}")
    files = {
        "README.md": template_root / "README.md.tpl",
        "pyproject.toml": template_root / "pyproject.toml.tpl",
        ".env": template_root / "env.tpl",
        "main.py": template_root / "main.py.tpl",
        "core/app.py": template_root / "core/app.py.tpl",
        "core/config.py": template_root / "core/config.py.tpl",
        "core/logger.py": template_root / "core/logger.py.tpl",
        "core/database.py": template_root / "core/database.py.tpl",
        "core/security.py": template_root / "core/security.py.tpl",
        "core/exceptions.py": template_root / "core/exceptions.py.tpl",
        "core/lifecycle.py": template_root / "core/lifecycle.py.tpl",
        "modules/health/controller.py": template_root / "modules/health/controller.py.tpl",
        "modules/health/service.py": template_root / "modules/health/service.py.tpl",
        "modules/health/schema.py": template_root / "modules/health/schema.py.tpl",
        "modules/health/routes.py": template_root / "modules/health/routes.py.tpl",
        "modules/health/module.py": template_root / "modules/health/module.py.tpl",
        "modules/user/controller.py": template_root / "modules/user/controller.py.tpl",
        "modules/user/service.py": template_root / "modules/user/service.py.tpl",
        "modules/user/module.py": template_root / "modules/user/module.py.tpl",
        "modules/user/test_service.py": template_root / "modules/user/test_service.py.tpl",
        "modules/user/test_controller.py": template_root / "modules/user/test_controller.py.tpl",
        "shared/response.py": template_root / "shared/response.py.tpl",
        "shared/base_model.py": template_root / "shared/base_model.py.tpl",
        "shared/constants.py": template_root / "shared/constants.py.tpl",
        "shared/decorators.py": template_root / "shared/decorators.py.tpl",
        "integrations/email/__init__.py": template_root / "integrations/email/__init__.py.tpl",
        "integrations/payment/__init__.py": template_root / "integrations/payment/__init__.py.tpl",
        "integrations/storage/__init__.py": template_root / "integrations/storage/__init__.py.tpl",
        "utils/helpers.py": template_root / "utils/helpers.py.tpl",
        "tests/__init__.py": template_root / "tests/__init__.py.tpl",
    }

    for target, template_path in files.items():
        output_path = root / target
        write_file(output_path, _render_template_file(template_path, **env_values), ctx)

    _create_package(root / "core", ctx)
    _create_package(root / "modules", ctx)
    _create_package(root / "modules" / "health", ctx)
    _create_package(root / "modules" / "user", ctx)
    _create_package(root / "shared", ctx)
    _create_package(root / "integrations", ctx)
    _create_package(root / "integrations" / "email", ctx)
    _create_package(root / "integrations" / "payment", ctx)
    _create_package(root / "integrations" / "storage", ctx)
    _create_package(root / "utils", ctx)
    ensure_dir(root / "tests", ctx)


from click import get_current_context


def new(
    name: str,
    db: str = typer.Option(
        "sql",
        "--db",
        help="Database driver for new project (sql, mongo, none).",
    ),
) -> None:
    """Create a new RacerAPI-compatible project."""
    context: CLIContext = get_current_context().obj
    normalized = db.lower()
    if normalized not in {"sql", "mongo", "none"}:
        raise typer.BadParameter("--db must be one of: sql, mongo, none")
    db_choice = ProjectDB(normalized)
    _project_root(name, context)
    _write_project_files(Path.cwd() / name, name, db_choice, context)
    typer.echo(f"Created project {name}")


def dev(ctx: typer.Context) -> None:
    """Run the application in development mode with reload."""
    context: CLIContext = ctx.obj
    if context.dry_run:
        typer.echo("[dry-run] start development server")
        return

    import uvicorn

    os.environ["APP_ENV"] = context.env.value
    if context.verbose:
        os.environ["APP_DEBUG"] = "1"
    typer.echo("Starting development server on http://127.0.0.1:8000")
    uvicorn.run("racerapi.main:app", host="127.0.0.1", port=8000, reload=True)


def start(ctx: typer.Context) -> None:
    """Run the application in production mode."""
    context: CLIContext = ctx.obj
    if context.dry_run:
        typer.echo("[dry-run] start production server")
        return

    import uvicorn

    os.environ["APP_ENV"] = context.env.value
    typer.echo("Starting production server on http://127.0.0.1:8000")
    uvicorn.run("racerapi.main:app", host="127.0.0.1", port=8000, reload=False)


def shell(ctx: typer.Context) -> None:
    """Open an interactive Python shell with RacerAPI app loaded."""
    context: CLIContext = ctx.obj
    if context.dry_run:
        typer.echo("[dry-run] launch interactive shell")
        return

    import code
    from racerapi.core.config import settings
    from racerapi.main import app

    banner = (
        "RacerAPI shell\n"
        "Available objects: app, settings\n"
        "Use app to inspect routes or settings for configuration."
    )
    local_vars = {"app": app, "settings": settings}
    code.interact(local=local_vars, banner=banner)
