from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class InitializerTests(unittest.TestCase):
    def copy_template(self, parent: Path) -> Path:
        destination = parent / "template-copy"
        shutil.copytree(
            ROOT,
            destination,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".git"),
        )
        return destination

    def command(self, root: Path, *extra: str) -> list[str]:
        return [
            sys.executable,
            str(root / "scripts/template/init_project.py"),
            "--name",
            "Example Project",
            "--description",
            "A generated example project",
            "--owner",
            "example-owner",
            "--author-name",
            "Example Maintainer",
            "--author-email",
            "maintainer@example.invalid",
            "--blueprint",
            "generic",
            "--license",
            "MIT",
            "--non-interactive",
            "--keep-template-assets",
            *extra,
        ]

    def test_dry_run_is_non_destructive(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = self.copy_template(Path(raw))
            before = (root / "README.md").read_bytes()
            result = subprocess.run(
                self.command(root, "--dry-run"),
                cwd=root,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue((root / ".template-state.json").exists())
            self.assertEqual((root / "README.md").read_bytes(), before)
            self.assertFalse((root / ".project.json").exists())

    def test_generic_project_initializes_and_verifies(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = self.copy_template(Path(raw))
            result = subprocess.run(
                self.command(root),
                cwd=root,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertFalse((root / ".template-state.json").exists())
            project = json.loads((root / ".project.json").read_text(encoding="utf-8"))
            self.assertEqual(project["slug"], "example-project")
            self.assertEqual(project["blueprint"], "generic")
            self.assertIn("# Example Project", (root / "README.md").read_text(encoding="utf-8"))
            self.assertNotIn("{{OWNER}}", (root / ".github/CODEOWNERS").read_text(encoding="utf-8"))
            self.assertTrue((root / "src/README.md").exists())

    def test_unexpected_overwrite_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = self.copy_template(Path(raw))
            (root / "src").mkdir()
            (root / "src/README.md").write_text("user data\n", encoding="utf-8")
            result = subprocess.run(
                self.command(root),
                cwd=root,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("unexpected files", result.stdout + result.stderr)
            self.assertTrue((root / ".template-state.json").exists())


if __name__ == "__main__":
    unittest.main()
