from pydantic import BaseModel, ConfigDict, Field, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=2)


class UserUpdate(BaseModel):
    full_name: str | None = None
    is_active: bool | None = None


class UserRead(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
