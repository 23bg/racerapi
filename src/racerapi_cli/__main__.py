from pathlib import Path
import subprocess
import typer

app = typer.Typer(help="RacerAPI CLI - FastAPI project generator")

BASE_DIR = Path(__file__).parent
TEMPLATES_DIR = BASE_DIR / "templates"
PROJECT_TEMPLATE_DIR = TEMPLATES_DIR / "project"
RESOURCE_TEMPLATE_DIR = TEMPLATES_DIR / "resource"


def copy_tree(src: Path, dest: Path, context: dict):
    for path in src.rglob("*"):
        rel = path.relative_to(src)
        target = dest / rel

        if path.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            continue

        content = path.read_text(encoding="utf-8")
        for key, value in context.items():
            content = content.replace(f"{{{{ {key} }}}}", value)

        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")


@app.command()
def new(name: str):
    project_root = Path(name)

    if project_root.exists():
        typer.echo(f"Directory '{name}' already exists.")
        raise typer.Exit(1)

    if not PROJECT_TEMPLATE_DIR.exists():
        typer.echo(
            f"[ERROR] Project template directory not found: {PROJECT_TEMPLATE_DIR}"
        )
        raise typer.Exit(1)

    typer.echo(f"Creating RacerAPI project in '{name}'...")
    copy_tree(
        PROJECT_TEMPLATE_DIR,
        project_root,
        {
            "project_name": name,
            "project_slug": name.replace("-", "_"),
        },
    )
    typer.echo("✅ RacerAPI project created")
    typer.echo(f"👉 cd {name}")
    typer.echo("👉 RacerAPI dev")


@app.command()
def generate(kind: str, name: str):
    kind = kind.lower()
    name = name.lower()

    if kind != "resource":
        typer.echo("Only 'resource' generator is supported for now.")
        raise typer.Exit(1)

    if not RESOURCE_TEMPLATE_DIR.exists():
        typer.echo(
            f"[ERROR] Resource template directory not found: {RESOURCE_TEMPLATE_DIR}"
        )
        raise typer.Exit(1)

    module_path = Path("app/modules") / name

    if module_path.exists():
        typer.echo(f"Module '{name}' already exists.")
        raise typer.Exit(1)

    typer.echo(f"Generating resource '{name}'...")
    copy_tree(
        RESOURCE_TEMPLATE_DIR,
        module_path,
        {
            "resource_name": name,
            "class_name": name.capitalize(),
        },
    )
    typer.echo("✅ Resource generated")


@app.command()
def dev():
    subprocess.run(["uvicorn", "main:app", "--reload"])


def main():
    app()


if __name__ == "__main__":
    main()
