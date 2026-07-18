#!/usr/bin/env python3
"""Synchronize canonical Agent Skills into Claude Code's project skill path."""

from __future__ import annotations

import argparse
import filecmp
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / ".agents" / "skills"
DESTINATION = ROOT / ".claude" / "skills"


def relative_files(root: Path) -> set[Path]:
    return {path.relative_to(root) for path in root.rglob("*") if path.is_file()}


def compare() -> list[str]:
    problems: list[str] = []
    source_files = relative_files(SOURCE) if SOURCE.exists() else set()
    destination_files = relative_files(DESTINATION) if DESTINATION.exists() else set()

    for missing in sorted(source_files - destination_files):
        problems.append(f"missing Claude skill copy: {missing.as_posix()}")
    for extra in sorted(destination_files - source_files):
        problems.append(f"unexpected Claude skill copy: {extra.as_posix()}")
    for common in sorted(source_files & destination_files):
        if not filecmp.cmp(SOURCE / common, DESTINATION / common, shallow=False):
            problems.append(f"skill copy differs: {common.as_posix()}")
    return problems


def synchronize() -> None:
    if not SOURCE.is_dir():
        raise SystemExit(f"canonical skill directory not found: {SOURCE}")
    if DESTINATION.exists():
        shutil.rmtree(DESTINATION)
    shutil.copytree(SOURCE, DESTINATION)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="report drift without modifying files")
    args = parser.parse_args()

    if args.check:
        problems = compare()
        if problems:
            for problem in problems:
                print(f"ERROR: {problem}")
            return 1
        print("Agent skills are synchronized.")
        return 0

    synchronize()
    print(f"Synchronized {SOURCE.relative_to(ROOT)} -> {DESTINATION.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
