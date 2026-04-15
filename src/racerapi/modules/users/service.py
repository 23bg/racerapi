from racerapi.core.exceptions import NotFoundError, ConflictError, ValidationError
from .repo import UserRepo
from .schemas import UserCreate, UserUpdate


class UserService:
    def __init__(self, repo: UserRepo):
        self.repo = repo

    def get_by_id(self, item_id: int):
        obj = self.repo.get_by_id(item_id)
        if obj is None:
            raise NotFoundError(f"User {item_id} not found")
        return obj

    def list_items(self, page: int, page_size: int):
        if page < 1 or page_size < 1:
            raise ValidationError("page and page_size must be positive")
        offset = (page - 1) * page_size
        return self.repo.list_items(offset=offset, limit=page_size)

    def create(self, payload: UserCreate):
        existing = None
        if hasattr(self.repo, 'get_by_unique'):
            existing = self.repo.get_by_unique(payload.email)
        elif hasattr(self.repo, 'get_by_email'):
            existing = self.repo.get_by_email(payload.email)
        if existing:
            raise ConflictError("duplicate")
        return self.repo.create(**payload.model_dump())

    def update(self, item_id: int, payload: UserUpdate):
        obj = self.get_by_id(item_id)
        for k, v in payload.model_dump(exclude_none=True).items():
            setattr(obj, k, v)
        return self.repo.update(obj)

    def delete(self, item_id: int):
        obj = self.get_by_id(item_id)
        self.repo.delete(item_id)
        return True

    # Backwards-compatible aliases
    def create_user(self, payload: UserCreate):
        return self.create(payload)

    def get_user(self, item_id: int):
        return self.get_by_id(item_id)

    def list_users(self, page: int, page_size: int):
        return self.list_items(page, page_size)

    def update_user(self, item_id: int, payload: UserUpdate):
        return self.update(item_id, payload)

    def delete_user(self, item_id: int):
        return self.delete(item_id)
