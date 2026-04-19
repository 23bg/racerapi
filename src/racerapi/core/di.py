from __future__ import annotations

import inspect
import sys
import typing
from dataclasses import dataclass
from typing import Any, Callable, Dict


class ContainerError(RuntimeError):
    pass


@dataclass
class _ProviderEntry:
    provider: Any
    scope: str = "singleton"
    instance: Any = None


class Container:
    """A minimal dependency injection container.

    - Tokens may be types or string keys.
    - Providers may be:
      * an instance (already constructed)
      * a class (to be instantiated; constructor injection applied)
      * a factory callable (called with the container when creating the value)

    Usage:
      container = Container()
      container.register(DatabaseProvider, SQLAlchemyProvider, scope="singleton")
      svc = container.resolve(MyService)
    """

    def __init__(self) -> None:
        self._providers: Dict[Any, _ProviderEntry] = {}
        self._resolving: set = set()

    def register(self, token: Any, provider: Any, scope: str = "singleton") -> None:
        if scope not in {"singleton", "transient"}:
            raise ContainerError("scope must be 'singleton' or 'transient'")
        self._providers[token] = _ProviderEntry(provider=provider, scope=scope, instance=None)

    def override(self, token: Any, provider: Any, scope: str = "singleton") -> None:
        """Override an existing registration (useful for tests)."""
        self.register(token, provider, scope=scope)

    def is_registered(self, token: Any) -> bool:
        return token in self._providers

    def resolve(self, token: Any) -> Any:
        if token in self._providers:
            entry = self._providers[token]
            return self._build_from_entry(entry, token)

        # fallback: if token is a class, try to construct it directly
        if inspect.isclass(token):
            # auto-register transient for raw classes
            self.register(token, token, scope="transient")
            return self.resolve(token)

        raise ContainerError(f"No provider registered for token: {token}")

    def _build_from_entry(self, entry: _ProviderEntry, token: Any) -> Any:
        # singleton already created
        if entry.scope == "singleton" and entry.instance is not None:
            return entry.instance

        provider = entry.provider
        # already an instance
        if not inspect.isclass(provider) and not callable(provider):
            val = provider
        elif inspect.isclass(provider):
            val = self._instantiate_class(provider)
        else:
            # factory callable
            try:
                val = provider(self)
            except TypeError:
                # factory that expects no args
                val = provider()

        if entry.scope == "singleton":
            entry.instance = val
        return val

    def _instantiate_class(self, cls: type) -> Any:
        token = cls
        if token in self._resolving:
            raise ContainerError(f"Circular dependency detected when resolving {token}")
        self._resolving.add(token)
        try:
            ctor = cls.__init__
            try:
                hints = typing.get_type_hints(ctor, globalns=sys.modules[cls.__module__].__dict__)
            except Exception:
                hints = {}

            sig = inspect.signature(ctor)
            kwargs: Dict[str, Any] = {}
            for name, param in sig.parameters.items():
                if name == "self":
                    continue
                if param.kind not in (inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.KEYWORD_ONLY):
                    continue
                ann = hints.get(name, param.annotation)
                dep_token = ann if ann is not inspect._empty else name
                try:
                    kwargs[name] = self.resolve(dep_token)
                except ContainerError as exc:
                    raise ContainerError(
                        f"Failed to resolve dependency '{name}' for {cls}: {exc}"
                    ) from exc
            return cls(**kwargs)
        finally:
            self._resolving.remove(token)


__all__ = ["Container", "ContainerError"]
