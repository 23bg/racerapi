from fastapi import Depends
from sqlalchemy.orm import Session

from racerapi.core.deps import get_db
from .repo import DemoresRepo
from .service import DemoresService


def get_demores_repo(db: Session = Depends(get_db)) -> DemoresRepo:
    return DemoresRepo(db)


def get_demores_service(repo: DemoresRepo = Depends(get_demores_repo)) -> DemoresService:
    return DemoresService(repo)
