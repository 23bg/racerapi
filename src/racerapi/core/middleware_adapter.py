# racerapi/core/middleware_adapter.py
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from racerapi.core.middleware import RequestContext, Middleware


class FastAPIMiddlewareAdapter(BaseHTTPMiddleware):
    """
    Internal adapter that converts RacerAPI Middleware
    into Starlette-compatible middleware.
    """

    def __init__(self, app, racer_middleware: Middleware):
        super().__init__(app)
        self._mw = racer_middleware

    async def dispatch(self, request: Request, call_next):
        ctx = RequestContext(request)

        async def _next():
            return await call_next(request)

        return await self._mw.handle(ctx, _next)
