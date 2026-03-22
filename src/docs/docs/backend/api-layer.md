# API Layer Contract

## Responsibilities

API layer owns:
- request/response schema validation
- HTTP status mapping
- dependency resolution via `Depends`

API layer must not own business decisions.

## Example

```python
@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, service: UserService = Depends(get_user_service)):
    user = service.get_user(user_id)
    return UserRead.model_validate(user)
```

## DO

- Keep handlers thin.
- Convert domain result to API schema.
- Use explicit status codes on write endpoints.

## DON'T

- Execute SQLAlchemy in route handlers.
- Embed business branching (`if role == ...`) in handlers.
- Build ad-hoc JSON response contracts per route.

## Common Mistakes

- Catching all exceptions in route and returning 200 with error body.
- Returning ORM objects directly.

## When to Break the Rule

Never for business endpoints. For very simple liveness checks, route can call a minimal service wrapper.
