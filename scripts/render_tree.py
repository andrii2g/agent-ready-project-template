#!/usr/bin/env python3
"""Render a deterministic repository tree into TREE.md."""

from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_IGNORES = {
    ".coverage",
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "htmlcov",
    "node_modules",
    "target",
}


def visible_children(directory: Path) -> list[Path]:
    return sorted(
        (item for item in directory.iterdir() if item.name not in DEFAULT_IGNORES),
        key=lambda item: (not item.is_dir(), item.name.lower(), item.name),
    )


def walk(directory: Path, prefix: str = "") -> list[str]:
    lines: list[str] = []
    children = visible_children(directory)
    for index, child in enumerate(children):
        last = index == len(children) - 1
        connector = "└── " if last else "├── "
        suffix = "/" if child.is_dir() else ""
        lines.append(f"{prefix}{connector}{child.name}{suffix}")
        if child.is_dir():
            extension = "    " if last else "│   "
            lines.extend(walk(child, prefix + extension))
    return lines


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stdout", action="store_true", help="print instead of updating TREE.md")
    args = parser.parse_args()

    target = ROOT / "TREE.md"
    target.touch(exist_ok=True)
    lines = [f"{ROOT.name}/", *walk(ROOT)]
    content = "# Repository Tree\n\n```text\n" + "\n".join(lines) + "\n```\n"
    if args.stdout:
        print(content, end="")
    else:
        (ROOT / "TREE.md").write_text(content, encoding="utf-8")
        print("Updated TREE.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
