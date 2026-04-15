# CLI Overview

The CLI is implemented as a modular collection of commands under `src/racerapi/cli` and exposed via a stable console script `racerapi` defined in `pyproject.toml`.

Structure:

- `src/racerapi/console.py` — Click-based entrypoint used as the installed console script.
- `src/racerapi/cli/` — Typer-based command modules: `commands/generate.py`, `commands/db.py`, `commands/new.py`, `commands/run.py`.

Design goals:
- Each command is testable in isolation
- CLI logic avoids global state and uses explicit parameters
- Generators use file-based templates stored under `src/racerapi/templates/module`
