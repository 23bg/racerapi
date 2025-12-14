from pathlib import Path
import typer
from jinja2 import Environment, FileSystemLoader

BASE_DIR = Path(__file__).parent.parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"


def to_pascal_case(name: str) -> str:
    return "".join(part.capitalize() for part in name.split("_"))


def generate_base(kind: str, name: str):
    kind = kind.lower()
    name = name.lower()

    template_dir = TEMPLATES_DIR / kind
    if not template_dir.exists():
        typer.echo(f"❌ Unknown generator type: {kind}")
        raise typer.Exit(1)

    module_path = Path("app/modules") / name
    if module_path.exists() and kind == "resource":
        typer.echo(f"❌ Module '{name}' already exists.")
        raise typer.Exit(1)

    typer.echo(f"Generating {kind} '{name}'...")

    env = Environment(
        loader=FileSystemLoader(str(template_dir)),
        autoescape=False,
    )

    context = {
        "class_name": to_pascal_case(name),
        "module_name": name,
    }

    for template_path in template_dir.rglob("*.jinja"):
        relative_path = template_path.relative_to(template_dir)

        if kind == "resource":
            target_base = module_path
        else:
            target_base = module_path

        target_path = target_base / relative_path.with_suffix("")
        target_path.parent.mkdir(parents=True, exist_ok=True)

        template = env.get_template(relative_path.as_posix())
        content = template.render(**context)

        if "{{" in content or "}}" in content:
            raise RuntimeError(f"Unrendered template variables in {relative_path}")

        target_path.write_text(content, encoding="utf-8")

    typer.echo(f"✅ {kind.capitalize()} generated successfully")
