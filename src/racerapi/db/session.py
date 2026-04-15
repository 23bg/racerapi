from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from racerapi.core.config import settings

# Lazy engine/session factory to allow tests to override engine before creation.
_engine: Optional[Engine] = None
_SessionLocal = None


def init_engine(database_url: Optional[str] = None) -> Engine:
    """Create and return a new SQLAlchemy Engine and session factory.

    This will set module-level engine and Session factory.
    """
    global _engine, _SessionLocal
    url = database_url or settings.database_url
    connect_args = {}
    engine_kwargs = {}
    if url.startswith("sqlite"):
        # For :memory: use StaticPool so connections share the same DB
        if ":memory:" in url:
            engine_kwargs["poolclass"] = StaticPool
            connect_args["check_same_thread"] = False
        else:
            connect_args["check_same_thread"] = False

    _engine = create_engine(url, future=True, connect_args=connect_args, **engine_kwargs)
    _SessionLocal = sessionmaker(bind=_engine, autoflush=False, autocommit=False, class_=Session)
    return _engine


def get_engine(database_url: Optional[str] = None) -> Engine:
    global _engine
    if _engine is None:
        return init_engine(database_url)
    return _engine


def get_session_maker():
    global _SessionLocal
    if _SessionLocal is None:
        init_engine()
    return _SessionLocal


def get_session() -> Session:
    factory = get_session_maker()
    return factory()


def set_engine(engine: Engine) -> None:
    """Override the engine (useful for tests)."""
    global _engine, _SessionLocal
    _engine = engine
    _SessionLocal = sessionmaker(bind=_engine, autoflush=False, autocommit=False, class_=Session)


def __getattr__(name: str):
    # provide backwards-compatible `engine` attribute lazily
    if name == "engine":
        return get_engine()
    raise AttributeError(name)


__all__ = ["get_engine", "get_session", "get_session_maker", "set_engine", "engine"]
