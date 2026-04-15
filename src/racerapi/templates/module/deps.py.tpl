from fastapi import Depends
from sqlalchemy.orm import Session

from racerapi.core.deps import get_db
from .repo import {Name}Repo
from .service import {Name}Service


def get_{singular}_repo(db: Session = Depends(get_db)) -> {Name}Repo:
    return {Name}Repo(db)


def get_{singular}_service(repo: {Name}Repo = Depends(get_{singular}_repo)) -> {Name}Service:
    return {Name}Service(repo)
