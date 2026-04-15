import os
import sys
from pathlib import Path

import pytest

# Ensure the package src is importable
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from racerapi.db.base import Base
from racerapi.db import models_registry


@pytest.fixture(scope="function")
def db_engine(tmp_path):
    url = os.environ.get("RACERAPI_DATABASE_URL", "sqlite+pysqlite:///:memory:")
    connect_args = {"check_same_thread": False}
    engine = create_engine(url, future=True, connect_args=connect_args)
    # Ensure all models are imported so Base.metadata is populated
    # (models are imported as a side-effect of models_registry import)
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(db_engine):
    SessionLocal = sessionmaker(bind=db_engine, autoflush=False, autocommit=False)
    connection = db_engine.connect()
    transaction = connection.begin()
    session = SessionLocal(bind=connection)
    try:
        yield session
    finally:
        session.rollback()
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture(scope="function")
def client(db_session):
    from fastapi.testclient import TestClient

    from racerapi.main import app
    from racerapi.core.deps import get_db as _get_db

    def _override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[_get_db] = _override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.pop(_get_db, None)
