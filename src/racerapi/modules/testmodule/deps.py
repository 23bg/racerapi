from fastapi import Depends
from sqlalchemy.orm import Session

from racerapi.core.deps import get_db
from .repo import TestmoduleRepo
from .service import TestmoduleService


def get_testmodule_repo(db: Session = Depends(get_db)) -> TestmoduleRepo:
    return TestmoduleRepo(db)


def get_testmodule_service(repo: TestmoduleRepo = Depends(get_testmodule_repo)) -> TestmoduleService:
    return TestmoduleService(repo)
