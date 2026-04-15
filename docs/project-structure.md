# Project structure

This section explains the on-disk layout of the framework and where to look for the core subsystems.

- `src/racerapi/` — framework package
  - `app/` — application factory & FastAPI wiring
  - `cli/` — modular CLI implementation and commands
  - `modules/` — built-in modules shipped with the framework
  - `db/` — SQLAlchemy base, session management, and model registry
  - `core/` — logging, config, deps, and shared utilities

Key files to inspect (examples):

- `src/racerapi/app/__init__.py` — application factory and middleware (request_id)
- `src/racerapi/cli/__init__.py` — CLI package (Typer wrappers)
- `src/racerapi/modules/registry.py` — module discovery and router registration
- `src/racerapi/db/models_registry.py` — imports models for deterministic Alembic autogenerate

When browsing code, prefer to read `create_app()` in [src/racerapi/app/__init__.py](src/racerapi/app/__init__.py) as the single entrypoint for request lifecycle and router registration.
