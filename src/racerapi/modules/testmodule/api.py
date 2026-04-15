from fastapi import APIRouter, Depends

from racerapi.modules.registry import register_router
from .deps import get_testmodule_service
from .schemas import TestmoduleRead, TestmoduleCreate, TestmoduleUpdate

router = APIRouter(prefix="/testmodule", tags=["testmodule"])


@router.get("", response_model=list[TestmoduleRead])
def list_items(service = Depends(get_testmodule_service)):
    items, total = service.list_testmodules(page=1, page_size=100)
    return [ TestmoduleRead.model_validate(x) for x in items ]


@router.post("", response_model=TestmoduleRead)
def create_item(payload: TestmoduleCreate, service = Depends(get_testmodule_service)):
    entity = service.create_testmodule(payload)
    return TestmoduleRead.model_validate(entity)


register_router(router)
