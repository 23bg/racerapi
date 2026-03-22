# Dependency Injection

## DI Standard

Use FastAPI `Depends` only. No custom container, no global registries, no service locators.

## Dependency Chain Pattern

```python
# src/racerapi/modules/users/deps.py

def get_user_repo(db: Session = Depends(get_db)) -> UserRepo:
    return UserRepo(db)


def get_user_service(repo: UserRepo = Depends(get_user_repo)) -> UserService:
    return UserService(repo)
```

This chain gives:
- explicit construction graph
- easy test overrides
- deterministic runtime wiring

## Endpoint Injection Example

```python
@router.get("/{user_id}")
def get_user(user_id: int, service: UserService = Depends(get_user_service)):
    return UserRead.model_validate(service.get_user(user_id))
```

## DO

- Put DI providers in each module `deps.py`.
- Keep provider functions small and pure.
- Reuse `core.get_db` for DB session ownership.

## DON'T

- Instantiate repos/services directly in route functions.
- Create module-level singleton services.
- Hide dependencies in globals.

## Common Mistakes

- Writing `service = UserService(UserRepo(SessionLocal()))` in API handlers.
- Passing FastAPI `Request` down into service layer.
- Mixing DI and manual construction in same endpoint.

## When to Break the Rule

In tests only, when overriding dependencies:

```python
app.dependency_overrides[get_user_service] = lambda: FakeUserService()
```

Do not carry test wiring into production code.
