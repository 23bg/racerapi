from sqlalchemy import select, func
from sqlalchemy.orm import Session

from .models import Demores


class DemoresRepo:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, item_id: int) -> Demores | None:
        return self.db.get(Demores, item_id)

    def list_items(self, offset: int, limit: int):
        items = self.db.execute(select(Demores).offset(offset).limit(limit)).scalars().all()
        total = self.db.execute(select(func.count()).select_from(Demores)).scalar_one()
        return items, total

    def create(self, **kwargs) -> Demores:
        obj = Demores(**kwargs)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, entity: Demores):
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def get_by_unique(self, value):
        # override per model
        return None
