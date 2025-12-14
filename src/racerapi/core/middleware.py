# racerapi/middleware.py
from abc import ABC, abstractmethod
from typing import Callable, Awaitable, Any


class RequestContext:
    """
    Framework-level request abstraction.
    Hides FastAPI / Starlette internals from users.
    """

    def __init__(self, request: Any):
        self._request = request

    @property
    def method(self) -> str:
        return self._request.method

    @property
    def path(self) -> str:
        return self._request.url.path

    @property
    def headers(self):
        return self._request.headers

    @property
    def state(self):
        return self._request.state

    def raw(self):
        """
        Escape hatch for advanced users.
        """
        return self._request


class Middleware(ABC):
    """
    RacerAPI Middleware base class.

    Users implement `handle`, NOT Starlette middleware.
    """

    @abstractmethod
    async def handle(
        self,
        ctx: RequestContext,
        next: Callable[[], Awaitable[Any]],
    ) -> Any:
        """
        Process request and return response.

        ctx   -> RacerAPI request context
        next  -> call next middleware / controller
        """
        raise NotImplementedError
