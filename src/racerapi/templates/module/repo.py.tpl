from sqlalchemy import select, func
from sqlalchemy.orm import Session

from .models import {Name}


class {Name}Repo:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, item_id: int) -> {Name} | None:
        return self.db.get({Name}, item_id)

    def list_items(self, offset: int, limit: int):
        items = self.db.execute(select({Name}).offset(offset).limit(limit)).scalars().all()
        total = self.db.execute(select(func.count()).select_from({Name})).scalar_one()
        return items, total

    def create(self, **kwargs) -> {Name}:
        obj = {Name}(**kwargs)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, entity: {Name}):
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def get_by_unique(self, value):
        # override per model
        return None
    def delete(self, item_id: int) -> bool:
        obj = self.get_by_id(item_id)
        if obj is None:
            return False
        self.db.delete(obj)
        self.db.commit()
        return True
