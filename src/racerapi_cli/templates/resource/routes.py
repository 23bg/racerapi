from fastapi import APIRouter
from .controllers import {{ class_name }}Controller

router = APIRouter(prefix="/{{ resource_name }}", tags=["{{ class_name }}"])

controller = {{ class_name }}Controller()


@router.get("/")
async def list_items():
    return await controller.list()


@router.post("/")
async def create_item(payload: dict):
    return await controller.create(payload)
