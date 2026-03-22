# Module Structure

## Required Files Per Module

Each domain module must contain:
- `api.py`
- `service.py`
- `repo.py`
- `schemas.py`
- `models.py`
- `deps.py`

## Why This Structure

It forces explicit ownership:
- transport in API
- rules in service
- persistence in repo

## Example

```text
src/racerapi/modules/users/
  api.py
  service.py
  repo.py
  schemas.py
  models.py
  deps.py
```

## DO

- Keep module files cohesive and small.
- Keep module tests close to behavior intent.

## DON'T

- Put shared app config inside module folders.
- Add extra abstraction folders without clear value.

## Common Mistakes

- Creating `managers`, `handlers`, and `processors` with overlapping responsibility.
- Using module `__init__.py` for runtime logic.

## When to Break the Rule

Add subpackages only when module complexity requires it, for example separate query/read model folders. Keep layer ownership unchanged.
