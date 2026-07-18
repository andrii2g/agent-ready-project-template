from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def invoke(relative: str, payload: dict[str, object]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(ROOT / relative)],
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        cwd=ROOT,
        check=False,
    )


class ClaudeHookTests(unittest.TestCase):
    def test_guard_allows_non_destructive_command(self) -> None:
        result = invoke(
            ".claude/hooks/guard_command.py",
            {"tool_name": "Bash", "tool_input": {"command": "git status --short"}},
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "")

    def test_guard_denies_force_push(self) -> None:
        result = invoke(
            ".claude/hooks/guard_command.py",
            {"tool_name": "Bash", "tool_input": {"command": "git push --force origin main"}},
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        output = json.loads(result.stdout)
        decision = output["hookSpecificOutput"]["permissionDecision"]
        self.assertEqual(decision, "deny")

    def test_sensitive_hook_denies_dotenv(self) -> None:
        result = invoke(
            ".claude/hooks/protect_sensitive_files.py",
            {"tool_name": "Read", "tool_input": {"file_path": "./services/api/.env"}},
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        output = json.loads(result.stdout)
        self.assertEqual(output["hookSpecificOutput"]["permissionDecision"], "deny")

    def test_sensitive_hook_allows_example(self) -> None:
        result = invoke(
            ".claude/hooks/protect_sensitive_files.py",
            {"tool_name": "Read", "tool_input": {"file_path": "./.env.example"}},
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "")

    def test_invalid_hook_input_fails_closed(self) -> None:
        result = subprocess.run(
            [sys.executable, str(ROOT / ".claude/hooks/guard_command.py")],
            input="not-json",
            text=True,
            capture_output=True,
            cwd=ROOT,
            check=False,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("invalid hook JSON", result.stderr)


if __name__ == "__main__":
    unittest.main()
