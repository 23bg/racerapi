from racerapi.core.exceptions import ConflictError, NotFoundError, ValidationError
from racerapi.modules.users.repo import UserRepo
from racerapi.modules.users.schemas import UserCreate, UserUpdate


class UserService:
    def __init__(self, repo: UserRepo):
        self.repo = repo

    def get_user(self, user_id: int):
        user = self.repo.get_by_id(user_id)
        if user is None:
            raise NotFoundError(f"User {user_id} was not found")
        return user

    def list_users(self, page: int, page_size: int):
        if page < 1 or page_size < 1:
            raise ValidationError("page and page_size must be positive integers")
        offset = (page - 1) * page_size
        return self.repo.list_users(offset=offset, limit=page_size)

    def create_user(self, payload: UserCreate):
        existing = self.repo.get_by_email(payload.email)
        if existing is not None:
            raise ConflictError(f"User with email {payload.email} already exists")
        return self.repo.create(email=str(payload.email), full_name=payload.full_name)

    def update_user(self, user_id: int, payload: UserUpdate):
        user = self.get_user(user_id)
        if payload.full_name is not None:
            user.full_name = payload.full_name
        if payload.is_active is not None:
            user.is_active = payload.is_active
        return self.repo.update(user)
