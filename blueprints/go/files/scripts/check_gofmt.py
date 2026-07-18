#!/usr/bin/env python3
"""Fail when tracked Go source files are not formatted by gofmt."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    result = subprocess.run(
        ["gofmt", "-l", "."], cwd=ROOT, check=True, text=True, capture_output=True
    )
    paths = [line for line in result.stdout.splitlines() if line.strip()]
    if paths:
        print("Go files require gofmt:", file=sys.stderr)
        for path in paths:
            print(f"  - {path}", file=sys.stderr)
        return 1
    print("All Go files are formatted.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
