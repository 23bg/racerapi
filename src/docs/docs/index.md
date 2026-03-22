# RacerAPI Engineering Handbook

This documentation is the architecture contract for this backend.

If you follow this handbook, you get:

- predictable code paths
- testable business logic
- safe module isolation
- low-risk onboarding for new engineers

If you ignore this handbook, you will produce hidden coupling, flaky tests, and expensive refactors.

## System Summary

- Runtime: FastAPI
- Architecture: modular monolith
- Layers: API -> Service -> Repo -> DB
- DI mechanism: FastAPI Depends only
- State model: no global mutable state
- Boundary model: no cross-module imports

## Non-Negotiable Rules

- API layer does validation and transport only.
- Service layer owns business rules and orchestration.
- Repo layer does persistence only.
- A module may import itself and core/shared only.
- No module imports another module directly.

## Read This In Order

1. Architecture overview
2. Request flow
3. Dependency injection
4. Module boundaries
5. Add new module guide
6. Coding rules and review checklist
