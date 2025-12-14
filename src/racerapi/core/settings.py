from pydantic import BaseModel, Field
from typing import Optional, Any, List, Dict, Callable


class AppSettings(BaseModel):
    title: str = "RacerAPI"
    description: Optional[str] = None
    version: str = "0.1.0"

    docs_url: Optional[str] = "/docs"
    redoc_url: Optional[str] = "/redoc"
    openapi_url: Optional[str] = "/openapi.json"

    # Middleware configuration
    # middlewares: List[Callable] = []

    # Exception handlers
    # exception_handlers: Dict[Any, Callable] = {}

    # CORS config (optional)
    # cors_origins: List[str] = []
    # cors_allow_credentials: bool = True
    # cors_allow_methods: List[str] = ["*"]
    # cors_allow_headers: List[str] = ["*"]

    # Additional routers (outside module system)
    extra_routers: List[Any] = []

    middlewares: List[type] = Field(default_factory=list)
    exception_handlers: Dict[Any, Callable] = Field(default_factory=dict)
    cors_origins: List[str] = Field(default_factory=list)
    cors_allow_credentials: List[str] = Field(default_factory=lambda: ["*"])
    cors_allow_methods: List[str] = Field(default_factory=lambda: ["*"])
    cors_allow_headers: List[str] = Field(default_factory=lambda: ["*"])
    extra_routers: List[Any] = Field(default_factory=list)
