# Users Module (Reference Implementation)

## Purpose

The users module demonstrates the production contract for all modules.

## API Layer

```python
@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, service: UserService = Depends(get_user_service)):
    user = service.create_user(payload)
    return UserRead.model_validate(user)
```

## Service Layer

```python
def create_user(self, payload: UserCreate):
    existing = self.repo.get_by_email(payload.email)
    if existing is not None:
        raise ConflictError(f"User with email {payload.email} already exists")
    return self.repo.create(email=str(payload.email), full_name=payload.full_name)
```

## Repo Layer

```python
def get_by_email(self, email: str) -> User | None:
    stmt = select(User).where(User.email == email)
    return self.db.execute(stmt).scalar_one_or_none()
```

## DI Wiring

```python
def get_user_repo(db: Session = Depends(get_db)) -> UserRepo:
    return UserRepo(db)

def get_user_service(repo: UserRepo = Depends(get_user_repo)) -> UserService:
    return UserService(repo)
```

## DO

- Raise domain exceptions from service.
- Keep repo methods query-focused.
- Return schema models from API.

## DON'T

- Raise HTTPException inside repo.
- Parse request headers in service.
- Commit DB transactions from API.

## Common Mistakes

- Duplicate uniqueness checks in both API and service.
- Returning ORM directly without schema mapping policy.

## When to Break the Rule

Never bypass service for create/update/delete flows.
