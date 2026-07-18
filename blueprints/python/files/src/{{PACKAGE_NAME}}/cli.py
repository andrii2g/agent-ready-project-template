"""Command-line entry point."""

from __future__ import annotations

import argparse
from collections.abc import Sequence


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser."""
    parser = argparse.ArgumentParser(
        prog="{{PROJECT_SLUG}}",
        description="{{PROJECT_DESCRIPTION}}",
    )
    parser.add_argument("--version", action="store_true", help="print the package version")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the command-line interface."""
    args = build_parser().parse_args(argv)
    if args.version:
        from . import __version__

        print(__version__)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
