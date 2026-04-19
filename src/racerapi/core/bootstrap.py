from __future__ import annotations

import importlib
import logging
import pkgutil
from pathlib import Path
from typing import List

from fastapi import FastAPI

from racerapi.core.config.settings import get_settings
from racerapi.core.logger import configure_logging, get_logger
from racerapi.core.di import Container
from racerapi.core.plugins.loader import load_plugins, register_app_plugins
from racerapi.modules import registry as modules_registry

logger = get_logger(__name__)


def create_app(title: str = "RacerAPI", version: str = "0.1.0") -> FastAPI:
    settings = get_settings()

    # Create DI container and register settings/container itself
    container = Container()
    container.register(type(settings), settings, scope="singleton")
    container.register("settings", settings, scope="singleton")
    container.register(Container, lambda _c: container, scope="singleton")

    # Load plugins and allow them to register providers into the container
    plugins = load_plugins(settings, container=container)

    # Configure logging early so plugins/app can log
    configure_logging(settings.log_level)

    app = FastAPI(title=title, version=version)
    # attach container so handlers and route dependencies can access it
    app.state.container = container

    # let plugins hook into the app lifecycle (startup/shutdown, routers)
    register_app_plugins(app, plugins)

    # Discover modules that live under racerapi.modules and let them register
    try:
        import racerapi.modules as modules_pkg

        for finder, name, ispkg in pkgutil.iter_modules(modules_pkg.__path__):
            if not ispkg or name.startswith("_"):
                continue

            pkg_dir = Path(modules_pkg.__file__).parent / name
            module_entry = pkg_dir / "module.py"
            api_entry = pkg_dir / "api.py"

            # prefer explicit module entrypoint
            if module_entry.exists():
                modname = f"racerapi.modules.{name}.module"
                try:
                    mod = importlib.import_module(modname)
                except Exception:
                    logger.exception("failed to import module entrypoint for %s", name)
                    continue
                reg = getattr(mod, "register", None)
                if callable(reg):
                    try:
                        reg(container, app)
                    except Exception:
                        logger.exception("module %s.register failed", name)
                continue

            # fallback for legacy modules: only import api if api.py exists
            if api_entry.exists():
                try:
                    importlib.import_module(f"racerapi.modules.{name}.api")
                except Exception:
                    logger.exception("failed to import api for module %s", name)
    except Exception:
        logger.exception("module discovery failed")

    # Include routers collected by modules via racerapi.modules.registry.register_router
    routers: List = modules_registry.get_routers()
    for r in routers:
        app.include_router(r)

    # built-in root endpoint
    @app.get("/")
    def _root() -> dict[str, str]:
        return {"status": "ok", "env": settings.app_env}

    return app


__all__ = ["create_app"]
