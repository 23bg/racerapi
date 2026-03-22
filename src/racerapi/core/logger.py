import logging

from racerapi.core.config import settings

_CONFIGURED = False


def configure_logging(level: int | None = None) -> None:
    global _CONFIGURED
    if _CONFIGURED:
        return

    resolved_level = level
    if resolved_level is None:
        resolved_level = getattr(logging, settings.log_level, logging.INFO)

    logging.basicConfig(
        level=resolved_level,
        format="ts=%(asctime)s level=%(levelname)s logger=%(name)s msg=%(message)s",
    )
    _CONFIGURED = True


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
