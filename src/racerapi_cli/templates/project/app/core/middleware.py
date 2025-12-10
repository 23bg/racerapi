# app/core/middleware.py

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

def register_middleware(app: FastAPI) -> None:
    """
    Register all global application middleware here.
    This function is called once during app startup.
    """

    # Example: CORS (optional default)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],      # tighten in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Future:
    # app.add_middleware(AuthMiddleware)
    # app.add_middleware(LoggingMiddleware)
    # app.add_middleware(RateLimitMiddleware)

