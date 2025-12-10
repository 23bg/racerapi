from fastapi import FastAPI
from app.core.middleware import register_middleware
from app.core.module_loader import load_modules


def create_app() -> FastAPI:
    app = FastAPI(
        title="hello",
        version="0.0.3",
    )

    # ✅ Register middleware FIRST
    register_middleware(app)

    # ✅ Auto-register all module routers
    load_modules(app)

    return app
