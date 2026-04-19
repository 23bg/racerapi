from __future__ import annotations

from abc import ABC, abstractmethod
from contextlib import AbstractContextManager
from typing import Any, Generator


class DatabaseProvider(ABC):
    """Abstract database provider contract.

    Implementations must manage connection lifecycle and provide a session
    context manager. Core code should only depend on this contract.
    """

    @abstractmethod
    def startup(self) -> None:
        """Called once when the application starts (optional)."""

    @abstractmethod
    def shutdown(self) -> None:
        """Called once when the application stops (optional)."""

    @abstractmethod
    def get_session(self) -> AbstractContextManager[Any]:
        """Return a context manager that yields a database session/object.

        The concrete session type is implementation-defined (SQLAlchemy Session,
        a raw connection, a pymongo client, etc.). Repositories should treat it
        opaquely.
        """


__all__ = ["DatabaseProvider"]
