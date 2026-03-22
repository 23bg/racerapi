# Request Flow

## Canonical Flow

`Request -> Router -> Service -> Repo -> DB -> Response`

This is mandatory. Any shortcut is architectural debt.

## Step-by-Step

1. Router parses HTTP input into schema objects.
2. Router resolves service via `Depends`.
3. Service validates business rules and orchestrates operations.
4. Service calls repo for persistence/query.
5. Repo executes SQLAlchemy operations.
6. Service returns domain result.
7. Router maps result to response schema.

## Real Code Walkthrough

```python
# src/racerapi/modules/users/api.py
@router.patch("/{user_id}", response_model=UserRead)
def patch_user(
    user_id: int,
    payload: UserUpdate,
    service: UserService = Depends(get_user_service),
):
    user = service.update_user(user_id=user_id, payload=payload)
    return UserRead.model_validate(user)
```

```python
# src/racerapi/modules/users/service.py
def update_user(self, user_id: int, payload: UserUpdate):
    user = self.get_user(user_id)
    if payload.full_name is not None:
        user.full_name = payload.full_name
    if payload.is_active is not None:
        user.is_active = payload.is_active
    return self.repo.update(user)
```

```python
# src/racerapi/modules/users/repo.py
def update(self, entity: User) -> User:
    self.db.add(entity)
    self.db.commit()
    self.db.refresh(entity)
    return entity
```

## Text Diagram

```text
HTTP PATCH /users/{id}
  |
  v
users.api.patch_user(...)
  |
  v
users.service.update_user(...)
  |
  v
users.repo.update(...)
  |
  v
SQLAlchemy Session -> Database
  |
  v
User ORM entity
  |
  v
UserRead response model
  |
  v
HTTP 200 JSON
```

## DO

- Keep transport concerns in API layer.
- Keep business branching in service layer.
- Keep DB session usage in repo layer only.

## DON'T

- Call SQLAlchemy directly in route handlers.
- Put business decisions inside repo methods.
- Return raw ORM internals without schema mapping.

## Common Mistakes

- Performing uniqueness checks in routes.
- Committing transactions from service methods.
- Returning dict literals from service while other endpoints return schemas.

## When to Break the Rule

Rare read-only health checks may skip service logic if there is no business rule. Even then, keep repo for DB calls.
