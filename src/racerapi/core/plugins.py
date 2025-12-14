# racerapi/core/plugins.py

from importlib import metadata as importlib_metadata
from fastapi import FastAPI
from racerapi.core.settings import AppSettings


def load_plugins(app: FastAPI, settings: AppSettings) -> None:
    """
    Load RacerAPI plugins via entry points.
    Compatible with Python 3.10+.
    """

    try:
        entry_points = importlib_metadata.entry_points(group="racerapi.plugins")
    except TypeError:
        # Fallback for very old Python (optional)
        entry_points = importlib_metadata.entry_points().get("racerapi.plugins", [])

    for ep in entry_points:
        try:
            plugin = ep.load()
            plugin(app, settings)
            print(f"✓ Loaded plugin: {ep.name}")
        except Exception as exc:
            raise RuntimeError(f"Failed loading plugin '{ep.name}': {exc}") from exc
