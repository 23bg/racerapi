from fastapi import APIRouter
from app.modules.system.services.system_service import SystemService

router = APIRouter(prefix="/system", tags=["System"])
service = SystemService()

@router.get("/health")
def health():
    return service.health()

@router.get("/version")
def version():
    return service.version()
