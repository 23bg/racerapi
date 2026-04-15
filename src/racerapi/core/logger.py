import contextvars
import json
import logging
from datetime import datetime
from typing import Optional

from racerapi.core.config import settings

_CONFIGURED = False
_request_id_ctx: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar(
    "racerapi_request_id", default=None
)


class RequestIdFilter(logging.Filter):
    def filter(self, record):
        rid = _request_id_ctx.get()
        record.request_id = rid or "-"
        return True


def set_request_id(rid: Optional[str]) -> None:
    _request_id_ctx.set(rid)


class _JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:  # pragma: no cover - logging
        payload = {
            "ts": datetime.utcfromtimestamp(record.created).isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "request_id": getattr(record, "request_id", None) or "-",
            "msg": record.getMessage(),
        }
        # include exception info if present
        if record.exc_info:
            payload["exc"] = self.formatException(record.exc_info)
        return json.dumps(payload)


def configure_logging(level: int | None = None) -> None:
    global _CONFIGURED
    if _CONFIGURED:
        return

    resolved_level = level
    if resolved_level is None:
        resolved_level = getattr(logging, settings.log_level, logging.INFO)

    root = logging.getLogger()
    root.setLevel(resolved_level)
    # clear existing handlers to avoid duplicate logs when reconfiguring
    for h in list(root.handlers):
        root.removeHandler(h)

    handler = logging.StreamHandler()

    if getattr(settings, "env", "dev") == "prod":
        handler.setFormatter(_JsonFormatter())
    else:
        fmt = (
            "ts=%(asctime)s level=%(levelname)s logger=%(name)s request_id=%(request_id)s msg=%(message)s"
        )
        handler.setFormatter(logging.Formatter(fmt))

    root.addHandler(handler)
    root.addFilter(RequestIdFilter())
    _CONFIGURED = True


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
