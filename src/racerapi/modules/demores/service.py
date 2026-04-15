from racerapi.core.exceptions import NotFoundError, ConflictError, ValidationError
from .repo import DemoresRepo
from .schemas import DemoresCreate, DemoresUpdate


class DemoresService:
    def __init__(self, repo: DemoresRepo):
        self.repo = repo

    def get_demores(self, item_id: int):
        obj = self.repo.get_by_id(item_id)
        if obj is None:
            raise NotFoundError(f"Demores {item_id} not found")
        return obj

    def list_demoress(self, page: int, page_size: int):
        if page < 1 or page_size < 1:
            raise ValidationError("page and page_size must be positive")
        offset = (page - 1) * page_size
        return self.repo.list_items(offset=offset, limit=page_size)

    def create_demores(self, payload: DemoresCreate):
        existing = self.repo.get_by_unique(payload.email) if hasattr(payload, 'email') else None
        if existing:
            raise ConflictError("duplicate")
        return self.repo.create(**payload.model_dump())

    def update_demores(self, item_id: int, payload: DemoresUpdate):
        obj = self.get_demores(item_id)
        for k, v in payload.model_dump(exclude_none=True).items():
            setattr(obj, k, v)
        return self.repo.update(obj)
