from __future__ import annotations

import importlib
import pkgutil
from pathlib import Path
from typing import List

from racerapi.core.logger import get_logger

logger = get_logger(__name__)


_routers: List = []


def register_router(router) -> None:
    # avoid duplicate registrations
    if router in _routers:
        return
    _routers.append(router)


def get_routers() -> List:
    # return routers in registration order without duplicates
    seen = set()
    out = []
    for r in _routers:
        rid = id(r)
        if rid in seen:
            continue
        seen.add(rid)
        out.append(r)
    return out


def discover_modules() -> None:
    """Discover modules under racerapi.modules and import their api modules.

    Importing the module's `api` will typically register the router via
    `register_router` and import models for metadata.
    """
    try:
        import racerapi.modules as modules_pkg
    except Exception:
        logger.exception("failed to import modules package")
    else:
        for finder, name, ispkg in pkgutil.iter_modules(modules_pkg.__path__):
            # only consider package modules (directories) under modules/
            if not ispkg:
                continue
            if name.startswith("_"):
                continue
            # basic module contract: must expose api.py and models.py
            pkg_path = Path(modules_pkg.__file__).parent / name
            api_file = pkg_path / "api.py"
            models_file = pkg_path / "models.py"
            if not api_file.exists() or not models_file.exists():
                logger.warning("skipping module %s - missing api.py or models.py", name)
                continue
            modname = f"racerapi.modules.{name}.api"
            try:
                importlib.import_module(modname)
                logger.info("discovered module %s", name)
            except Exception:
                logger.exception("failed to import module %s", name)

    # Also discover modules under a user project in the working directory (src/<pkg>/modules)
    try:
        cwd_src = Path.cwd() / "src"
        if cwd_src.exists():
            for pkg in cwd_src.iterdir():
                if not pkg.is_dir():
                    continue
                if not (pkg / "__init__.py").exists():
                    continue
                if pkg.name == "racerapi":
                    continue
                # try importing <pkg>.modules
                try:
                    pkg_modules = importlib.import_module(f"{pkg.name}.modules")
                except Exception:
                    # no modules package, skip
                    continue
                for finder, name, ispkg in pkgutil.iter_modules(pkg_modules.__path__):
                    if not ispkg:
                        continue
                    if name.startswith("_"):
                        continue
                    pkg_path = Path(pkg_modules.__file__).parent / name
                    api_file = pkg_path / "api.py"
                    models_file = pkg_path / "models.py"
                    if not api_file.exists() or not models_file.exists():
                        logger.warning(
                            "skipping project module %s.%s - missing api.py or models.py",
                            pkg.name,
                            name,
                        )
                        continue
                    modname = f"{pkg.name}.modules.{name}.api"
                    try:
                        importlib.import_module(modname)
                        logger.info("discovered project module %s.%s", pkg.name, name)
                    except Exception:
                        logger.exception("failed to import project module %s.%s", pkg.name, name)
    except Exception:
        # discovery best-effort: don't fail app startup
        logger.exception("project module discovery failed")
