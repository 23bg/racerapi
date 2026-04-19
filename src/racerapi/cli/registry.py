import typer
from typer import Typer

from racerapi.cli.commands import project, runtime
from racerapi.cli.commands.db import db_app
from racerapi.cli.commands.generate import generate_app


def register_commands(app: Typer, generate_app: Typer, db_app: Typer) -> None:
    app.command("new")(project.new)
    app.command("dev")(project.dev)
    app.command("start")(project.start)
    app.command("shell")(project.shell)
    app.command("routes")(runtime.routes)
    app.command("doctor")(runtime.doctor)
    app.command("version")(runtime.version)

    app.add_typer(generate_app, name="generate")
    app.add_typer(db_app, name="db")
    # Convenience alias: `racerapi gen <module>` -> `racerapi generate module <module>`
    from racerapi.cli.commands.generate import generate_module


    def _gen(name: str, ctx: typer.Context) -> None:
        """Alias command to quickly generate a module by name."""
        return generate_module(name, ctx)


    app.command("gen")(_gen)
