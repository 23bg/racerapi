from sqlalchemy import select, func
from sqlalchemy.orm import Session

from .models import Testmodule


class TestmoduleRepo:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, item_id: int) -> Testmodule | None:
        return self.db.get(Testmodule, item_id)

    def list_items(self, offset: int, limit: int):
        items = self.db.execute(select(Testmodule).offset(offset).limit(limit)).scalars().all()
        total = self.db.execute(select(func.count()).select_from(Testmodule)).scalar_one()
        return items, total

    def create(self, **kwargs) -> Testmodule:
        obj = Testmodule(**kwargs)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, entity: Testmodule):
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def get_by_unique(self, value):
        # override per model
        return None
