from __future__ import annotations

from fastapi import Depends, Request
from typing import Any


def provide(token: Any):
    """Return a FastAPI dependency that resolves `token` from the app container.

    Example:
        def get_items(repo = Depends(provide(MyRepo))):
            return repo.list()
    """

    def _resolve(request: Request):
        container = getattr(request.app.state, "container", None)
        if container is None:
            raise RuntimeError("DI container not configured on app.state.container")
        return container.resolve(token)

    return Depends(_resolve)


__all__ = ["provide"]
