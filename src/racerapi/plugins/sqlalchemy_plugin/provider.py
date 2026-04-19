from __future__ import annotations

import logging
from contextlib import contextmanager
from typing import Any

logger = logging.getLogger(__name__)


class SQLAlchemyProvider:
    def __init__(self, database_url: str) -> None:
        try:
            from sqlalchemy import create_engine
            from sqlalchemy.orm import sessionmaker
        except Exception as exc:  # pragma: no cover - optional dependency
            raise RuntimeError("SQLAlchemy is required for SQLAlchemyProvider") from exc

        self.database_url = database_url
        self._create_engine = create_engine
        self._sessionmaker = sessionmaker
        self.engine = None
        self.SessionLocal = None

    def startup(self) -> None:
        if self.engine is not None:
            return
        # create engine lazily on startup
        self.engine = self._create_engine(self.database_url, future=True)
        self.SessionLocal = self._sessionmaker(bind=self.engine)
        logger.info("SQLAlchemy engine initialized for %s", self.database_url)

    def shutdown(self) -> None:
        if self.engine is not None:
            self.engine.dispose()
            self.engine = None
            self.SessionLocal = None
            logger.info("SQLAlchemy engine disposed")

    @contextmanager
    def get_session(self):
        if self.SessionLocal is None:
            self.startup()
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
