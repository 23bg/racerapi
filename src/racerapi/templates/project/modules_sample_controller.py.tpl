from fastapi import APIRouter, HTTPException

from modules.sample.service import SampleService

router = APIRouter(prefix="/sample", tags=["sample"])

@router.get("/")
async def list_samples():
    service = SampleService(None)
    return await service.list()

@router.post("/")
async def create_sample(payload: dict):
    service = SampleService(None)
    return await service.create(payload)

@router.get("/{item_id}")
async def get_sample(item_id: str):
    service = SampleService(None)
    item = await service.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    return item
