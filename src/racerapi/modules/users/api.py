from fastapi import APIRouter, Depends

try:
    from racerapi.modules.registry import register_router
except Exception:
    register_router = None

from .deps import get_user_service
from .schemas import UserRead, UserCreate, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


@router.get("")
def list_items(service = Depends(get_user_service)):
    items, total = service.list_items(page=1, page_size=100)
    return {"items": [ UserRead.model_validate(x) for x in items ], "total": total}


@router.post("", response_model=UserRead, status_code=201)
def create_item(payload: UserCreate, service = Depends(get_user_service)):
    entity = service.create(payload)
    return UserRead.model_validate(entity)


@router.get("/{item_id}", response_model=UserRead)
def get_item(item_id: int, service = Depends(get_user_service)):
    obj = service.get_by_id(item_id)
    return UserRead.model_validate(obj)


@router.patch("/{item_id}", response_model=UserRead)
def patch_item(item_id: int, payload: UserUpdate, service = Depends(get_user_service)):
    obj = service.update(item_id, payload)
    return UserRead.model_validate(obj)


@router.delete("/{item_id}")
def delete_item(item_id: int, service = Depends(get_user_service)):
    service.delete(item_id)
    return {"ok": True}


if register_router:
    register_router(router)
