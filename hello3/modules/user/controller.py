from fastapi import APIRouter
from .service import UserService

router = APIRouter()
service = UserService()


@router.get("/")
def get_items():
    return service.get_items()


@router.post("/")
def create_item(data: dict):
    return service.create_item(data)
