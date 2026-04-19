from __future__ import annotations

import importlib
import logging
import sys
from pathlib import Path
from typing import Any, List

from racerapi.core.config.settings import get_settings

logger = logging.getLogger(__name__)


def _import_plugin_module(path: str):
    """Try to import a plugin module.

    Accepts values like 'racerapi.plugins.sqlalchemy_plugin' or a package
    path; will also try importing '<path>.plugin'.
    """
    try:
        return importlib.import_module(path)
    except Exception:
        # try <path>.plugin entrypoint
        try:
            return importlib.import_module(path + ".plugin")
        except Exception:
            return None


def discover_plugins(settings=None) -> List[Any]:
    """Import plugin modules declared in settings and return plugin instances.

    Plugins may be either installed packages or local project plugins located
    under the `plugins/` directory in the project root.
    """
    settings = settings or get_settings()
    plugin_names = getattr(settings, "plugins", []) or []
    plugins: List[Any] = []

    # First, try configured plugin paths (installed packages)
    for name in plugin_names:
        mod = _import_plugin_module(name)
        if mod is None:
            logger.exception("failed to import configured plugin %s", name)
            continue
        inst = getattr(mod, "plugin", None)
        if inst is None:
            cls = getattr(mod, "Plugin", None)
            if cls is not None:
                try:
                    inst = cls()
                except Exception:
                    logger.exception("failed to instantiate Plugin in %s", name)
                    continue
        if inst is None:
            logger.warning("configured plugin %s does not expose 'plugin' or 'Plugin'", name)
            continue
        plugins.append(inst)

    # Second, discover local plugins under project_root/plugins/*
    project_root = Path.cwd()
    local_plugins_dir = project_root / "plugins"
    if local_plugins_dir.exists() and local_plugins_dir.is_dir():
        # Ensure project root is on sys.path so imports like 'plugins.foo' work
        if str(project_root) not in sys.path:
            sys.path.insert(0, str(project_root))
        for child in local_plugins_dir.iterdir():
            if not child.is_dir():
                continue
            # attempt to import plugins.<name>.plugin
            name = f"plugins.{child.name}.plugin"
            try:
                mod = importlib.import_module(name)
            except Exception:
                logger.exception("failed to import local plugin %s", child.name)
                continue
            inst = getattr(mod, "plugin", None)
            if inst is None:
                cls = getattr(mod, "Plugin", None)
                if cls is not None:
                    try:
                        inst = cls()
                    except Exception:
                        logger.exception("failed to instantiate local Plugin %s", child.name)
                        continue
            if inst is None:
                logger.warning("local plugin %s does not expose 'plugin' or 'Plugin'", child.name)
                continue
            plugins.append(inst)

    return plugins


def load_plugins(settings=None, container=None) -> List[Any]:
    settings = settings or get_settings()
    instances = discover_plugins(settings)
    for inst in instances:
        try:
            inst.register(container)
        except Exception:
            logger.exception("plugin register() failed: %s", inst)
    return instances


def register_app_plugins(app, plugins: List[Any]) -> None:
    for inst in plugins:
        try:
            inst.register_app(app)
        except Exception:
            logger.exception("plugin register_app() failed: %s", inst)


def register_cli_plugins(cli, plugins: List[Any]) -> None:
    for inst in plugins:
        try:
            inst.register_cli(cli)
        except Exception:
            logger.exception("plugin register_cli() failed: %s", inst)


__all__ = [
    "discover_plugins",
    "load_plugins",
    "register_app_plugins",
    "register_cli_plugins",
]
