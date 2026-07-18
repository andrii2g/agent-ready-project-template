#!/usr/bin/env python3
"""Initialize every blueprint in isolation and validate its generated file set.

The unit test suite separately exercises initialized-repository verification.
This command skips duplicate policy runs for each stack so the full template
check remains practical locally and in CI.
"""

from __future__ import annotations

import argparse
import json
import py_compile
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TOKEN_PATTERN = re.compile(r"\{\{[A-Z_]+\}\}")


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def package_name(slug: str) -> str:
    return slug.replace("-", "_")


def rendered_path(path: Path, slug: str) -> Path:
    return Path(
        path.as_posix()
        .replace("{{PROJECT_SLUG}}", slug)
        .replace("{{PACKAGE_NAME}}", package_name(slug))
    )


def copied_template(parent: Path) -> Path:
    destination = parent / "repository"
    shutil.copytree(
        ROOT,
        destination,
        ignore=shutil.ignore_patterns(
            ".git", "__pycache__", "*.pyc", ".venv", "node_modules", "target"
        ),
    )
    return destination


def assert_no_tokens(paths: list[Path]) -> None:
    for path in paths:
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        match = TOKEN_PATTERN.search(text)
        if match:
            raise AssertionError(f"unresolved token {match.group(0)} in {path}")


def validate_one(name: str, *, verbose: bool) -> None:
    slug = f"{name}-validation-project"

    with tempfile.TemporaryDirectory(prefix=f"agent-template-{name}-") as raw:
        project = copied_template(Path(raw))
        command = [
            sys.executable,
            str(project / "scripts/template/init_project.py"),
            "--name",
            f"{name.title()} Validation Project",
            "--description",
            f"Generated validation project for the {name} blueprint",
            "--owner",
            "example-owner",
            "--author-name",
            "Template Validator",
            "--author-email",
            "validator@example.invalid",
            "--slug",
            slug,
            "--blueprint",
            name,
            "--license",
            "MIT",
            "--non-interactive",
            "--skip-verify",
        ]
        result = subprocess.run(
            command,
            cwd=project,
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode:
            raise RuntimeError(
                f"initializer failed for {name}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
            )

        metadata = load_json(project / ".project.json")
        if metadata.get("blueprint") != name or metadata.get("slug") != slug:
            raise AssertionError(f"incorrect generated metadata for {name}")
        if (project / ".template-state.json").exists():
            raise AssertionError(f"template state remains after {name} initialization")
        if (project / "scripts/template").exists():
            raise AssertionError(f"template-only initializer remains after {name} initialization")

        generated: list[Path] = []
        files_root = ROOT / "blueprints" / name / "files"
        for source in files_root.rglob("*"):
            if source.is_file():
                relative = rendered_path(source.relative_to(files_root), slug)
                target = project / relative
                if not target.exists():
                    raise AssertionError(f"generated path missing for {name}: {relative}")
                generated.append(target)

        generated.extend(
            project / relative
            for relative in (
                "AGENTS.md",
                "PROJECT.md",
                "README.md",
                "LICENSE",
                "Makefile",
                ".project.json",
                ".github/CODEOWNERS",
                ".github/ISSUE_TEMPLATE/config.yml",
            )
        )
        assert_no_tokens(generated)

        if name == "python":
            for path in [*(project / "src").rglob("*.py"), *(project / "tests").rglob("*.py")]:
                py_compile.compile(str(path), doraise=True)
        if name == "typescript":
            load_json(project / "package.json")
            load_json(project / "tsconfig.json")
        if name == "rust":
            cargo = (project / "Cargo.toml").read_text(encoding="utf-8")
            if f'name = "{slug}"' not in cargo:
                raise AssertionError("Rust package name was not rendered")

        if verbose:
            print(result.stdout, end="")
        print(
            f"OK: {name} blueprint initialized and validated "
            f"({len(generated)} generated files checked)"
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--blueprint",
        action="append",
        dest="blueprints",
        help="validate only this blueprint; may be supplied more than once",
    )
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    state = load_json(ROOT / ".template-state.json")
    supported = state.get("supportedBlueprints", [])
    if not isinstance(supported, list) or not all(isinstance(item, str) for item in supported):
        raise SystemExit(".template-state.json has an invalid supportedBlueprints list")
    selected = args.blueprints or supported
    unknown = sorted(set(selected) - set(supported))
    if unknown:
        parser.error("unknown blueprint(s): " + ", ".join(unknown))

    failures: list[str] = []
    for name in selected:
        try:
            validate_one(name, verbose=args.verbose)
        except Exception as exc:
            failures.append(f"{name}: {exc}")
            print(f"ERROR: {name}: {exc}", file=sys.stderr)
    if failures:
        print(f"\n{len(failures)} blueprint validation failure(s)", file=sys.stderr)
        return 1
    print(f"\nValidated {len(selected)} blueprint(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
