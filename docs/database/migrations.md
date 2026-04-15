# Migrations

RacerAPI integrates Alembic via a thin CLI wrapper. The wrapper will initialize a minimal Alembic environment in your project root when needed.

Typical workflow:

1. Generate an autogenerate revision:

```bash
racerapi db migrate -m "add users table"
```

2. Review the generated migration file in `alembic/versions/` and edit as appropriate.

3. Apply the migration:

```bash
racerapi db upgrade
```

Implementation notes
- The Alembic `env.py` used by the CLI imports `racerapi.db.models_registry` to ensure `Base.metadata` contains all models before autogenerate runs. This eliminates fragile import-order bugs.
- The framework intentionally avoids `Base.metadata.create_all()` at app startup — migrations are the source of truth for schema changes.
