# Getting Started

This guide walks a new developer through creating a demo app, generating a module, running migrations, and launching the server. It uses the real CLI shipped with the project.

1. Install the package in editable/development mode

```bash
python -m pip install -e .
```

2. Verify the CLI is available

```bash
racerapi --help
```

3. Create a new demo project and generate a `users` module

```bash
racerapi new demo_app
cd demo_app
racerapi generate module users
```

Notes:
- The generator writes code into `src/<pkg>/modules/<name>` and validates the module is importable after generation.
- The generated module follows the framework contract: `api.py`, `service.py`, `repo.py`, `models.py`, `schemas.py`, `deps.py`.

4. Prepare the database and run migrations

By design, the application does not create or modify schema at startup. Use the CLI's Alembic wrapper to create migrations and apply them:

```bash
racerapi db migrate
racerapi db upgrade
```

If you see `Initializing alembic environment` during the first run, that's expected — the CLI will scaffold a minimal Alembic environment in your project directory.

5. Run the application

```bash
racerapi run
# or to bind to a different host/port:
racerapi run --host 0.0.0.0 --port 8080
```

6. Try the generated endpoint

```bash
curl -sS http://127.0.0.1:8000/users | jq
```

Why this matters
- The `new` and `generate` commands create code that is valid and importable — you should not need to edit generated files to get a working endpoint.
- Migrations are authoritative: you must run `db migrate` / `db upgrade` for schema changes.
