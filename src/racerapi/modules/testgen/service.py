from racerapi.core.exceptions import NotFoundError, ConflictError, ValidationError
from .repo import TestgenRepo
from .schemas import TestgenCreate, TestgenUpdate


class TestgenService:
    def __init__(self, repo: TestgenRepo):
        self.repo = repo

    def get_testgen(self, item_id: int):
        obj = self.repo.get_by_id(item_id)
        if obj is None:
            raise NotFoundError(f"Testgen {item_id} not found")
        return obj

    def list_testgens(self, page: int, page_size: int):
        if page < 1 or page_size < 1:
            raise ValidationError("page and page_size must be positive")
        offset = (page - 1) * page_size
        return self.repo.list_items(offset=offset, limit=page_size)

    def create_testgen(self, payload: TestgenCreate):
        existing = self.repo.get_by_unique(payload.email) if hasattr(payload, 'email') else None
        if existing:
            raise ConflictError("duplicate")
        return self.repo.create(**payload.model_dump())

    def update_testgen(self, item_id: int, payload: TestgenUpdate):
        obj = self.get_testgen(item_id)
        for k, v in payload.model_dump(exclude_none=True).items():
            setattr(obj, k, v)
        return self.repo.update(obj)
