# Development Setup

## Prerequisites

- Python 3.10+
- virtual environment
- editable install

## Setup Commands

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .
pip install -e .[dev]
```

## DO

- Use isolated virtual env per clone.
- Keep dependencies pinned through project metadata.

## DON'T

- Install random global packages and assume project works for others.
- Skip `-e` install when developing package code.

## Common Mistakes

- Running tests without editable install and getting import errors.
- Mixing multiple Python interpreters in one shell.

## When to Break the Rule

Containerized CI can install non-editable wheels; local dev should stay editable.
