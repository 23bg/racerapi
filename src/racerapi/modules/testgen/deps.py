from fastapi import Depends
from sqlalchemy.orm import Session

from racerapi.core.deps import get_db
from .repo import TestgenRepo
from .service import TestgenService


def get_testgen_repo(db: Session = Depends(get_db)) -> TestgenRepo:
    return TestgenRepo(db)


def get_testgen_service(repo: TestgenRepo = Depends(get_testgen_repo)) -> TestgenService:
    return TestgenService(repo)
