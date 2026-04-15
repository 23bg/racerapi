from sqlalchemy import select, func
from sqlalchemy.orm import Session

from .models import User


class UserRepo:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, item_id: int) -> User | None:
        return self.db.get(User, item_id)

    def list_items(self, offset: int, limit: int):
        items = self.db.execute(select(User).offset(offset).limit(limit)).scalars().all()
        total = self.db.execute(select(func.count()).select_from(User)).scalar_one()
        return items, total

    def create(self, **kwargs) -> User:
        obj = User(**kwargs)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, entity: User):
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def get_by_unique(self, value):
        # override per model
        # Basic default: treat 'unique' as email lookup
        return self.get_by_email(value)

    def get_by_email(self, email: str):
        stmt = select(User).where(User.email == email)
        return self.db.execute(stmt).scalars().first()

    def list_users(self, offset: int, limit: int):
        return self.list_items(offset=offset, limit=limit)

    def delete(self, item_id: int) -> bool:
        obj = self.get_by_id(item_id)
        if obj is None:
            return False
        self.db.delete(obj)
        self.db.commit()
        return True
