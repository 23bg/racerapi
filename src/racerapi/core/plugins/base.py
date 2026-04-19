from __future__ import annotations

from typing import Any


class Plugin:
    """Base plugin interface.

    Plugins should subclass or provide an object with these methods. Core will
    dynamically import plugin modules and invoke these hooks.
    """

    def register(self, container: Any) -> None:
        """Register providers into the DI container."""

    def register_app(self, app: Any) -> None:
        """Hook into the FastAPI app lifecycle (startup/shutdown, routers)."""

    def register_cli(self, cli: Any) -> None:
        """Register CLI commands (Typer) for the plugin."""


__all__ = ["Plugin"]
