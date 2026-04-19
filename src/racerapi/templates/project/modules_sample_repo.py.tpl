class SampleRepository:
    def __init__(self, driver):
        self._driver = driver

    async def list(self):
        return await self._driver.find_all("sample")

    async def get(self, id_):
        return await self._driver.find_by_id("sample", id_)

    async def create(self, payload):
        return await self._driver.create("sample", payload)

    async def update(self, id_, payload):
        return await self._driver.update("sample", id_, payload)

    async def delete(self, id_):
        return await self._driver.delete("sample", id_)
