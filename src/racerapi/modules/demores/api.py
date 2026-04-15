from fastapi import APIRouter, Depends

from racerapi.modules.registry import register_router
from .deps import get_demores_service
from .schemas import DemoresRead, DemoresCreate, DemoresUpdate

router = APIRouter(prefix="/demores", tags=["demores"])


@router.get("", response_model=list[DemoresRead])
def list_items(service = Depends(get_demores_service)):
    items, total = service.list_demoress(page=1, page_size=100)
    return [ DemoresRead.model_validate(x) for x in items ]


@router.post("", response_model=DemoresRead)
def create_item(payload: DemoresCreate, service = Depends(get_demores_service)):
    entity = service.create_demores(payload)
    return DemoresRead.model_validate(entity)


register_router(router)
