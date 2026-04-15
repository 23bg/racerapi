from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from racerapi.db.base import Base


class Testgen(Base):
    __tablename__ = "testgens"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
