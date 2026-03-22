# Adding a New Module

## Step-by-Step

1. Create folder: `src/racerapi/modules/<module_name>/`
2. Add required files: `api.py`, `service.py`, `repo.py`, `schemas.py`, `models.py`, `deps.py`
3. Add model to SQLAlchemy metadata import path.
4. Implement DI providers in `deps.py`.
5. Register router in `src/racerapi/app/__init__.py`.
6. Add tests: service unit, repo integration, API tests.

## Full Example Skeleton

```python
# modules/orders/deps.py

def get_order_repo(db: Session = Depends(get_db)) -> OrderRepo:
    return OrderRepo(db)


def get_order_service(repo: OrderRepo = Depends(get_order_repo)) -> OrderService:
    return OrderService(repo)
```

```python
# modules/orders/api.py
router = APIRouter(prefix="/orders", tags=["orders"])

@router.get("/{order_id}", response_model=OrderRead)
def get_order(order_id: int, service: OrderService = Depends(get_order_service)):
    return OrderRead.model_validate(service.get_order(order_id))
```

```python
# app/__init__.py
from racerapi.modules.orders.api import router as orders_router
app.include_router(orders_router)
```

## DO

- Start from a small read endpoint.
- Add service business checks before write endpoints.
- Keep module self-contained.

## DON'T

- Reuse another module's repo to move faster.
- Add endpoints before schemas are stable.

## Common Mistakes

- Forgetting to include router in app factory.
- Missing dependency provider chain.
- Putting business branching in route handlers.

## When to Break the Rule

During emergency fixes you may implement a minimal read endpoint first, but follow with full layer separation in the same PR cycle.
