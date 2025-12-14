import typer
from racerapi.cmd.generate.base import generate_base

app = typer.Typer()


@app.command()
def resource(name: str):
    generate_base("resource", name)


@app.command()
def controller(name: str):
    generate_base("controller", name)


@app.command()
def service(name: str):
    generate_base("service", name)


@app.command()
def job(name: str):
    generate_base("job", name)


@app.command()
def event(name: str):
    generate_base("event", name)


@app.command()
def consumer(name: str):
    generate_base("consumer", name)
