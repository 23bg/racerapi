from fastapi import APIRouter, Depends

from racerapi.modules.health.deps import get_health_service
from racerapi.modules.health.schemas import HealthResponse
from racerapi.modules.health.service import HealthService

router = APIRouter(prefix="/health", tags=["health"])


@router.get("", response_model=HealthResponse)
def health(service: HealthService = Depends(get_health_service)):
    result = service.check()
    return HealthResponse(**result)
