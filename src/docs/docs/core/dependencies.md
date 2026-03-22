# Core Dependencies

## Root Dependencies

Core dependency providers live in `src/racerapi/core/deps.py`.

```python
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

## Chained Dependencies

Module providers build on core providers:

```python
def get_user_repo(db: Session = Depends(get_db)) -> UserRepo:
    return UserRepo(db)
```

## DO

- Keep providers side-effect free.
- Keep dependency graph explicit and linear.

## DON'T

- Hide service construction in startup hooks.
- Use global object registries.

## Common Mistakes

- Creating providers that perform DB writes.
- Injecting more dependencies than endpoint needs.

## When to Break the Rule

Complex graph factories are acceptable only when domain complexity requires them and the graph remains explicit in provider code.
