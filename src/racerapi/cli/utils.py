import inspect
import os
from pathlib import Path
from typing import Any

import typer

from racerapi.cli.context import CLIContext


def ensure_dir(path: Path, ctx: CLIContext) -> None:
    if ctx.dry_run:
        typer.echo(f"[dry-run] mkdir -p {path}")
        return
    path.mkdir(parents=True, exist_ok=True)


def ensure_package(path: Path, ctx: CLIContext) -> None:
    ensure_dir(path, ctx)
    init_path = path / "__init__.py"
    if init_path.exists() and not ctx.force:
        return
    write_file(init_path, "# generated package\n", ctx)


def write_file(path: Path, content: str, ctx: CLIContext) -> None:
    if path.exists() and not ctx.force:
        raise typer.Exit(f"File already exists: {path}. Use --force to overwrite.")
    action = "[dry-run] write" if ctx.dry_run else "write"
    typer.echo(f"{action} {path}")
    if ctx.dry_run:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def confirm_action(prompt: str, ctx: CLIContext) -> bool:
    if ctx.force:
        typer.echo("Force enabled; skipping confirmation.")
        return True
    if ctx.dry_run:
        typer.echo(f"[dry-run] confirm: {prompt}")
        return True
    return typer.confirm(prompt)


def load_seed_callable(seed_path: Path) -> Any:
    from importlib.util import module_from_spec, spec_from_file_location

    spec = spec_from_file_location("racerapi_seed", str(seed_path))
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load seed file {seed_path}")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    seed_fn = getattr(module, "seed", None)
    if not callable(seed_fn):
        raise ImportError("seed.py must define a callable seed(session=...) or seed(client=...)")
    return seed_fn


def run_seed(seed_path: Path, runner: Any, ctx: CLIContext) -> None:
    seed_fn = load_seed_callable(seed_path)
    params = inspect.signature(seed_fn).parameters
    kwargs = {}
    if "session" in params:
        kwargs["session"] = runner
    elif "client" in params:
        kwargs["client"] = runner
    if ctx.dry_run:
        typer.echo(f"[dry-run] would run seed script: {seed_path}")
        return
    seed_fn(**kwargs)


def resolve_project_package_root() -> Path:
    cwd = Path.cwd()
    src_root = cwd / "src"
    if not src_root.exists():
        return cwd
    for child in src_root.iterdir():
        if child.is_dir() and (child / "__init__.py").exists():
            return cwd
    return cwd


def get_package_name() -> str | None:
    src_root = Path.cwd() / "src"
    if not src_root.exists():
        return None
    for child in src_root.iterdir():
        if child.is_dir() and (child / "__init__.py").exists():
            return child.name
    return None


def get_version() -> str:
    from racerapi import __version__

    return __version__
