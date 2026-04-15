from pydantic import BaseModel, ConfigDict, Field, EmailStr


class DemoresCreate(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=2)


class DemoresUpdate(BaseModel):
    full_name: str | None = None
    is_active: bool | None = None


class DemoresRead(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
