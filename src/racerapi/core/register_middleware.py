# racerapi/core/middleware.py

from fastapi import FastAPI

# from starlette.middleware.cors import CORSMiddleware
from racerapi.core.middleware import Middleware
from racerapi.core.application import Application
from racerapi.core.middleware_adapter import FastAPIMiddlewareAdapter


# def register_middleware(app: FastAPI, settings: AppSettings) -> None:
#     """
#     Register all global application middleware.

#     This function is called exactly once during application bootstrap.
#     Middleware registration is deterministic and settings-driven.
#     """

#     # --------------------------------------------------
#     # CORS
#     # --------------------------------------------------
#     # if settings.cors_enabled:
#     app.add_middleware(
#         CORSMiddleware,
#         allow_origins=settings.cors_origins,
#         allow_credentials=settings.cors_allow_credentials,
#         allow_methods=settings.cors_allow_methods,
#         allow_headers=settings.cors_allow_headers,
#     )

#     # --------------------------------------------------
#     # Custom / User-defined middleware
#     # --------------------------------------------------
#     # These are explicitly provided by the application,
#     # not auto-discovered (enterprise-safe).
#     for middleware_cls in settings.middlewares:
#         app.add_middleware(FastAPIMiddlewareAdapter, middleware_cls)

#     # --------------------------------------------------
#     # Future (intentionally explicit)
#     # --------------------------------------------------
#     # if settings.auth_enabled:
#     #     app.add_middleware(AuthMiddleware)
#     #
#     # if settings.rate_limit_enabled:
#     #     app.add_middleware(RateLimitMiddleware)
#     #
#     # if settings.tracing_enabled:
#     #     app.add_middleware(TracingMiddleware)


def register_middleware(app: Application, settings):
    for mw_cls in settings.middlewares or []:
        if not issubclass(mw_cls, Middleware):
            raise TypeError(f"{mw_cls.__name__} must extend racerapi.Middleware")

        app.add_middleware(
            FastAPIMiddlewareAdapter,
            middleware_cls=mw_cls,
        )
