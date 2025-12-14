# from pathlib import Path
# import typer
# from jinja2 import Environment, FileSystemLoader

# BASE_DIR = Path(__file__).parent.parent.parent
# TEMPLATES_DIR = BASE_DIR / "templates"
# RESOURCE_TEMPLATE_DIR = TEMPLATES_DIR / "resource"


# def to_pascal_case(name: str) -> str:
#     return "".join(part.capitalize() for part in name.split("_"))


# def generate_resource(kind: str, name: str):
#     kind = kind.lower()
#     name = name.lower()

#     if kind != "resource":
#         typer.echo("Only 'resource' generator is supported for now.")
#         raise typer.Exit(1)

#     module_path = Path("app/modules") / name
#     if module_path.exists():
#         typer.echo(f"Module '{name}' already exists.")
#         raise typer.Exit(1)

#     typer.echo(f"Generating resource '{name}'...")

#     env = Environment(
#         loader=FileSystemLoader(str(RESOURCE_TEMPLATE_DIR)),
#         autoescape=False,
#     )

#     context = {
#         "class_name": to_pascal_case(name),
#     }

#     for template_path in RESOURCE_TEMPLATE_DIR.rglob("*.jinja"):
#         relative_path = template_path.relative_to(RESOURCE_TEMPLATE_DIR)

#         target_path = module_path / relative_path.with_suffix("")
#         target_path.parent.mkdir(parents=True, exist_ok=True)

#         template = env.get_template(relative_path.as_posix())
#         content = template.render(**context)

#         # SAFETY CHECK
#         if "{{" in content or "}}" in content:
#             raise RuntimeError(f"Unrendered template variables in {relative_path}")

#         target_path.write_text(content, encoding="utf-8")

#     typer.echo("✅ Resource generated successfully")
