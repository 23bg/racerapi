from core.logger.logger import get_logger

logger = get_logger("sample.service")

class SampleService:
    def __init__(self, repo):
        self._repo = repo

    async def list(self):
        logger.info("Listing samples")
        return await self._repo.list()

    async def get(self, id_):
        return await self._repo.get(id_)

    async def create(self, payload):
        return await self._repo.create(payload)

    async def update(self, id_, payload):
        return await self._repo.update(id_, payload)

    async def delete(self, id_):
        return await self._repo.delete(id_)
