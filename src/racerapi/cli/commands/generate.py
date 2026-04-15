from __future__ import annotations

import importlib
import textwrap
from pathlib import Path
from typing import Optional

import typer

from racerapi.core.logger import get_logger

logger = get_logger(__name__)


def _ensure_pkg(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    init = path / "__init__.py"
    if not init.exists():
        init.write_text("# Generated package\n")


def _render_template_file(path: Path, **ctx) -> str:
    tpl = path.read_text(encoding="utf-8")
    return textwrap.dedent(tpl).lstrip("\n").format(**ctx)


def _find_templates_dir() -> Path:
    # templates are located in src/racerapi/templates
    return Path(__file__).resolve().parents[2] / "templates" / "module"


def _validate_module_import(package: str, module_name: str) -> None:
    modname = f"{package}.modules.{module_name}.api"
    try:
        m = importlib.import_module(modname)
    except Exception as exc:  # pragma: no cover - runtime validation
        logger.exception("Failed to import generated module %s: %s", modname, exc)
        raise typer.Exit(code=2)
    # basic sanity: module should expose `router`
    if not hasattr(m, "router"):
        logger.error("Generated module %s has no 'router' attribute", modname)
        raise typer.Exit(code=2)


app = typer.Typer()


@app.command("module")
def generate_module(name: str, path: Optional[str] = typer.Option(None, "--path")) -> None:
    """Generate a new module skeleton under src/<pkg>/modules/<name>"""
    pkg_root = Path(path or Path.cwd())
    src_dir = pkg_root / "src"
    target_pkg = None
    if src_dir.exists():
        for child in src_dir.iterdir():
            if child.is_dir() and (child / "__init__.py").exists():
                if child.name != "racerapi":
                    target_pkg = child.name
                    break
    if target_pkg:
        modules_dir = src_dir / target_pkg / "modules"
        package_name = target_pkg
    else:
        modules_dir = src_dir / "racerapi" / "modules"
        package_name = "racerapi"

    target = modules_dir / name
    _ensure_pkg(target)

    singular = name[:-1] if name.endswith("s") else name
    Name = singular.capitalize()
    table_name = name if name.endswith("s") else f"{name}s"
    ctx = {"name": name, "singular": singular, "Name": Name, "table_name": table_name}

    templates_dir = _find_templates_dir()
    files = {
        "api.py": templates_dir / "api.py.tpl",
        "service.py": templates_dir / "service.py.tpl",
        "repo.py": templates_dir / "repo.py.tpl",
        "schemas.py": templates_dir / "schemas.py.tpl",
        "models.py": templates_dir / "models.py.tpl",
        "deps.py": templates_dir / "deps.py.tpl",
        f"tests/test_module_{name}_api.py": templates_dir / "tests.py.tpl",
    }

    for fname, tpl_path in files.items():
        content = _render_template_file(tpl_path, **ctx)
        fpath = target / fname
        fpath.parent.mkdir(parents=True, exist_ok=True)
        fpath.write_text(content, encoding="utf-8")

    typer.echo(f"Generated module '{name}' at {target}")

    # Validate the generated module is importable and has a router
    _validate_module_import(package_name, name)


@app.command("service")
def generate_service(name: str, path: Optional[str] = typer.Option(None, "--path")) -> None:
    pkg_root = Path(path or Path.cwd())
    src_dir = pkg_root / "src"
    target_pkg = None
    if src_dir.exists():
        for child in src_dir.iterdir():
            if child.is_dir() and (child / "__init__.py").exists():
                if child.name != "racerapi":
                    target_pkg = child.name
                    break
    if target_pkg:
        modules_dir = src_dir / target_pkg / "modules"
        package_name = target_pkg
    else:
        modules_dir = src_dir / "racerapi" / "modules"
        package_name = "racerapi"
    target = modules_dir / name
    if not target.exists():
        typer.echo("Module does not exist. Generate module first.")
        raise typer.Exit(code=1)

    templates_dir = _find_templates_dir()
    singular = name[:-1] if name.endswith("s") else name
    Name = singular.capitalize()
    table_name = name if name.endswith("s") else f"{name}s"
    ctx = {"name": name, "singular": singular, "Name": Name, "table_name": table_name}
    fpath = target / "service.py"
    if fpath.exists():
        typer.echo("service already exists")
        raise typer.Exit()
    fpath.write_text(_render_template_file(templates_dir / "service.py.tpl", **ctx), encoding="utf-8")
    typer.echo(f"Wrote {fpath}")


@app.command("repo")
def generate_repo(name: str, path: Optional[str] = typer.Option(None, "--path")) -> None:
    pkg_root = Path(path or Path.cwd())
    src_dir = pkg_root / "src"
    target_pkg = None
    if src_dir.exists():
        for child in src_dir.iterdir():
            if child.is_dir() and (child / "__init__.py").exists():
                if child.name != "racerapi":
                    target_pkg = child.name
                    break
    if target_pkg:
        modules_dir = src_dir / target_pkg / "modules"
    else:
        modules_dir = src_dir / "racerapi" / "modules"
    target = modules_dir / name
    if not target.exists():
        typer.echo("Module does not exist. Generate module first.")
        raise typer.Exit(code=1)
    templates_dir = _find_templates_dir()
    singular = name[:-1] if name.endswith("s") else name
    Name = singular.capitalize()
    table_name = name if name.endswith("s") else f"{name}s"
    ctx = {"name": name, "singular": singular, "Name": Name, "table_name": table_name}
    fpath = target / "repo.py"
    if fpath.exists():
        typer.echo("repo already exists")
        raise typer.Exit()
    fpath.write_text(_render_template_file(templates_dir / "repo.py.tpl", **ctx), encoding="utf-8")
    typer.echo(f"Wrote {fpath}")


@app.command("resource")
def generate_resource(name: str, path: Optional[str] = typer.Option(None, "--path")) -> None:
    pkg_root = Path(path or Path.cwd())
    src_dir = pkg_root / "src"
    target_pkg = None
    if src_dir.exists():
        for child in src_dir.iterdir():
            if child.is_dir() and (child / "__init__.py").exists():
                if child.name != "racerapi":
                    target_pkg = child.name
                    break
    if target_pkg:
        modules_dir = src_dir / target_pkg / "modules"
    else:
        modules_dir = src_dir / "racerapi" / "modules"
    target = modules_dir / name
    if not target.exists():
        # generate base module files
        generate_module(name, path)

    # ensure service and repo exist
    try:
        generate_service(name, path)
    except SystemExit:
        # already exists
        pass
    try:
        generate_repo(name, path)
    except SystemExit:
        pass
    typer.echo(f"Generated resource '{name}'")
