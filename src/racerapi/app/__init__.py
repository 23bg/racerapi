import time
import uuid
from collections.abc import AsyncIterator, Callable

from fastapi import FastAPI

from racerapi.core.logger import get_logger, set_request_id
from racerapi.modules.registry import discover_modules, get_routers

logger = get_logger(__name__)


def create_app(
    lifespan: Callable[[FastAPI], AsyncIterator[None]] | None = None,
) -> FastAPI:
    app = FastAPI(title="RacerAPI", version="0.0.6", lifespan=lifespan)

    @app.middleware("http")
    async def request_logging_middleware(request, call_next):
        request_id = request.headers.get("x-request-id") or str(uuid.uuid4())
        request.state.request_id = request_id
        # populate logging context var for this request
        set_request_id(request_id)
        start = time.perf_counter()
        try:
            response = await call_next(request)
        except Exception:
            duration_ms = round((time.perf_counter() - start) * 1000, 2)
            logger.exception(
                "request_failed request_id=%s method=%s path=%s duration_ms=%s",
                request_id,
                request.method,
                request.url.path,
                duration_ms,
            )
            raise

        duration_ms = round((time.perf_counter() - start) * 1000, 2)
        logger.info(
            "request_completed request_id=%s method=%s path=%s status_code=%s duration_ms=%s",
            request_id,
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
        )
        response.headers["x-request-id"] = request_id
        # clear request id from context var
        set_request_id(None)
        return response

    # discover modules and register their routers
    discover_modules()
    for r in get_routers():
        app.include_router(r)
    return app
