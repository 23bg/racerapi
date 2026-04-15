from fastapi import APIRouter, Depends

try:
    from racerapi.modules.registry import register_router
except Exception:
    register_router = None

from .deps import get_{singular}_service
from .schemas import {Name}Read, {Name}Create, {Name}Update

router = APIRouter(prefix="/{name}", tags=["{name}"])


@router.get("")
def list_items(service = Depends(get_{singular}_service)):
    items, total = service.list_items(page=1, page_size=100)
    return {{"items": [ {Name}Read.model_validate(x) for x in items ], "total": total}}


@router.post("", response_model={Name}Read, status_code=201)
def create_item(payload: {Name}Create, service = Depends(get_{singular}_service)):
    entity = service.create(payload)
    return {Name}Read.model_validate(entity)


@router.get("/{{item_id}}", response_model={Name}Read)
def get_item(item_id: int, service = Depends(get_{singular}_service)):
    obj = service.get_by_id(item_id)
    return {Name}Read.model_validate(obj)


@router.patch("/{{item_id}}", response_model={Name}Read)
def patch_item(item_id: int, payload: {Name}Update, service = Depends(get_{singular}_service)):
    obj = service.update(item_id, payload)
    return {Name}Read.model_validate(obj)


@router.delete("/{{item_id}}")
def delete_item(item_id: int, service = Depends(get_{singular}_service)):
    service.delete(item_id)
    return {{"ok": True}}


if register_router:
    register_router(router)
