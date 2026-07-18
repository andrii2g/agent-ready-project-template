#!/usr/bin/env python3
"""Block a narrow set of clearly destructive Claude Code Bash tool calls."""

from __future__ import annotations

import json
import re
import sys
from typing import Any

BLOCKED: tuple[tuple[re.Pattern[str], str], ...] = (
    (
        re.compile(r"(^|[;&|]\s*)sudo(?:\s|$)", re.I),
        "Privileged sudo execution is not permitted by repository policy.",
    ),
    (
        re.compile(r"\bgit\s+push\b[^\n]*(?:--force(?:-with-lease)?|-f)(?:\s|$)", re.I),
        "Force-pushing is not permitted by repository policy.",
    ),
    (
        re.compile(r"\bgit\s+reset\s+--hard\b", re.I),
        "Hard reset can discard work and requires a manual workflow outside the agent session.",
    ),
    (
        re.compile(r"\bgit\s+clean\b[^\n]*(?:-[^\s]*f|--force)", re.I),
        "Forced git clean can permanently delete untracked files.",
    ),
    (
        re.compile(r"\bgh\s+repo\s+delete\b", re.I),
        "Repository deletion is forbidden in the agent workflow.",
    ),
    (
        re.compile(r"\b(?:terraform|tofu)\s+destroy\b", re.I),
        "Infrastructure destruction requires a separately reviewed human-controlled procedure.",
    ),
    (
        re.compile(r"\bkubectl\s+delete\s+(?:namespace|ns)\b", re.I),
        "Namespace deletion is forbidden in the agent workflow.",
    ),
    (
        re.compile(r"\bdocker\s+system\s+prune\b", re.I),
        "Docker system pruning can delete unrelated local resources.",
    ),
    (
        re.compile(r"\brm\s+(?:-[^\s]*r[^\s]*f|-[^\s]*f[^\s]*r)\s+(?:/|~)(?:\s|$|\*)", re.I),
        "Recursive forced deletion of a root or home path is forbidden.",
    ),
    (
        re.compile(r"(^|[;&|]\s*)mkfs(?:\.|\s|$)", re.I),
        "Filesystem formatting is forbidden in the agent workflow.",
    ),
    (
        re.compile(r"(^|[;&|]\s*)dd\s+[^\n]*\bof=/dev/", re.I),
        "Raw writes to block devices are forbidden in the agent workflow.",
    ),
    (
        re.compile(r"(^|[;&|]\s*)(?:shutdown|reboot|poweroff)(?:\s|$)", re.I),
        "Host shutdown or reboot is forbidden in the agent workflow.",
    ),
)


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


def main() -> int:
    try:
        payload: dict[str, Any] = json.load(sys.stdin)
    except (json.JSONDecodeError, TypeError) as exc:
        print(f"guard_command.py received invalid hook JSON: {exc}", file=sys.stderr)
        return 2

    if payload.get("tool_name") != "Bash":
        return 0

    tool_input = payload.get("tool_input")
    if not isinstance(tool_input, dict):
        print("guard_command.py did not receive a Bash tool_input object", file=sys.stderr)
        return 2

    command = tool_input.get("command", "")
    if not isinstance(command, str):
        print("guard_command.py received a non-string Bash command", file=sys.stderr)
        return 2

    normalized = " ".join(command.replace("\\\n", " ").split())
    for pattern, reason in BLOCKED:
        if pattern.search(normalized):
            deny(reason)
            return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
