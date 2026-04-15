# Architecture Rules

RacerAPI enforces the following strict layering rules to keep modules decoupled and testable:

1. API → Service → Repo → DB
   - The API layer may depend on the Service layer only.
   - The Service layer may depend on Repo and other domain services.
   - The Repo layer is the only layer permitted to import persistence internals (SQLAlchemy).

2. No cross-module implementation imports
   - Modules must not import other modules' implementation files (for example one module's `repo.py` should not be imported by another module's `api.py`).

3. Framework allowlist
   - Framework internals such as the module registry and shared utils are exempted from cross-module rules.

These rules are enforced by `scripts/check_architecture.py` (see Enforcement documentation).
