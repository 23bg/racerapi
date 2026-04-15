from __future__ import annotations

import typer

app = typer.Typer()
generate_app = typer.Typer()
app.add_typer(generate_app, name="generate")

# Command implementations live in racerapi.cli.commands and are imported
# lazily by the package __init__.py to keep a small surface here.
