from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, ConfigDict

from racerapi.modules.sample.service import SampleService


class SampleCreateRequest(BaseModel):
    name: str
    value: str | None = None


class SampleUpdateRequest(BaseModel):
    name: str | None = None
    value: str | None = None


class SampleResponse(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: int | str
    name: str
    value: str | None = None


def create_router(service: SampleService) -> APIRouter:
    router = APIRouter(prefix="/sample", tags=["sample"])

    @router.get("", response_model=list[SampleResponse])
    def list_items() -> list[dict[str, Any]]:
        return service.list_items()

    @router.get("/{item_id}", response_model=SampleResponse)
    def get_item(item_id: int) -> dict[str, Any]:
        item = service.get_item(item_id)
        if item is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
        return item

    @router.post("", response_model=SampleResponse, status_code=status.HTTP_201_CREATED)
    def create_item(payload: SampleCreateRequest) -> dict[str, Any]:
        return service.create_item(payload.model_dump(exclude_none=True))

    @router.put("/{item_id}", response_model=SampleResponse)
    def update_item(item_id: int, payload: SampleUpdateRequest) -> dict[str, Any]:
        updated = service.update_item(item_id, payload.model_dump(exclude_none=True))
        if updated is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
        return updated

    @router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
    def delete_item(item_id: int) -> None:
        deleted = service.delete_item(item_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    return router
