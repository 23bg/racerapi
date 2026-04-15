# Testing Overview

RacerAPI encourages isolated tests with a fresh database per test and clear dependency overrides. Tests are deterministic and run without requiring a live external database.

Run tests:

```bash
pytest -q
```

High level guarantees:
- The test fixtures create a temporary engine or in-memory SQLite per test.
- `app.dependency_overrides` is used to inject the test session into routes.
- TestClient instances are created inside fixtures so application lifespan events run correctly.
