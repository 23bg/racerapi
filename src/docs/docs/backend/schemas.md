# Schemas

## Purpose

Schemas define external and internal data contracts:
- request payload validation
- response shaping
- contract stability across endpoints

## Example

```python
class UserCreate(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=2, max_length=255)

class UserRead(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    is_active: bool
    model_config = ConfigDict(from_attributes=True)
```

## DO

- Keep API schemas in module `schemas.py`.
- Use strict field constraints.
- Separate create/update/read schemas.

## DON'T

- Reuse DB ORM classes as API schemas.
- Put business logic methods inside schemas.

## Common Mistakes

- One giant schema used for create/update/read.
- Optional fields in create payloads without explicit reason.

## When to Break the Rule

Temporary compatibility schemas are allowed during version migrations; add removal plan in PR.
