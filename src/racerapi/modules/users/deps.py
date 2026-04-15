from fastapi import Depends
from sqlalchemy.orm import Session

from racerapi.core.deps import get_db
from .repo import UserRepo
from .service import UserService


def get_user_repo(db: Session = Depends(get_db)) -> UserRepo:
    return UserRepo(db)


def get_user_service(repo: UserRepo = Depends(get_user_repo)) -> UserService:
    return UserService(repo)
