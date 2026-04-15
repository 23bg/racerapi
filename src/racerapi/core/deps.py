from collections.abc import Generator

from sqlalchemy.orm import Session

from racerapi.db.session import get_session


def get_db() -> Generator[Session, None, None]:
    db = get_session()
    try:
        yield db
    finally:
        db.close()
