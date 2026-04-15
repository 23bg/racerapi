from racerapi.core.exceptions import NotFoundError, ConflictError, ValidationError
from .repo import {Name}Repo
from .schemas import {Name}Create, {Name}Update


class {Name}Service:
    def __init__(self, repo: {Name}Repo):
        self.repo = repo

    def get_by_id(self, item_id: int):
        obj = self.repo.get_by_id(item_id)
        if obj is None:
            raise NotFoundError(f"{Name} {{item_id}} not found")
        return obj

    def list_items(self, page: int, page_size: int):
        if page < 1 or page_size < 1:
            raise ValidationError("page and page_size must be positive")
        offset = (page - 1) * page_size
        return self.repo.list_items(offset=offset, limit=page_size)

    def create(self, payload: {Name}Create):
        existing = self.repo.get_by_unique(payload.email) if hasattr(payload, 'email') else None
        if existing:
            raise ConflictError("duplicate")
        return self.repo.create(**payload.model_dump())

    def update(self, item_id: int, payload: {Name}Update):
        obj = self.get_by_id(item_id)
        for k, v in payload.model_dump(exclude_none=True).items():
            setattr(obj, k, v)
        return self.repo.update(obj)

    def delete(self, item_id: int):
        obj = self.get_by_id(item_id)
        self.repo.delete(item_id)
        return True
