# Module System

Each module is an independently testable unit that follows a small contract. The registry discovers modules and imports their `api` modules which register routers with the application.

Module layout

```
modules/<name>/
  api.py      # APIRouter and endpoints
  service.py  # business logic
  repo.py     # persistence
  models.py   # SQLAlchemy models
  schemas.py  # Pydantic DTOs
  deps.py     # DI helpers (get_<singular>_service)
```

The generator templates live in `src/racerapi/templates/module` and the generator validates the module is importable after creating files.

See the registry implementation at [src/racerapi/modules/registry.py](src/racerapi/modules/registry.py).
