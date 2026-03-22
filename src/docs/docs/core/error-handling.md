# Error Handling

## Strategy

- Services raise domain exceptions (`NotFoundError`, `ConflictError`, `ValidationError`).
- App-level exception handlers map domain exceptions to HTTP responses.

## Example

```python
@app.exception_handler(NotFoundError)
async def not_found_handler(_: Request, exc: NotFoundError):
    return JSONResponse(status_code=404, content={"detail": str(exc)})
```

## DO

- Raise domain-specific exceptions from service layer.
- Keep HTTP status mapping centralized in app composition.

## DON'T

- Raise HTTPException in repo.
- Return error dicts with 200 status.

## Common Mistakes

- Catching broad exceptions and hiding root cause.
- Duplicating exception-to-status mapping in every endpoint.

## When to Break the Rule

For external SDK failures, you may map to domain exceptions at service boundary before re-raising.
