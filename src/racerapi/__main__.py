import typer

from racerapi.cmd.new_cmd import new_cmd
from racerapi.cmd.dev_cmd import dev_cmd
from racerapi.cmd.generate.base import generate_base
from racerapi.cmd.doctor_cmd import doctor_cmd
from racerapi.cmd.routes_cmd import routes_cmd
from racerapi.cmd.config.config_cmd import config_cmd
from racerapi.cmd.env_cmd import env_cmd
from racerapi.cmd.eval_cmd import eval_cmd
from racerapi.cmd.trace_cmd import trace_cmd
from racerapi.cmd.test_cmd import test_cmd
from racerapi.cmd.version_cmd import version_cmd
from racerapi.cmd.format_cmd import format_cmd


app = typer.Typer(
    help="RacerAPI CLI – AI-first Enterprise Backend Framework",
    add_completion=True,
    no_args_is_help=True,
)

# -------------------------------------------------------------------
# CORE v1 COMMANDS (STABLE – SEMVER GUARANTEED)
# -------------------------------------------------------------------


@app.command()
def new(
    name: str = typer.Argument(..., help="Project name"),
):
    """
    Create a new RacerAPI project.

    This command scaffolds a production-ready backend with:
    - Modular architecture
    - Clean service/controller separation
    - Optional AI-first structure

    Example:
      racerapi new myapp
    """
    new_cmd(name=name)


@app.command()
def dev():
    """
    Start the development server with hot reload.

    - Loads environment variables
    - Discovers modules automatically
    - Enables FastAPI reload mode

    Example:
      racerapi dev
    """
    dev_cmd()


@app.command()
def generate(
    kind: str = typer.Argument(..., help="Resource type (module, ai-module)"),
    name: str = typer.Argument(..., help="Resource name"),
):
    """
    Generate framework resources.

    Supported kinds:
      - module     : Standard feature module
      - ai-module  : AI-enabled feature module

    Example:
      racerapi generate module users
      racerapi generate ai-module chat
    """
    generate_base(kind=kind, name=name)


@app.command()
def doctor():
    """
    Validate project structure and runtime readiness.

    Checks:
    - Required folders and files
    - Module contracts
    - Dependency availability
    - AI layer presence (if applicable)

    Intended for:
    - CI pipelines
    - Pre-commit checks
    - Debugging setup issues

    Example:
      racerapi doctor
    """
    doctor_cmd()


@app.command()
def routes():
    """
    List all registered API routes.

    Shows:
    - HTTP method
    - Path
    - Owning module

    Useful for:
    - Debugging routing
    - Verifying module discovery

    Example:
      racerapi routes
    """
    routes_cmd()


@app.command()
def version():
    """
    Show RacerAPI version and runtime information.

    Displays:
    - RacerAPI version
    - Python version
    - Platform info

    Example:
      racerapi version
    """
    version_cmd()


# -------------------------------------------------------------------
# CONFIGURATION & ENVIRONMENT (STABLE)
# -------------------------------------------------------------------


@app.command()
def config():
    """
    Show effective runtime configuration.

    Displays resolved configuration values after:
    - Defaults
    - Environment variables
    - .env overrides

    Secrets are redacted automatically.

    Example:
      racerapi config
    """
    config_cmd()


@app.command()
def env():
    """
    Inspect and validate environment variables.

    Checks:
    - Required variables
    - Missing AI provider keys
    - Invalid values

    Example:
      racerapi env
    """
    env_cmd()


# -------------------------------------------------------------------
# AI COMMANDS (EXPERIMENTAL – EXPLICIT OPT-IN)
# -------------------------------------------------------------------


@app.command()
def eval(
    module: str | None = typer.Argument(
        None,
        help="Optional module name (e.g. chat)",
    ),
    experimental: bool = typer.Option(
        False,
        "--experimental",
        help="Acknowledge experimental command",
    ),
):
    """
    Run AI evaluation scenarios.

    Maturity: EXPERIMENTAL

    This command may change behavior or output format.

    Example:
      racerapi eval --experimental
      racerapi eval chat --experimental
    """
    if not experimental:
        typer.secho(
            "This command is experimental. Re-run with --experimental.",
            fg="yellow",
        )
        raise typer.Exit(1)

    eval_cmd(module)


@app.command()
def trace(
    limit: int = typer.Option(
        10,
        help="Number of recent AI traces to display",
    ),
    experimental: bool = typer.Option(
        False,
        "--experimental",
        help="Acknowledge experimental command",
    ),
):
    """
    Inspect recent AI execution traces.

    Maturity: EXPERIMENTAL

    Displays:
    - Model used
    - Latency
    - Metadata (no raw prompts by default)

    Example:
      racerapi trace --limit 20 --experimental
    """
    if not experimental:
        typer.secho(
            "This command is experimental. Re-run with --experimental.",
            fg="yellow",
        )
        raise typer.Exit(1)

    trace_cmd(limit)


# -------------------------------------------------------------------
# TOOLING (STABLE)
# -------------------------------------------------------------------


@app.command()
def test():
    """
    Run project tests.

    Thin wrapper around pytest that:
    - Ensures correct PYTHONPATH
    - Loads framework context

    Example:
      racerapi test
    """
    test_cmd()


@app.command()
def format():
    """
    Format project code.

    Runs:
    - black
    - ruff (fix mode)

    Example:
      racerapi format
    """
    format_cmd()


def main():
    app()


if __name__ == "__main__":
    main()
