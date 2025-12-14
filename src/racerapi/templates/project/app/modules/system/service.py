from typing import List
from .schema import (
    SystemCreate,
    SystemUpdate,
    SystemOut,
)


class SystemService:
    """
    System Service
    Contains business logic only.
    No FastAPI, no decorators, no transport concerns.
    """

    async def list(self) -> List[SystemOut]:
        """
        Return all system records.
        """
        # TODO: fetch from repository / data source
        return []

    async def get(self, id: int) -> SystemOut:
        """
        Get a single system by ID.
        """
        # TODO: fetch by id
        raise NotImplementedError

    async def create(self, payload: SystemCreate) -> SystemOut:
        """
        Create a new system.
        """
        # TODO: persist entity
        return SystemOut(
            id=1,
            **payload.model_dump(),
        )

    async def update(
        self,
        id: int,
        payload: SystemUpdate,
    ) -> SystemOut:
        """
        Update an existing system.
        """
        # TODO: update entity
        return SystemOut(
            id=id,
            **payload.model_dump(),
        )

    async def delete(self, id: int) -> None:
        """
        Delete a system.
        """
        # TODO: delete entity
        return None