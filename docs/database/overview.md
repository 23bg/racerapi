# Database Overview

RacerAPI uses SQLAlchemy 2.x for ORM and a lightweight session factory in `src/racerapi/db/session.py`.

Key points:
- The framework provides a lazy engine/session factory that is overridable in tests via `set_engine`.
- Models are defined per-module in `modules/<name>/models.py` and the framework uses a models registry to import them for deterministic metadata during Alembic autogenerate.

See `src/racerapi/db/models_registry.py` for the import logic used by Alembic.
