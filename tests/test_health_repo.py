from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from racerapi.modules.health.repo import HealthRepo


def test_health_repo_database_ready_returns_true():
    engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
    factory = sessionmaker(
        bind=engine, class_=Session, autoflush=False, autocommit=False
    )

    with factory() as db:
        repo = HealthRepo(db)
        assert repo.database_ready() is True
