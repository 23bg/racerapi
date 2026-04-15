# Dependency Injection Patterns

RacerAPI uses FastAPI's `Depends` to express dependencies between layers. The framework provides a `get_db` dependency and generators create `get_<singular>_service` helpers for module services.

Example: `deps.py` generated for a module provides:

```python
from fastapi import Depends
from racerapi.core.deps import get_db

def get_user_repo(db=Depends(get_db)):
    return UserRepo(db)

def get_user_service(repo=Depends(get_user_repo)):
    return UserService(repo)
```

Testing: injection points are intentionally small and easy to override in tests via `app.dependency_overrides` (see [Testing → Fixtures](../testing/fixtures.md)).
