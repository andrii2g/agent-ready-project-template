from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class SkillSynchronizationTests(unittest.TestCase):
    def test_skill_copies_are_synchronized(self) -> None:
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/sync_agent_skills.py"), "--check"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
