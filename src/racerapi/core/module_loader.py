# racerapi/core/module_loader.py

import importlib
from pathlib import Path
from fastapi import FastAPI

from racerapi.core.registry import get_registered_controllers
from racerapi.core.controller import build_router


MODULES_ROOT = Path("app/modules")


def discover_modules() -> None:
    """
    Discover and import controller modules only.
    Tests, services, domains are never imported here.
    """
    if not MODULES_ROOT.exists():
        return

    for module_dir in MODULES_ROOT.iterdir():
        if not module_dir.is_dir():
            continue

        controller_file = module_dir / "controller.py"
        if not controller_file.exists():
            continue

        module_path = f"app.modules.{module_dir.name}.controller"

        try:
            importlib.import_module(module_path)
        except Exception as exc:
            raise RuntimeError(
                f"Failed loading controller module {module_path}: {exc}"
            ) from exc


def load_controllers(app: FastAPI) -> None:
    """
    Build routers from registered controllers and attach them to FastAPI.
    """
    for entry in get_registered_controllers():
        prefix = entry["prefix"]
        controller = entry["controller"]

        router = build_router(prefix, controller)
        app.include_router(router)

        print(f"✓ Registered Controller: {controller.__name__} → /{prefix}")
