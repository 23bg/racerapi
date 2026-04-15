from pydantic import BaseModel, ConfigDict, EmailStr, Field


class TestgenCreate(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=2)


class TestgenUpdate(BaseModel):
    full_name: str | None = None
    is_active: bool | None = None


class TestgenRead(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
