from __future__ import annotations

from typing import Any

from racerapi.core.db.base_driver import BaseDriver


class MongoDriver(BaseDriver):
    """Mongo-backed driver using pymongo internally when available."""

    def __init__(self, database_url: str):
        self._database_url = database_url
        self._client = None
        self._database = None

    def _get_collection(self, name: str):
        if self._database is None:
            try:
                from pymongo import MongoClient
            except ImportError as exc:  # pragma: no cover - optional dependency
                raise RuntimeError(
                    "MongoDriver requires pymongo. Install it to use mongo features."
                ) from exc

            client = MongoClient(self._database_url)
            db_name = self._database_url.rsplit("/", 1)[-1]
            self._client = client
            self._database = client[db_name]

        return self._database[name]

    def find_all(self, collection: str, filters: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        mongo_collection = self._get_collection(collection)
        filters = filters or {}
        rows = mongo_collection.find(filters)
        return [{"id": str(row["_id"]), **{k: v for k, v in row.items() if k != "_id"}} for row in rows]

    def find_by_id(self, collection: str, item_id: int) -> dict[str, Any] | None:
        from bson import ObjectId

        mongo_collection = self._get_collection(collection)
        row = mongo_collection.find_one({"_id": ObjectId(str(item_id))})
        if row is None:
            return None
        return {"id": str(row["_id"]), **{k: v for k, v in row.items() if k != "_id"}}

    def create(self, collection: str, payload: dict[str, Any]) -> dict[str, Any]:
        mongo_collection = self._get_collection(collection)
        result = mongo_collection.insert_one(dict(payload))
        return {"id": str(result.inserted_id), **payload}

    def update(self, collection: str, item_id: int, payload: dict[str, Any]) -> dict[str, Any] | None:
        from bson import ObjectId

        mongo_collection = self._get_collection(collection)
        result = mongo_collection.find_one_and_update(
            {"_id": ObjectId(str(item_id))},
            {"$set": dict(payload)},
            return_document=True,
        )
        if result is None:
            return None
        return {"id": str(result["_id"]), **{k: v for k, v in result.items() if k != "_id"}}

    def delete(self, collection: str, item_id: int) -> bool:
        from bson import ObjectId

        mongo_collection = self._get_collection(collection)
        deleted = mongo_collection.delete_one({"_id": ObjectId(str(item_id))})
        return deleted.deleted_count > 0
