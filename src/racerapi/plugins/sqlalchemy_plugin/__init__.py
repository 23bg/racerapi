"""SQLAlchemy plugin package - lightweight wrapper.

This package exposes a `plugin` object (SQLAlchemyPlugin) which the core
loader can discover under the package's `plugin` entrypoint. The actual
implementation is split into `provider.py`, `plugin.py`, and `cli.py`.
"""

from .plugin import plugin

__all__ = ["plugin"]
