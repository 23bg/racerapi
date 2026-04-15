"""Dynamically import all module models so SQLAlchemy MetaData is populated.

Alembic autogeneration requires that all model classes are imported so
that `Base.metadata` contains table definitions. This module performs a
best-effort import of `*.models` modules under both the framework's
`racerapi.modules` package and any project package found under the
current working directory `src/`.
"""
from __future__ import annotations

import importlib
import pkgutil
from pathlib import Path
from typing import Iterable

from racerapi.core.logger import get_logger
from racerapi.db.base import Base

logger = get_logger(__name__)


def _iter_framework_modules() -> Iterable[str]:
    try:
        import racerapi.modules as modules_pkg
    except Exception:
        return []
    for finder, name, ispkg in pkgutil.iter_modules(modules_pkg.__path__):
        if not ispkg or name.startswith("_"):
            continue
        yield f"racerapi.modules.{name}.models"


def _iter_project_modules() -> Iterable[str]:
    try:
        cwd_src = Path.cwd() / "src"
        if not cwd_src.exists():
            return []
        for pkg in cwd_src.iterdir():
            if not pkg.is_dir():
                continue
            if not (pkg / "__init__.py").exists():
                continue
            # try importing <pkg>.modules
            try:
                pkg_modules = importlib.import_module(f"{pkg.name}.modules")
            except Exception:
                continue
            for finder, name, ispkg in pkgutil.iter_modules(pkg_modules.__path__):
                if not ispkg or name.startswith("_"):
                    continue
                yield f"{pkg.name}.modules.{name}.models"
    except Exception:
        return []


def import_all_models() -> None:
    for modname in list(_iter_framework_modules()) + list(_iter_project_modules()):
        try:
            importlib.import_module(modname)
            logger.info("imported models module %s", modname)
        except Exception:
            logger.exception("failed to import models module %s", modname)


# Trigger import when module is imported
import_all_models()

# Expose metadata for Alembic
metadata = Base.metadata
