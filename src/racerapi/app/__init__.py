import time
import uuid
from collections.abc import AsyncIterator, Callable

from fastapi import FastAPI

from racerapi.core.logger import get_logger
from racerapi.modules.health.api import router as health_router
from racerapi.modules.users.api import router as users_router

logger = get_logger(__name__)


def create_app(
    lifespan: Callable[[FastAPI], AsyncIterator[None]] | None = None,
) -> FastAPI:
    app = FastAPI(title="RacerAPI", version="0.0.5", lifespan=lifespan)

    @app.middleware("http")
    async def request_logging_middleware(request, call_next):
        request_id = request.headers.get("x-request-id") or str(uuid.uuid4())
        request.state.request_id = request_id
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
        return response

    app.include_router(health_router)
    app.include_router(users_router)
    return app
