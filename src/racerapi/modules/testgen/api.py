from fastapi import APIRouter, Depends

from racerapi.modules.registry import register_router
from .deps import get_testgen_service
from .schemas import TestgenRead, TestgenCreate

router = APIRouter(prefix="/testgen", tags=["testgen"])


@router.get("", response_model=list[TestgenRead])
def list_items(service = Depends(get_testgen_service)):
    items, total = service.list_testgens(page=1, page_size=100)
    return [ TestgenRead.model_validate(x) for x in items ]


@router.post("", response_model=TestgenRead)
def create_item(payload: TestgenCreate, service = Depends(get_testgen_service)):
    entity = service.create_testgen(payload)
    return TestgenRead.model_validate(entity)


register_router(router)
