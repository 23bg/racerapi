from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "racerapi"
MODULES = SRC / "modules"


class Violation(Exception):
    pass


def _module_name_from_path(path: Path) -> str | None:
    try:
        rel = path.relative_to(MODULES)
    except ValueError:
        return None
    if len(rel.parts) < 2:
        return None
    return rel.parts[0]


def _is_api_file(path: Path) -> bool:
    return path.name == "api.py" and "modules" in path.parts


def _is_repo_file(path: Path) -> bool:
    return path.name == "repo.py" and "modules" in path.parts


def _validate_file(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    tree = ast.parse(text, filename=str(path))
    violations: list[str] = []

    current_module = _module_name_from_path(path)

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            mod = node.module

            # Rule 1: no cross-module imports
            if current_module and mod.startswith("racerapi.modules."):
                parts = mod.split(".")
                if len(parts) >= 3:
                    imported_module = parts[2]
                    if imported_module != current_module:
                        violations.append(
                            f"{path}: cross-module import '{mod}' is forbidden"
                        )

            # Rule 2: no DB in routes
            if _is_api_file(path):
                if mod in {
                    "sqlalchemy",
                    "sqlalchemy.orm",
                    "racerapi.core.deps",
                    "racerapi.db.session",
                }:
                    violations.append(
                        f"{path}: api layer must not import DB/session module '{mod}'"
                    )

            # Rule 3: no business exception semantics in repo
            if _is_repo_file(path) and mod == "racerapi.core.exceptions":
                violations.append(
                    f"{path}: repo layer must not import domain/business exceptions"
                )

    return violations


def main() -> int:
    violations: list[str] = []

    for path in SRC.rglob("*.py"):
        if ".venv" in path.parts or "__pycache__" in path.parts:
            continue
        violations.extend(_validate_file(path))

    if violations:
        print("Architecture check failed:")
        for v in violations:
            print(f" - {v}")
        return 1

    print("Architecture check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
