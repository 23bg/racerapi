from pydantic import BaseModel


class SystemBase(BaseModel):
    name: str


class SystemCreate(SystemBase):
    pass

class SystemUpdate(SystemBase):
    pass


class SystemOut(SystemBase):
    id: int