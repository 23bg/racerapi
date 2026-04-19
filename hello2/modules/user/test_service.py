from .service import UserService


def test_get_items():
    service = UserService()
    assert isinstance(service.get_items(), list)
