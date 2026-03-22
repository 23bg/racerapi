from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from racerapi.db.base import Base
from racerapi.modules.users.repo import UserRepo


def test_user_repo_create_and_get_by_email():
    engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
    Base.metadata.create_all(bind=engine)
    factory = sessionmaker(
        bind=engine, class_=Session, autoflush=False, autocommit=False
    )

    with factory() as db:
        repo = UserRepo(db)
        created = repo.create(email="repo@example.com", full_name="Repo User")

        assert created.id is not None
        fetched = repo.get_by_email("repo@example.com")
        assert fetched is not None
        assert fetched.full_name == "Repo User"

        items, total = repo.list_users(offset=0, limit=10)
        assert total == 1
        assert items[0].email == "repo@example.com"
