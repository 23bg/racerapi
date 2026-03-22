# Repo Layer Contract

## Responsibilities

Repo layer owns:
- SQLAlchemy query and persistence operations
- transaction commit/refresh for entity mutations

Repo layer does not own business decisions.

## Example

```python
def list_users(self, offset: int, limit: int) -> tuple[list[User], int]:
    items = self.db.execute(select(User).offset(offset).limit(limit)).scalars().all()
    total = self.db.execute(select(func.count()).select_from(User)).scalar_one()
    return items, total
```

## DO

- Keep methods query-focused and deterministic.
- Return typed ORM/domain objects.

## DON'T

- Raise HTTPException from repo.
- Validate business policy in repo (`if user is premium`).
- Import other module repos.

## Common Mistakes

- Putting pagination parameter validation in repo.
- Returning mixed return types (`dict` in one method, ORM in another).

## When to Break the Rule

Never for business policy. Keep repo pure persistence.
