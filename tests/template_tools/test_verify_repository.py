from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class RepositoryVerificationTests(unittest.TestCase):
    def test_template_verifies(self) -> None:
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/verify_repository.py"), "--json"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertTrue(report["ok"])
        self.assertEqual(report["errors"], [])


if __name__ == "__main__":
    unittest.main()
