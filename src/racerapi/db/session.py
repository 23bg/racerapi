from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from racerapi.core.config import settings

engine = create_engine(settings.database_url, future=True)
SessionLocal = sessionmaker(
    bind=engine, autoflush=False, autocommit=False, class_=Session
)
