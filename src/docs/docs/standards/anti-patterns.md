# Anti-Patterns

## 1) Business Logic in Routes

Bad:

```python
@router.post("")
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    if db.execute(...):
        raise HTTPException(409, "duplicate")
```

Why dangerous:
- duplicates service behavior
- hard to unit test
- spreads business policy across transport layer

## 2) Cross-Module Imports

Bad:

```python
from racerapi.modules.auth.service import AuthService
```

Why dangerous:
- hidden coupling
- extraction cost multiplies

## 3) Global State

Bad:

```python
CURRENT_USER_CACHE = {}
```

Why dangerous:
- request leakage
- concurrency bugs
- non-deterministic tests

## 4) Fake Service Layer

Bad:

```python
def create_user(self, payload):
    return self.repo.create(payload)
```

Why dangerous:
- layer exists without value
- business rules leak upward or downward

## 5) Over-Engineering

Bad signs:
- custom DI container
- custom routing DSL
- custom lifecycle engine

Why dangerous:
- framework drift
- onboarding friction
- stale abstractions

## DO

- Keep architecture explicit and boring.
- Delete abstractions that do not reduce real complexity.

## DON'T

- Introduce “future-proofing” patterns with no current need.

## When to Break the Rule

Never for global state and cross-module imports. Those are hard stops.
