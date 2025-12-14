from racerapi.core.application import Application
from racerapi.core.register_middleware import register_middleware
from racerapi.core.module_loader import discover_modules, load_controllers
from racerapi.core.plugins import load_plugins
from racerapi.core.settings import AppSettings


def racerAPI(settings: AppSettings):
    """
    Application factory.
    Receives fully resolved settings and assembles the app.
    """

    if settings is None:
        raise RuntimeError(
            "AppSettings must be provided explicitly. "
            "Do not instantiate settings inside the factory."
        )

    # 1. Create application shell
    application = Application(settings)
    app = application.fastapi

    # 2. Register middleware (structure only)
    register_middleware(app, application.settings)

    # 3. Discover & load modules
    discover_modules()
    load_controllers(app)

    # 4. Load plugins (config-driven)
    load_plugins(app, settings)

    return app
