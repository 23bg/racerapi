from __future__ import annotations

from typing import Any

from racerapi.core.logger import get_logger
from racerapi.modules.sample.repo import SampleRepository

logger = get_logger(__name__)


class SampleService:
    """Business logic layer with no direct DB access."""

    def __init__(self, repo: SampleRepository):
        self._repo = repo

    def list_items(self) -> list[dict[str, Any]]:
        logger.info("listing sample items")
        return self._repo.list_items()

    def get_item(self, item_id: int) -> dict[str, Any] | None:
        logger.info("fetching sample item id=%s", item_id)
        return self._repo.get_item(item_id)

    def create_item(self, payload: dict[str, Any]) -> dict[str, Any]:
        logger.info("creating sample item")
        return self._repo.create_item(payload)

    def update_item(self, item_id: int, payload: dict[str, Any]) -> dict[str, Any] | None:
        logger.info("updating sample item id=%s", item_id)
        return self._repo.update_item(item_id, payload)

    def delete_item(self, item_id: int) -> bool:
        logger.info("deleting sample item id=%s", item_id)
        return self._repo.delete_item(item_id)
