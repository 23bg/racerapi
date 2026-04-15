# Enforcement and CI

The repository includes an AST-based architecture checker at `scripts/check_architecture.py`.

Run locally with report output:

```bash
python scripts/check_architecture.py --report
```

In CI this script should run and fail the build when rules are violated. Example usage in a CI step:

```bash
python scripts/check_architecture.py || (echo "Architecture violations detected" && exit 1)
```

The checker inspects `import from` statements and enforces the rules documented in [Architecture → Rules](rules.md). A small allowlist is included for framework internals.
