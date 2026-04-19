from __future__ import annotations

import contextvars
import json
import logging
from datetime import datetime, timezone
from typing import Optional

from racerapi.core.config.settings import get_settings

_request_id_ctx: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar(
    "racerapi_request_id", default=None
)
_configured = False


class _RequestContextFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = _request_id_ctx.get() or "-"
        return True


class _StructuredFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "request_id": getattr(record, "request_id", "-"),
        }
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=True)


def set_request_id(request_id: Optional[str]) -> None:
    _request_id_ctx.set(request_id)


def configure_logging(level: str | int | None = None) -> None:
    global _configured
    if _configured:
        return

    settings = get_settings()
    # Allow callers to pass either a logging level name (str) or an int constant.
    if isinstance(level, int):
        resolved_level = level
    else:
        resolved_name = (level or settings.log_level).upper()
        resolved_level = getattr(logging, resolved_name, logging.INFO)

    root = logging.getLogger()
    root.setLevel(resolved_level)

    for handler in list(root.handlers):
        root.removeHandler(handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(_StructuredFormatter())
    stream_handler.addFilter(_RequestContextFilter())

    root.addHandler(stream_handler)
    root.addFilter(_RequestContextFilter())
    _configured = True


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
