# RacerAPI

Production-grade FastAPI modular monolith baseline.

## Architecture

- FastAPI (no framework wrapping)
- Domain modules in `src/racerapi/modules`
- Layering: API -> Service -> Repo -> DB
- FastAPI `Depends` for DI
- No cross-module imports

## Quick Start

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e .
```

Run the application:

```bash
python -m racerapi.main
```

Health check:

```bash
curl http://127.0.0.1:8000/health
```

## Release Validation Commands

```bash
python -m pytest -q
python -m ruff check src tests
python scripts/check_architecture.py
```

## Environment

Copy `.env.example` to `.env` and adjust values for your environment.

Key variables:

- `RACERAPI_ENV=dev|test|prod`
- `RACERAPI_DATABASE_URL=...`
- `RACERAPI_LOG_LEVEL=INFO`
- `RACERAPI_DEBUG=false`

