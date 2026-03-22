# PR Review Checklist

Use this checklist in every backend PR.

## Architecture

- [ ] Route logic stays in API layer only
- [ ] Business rules are in service layer
- [ ] Repo contains only DB operations
- [ ] No cross-module imports
- [ ] DI uses `Depends` providers, no manual wiring in routes

## Code Quality

- [ ] New endpoints have request and response schemas
- [ ] Exceptions are domain exceptions in service layer
- [ ] API status code mapping is correct
- [ ] No global mutable state introduced

## Testing

- [ ] Service unit tests added/updated
- [ ] Repo integration tests added/updated
- [ ] API tests added/updated
- [ ] Regression test exists for bug fixes

## Operational Readiness

- [ ] Config changes documented
- [ ] Migration impact documented
- [ ] Backward compatibility considered

## Common Reviewer Misses

- Verifying endpoint works but missing service-level invariant checks.
- Accepting cross-module imports hidden in helper files.
- Ignoring response schema drift.

## When to Approve Exceptions

Only with explicit rationale, owner, and cleanup deadline in PR description.
