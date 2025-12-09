
from .services import {{ class_name }}Service
from .schemas import {{ class_name }}Create, {{ class_name }}Out


class {{ class_name }}Controller:
    def __init__(self):
        self.service = {{ class_name }}Service()

    async def list(self) -> list[{{ class_name }}Out]:
        return await self.service.list()

    async def create(self, payload: {{ class_name }}Create):
        return await self.service.create(payload)
