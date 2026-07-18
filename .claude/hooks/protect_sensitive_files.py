#!/usr/bin/env python3
"""Deny Claude Code file-tool access to common secret and credential paths."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path, PurePosixPath
from typing import Any

ALLOWED_ENV_NAMES = {".env.example", ".env.sample", ".env.template"}
SENSITIVE_NAMES = {
    "id_rsa",
    "id_dsa",
    "id_ecdsa",
    "id_ed25519",
    "credentials",
    "credentials.json",
    "service-account.json",
    "application_default_credentials.json",
    ".npmrc",
    ".pypirc",
}
SENSITIVE_SUFFIXES = {".pem", ".key", ".p12", ".pfx", ".jks", ".keystore"}
SENSITIVE_PARTS = {"secrets", "credentials", ".ssh"}


def deny(reason: str) -> None:
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": reason,
                }
            }
        )
    )


def normalized_parts(raw: str) -> tuple[str, ...]:
    value = raw.replace("\\", "/")
    try:
        return tuple(part.lower() for part in PurePosixPath(value).parts)
    except Exception:
        return tuple(part.lower() for part in value.split("/") if part)


def is_sensitive(raw_path: str) -> bool:
    expanded = os.path.expanduser(raw_path)
    name = Path(expanded).name.lower()
    parts = normalized_parts(expanded)

    if name in ALLOWED_ENV_NAMES or name.endswith((".example", ".sample", ".template")):
        return False
    if name == ".env" or name.startswith(".env."):
        return True
    if name in SENSITIVE_NAMES or Path(name).suffix.lower() in SENSITIVE_SUFFIXES:
        return True
    if any(part in SENSITIVE_PARTS for part in parts):
        return True
    if len(parts) >= 2 and parts[-2:] in (
        (".aws", "credentials"),
        ("gcloud", "application_default_credentials.json"),
    ):
        return True
    return False


def main() -> int:
    try:
        payload: dict[str, Any] = json.load(sys.stdin)
    except (json.JSONDecodeError, TypeError) as exc:
        print(f"protect_sensitive_files.py received invalid hook JSON: {exc}", file=sys.stderr)
        return 2

    if payload.get("tool_name") not in {"Read", "Edit", "Write"}:
        return 0

    tool_input = payload.get("tool_input")
    if not isinstance(tool_input, dict):
        print(
            "protect_sensitive_files.py did not receive a file-tool input object", file=sys.stderr
        )
        return 2

    raw_path = tool_input.get("file_path") or tool_input.get("path")
    if not isinstance(raw_path, str) or not raw_path:
        print("protect_sensitive_files.py did not receive a file path", file=sys.stderr)
        return 2

    if is_sensitive(raw_path):
        reason = (
            f"Access to sensitive path '{raw_path}' is blocked by repository policy. "
            "Use a sanitized example file instead."
        )
        deny(reason)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
