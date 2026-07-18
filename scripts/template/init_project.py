#!/usr/bin/env python3
"""Initialize a new project from one blueprint without installing or publishing."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
STATE_PATH = ROOT / ".template-state.json"


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.strip().lower()).strip("-")
    if not slug:
        raise ValueError("project name does not produce a valid slug")
    if slug[0].isdigit():
        slug = f"project-{slug}"
    return slug


def package_name(slug: str) -> str:
    name = slug.replace("-", "_")
    if name[0].isdigit():
        name = f"project_{name}"
    return name


def render(text: str, context: dict[str, str]) -> str:
    for token, value in context.items():
        text = text.replace(token, value)
    return text


def render_path(path: Path, context: dict[str, str]) -> Path:
    rendered = path.as_posix()
    for token, value in context.items():
        rendered = rendered.replace(token, value)
    return Path(rendered)


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"cannot read {path.relative_to(ROOT)}: {exc}") from exc
    if not isinstance(value, dict):
        raise SystemExit(f"expected a JSON object in {path.relative_to(ROOT)}")
    return value


def prompt(
    current: str | None, label: str, *, default: str | None = None, required: bool = True
) -> str:
    if current is not None and current.strip():
        return current.strip()
    suffix = f" [{default}]" if default else ""
    value = input(f"{label}{suffix}: ").strip()
    if not value and default is not None:
        value = default
    if required and not value:
        raise SystemExit(f"{label} is required")
    return value


def validate_owner(owner: str) -> str:
    owner = owner.lstrip("@").strip()
    if not re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})", owner):
        raise SystemExit("owner must look like a GitHub user or organization name")
    return owner


def makefile(commands: dict[str, str]) -> str:
    targets = ["setup", "format", "lint", "typecheck", "test", "build", "verify"]
    lines = [".PHONY: " + " ".join(targets), ""]
    for target in targets:
        lines.extend([f"{target}:", f"\t{commands[target]}", ""])
    return "\n".join(lines).rstrip() + "\n"


def collect_blueprint_files(
    blueprint_dir: Path, context: dict[str, str]
) -> list[tuple[Path, Path]]:
    files_dir = blueprint_dir / "files"
    pairs: list[tuple[Path, Path]] = []
    for source in sorted(path for path in files_dir.rglob("*") if path.is_file()):
        relative = source.relative_to(files_dir)
        pairs.append((source, ROOT / render_path(relative, context)))
    return pairs


def write_rendered(source: Path, target: Path, context: dict[str, str]) -> None:
    data = source.read_bytes()
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render(text, context), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--name")
    parser.add_argument("--description")
    parser.add_argument("--owner")
    parser.add_argument("--author-name")
    parser.add_argument("--author-email", default="")
    parser.add_argument("--slug")
    parser.add_argument("--blueprint", default="generic")
    parser.add_argument(
        "--license", dest="license_id", default="MIT", choices=("MIT", "Apache-2.0", "Proprietary")
    )
    parser.add_argument("--year", type=int, default=dt.date.today().year)
    parser.add_argument("--default-branch", default="main")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--force", action="store_true", help="allow intended or unexpected file overwrites"
    )
    parser.add_argument("--keep-template-assets", action="store_true")
    parser.add_argument("--skip-verify", action="store_true")
    parser.add_argument("--non-interactive", action="store_true")
    args = parser.parse_args()

    if not STATE_PATH.exists():
        raise SystemExit("repository is already initialized or .template-state.json is missing")
    state = read_json(STATE_PATH)

    interactive = not args.non_interactive and sys.stdin.isatty()
    if interactive:
        args.name = prompt(args.name, "Project name")
        args.description = prompt(args.description, "Project description")
        args.owner = prompt(args.owner, "GitHub owner")
        args.author_name = prompt(args.author_name, "Copyright holder", default=args.owner)
    else:
        missing = [
            flag
            for flag, value in (
                ("--name", args.name),
                ("--description", args.description),
                ("--owner", args.owner),
            )
            if not value
        ]
        if missing:
            parser.error(
                "missing required arguments in non-interactive input: " + ", ".join(missing)
            )
        if not args.author_name:
            args.author_name = args.owner

    owner = validate_owner(args.owner)
    project_slug = args.slug or slugify(args.name)
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", project_slug):
        parser.error("--slug must contain lowercase letters, digits, and single hyphens")

    supported = state.get("supportedBlueprints", [])
    if args.blueprint not in supported:
        parser.error(
            f"unsupported blueprint {args.blueprint!r}; choose from {', '.join(supported)}"
        )

    blueprint_dir = ROOT / "blueprints" / args.blueprint
    manifest = read_json(blueprint_dir / "blueprint.json")
    commands = manifest.get("commands")
    if not isinstance(commands, dict):
        raise SystemExit("blueprint manifest lacks commands")

    command_tokens = {
        "{{SETUP_COMMAND}}": str(commands["setup"]),
        "{{FORMAT_COMMAND}}": str(commands["format"]),
        "{{LINT_COMMAND}}": str(commands["lint"]),
        "{{TYPECHECK_COMMAND}}": str(commands["typecheck"]),
        "{{TEST_COMMAND}}": str(commands["test"]),
        "{{BUILD_COMMAND}}": str(commands["build"]),
        "{{VERIFY_COMMAND}}": str(commands["verify"]),
    }
    context = {
        "{{PROJECT_NAME}}": args.name.strip(),
        "{{PROJECT_SLUG}}": project_slug,
        "{{PACKAGE_NAME}}": package_name(project_slug),
        "{{PROJECT_DESCRIPTION}}": args.description.strip(),
        "{{OWNER}}": owner,
        "{{AUTHOR_NAME}}": args.author_name.strip(),
        "{{AUTHOR_EMAIL}}": args.author_email.strip(),
        "{{YEAR}}": str(args.year),
        "{{LICENSE_ID}}": args.license_id,
        "{{TEMPLATE_VERSION}}": str(state.get("templateVersion", "unknown")),
        "{{DEFAULT_BRANCH}}": args.default_branch,
        **command_tokens,
    }

    overwrites = {Path(path).as_posix() for path in manifest.get("overwrites", [])}
    blueprint_files = collect_blueprint_files(blueprint_dir, context)
    planned_targets = {target.relative_to(ROOT).as_posix() for _, target in blueprint_files}
    planned_targets.update({"README.md", "LICENSE", "Makefile", ".project.json"})

    conflicts: list[str] = []
    for _, target in blueprint_files:
        relative = target.relative_to(ROOT).as_posix()
        if target.exists() and relative not in overwrites and not args.force:
            conflicts.append(relative)
    if conflicts:
        raise SystemExit(
            "initializer would overwrite unexpected files; use --force only after review:\n  "
            + "\n  ".join(sorted(conflicts))
        )

    print(f"Project: {args.name}")
    print(f"Slug: {project_slug}")
    print(f"Blueprint: {args.blueprint}")
    print(f"License: {args.license_id}")
    print("Planned generated or replaced paths:")
    for path in sorted(planned_targets):
        print(f"  - {path}")
    if not args.keep_template_assets:
        print(
            "Planned template asset removal: blueprints/, licenses/, tests/template_tools/, "
            "scripts/template/, scripts/validate_blueprints.py"
        )
    if args.dry_run:
        print("Dry run complete; no files were changed.")
        return 0

    for source, target in blueprint_files:
        write_rendered(source, target, context)

    for relative in (
        "AGENTS.md",
        "PROJECT.md",
        ".github/CODEOWNERS",
        ".github/ISSUE_TEMPLATE/config.yml",
    ):
        path = ROOT / relative
        path.write_text(render(path.read_text(encoding="utf-8"), context), encoding="utf-8")

    write_rendered(ROOT / "blueprints/_shared/README.md.tpl", ROOT / "README.md", context)
    write_rendered(ROOT / f"licenses/{args.license_id}.txt", ROOT / "LICENSE", context)
    (ROOT / "Makefile").write_text(
        makefile({key: str(value) for key, value in commands.items()}), encoding="utf-8"
    )

    project_meta = {
        "status": "initialized",
        "templateVersion": state.get("templateVersion", "unknown"),
        "name": args.name.strip(),
        "slug": project_slug,
        "packageName": package_name(project_slug),
        "description": args.description.strip(),
        "owner": owner,
        "authorName": args.author_name.strip(),
        "authorEmail": args.author_email.strip(),
        "license": args.license_id,
        "blueprint": args.blueprint,
        "defaultBranch": args.default_branch,
        "commands": commands,
        "initializedOn": dt.date.today().isoformat(),
    }
    (ROOT / ".project.json").write_text(json.dumps(project_meta, indent=2) + "\n", encoding="utf-8")
    STATE_PATH.unlink()

    if not args.keep_template_assets:
        for relative in ("blueprints", "licenses", "tests/template_tools"):
            path = ROOT / relative
            if path.exists():
                shutil.rmtree(path)

    if not args.keep_template_assets:
        template_scripts = ROOT / "scripts/template"
        if template_scripts.exists():
            shutil.rmtree(template_scripts)
        blueprint_validator = ROOT / "scripts/validate_blueprints.py"
        if blueprint_validator.exists():
            blueprint_validator.unlink()

    tree_renderer = ROOT / "scripts/render_tree.py"
    if tree_renderer.exists():
        subprocess.run([sys.executable, str(tree_renderer)], cwd=ROOT, check=True)

    if not args.skip_verify:
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/verify_repository.py")], cwd=ROOT
        )
        if result.returncode:
            raise SystemExit("initialization completed, but repository verification failed")

    print(
        "Project initialization completed. No dependencies were installed and no Git or "
        "GitHub changes were made."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
