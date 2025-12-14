import typer
import sys
import json
from pathlib import Path
from datetime import datetime


def trace_cmd(limit: int = 10):
    """
    Inspect recent AI execution traces.

    Example:
      racerapi trace
      racerapi trace --limit 20
    """

    typer.echo("")
    typer.secho("RacerAPI AI Traces", bold=True)
    typer.echo("──────────────────────────────")
    typer.echo("")

    trace_file = Path.cwd() / ".var" / "racerapi" / "traces" / "ai.log"

    if not trace_file.exists():
        typer.secho(
            "✗ No AI trace file found (.var/racerapi/traces/ai.log)",
            fg="red",
        )
        typer.echo(
            "  Make sure AI telemetry is enabled and AI endpoints have been called."
        )
        sys.exit(1)

    try:
        lines = trace_file.read_text().splitlines()
    except Exception as e:
        typer.secho(f"✗ Failed to read trace file\n  {e}", fg="red")
        sys.exit(1)

    if not lines:
        typer.secho("⚠ Trace file is empty", fg="yellow")
        sys.exit(0)

    # Limit output
    records = lines[-limit:]

    typer.secho(
        f"{'TIME':<20} {'MODULE':<15} {'MODEL':<18} {'LAT(ms)':<8} STATUS",
        bold=True,
    )
    typer.secho(f"{'-'*20} {'-'*15} {'-'*18} {'-'*8} {'-'*8}")

    for raw in records:
        try:
            entry = json.loads(raw)
        except json.JSONDecodeError:
            typer.secho("  ⚠ Invalid trace entry skipped", fg="yellow")
            continue

        ts = entry.get("timestamp", "")
        module = entry.get("module", "unknown")
        model = entry.get("model", "unknown")
        latency = entry.get("latency_ms", "-")
        status = entry.get("status", "unknown")

        # Normalize timestamp
        try:
            ts = datetime.fromisoformat(ts.replace("Z", "")).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        except Exception:
            pass

        color = "green" if status == "success" else "red"

        typer.secho(
            f"{ts:<20} {module:<15} {model:<18} {latency:<8} {status}",
            fg=color,
        )

    typer.echo("")
    typer.secho(f"Showing last {len(records)} trace(s)", bold=True)
    typer.echo("")
