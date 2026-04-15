import click

from racerapi import cli as _cli


@click.group()
def main():
    """RacerAPI CLI (stable console script wrapper)."""


@main.command()
@click.argument("project_name")
@click.option("--path", default=None)
def new(project_name, path):
    _cli.new(project_name, path)


@main.command()
@click.option("--host", default="127.0.0.1")
@click.option("--port", default=8000)
@click.option("--reload", is_flag=True)
def run(host, port, reload):
    _cli.run(host=host, port=port, reload=reload)


@click.group(name="generate")
def generate():
    """Generate scaffolding (module/resource/service/repo)."""


@generate.command("module")
@click.argument("name")
@click.option("--path", default=None)
def gen_module(name, path):
    _cli.generate_module(name, path)


@generate.command("resource")
@click.argument("name")
@click.option("--path", default=None)
def gen_resource(name, path):
    _cli.generate_resource(name, path)


@generate.command("service")
@click.argument("name")
@click.option("--path", default=None)
def gen_service(name, path):
    _cli.generate_service(name, path)


@generate.command("repo")
@click.argument("name")
@click.option("--path", default=None)
def gen_repo(name, path):
    _cli.generate_repo(name, path)


main.add_command(generate)


@main.group(name="db")
def db():
    """Database migrations using Alembic."""


@db.command("init")
def db_init():
    _cli.db("init")


@db.command("migrate")
def db_migrate():
    _cli.db("migrate")


@db.command("upgrade")
def db_upgrade():
    _cli.db("upgrade")


if __name__ == "__main__":
    main()
