from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from sqlalchemy import JSON, Integer, String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

from racerapi.core.db.base_driver import BaseDriver


class _Base(DeclarativeBase):
    pass


class _Record(_Base):
    __tablename__ = "records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    collection: Mapped[str] = mapped_column(String(64), index=True)
    payload: Mapped[dict[str, Any]] = mapped_column(JSON)


class SQLDriver(BaseDriver):
    """SQL-backed driver using SQLAlchemy ORM internally."""

    def __init__(self, database_url: str):
        self._engine = create_engine(database_url, future=True)
        self._session_factory = sessionmaker(
            bind=self._engine,
            autoflush=False,
            autocommit=False,
            class_=Session,
        )
        _Base.metadata.create_all(self._engine)

    def _session(self) -> Session:
        return self._session_factory()

    def find_all(self, collection: str, filters: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        filters = filters or {}
        with self._session() as session:
            records = session.execute(
                select(_Record).where(_Record.collection == collection)
            ).scalars().all()
            results: list[dict[str, Any]] = []
            for record in records:
                if self._matches_filters(record.payload, filters):
                    results.append({"id": record.id, **record.payload})
            return results

    def find_by_id(self, collection: str, item_id: int) -> dict[str, Any] | None:
        with self._session() as session:
            record = session.get(_Record, item_id)
            if record is None or record.collection != collection:
                return None
            return {"id": record.id, **record.payload}

    def create(self, collection: str, payload: dict[str, Any]) -> dict[str, Any]:
        with self._session() as session:
            record = _Record(collection=collection, payload=dict(payload))
            session.add(record)
            session.commit()
            session.refresh(record)
            return {"id": record.id, **record.payload}

    def update(self, collection: str, item_id: int, payload: dict[str, Any]) -> dict[str, Any] | None:
        with self._session() as session:
            record = session.get(_Record, item_id)
            if record is None or record.collection != collection:
                return None
            merged_payload = dict(record.payload)
            merged_payload.update(payload)
            record.payload = merged_payload
            session.add(record)
            session.commit()
            session.refresh(record)
            return {"id": record.id, **record.payload}

    def delete(self, collection: str, item_id: int) -> bool:
        with self._session() as session:
            record = session.get(_Record, item_id)
            if record is None or record.collection != collection:
                return False
            session.delete(record)
            session.commit()
            return True

    @staticmethod
    def _matches_filters(payload: Mapping[str, Any], filters: Mapping[str, Any]) -> bool:
        for key, value in filters.items():
            if payload.get(key) != value:
                return False
        return True
