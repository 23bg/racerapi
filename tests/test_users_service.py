import pytest

from racerapi.core.exceptions import ConflictError, NotFoundError
from racerapi.modules.users.schemas import UserCreate, UserUpdate
from racerapi.modules.users.service import UserService


class FakeUser:
    def __init__(
        self, user_id: int, email: str, full_name: str, is_active: bool = True
    ):
        self.id = user_id
        self.email = email
        self.full_name = full_name
        self.is_active = is_active


class FakeRepo:
    def __init__(self):
        self.items = {1: FakeUser(1, "john@example.com", "John")}

    def get_by_id(self, user_id: int):
        return self.items.get(user_id)

    def get_by_email(self, email: str):
        return next((x for x in self.items.values() if x.email == email), None)

    def list_users(self, offset: int, limit: int):
        data = list(self.items.values())[offset : offset + limit]
        return data, len(self.items)

    def create(self, email: str, full_name: str):
        user = FakeUser(2, email, full_name)
        self.items[user.id] = user
        return user

    def update(self, entity):
        self.items[entity.id] = entity
        return entity


def test_create_user_rejects_duplicate_email():
    service = UserService(FakeRepo())

    with pytest.raises(ConflictError):
        service.create_user(UserCreate(email="john@example.com", full_name="John"))


def test_get_user_raises_not_found():
    service = UserService(FakeRepo())

    with pytest.raises(NotFoundError):
        service.get_user(999)


def test_update_user_changes_fields():
    service = UserService(FakeRepo())
    updated = service.update_user(1, UserUpdate(full_name="John Doe", is_active=False))

    assert updated.full_name == "John Doe"
    assert updated.is_active is False
