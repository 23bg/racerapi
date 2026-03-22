# Coding Rules

## Naming Conventions

- Module folders: plural nouns (`users`, `orders`)
- Files: fixed layer names (`api.py`, `service.py`, `repo.py`, `schemas.py`, `models.py`, `deps.py`)
- Service methods: business-intent verbs (`create_user`, `deactivate_user`)
- Repo methods: data operation names (`get_by_id`, `list_users`, `update`)

## File Structure Rules

- Keep one domain per module folder.
- Keep API handlers short and deterministic.
- Keep schema and ORM model separated.

## Functions vs Classes

- Use classes where stateful dependency is meaningful (`UserService`, `UserRepo`).
- Use functions for providers and simple utilities.

## Error Handling Rules

- Raise domain exceptions in service layer.
- Map to HTTP once in app-level handlers.

## DO

- Write explicit type hints on public methods.
- Keep return types stable.
- Make side effects obvious.

## DON'T

- Hide behavior in magic decorators.
- Add custom framework layers around FastAPI.

## Common Mistakes

- Utility sprawl in `shared` with domain behavior.
- Endpoint-specific one-off patterns that bypass conventions.

## When to Break the Rule

A narrow exception is acceptable if it removes complexity and is documented in PR with trade-off rationale.
