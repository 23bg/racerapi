
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class System:
    """
    Domain entity for System.
    Pure business object, no framework dependencies.
    """

    id: Optional[int]
    name: str

    def rename(self, new_name: str) -> "System":
        if not new_name:
            raise ValueError("Name cannot be empty")

        return System(
            id=self.id,
            name=new_name,
        )