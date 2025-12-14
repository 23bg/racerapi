# from fastapi import FastAPI, middleware


# class Application:
#     def __init__(self, settings):
#         self._app = FastAPI(
#             title=settings.title,
#             version=settings.version,
#             description=settings.description,
#             docs_url=settings.docs_url,
#             redoc_url=settings.redoc_url,
#             openapi_url=settings.openapi_url,
#         )

#     @property
#     def fastapi(self):
#         return self._app

#     # Abstracted convenience API:

#     def add_middleware(self, *args, **kwargs):
#         return self._app.add_middleware(*args, **kwargs)

#     def add_exception_handler(self, *args, **kwargs):
#         return self._app.add_exception_handler(*args, **kwargs)

#     def include_router(self, *args, **kwargs):
#         return self._app.include_router(*args, **kwargs)

#     def add_event_handler(self, *args, **kwargs):
#         return self._app.add_event_handler(*args, **kwargs)

# racerapi/core/application.py

from fastapi import FastAPI
from racerapi.core.settings import AppSettings


class Application:
    """
    Framework-owned application container.
    Owns the FastAPI instance and enforces lifecycle boundaries.
    """

    def __init__(self, settings: AppSettings):
        self.settings = settings

        self._app = FastAPI(
            title=settings.title,
            version=settings.version,
            description=settings.description,
            docs_url=settings.docs_url,
            redoc_url=settings.redoc_url,
            openapi_url=settings.openapi_url,
        )

    # --------------------------------------------------
    # Public API (controlled exposure)
    # --------------------------------------------------

    @property
    def fastapi(self) -> FastAPI:
        """
        Expose the underlying FastAPI app to ASGI servers.
        """
        return self._app

    # --------------------------------------------------
    # Controlled delegation
    # --------------------------------------------------

    def add_middleware(self, middleware_cls, **options):
        self._app.add_middleware(middleware_cls, **options)

    def add_exception_handler(self, exc_class, handler):
        self._app.add_exception_handler(exc_class, handler)

    def include_router(self, *args, **kwargs):
        self._app.include_router(*args, **kwargs)

    def add_event_handler(self, event: str, handler):
        self._app.add_event_handler(event, handler)
