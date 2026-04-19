from __future__ import annotations

from typing import Any

from racerapi.core.plugins.base import Plugin
from racerapi.core.contracts.database import DatabaseProvider
from racerapi.core.config.settings import get_settings

from .provider import SQLAlchemyProvider


class SQLAlchemyPlugin(Plugin):
    def __init__(self) -> None:
        self._provider_token = DatabaseProvider

    def register(self, container: Any) -> None:
        settings = get_settings()

        def _factory(_container: Any) -> SQLAlchemyProvider:
            return SQLAlchemyProvider(settings.sql_database_url)

        container.register(self._provider_token, _factory, scope="singleton")

    def register_app(self, app: Any) -> None:
        # attach app lifecycle handlers to start/stop the DB provider
        @app.on_event("startup")
        def _startup() -> None:
            container = getattr(app.state, "container", None)
            if container is None:
                return
            try:
                provider = container.resolve(self._provider_token)
                provider.startup()
            except Exception:
                app.logger.exception("database provider startup failed")

        @app.on_event("shutdown")
        def _shutdown() -> None:
            container = getattr(app.state, "container", None)
            if container is None:
                return
            try:
                provider = container.resolve(self._provider_token)
                provider.shutdown()
            except Exception:
                app.logger.exception("database provider shutdown failed")

    def register_cli(self, cli: Any) -> None:
        # defer CLI registration to cli.py helper
        try:
            from . import cli as _cli

            _cli.register_cli(cli)
        except Exception:
            # optional CLI - swallow errors during CLI setup
            pass


plugin = SQLAlchemyPlugin()
