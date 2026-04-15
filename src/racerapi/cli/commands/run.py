from __future__ import annotations

import uvicorn
from typing import Optional


def run_app(host: str = "127.0.0.1", port: int = 8000, reload: bool = False) -> None:
    """Run the application using uvicorn."""
    uvicorn.run("racerapi.main:app", host=host, port=port, reload=reload)
