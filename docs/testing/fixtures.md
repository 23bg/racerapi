# Fixtures and DB Overrides

Key fixtures used in this project (see `tests/conftest.py` and `src/conftest.py`):

- `db_engine` / `db_session` — create an engine and session per test and ensure schema is created/dropped for the engine.
- `client` — TestClient created inside the fixture; the fixture overrides `get_db` dependency to yield the test session.

Example test using the `client` fixture:

```python
def test_get_users_empty(client):
    r = client.get("/users")
    assert r.status_code == 200
    assert isinstance(r.json(), dict)
    assert "items" in r.json()
```

Override pattern

```python
from racerapi.core.deps import get_db as _get_db

def override_get_db():
    yield test_session

app.dependency_overrides[_get_db] = override_get_db
```

This pattern ensures that the application code uses the test session from the fixture and that tests remain isolated and repeatable.
