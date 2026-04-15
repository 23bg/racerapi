from sqlalchemy import select, func
from sqlalchemy.orm import Session

from .models import Testgen


class TestgenRepo:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, item_id: int) -> Testgen | None:
        return self.db.get(Testgen, item_id)

    def list_items(self, offset: int, limit: int):
        items = self.db.execute(select(Testgen).offset(offset).limit(limit)).scalars().all()
        total = self.db.execute(select(func.count()).select_from(Testgen)).scalar_one()
        return items, total

    def create(self, **kwargs) -> Testgen:
        obj = Testgen(**kwargs)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, entity: Testgen):
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def get_by_unique(self, value):
        # override per model
        return None
