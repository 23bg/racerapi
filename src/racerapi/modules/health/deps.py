from fastapi import Depends
from sqlalchemy.orm import Session

from racerapi.core.deps import get_db
from racerapi.modules.health.repo import HealthRepo
from racerapi.modules.health.service import HealthService


def get_health_repo(db: Session = Depends(get_db)) -> HealthRepo:
    return HealthRepo(db)


def get_health_service(repo: HealthRepo = Depends(get_health_repo)) -> HealthService:
    return HealthService(repo)
