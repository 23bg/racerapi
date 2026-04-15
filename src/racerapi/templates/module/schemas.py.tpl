from pydantic import BaseModel, ConfigDict, Field, EmailStr


class {Name}Create(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=2)


class {Name}Update(BaseModel):
    full_name: str | None = None
    is_active: bool | None = None


class {Name}Read(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
