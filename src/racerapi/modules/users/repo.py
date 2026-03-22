from sqlalchemy import func, select
from sqlalchemy.orm import Session

from racerapi.modules.users.models import User


class UserRepo:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.get(User, user_id)

    def get_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        return self.db.execute(stmt).scalar_one_or_none()

    def list_users(self, offset: int, limit: int) -> tuple[list[User], int]:
        items = (
            self.db.execute(select(User).offset(offset).limit(limit)).scalars().all()
        )
        total = self.db.execute(select(func.count()).select_from(User)).scalar_one()
        return items, total

    def create(self, email: str, full_name: str) -> User:
        entity = User(email=email, full_name=full_name, is_active=True)
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def update(self, entity: User) -> User:
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity
