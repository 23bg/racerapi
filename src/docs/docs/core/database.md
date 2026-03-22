# Database

## Current Setup

- SQLAlchemy engine/session in `src/racerapi/db/session.py`
- Declarative base in `src/racerapi/db/base.py`
- Tables created on app startup lifespan

## Example

```python
engine = create_engine(settings.database_url, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, class_=Session)
```

## DO

- Access DB through repo layer only.
- Keep one session lifecycle ownership path (`get_db`).
- Use migrations for schema evolution in real environments.

## DON'T

- Open new sessions manually in services/routes.
- Share session globals across requests.

## Common Mistakes

- Committing inside loops in service code.
- Creating engine in module-level code outside DB core package.

## When to Break the Rule

One-off scripts may construct sessions directly, but never in request handlers.
