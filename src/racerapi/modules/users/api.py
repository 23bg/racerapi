from fastapi import APIRouter, Depends, Query, status

from racerapi.modules.users.deps import get_user_service
from racerapi.modules.users.schemas import (
    UserCreate,
    UserRead,
    UsersListResponse,
    UserUpdate,
)
from racerapi.modules.users.service import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=UsersListResponse)
def list_users(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    service: UserService = Depends(get_user_service),
):
    items, total = service.list_users(page=page, page_size=page_size)
    return UsersListResponse(
        items=[UserRead.model_validate(x) for x in items], total=total
    )


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(
    payload: UserCreate,
    service: UserService = Depends(get_user_service),
):
    user = service.create_user(payload)
    return UserRead.model_validate(user)


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, service: UserService = Depends(get_user_service)):
    user = service.get_user(user_id)
    return UserRead.model_validate(user)


@router.patch("/{user_id}", response_model=UserRead)
def patch_user(
    user_id: int,
    payload: UserUpdate,
    service: UserService = Depends(get_user_service),
):
    user = service.update_user(user_id=user_id, payload=payload)
    return UserRead.model_validate(user)
