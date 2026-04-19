from __future__ import annotations

from typing import Any

from racerapi.core.plugins.base import Plugin
from racerapi.core.contracts.database import DatabaseProvider
from racerapi.core.config.settings import get_settings

from .provider import MongoProvider


class MongoDBPlugin(Plugin):
    def __init__(self) -> None:
        self._provider_token = DatabaseProvider

    def register(self, container: Any) -> None:
        settings = get_settings()

        def _factory(_container: Any) -> MongoProvider:
            return MongoProvider(settings.mongo_database_url)

        container.register(self._provider_token, _factory, scope="singleton")

    def register_app(self, app: Any) -> None:
        @app.on_event("startup")
        def _startup() -> None:
            container = getattr(app.state, "container", None)
            if container is None:
                return
            try:
                provider = container.resolve(self._provider_token)
                provider.startup()
            except Exception:
                app.logger.exception("mongo provider startup failed")

        @app.on_event("shutdown")
        def _shutdown() -> None:
            container = getattr(app.state, "container", None)
            if container is None:
                return
            try:
                provider = container.resolve(self._provider_token)
                provider.shutdown()
            except Exception:
                app.logger.exception("mongo provider shutdown failed")

    def register_cli(self, cli: Any) -> None:
        try:
            from . import cli as _cli

            _cli.register_cli(cli)
        except Exception:
            pass


plugin = MongoDBPlugin()
