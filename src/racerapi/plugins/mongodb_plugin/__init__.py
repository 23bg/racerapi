"""MongoDB plugin package.

Provides a `plugin` instance the loader can discover. The implementation uses
pymongo synchronously; projects that require async drivers should provide a
separate async plugin (e.g. using motor).
"""

from .plugin import plugin

__all__ = ["plugin"]
