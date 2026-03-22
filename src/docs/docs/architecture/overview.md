# Architecture Overview

## What We Built

RacerAPI is a FastAPI modular monolith optimized for team scale before infrastructure scale.

Key decisions:
- One deployable unit, many isolated domain modules.
- Strict layer boundaries: API -> Service -> Repo -> DB.
- FastAPI `Depends` as the only dependency wiring mechanism.

## Why Modular Monolith

We chose a modular monolith because current complexity is domain complexity, not distributed-systems complexity.

What this gives us now:
- single-process local debugging
- no network calls between business domains
- lower cognitive load for new developers
- simpler transactions and consistency

## Why Not Microservices Yet

Microservices add operational cost immediately:
- service discovery
- distributed tracing
- retry/idempotency policy everywhere
- per-service CI/CD and ownership overhead

Until module boundaries are stable and scaling pain is proven, microservices are architecture tax.

## Why Not Engine-Based Architecture

The old engine/pipeline approach hid business flow behind framework-like orchestration.

Problems it caused:
- stale APIs and dead abstractions
- unclear ownership of business rules
- difficult onboarding because control flow was implicit

Current approach makes flow explicit in code everyone can read.

## Example: Explicit Flow in Code

```python
# src/racerapi/modules/users/api.py
@router.post("", response_model=UserRead)
def create_user(payload: UserCreate, service: UserService = Depends(get_user_service)):
    user = service.create_user(payload)
    return UserRead.model_validate(user)
```

## DO

- Keep architecture boring and explicit.
- Make business flow visible from route to service to repo.
- Keep each module independently testable.

## DON'T

- Add new framework layers (custom containers, decorators, lifecycle engines).
- Introduce cross-module direct calls.
- Hide logic in implicit middleware chains.

## Common Mistakes

- Treating modular monolith as a temporary toy and skipping boundaries.
- Creating “utility” modules that become cross-domain backdoors.
- Writing services that only pass through to repos with no business logic.

## When to Break the Rule

Break “single deployable unit” only when all are true:
- one module has independent scaling profile for months,
- module contracts are stable,
- team ownership and SLO boundaries are already clear.
