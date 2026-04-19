from __future__ import annotations

from typing import Any

from racerapi.core.db.base_driver import BaseDriver


class SampleRepository:
    """Repository layer that only talks to the driver abstraction."""

    def __init__(self, driver: BaseDriver, collection: str = "sample_items"):
        self._driver = driver
        self._collection = collection

    def list_items(self) -> list[dict[str, Any]]:
        return self._driver.find_all(self._collection)

    def get_item(self, item_id: int) -> dict[str, Any] | None:
        return self._driver.find_by_id(self._collection, item_id)

    def create_item(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self._driver.create(self._collection, payload)

    def update_item(self, item_id: int, payload: dict[str, Any]) -> dict[str, Any] | None:
        return self._driver.update(self._collection, item_id, payload)

    def delete_item(self, item_id: int) -> bool:
        return self._driver.delete(self._collection, item_id)
