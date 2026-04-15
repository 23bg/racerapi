# CLI Commands

This section documents the primary CLI commands and examples.

`racerapi new <project_name>`

Creates a minimal scaffold for a new project. Example:

```bash
racerapi new demo_app
```

`racerapi generate module <name>`

Generate a new module skeleton (api, service, repo, models, schemas, deps).

```bash
racerapi generate module users
```

`racerapi generate resource|service|repo <name>`

Generate only the requested sub-piece if you want to add a service or repo to an existing module.

`racerapi db migrate`

Autogenerate a migration revision based on model metadata (Alembic autogenerate). The CLI will scaffold a minimal Alembic environment in the current working directory if one does not exist.

`racerapi db upgrade`

Apply unapplied migrations (equivalent to `alembic upgrade head`).

`racerapi run [--host] [--port] [--reload]`

Launch the application using uvicorn. When run from inside a generated project (cwd/src/<pkg>/main.py), the CLI uses the project's `main:app` instead of the framework's own app.
