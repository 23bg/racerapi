# Running the Backend

## Start Server

```bash
python -m racerapi.main
```

or

```bash
uvicorn racerapi.main:app --reload
```

## Validate Endpoints

```bash
curl http://127.0.0.1:8000/health
curl "http://127.0.0.1:8000/users?page=1&page_size=10"
```

## DO

- Use `--reload` for local iteration only.
- Verify docs and health endpoint after startup.

## DON'T

- Run production with reload mode.
- Treat startup table creation as replacement for migrations in prod.

## Common Mistakes

- Using wrong import path (`app.main` instead of `racerapi.main`).
- Assuming DB is initialized without startup lifespan execution.

## When to Break the Rule

For smoke tests, running module directly is acceptable if command environment is controlled.
