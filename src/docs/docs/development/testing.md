# Testing Strategy

## Test Pyramid

- Unit tests: service logic (fast, isolated)
- Integration tests: repo + in-memory DB
- API tests: FastAPI `TestClient`

Current examples:
- `tests/test_users_service.py`
- `tests/test_users_repo.py`
- `tests/test_users_api.py`

## Run Tests

```bash
pytest -q
```

## Service Unit Test Example

```python
with pytest.raises(ConflictError):
    service.create_user(UserCreate(email="john@example.com", full_name="John"))
```

## DO

- Keep service tests independent from DB.
- Use in-memory SQLite for repo integration tests.
- Test endpoint status and response contracts.

## DON'T

- Mock everything in repo tests.
- Assert implementation details instead of behavior.

## Common Mistakes

- Writing only API tests and skipping business-rule unit tests.
- Sharing mutable test database state across test modules.

## When to Break the Rule

End-to-end tests may use real DB containers for critical flows, but keep unit/integration suite as fast gate.
