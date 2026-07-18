#!/usr/bin/env python3
"""Preview or apply conservative GitHub repository settings with the gh CLI."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def parse_labels(path: Path) -> list[dict[str, str]]:
    labels: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        stripped = raw.strip()
        if stripped.startswith("- name:"):
            if current:
                labels.append(current)
            current = {"name": stripped.split(":", 1)[1].strip().strip('"')}
        elif current is not None and stripped.startswith("color:"):
            current["color"] = stripped.split(":", 1)[1].strip().strip('"')
        elif current is not None and stripped.startswith("description:"):
            current["description"] = stripped.split(":", 1)[1].strip().strip('"')
    if current:
        labels.append(current)
    return labels


def display(command: list[str]) -> str:
    return " ".join(
        json.dumps(part) if any(c.isspace() for c in part) else part for part in command
    )


def run(command: list[str], apply: bool, input_text: str | None = None) -> None:
    print(("APPLY " if apply else "PLAN  ") + display(command))
    if not apply:
        return
    subprocess.run(command, input=input_text, text=True, check=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, help="repository in owner/name form")
    parser.add_argument("--apply", action="store_true", help="execute the displayed operations")
    parser.add_argument(
        "--components",
        nargs="+",
        choices=("labels", "settings", "ruleset"),
        default=("labels", "settings", "ruleset"),
        help="components to preview or apply (default: all)",
    )
    args = parser.parse_args()

    if "/" not in args.repo or args.repo.count("/") != 1:
        parser.error("--repo must use owner/name form")
    if args.apply and shutil.which("gh") is None:
        print("ERROR: GitHub CLI 'gh' is required for --apply", file=sys.stderr)
        return 2

    selected = set(args.components)
    if "labels" in selected:
        for label in parse_labels(ROOT / "ops/github/labels.yml"):
            command = [
                "gh",
                "label",
                "create",
                label["name"],
                "--repo",
                args.repo,
                "--color",
                label.get("color", "ededed"),
                "--description",
                label.get("description", ""),
                "--force",
            ]
            run(command, args.apply)

    if "settings" in selected:
        command = [
            "gh",
            "repo",
            "edit",
            args.repo,
            "--delete-branch-on-merge",
            "--enable-issues",
            "--enable-squash-merge",
            "--enable-merge-commit",
            "--disable-rebase-merge",
        ]
        run(command, args.apply)

    if "ruleset" in selected:
        ruleset = (ROOT / "ops/github/main-ruleset.json").read_text(encoding="utf-8")
        command = [
            "gh",
            "api",
            "--method",
            "POST",
            f"repos/{args.repo}/rulesets",
            "--header",
            "Accept: application/vnd.github+json",
            "--input",
            "-",
        ]
        run(command, args.apply, input_text=ruleset)

    if not args.apply:
        print(
            "\nPreview only. Re-run with --apply after reviewing repository plan "
            "availability, required check names, and permissions."
        )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except subprocess.CalledProcessError as exc:
        print(f"ERROR: command failed with exit status {exc.returncode}", file=sys.stderr)
        raise SystemExit(exc.returncode) from exc
