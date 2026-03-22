# Modular Monolith Contract

## Module Isolation Model

A module is a business capability with internal files:
- `api.py`
- `service.py`
- `repo.py`
- `schemas.py`
- `models.py`
- `deps.py`

Each module owns its own behavior and data access rules.

## Allowed Imports

- module -> itself
- module -> `racerapi.core.*`
- module -> `racerapi.shared.*`

## Forbidden Imports

- module -> another module (for example `users -> auth`)

## Example Layout

```text
src/racerapi/modules/
  users/
  health/
```

## Example of Correct Internal Use

```python
# users/service.py
from racerapi.modules.users.repo import UserRepo
```

## Example of Forbidden Coupling

```python
# forbidden: users/service.py
from racerapi.modules.health.service import HealthService
```

## Why This Matters

Direct cross-module imports create hidden dependency graphs that eventually block independent extraction and safe refactoring.

## DO

- Communicate across modules via API boundaries or explicit shared abstractions in `core`/`shared`.
- Keep module-local invariants inside service layer.

## DON'T

- Import another module because “it is easy right now”.
- Put domain logic in shared helpers.

## Common Mistakes

- Building a "shared business utils" file that contains domain behavior.
- Copying repo queries between modules instead of creating module-owned queries.

## When to Break the Rule

Only for controlled migrations where temporary adapters exist with:
- TODO + owner + removal date,
- test coverage proving behavior,
- architecture review approval.
