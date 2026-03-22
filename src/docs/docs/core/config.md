# Core Configuration

## Current Model

Configuration is centralized in `src/racerapi/core/config.py` through `pydantic-settings`.

```python
class Settings(BaseSettings):
    app_name: str = "RacerAPI"
    debug: bool = False
    database_url: str = "sqlite:///./racerapi.db"
```

## DO

- Add new settings fields in one place.
- Use environment variable prefix for all runtime config.
- Keep defaults safe for local dev only.

## DON'T

- Scatter config reads across modules.
- Read environment variables directly from business code.

## Common Mistakes

- Adding module-specific constants in service code instead of config.
- Introducing mutable global config objects.

## When to Break the Rule

Never in production paths. Test-only overrides are acceptable via fixtures.
