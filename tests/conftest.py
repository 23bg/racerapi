import os
import sys
from pathlib import Path

import pytest

# Ensure the package src is importable before any racerapi imports
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

# Ensure tests run with a safe test DB by default
os.environ.setdefault("RACERAPI_ENV", "test")
os.environ.setdefault("RACERAPI_DATABASE_URL", "sqlite+pysqlite:///:memory:")


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from racerapi.db.base import Base


@pytest.fixture(scope="function")
def db_engine(tmp_path_factory):
    """Create a fresh engine per-test to ensure isolation and avoid a
    shared global engine across tests.
    """
    url = os.environ.get("RACERAPI_DATABASE_URL", "sqlite+pysqlite:///:memory:")
    # For in-memory SQLite ensure the connection is not shared accidentally
    connect_args = {"check_same_thread": False}
    engine = create_engine(url, future=True, connect_args=connect_args)
    # create schema for this engine
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(db_engine):
    """Provide a function-scoped database session tied to a fresh engine."""
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
    """Test client that overrides DB dependency to use the test session."""
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
