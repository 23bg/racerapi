# Module Boundaries

## Boundary Rules

Allowed:
- module -> itself
- module -> core
- module -> shared

Forbidden:
- module -> another module

## Enforcement Intent

This rule exists to keep domains independently maintainable and future-extractable.

## Consequences of Violation

- Hidden business coupling
- Circular design pressure
- Refactor blast radius grows
- Teams block each other on unrelated changes

## Practical Example

Good:

```python
from racerapi.modules.users.repo import UserRepo
from racerapi.core.exceptions import NotFoundError
```

Bad:

```python
from racerapi.modules.health.service import HealthService
```

## DO

- Duplicate tiny logic if it avoids domain coupling.
- Move generic, domain-neutral helpers to `shared`.
- Move cross-cutting policy to `core`.

## DON'T

- Centralize domain behavior in shared for convenience.
- Read another module's tables/repo directly.

## Common Mistakes

- Importing another module's schemas because they “already exist”.
- Reusing another module's repo query method.
- Building orchestration logic in API layer to stitch two modules.

## When to Break the Rule

Only during planned strangler migrations with:
- explicit temporary adapter,
- defined end date,
- tests proving no functional drift.
