from sqlalchemy import text
from sqlalchemy.orm import Session


class HealthRepo:
    def __init__(self, db: Session):
        self.db = db

    def database_ready(self) -> bool:
        self.db.execute(text("SELECT 1"))
        return True
