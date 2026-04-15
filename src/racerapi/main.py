from contextlib import asynccontextmanager

# Configure logging early to avoid formatting issues from imports
from racerapi.core.logger import configure_logging, get_logger

configure_logging()

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from racerapi.app import create_app
from racerapi.core.exceptions import ConflictError, NotFoundError, ValidationError
from racerapi.db.base import Base
from racerapi.db.session import get_engine

logger = get_logger(__name__)


def _error_payload(code: str, message: str, request_id: str | None) -> dict:
    return {
        "error": {
            "code": code,
            "message": message,
            "request_id": request_id,
        }
    }


def _install_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(NotFoundError)
    async def not_found_handler(request: Request, exc: NotFoundError):
        request_id = getattr(request.state, "request_id", None)
        logger.warning("not_found_error request_id=%s detail=%s", request_id, str(exc))
        return JSONResponse(
            status_code=404,
            content=_error_payload("not_found", str(exc), request_id),
        )

    @app.exception_handler(ConflictError)
    async def conflict_handler(request: Request, exc: ConflictError):
        request_id = getattr(request.state, "request_id", None)
        logger.warning("conflict_error request_id=%s detail=%s", request_id, str(exc))
        return JSONResponse(
            status_code=409,
            content=_error_payload("conflict", str(exc), request_id),
        )

    @app.exception_handler(ValidationError)
    async def validation_handler(request: Request, exc: ValidationError):
        request_id = getattr(request.state, "request_id", None)
        logger.warning("validation_error request_id=%s detail=%s", request_id, str(exc))
        return JSONResponse(
            status_code=422,
            content=_error_payload("validation_error", str(exc), request_id),
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        request_id = getattr(request.state, "request_id", None)
        logger.exception(
            "unhandled_exception request_id=%s detail=%s", request_id, str(exc)
        )
        return JSONResponse(
            status_code=500,
            content=_error_payload(
                "internal_server_error", "Internal Server Error", request_id
            ),
        )


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Initialize engine lazily. For production, migrations (Alembic) should
    # be used instead of `create_all`.
    engine = get_engine()
    # DO NOT create or modify schema at application startup. Database schema
    # management must be performed via migrations (Alembic) or explicit
    # provisioning scripts. The application should assume the schema exists.
    yield


app = create_app(lifespan=lifespan)
_install_exception_handlers(app)


def run() -> None:
    uvicorn.run("racerapi.main:app", host="127.0.0.1", port=8000, reload=False)


if __name__ == "__main__":
    run()
