import os
from pathlib import Path

import typer

from racerapi.cli.context import CLIContext
from racerapi.db.base_driver import BaseDriver


class MongoDriver(BaseDriver):
    def __init__(self, context: CLIContext) -> None:
        super().__init__(context)
        self.uri = os.environ.get("RACERAPI_DATABASE_URL", "mongodb://localhost:27017/racerapi")

    def _get_client(self):
        try:
            from pymongo import MongoClient

            return MongoClient(self.uri, serverSelectionTimeoutMS=2000)
        except ImportError as exc:
            raise typer.Exit("pymongo is required for mongo driver support. Install it and retry.") from exc

    def _database_name(self) -> str:
        parsed = self.uri.rsplit("/", 1)
        return parsed[-1] if len(parsed) > 1 else "racerapi"

    def init(self) -> None:
        typer.echo("Initializing MongoDB connection")
        if self.context.dry_run:
            typer.echo(f"[dry-run] would ping {self.uri}")
            return
        client = self._get_client()
        client.admin.command("ping")
        typer.echo("MongoDB connection is healthy")

    def migrate(self) -> None:
        typer.echo("MongoDB does not use SQL-style migrations. Use seed or reset instead.")

    def upgrade(self) -> None:
        typer.echo("MongoDB does not support upgrade operations in this CLI.")

    def reset(self) -> None:
        typer.echo("Resetting MongoDB database")
        if self.context.dry_run:
            typer.echo(f"[dry-run] would drop database {self._database_name()}")
            return
        client = self._get_client()
        client.drop_database(self._database_name())
        typer.echo("MongoDB database dropped")

    def seed(self) -> None:
        seed_path = Path.cwd() / "seed.py"
        if not seed_path.exists():
            typer.echo("No seed.py found in the current project root.")
            return
        client = self._get_client()
        from racerapi.cli.utils import run_seed

        run_seed(seed_path, client, self.context)

    def check_connection(self) -> None:
        if self.context.dry_run:
            typer.echo("[dry-run] checking mongo connection")
            return
        client = self._get_client()
        client.admin.command("ping")
