from __future__ import annotations

import logging
from contextlib import contextmanager
from typing import Any

logger = logging.getLogger(__name__)


class MongoProvider:
    def __init__(self, uri: str) -> None:
        self.uri = uri
        self._client = None

    def _ensure_client(self):
        if self._client is not None:
            return
        try:
            from pymongo import MongoClient
        except Exception as exc:
            raise RuntimeError("pymongo is required for MongoProvider") from exc
        self._client = MongoClient(self.uri, serverSelectionTimeoutMS=2000)

    def startup(self) -> None:
        self._ensure_client()
        # attempt ping
        try:
            self._client.admin.command("ping")
        except Exception:
            logger.exception("mongo startup ping failed")

    def shutdown(self) -> None:
        if self._client is not None:
            try:
                self._client.close()
            finally:
                self._client = None

    @contextmanager
    def get_session(self):
        self._ensure_client()
        # yield the database object (db name parsed from uri if present)
        dbname = self.uri.rsplit("/", 1)[-1] if "/" in self.uri else "racerapi"
        db = self._client[dbname]
        try:
            yield db
        finally:
            pass
