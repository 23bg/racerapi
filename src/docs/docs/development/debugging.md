# Debugging Guide

## Debugging Order

1. Reproduce with failing test.
2. Confirm layer where behavior diverges.
3. Fix in correct layer only.
4. Add regression test.

## Layer-Oriented Triage

- Wrong status code or response shape -> API layer
- Wrong business decision -> Service layer
- Wrong data returned/written -> Repo layer
- Session/config issues -> Core/DB layer

## Example Workflow

```bash
pytest tests/test_users_service.py -q
pytest tests/test_users_api.py -q
```

## DO

- Start debugging from failing behavior, not assumptions.
- Keep breakpoints near boundary transitions.

## DON'T

- Patch symptom in API if root cause is service/repo.
- Add broad try/except to silence failures.

## Common Mistakes

- Fixing test to match bug.
- Introducing cross-module import during emergency patch.

## When to Break the Rule

Temporary hotfixes are allowed only with follow-up ticket and regression test in same change set.
