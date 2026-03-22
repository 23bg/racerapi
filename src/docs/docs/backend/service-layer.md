# Service Layer Contract

## Responsibilities

Service layer owns:
- business rules
- orchestration across repo operations
- domain error generation

## Example

```python
def get_user(self, user_id: int):
    user = self.repo.get_by_id(user_id)
    if user is None:
        raise NotFoundError(f"User {user_id} was not found")
    return user
```

## DO

- Keep service methods named by business intent (`create_user`, `deactivate_user`).
- Validate business invariants here.
- Raise domain exceptions, not HTTP errors.

## DON'T

- Put HTTP request objects in service signatures.
- Put SQL query composition in service.

## Common Mistakes

- Fake service layer that just forwards `repo.method(...)` with no rules.
- Service committing raw transaction boundaries through direct DB session access.

## When to Break the Rule

Read-only pass-through methods are acceptable if the business rule is truly empty and likely to stay empty. Document this in code review.
