#!/usr/bin/env python3
"""Validate the agent-ready repository in template or initialized state."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python < 3.11
    tomllib = None  # type: ignore[assignment]

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_PATHS = (
    "AGENTS.md",
    "CLAUDE.md",
    "PROJECT.md",
    "README.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "VERSION",
    "TREE.md",
    ".gitignore",
    ".mcp.json",
    ".github/CODEOWNERS",
    ".github/pull_request_template.md",
    ".github/workflows/policy.yml",
    ".github/workflows/ci.yml",
    ".codex/config.toml",
    ".codex/rules/default.rules",
    ".claude/settings.json",
    ".claude/output-styles/README.md",
    ".agents/skills",
    ".claude/skills",
    "docs/agent-configuration-matrix.md",
    "docs/architecture.md",
    "docs/threat-model.md",
    "docs/claude-code.md",
    "docs/mcp.md",
    "docs/repository-structure.md",
    "scripts/sync_agent_skills.py",
    "scripts/validate_blueprints.py",
)

DEFAULT_PLACEHOLDERS = {
    "{{PROJECT_NAME}}",
    "{{PROJECT_SLUG}}",
    "{{PACKAGE_NAME}}",
    "{{PROJECT_DESCRIPTION}}",
    "{{OWNER}}",
    "{{AUTHOR_NAME}}",
    "{{AUTHOR_EMAIL}}",
    "{{YEAR}}",
    "{{LICENSE_ID}}",
    "{{TEMPLATE_VERSION}}",
    "{{SETUP_COMMAND}}",
    "{{FORMAT_COMMAND}}",
    "{{LINT_COMMAND}}",
    "{{TYPECHECK_COMMAND}}",
    "{{TEST_COMMAND}}",
    "{{BUILD_COMMAND}}",
    "{{VERIFY_COMMAND}}",
}

FORBIDDEN_BASENAMES = {
    ".env",
    ".env.local",
    ".env.development",
    ".env.production",
    "id_rsa",
    "id_dsa",
    "id_ecdsa",
    "id_ed25519",
    "credentials.json",
}
FORBIDDEN_SUFFIXES = {".pem", ".p12", ".pfx"}
IGNORED_SCAN_PARTS = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "htmlcov",
    "node_modules",
    "target",
}
WORKFLOW_MUTABLE_REFS = {"main", "master", "HEAD", "latest", "stable"}


@dataclass
class Report:
    checks: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def ok(self, message: str) -> None:
        self.checks.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)

    def error(self, message: str) -> None:
        self.errors.append(message)


def relative(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def load_json(path: Path, report: Report) -> Any | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        report.error(f"invalid JSON in {relative(path)}: {exc}")
        return None


def load_toml(path: Path, report: Report) -> dict[str, Any] | None:
    if tomllib is None:
        report.error("Python 3.11 or newer is required to validate TOML files")
        return None
    try:
        with path.open("rb") as handle:
            return tomllib.load(handle)
    except (OSError, tomllib.TOMLDecodeError) as exc:
        report.error(f"invalid TOML in {relative(path)}: {exc}")
        return None


def frontmatter_value(text: str, key: str) -> str | None:
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end < 0:
        return None
    for line in text[4:end].splitlines():
        if line.startswith(f"{key}:"):
            return line.split(":", 1)[1].strip().strip("\"'")
    return None


def compile_text(text: str, filename: str, report: Report) -> None:
    try:
        compile(text, filename, "exec")
    except SyntaxError as exc:
        report.error(f"Python file does not compile: {filename}: {exc.msg} at line {exc.lineno}")


def render(text: str, context: dict[str, str]) -> str:
    for token, value in context.items():
        text = text.replace(token, value)
    return text


def check_required(report: Report) -> None:
    required = list(REQUIRED_PATHS)
    if not (ROOT / ".template-state.json").exists():
        required.remove("scripts/validate_blueprints.py")
    missing = [path for path in required if not (ROOT / path).exists()]
    for path in missing:
        report.error(f"required path is missing: {path}")
    if not missing:
        report.ok(f"{len(required)} required repository paths exist")


def check_versions(report: Report) -> None:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?", version):
        report.error(f"VERSION is not a semantic version: {version!r}")
        return

    metadata_path = ROOT / ".template-state.json"
    key = "templateVersion"
    if not metadata_path.exists():
        metadata_path = ROOT / ".project.json"
    metadata = load_json(metadata_path, report) if metadata_path.exists() else None
    if isinstance(metadata, dict) and metadata.get(key) != version:
        report.error(f"{relative(metadata_path)} {key} does not match VERSION")
    else:
        report.ok(f"template version metadata is consistent at {version}")


def check_shared_contract(report: Report) -> None:
    claude = (ROOT / "CLAUDE.md").read_text(encoding="utf-8")
    agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    if "@AGENTS.md" not in claude:
        report.error("CLAUDE.md must import @AGENTS.md")
    if "canonical shared agent contract" not in agents.lower():
        report.warn(
            "AGENTS.md does not explicitly describe itself as the canonical shared contract"
        )
    if "Do not add permissions to `.claude/settings.local.json`" not in claude:
        report.error("CLAUDE.md must prohibit agents from broadening local Claude permissions")
    report.ok("shared AGENTS.md and Claude adapter contract was inspected")


def check_codex(report: Report) -> None:
    config_path = ROOT / ".codex/config.toml"
    config = load_toml(config_path, report)
    if isinstance(config, dict):
        if config.get("approval_policy") == "never":
            report.error("Codex approval_policy must not be 'never' in the template")
        if config.get("sandbox_mode") != "workspace-write":
            report.error("Codex template sandbox_mode must be workspace-write")
        network = config.get("sandbox_workspace_write", {}).get("network_access")
        if network is not False:
            report.error("Codex workspace-write network_access must be false")
        agents = config.get("agents", {})
        if int(agents.get("max_depth", 99)) > 1:
            report.error("Codex max_depth must not exceed 1 in the baseline template")
        if int(agents.get("max_threads", 0)) < 1:
            report.error("Codex max_threads must be a positive integer")

    expected = {
        "repo-mapper.toml",
        "change-worker.toml",
        "test-verifier.toml",
        "risk-reviewer.toml",
    }
    actual = {path.name for path in (ROOT / ".codex/agents").glob("*.toml")}
    if expected - actual:
        report.error("missing Codex custom agents: " + ", ".join(sorted(expected - actual)))
    for path in sorted((ROOT / ".codex/agents").glob("*.toml")):
        data = load_toml(path, report)
        if not isinstance(data, dict):
            continue
        missing = [
            key for key in ("name", "description", "developer_instructions") if not data.get(key)
        ]
        if missing:
            report.error(f"{relative(path)} missing fields: {', '.join(missing)}")
        if (
            path.name in {"repo-mapper.toml", "risk-reviewer.toml"}
            and data.get("sandbox_mode") != "read-only"
        ):
            report.error(f"{relative(path)} must use read-only sandbox_mode")
    report.ok("Codex configuration, sandbox, command rules, and custom agents were inspected")


def collect_hook_entries(settings: dict[str, Any]) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for group in settings.get("hooks", {}).get("PreToolUse", []):
        if not isinstance(group, dict):
            continue
        for hook in group.get("hooks", []):
            if isinstance(hook, dict):
                entries.append(hook)
    return entries


def check_claude(report: Report) -> None:
    settings_path = ROOT / ".claude/settings.json"
    settings = load_json(settings_path, report)
    if isinstance(settings, dict):
        permissions = settings.get("permissions", {})
        if permissions.get("defaultMode") != "default":
            report.error("Claude project defaultMode must be 'default'")
        if settings.get("disableBypassPermissionsMode") != "disable":
            report.error("Claude bypass permissions mode must be disabled")

        deny = set(permissions.get("deny", []))
        for expected in ("Read(./.env)", "Read(./.env.local)", "Read(./secrets/**)"):
            if expected not in deny:
                report.error(f"Claude settings missing deny rule: {expected}")

        ask = set(permissions.get("ask", []))
        for expected in ("Edit(/.claude/**)", "Edit(/.codex/**)", "Edit(/.mcp.json)"):
            if expected not in ask:
                report.error(f"Claude settings missing governance approval rule: {expected}")

        sandbox = settings.get("sandbox", {})
        if sandbox.get("enabled") is not True:
            report.error("Claude Bash sandbox must be enabled in project settings")
        if sandbox.get("autoAllowBashIfSandboxed") is not False:
            report.error("Claude sandboxed Bash commands must not be auto-approved")

        hooks = collect_hook_entries(settings)
        discovered: set[str] = set()
        for hook in hooks:
            command = hook.get("command")
            args = hook.get("args")
            if isinstance(command, str) and "${CLAUDE_PROJECT_DIR}" in command:
                report.error(
                    "Claude project-path hooks must use exec-form args, not a shell-form command"
                )
            if not isinstance(args, list):
                continue
            for arg in args:
                if isinstance(arg, str):
                    for expected in ("guard_command.py", "protect_sensitive_files.py"):
                        if expected in arg:
                            discovered.add(expected)
                            if command not in {"python", "python3"}:
                                report.error(
                                    f"Claude hook {expected} must execute through python or python3"
                                )
        missing_hooks = {"guard_command.py", "protect_sensitive_files.py"} - discovered
        for expected in sorted(missing_hooks):
            report.error(f"Claude PreToolUse hook missing or not in exec form: {expected}")

    expected_agents = {
        "repo-mapper",
        "change-worker",
        "test-verifier",
        "risk-reviewer",
        "coordinator",
    }
    names: set[str] = set()
    for path in sorted((ROOT / ".claude/agents").glob("*.md")):
        text = path.read_text(encoding="utf-8")
        name = frontmatter_value(text, "name")
        description = frontmatter_value(text, "description")
        if not name or not description:
            report.error(f"{relative(path)} lacks required name/description frontmatter")
            continue
        if name in names:
            report.error(f"duplicate Claude subagent name: {name}")
        names.add(name)
    if expected_agents - names:
        report.error("missing Claude subagents: " + ", ".join(sorted(expected_agents - names)))

    rules = sorted((ROOT / ".claude/rules").glob("*.md"))
    if len(rules) < 4:
        report.error("Claude rules directory must contain baseline and path-specific rules")
    for hook in sorted((ROOT / ".claude/hooks").glob("*.py")):
        compile_text(hook.read_text(encoding="utf-8"), relative(hook), report)
    report.ok("Claude settings, sandbox, subagents, rules, and exec-form hooks were inspected")


def inspect_literal_secrets(value: Any, path: str, report: Report) -> None:
    secret_keys = {"token", "api_key", "apikey", "password", "secret", "private_key"}
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}" if path else str(key)
            if str(key).lower() in secret_keys and isinstance(child, str):
                if child and not re.fullmatch(r"\$\{[A-Za-z_][A-Za-z0-9_]*\}", child):
                    report.error(f"literal secret-like value in .mcp.json at {child_path}")
            inspect_literal_secrets(child, child_path, report)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            inspect_literal_secrets(child, f"{path}[{index}]", report)


def check_mcp(report: Report) -> None:
    data = load_json(ROOT / ".mcp.json", report)
    if not isinstance(data, dict):
        return
    servers = data.get("mcpServers")
    if not isinstance(servers, dict):
        report.error(".mcp.json must contain an mcpServers object")
        return
    inspect_literal_secrets(data, "", report)
    if (ROOT / ".template-state.json").exists() and servers:
        report.error("the distributable template must not enable MCP servers by default")
    elif servers:
        report.warn(
            f"initialized project enables {len(servers)} MCP server(s); "
            "review the expanded trust boundary"
        )
    else:
        report.ok("project-scoped MCP registry is valid and empty")


def list_files(root: Path) -> set[Path]:
    if not root.exists():
        return set()
    return {path.relative_to(root) for path in root.rglob("*") if path.is_file()}


def check_skills(report: Report) -> None:
    source = ROOT / ".agents/skills"
    destination = ROOT / ".claude/skills"
    source_files = list_files(source)
    destination_files = list_files(destination)
    if source_files != destination_files:
        report.error("canonical and Claude skill file sets differ")
    skill_count = 0
    for relative_path in sorted(source_files & destination_files):
        if (source / relative_path).read_bytes() != (destination / relative_path).read_bytes():
            report.error(f"Claude skill copy differs: {relative_path.as_posix()}")
        if relative_path.name == "SKILL.md":
            skill_count += 1
            text = (source / relative_path).read_text(encoding="utf-8")
            if not frontmatter_value(text, "name") or not frontmatter_value(text, "description"):
                report.error(f"skill missing required frontmatter: {relative_path.as_posix()}")
    if not source_files:
        report.error("no canonical skills found")
    else:
        report.ok(f"{skill_count} portable skills are synchronized")


def dummy_context(version: str) -> dict[str, str]:
    return {
        "{{PROJECT_NAME}}": "Example Project",
        "{{PROJECT_SLUG}}": "example-project",
        "{{PACKAGE_NAME}}": "example_project",
        "{{PROJECT_DESCRIPTION}}": "Example generated project",
        "{{OWNER}}": "example-owner",
        "{{AUTHOR_NAME}}": "Example Maintainer",
        "{{AUTHOR_EMAIL}}": "maintainer@example.invalid",
        "{{YEAR}}": "2026",
        "{{LICENSE_ID}}": "MIT",
        "{{TEMPLATE_VERSION}}": version,
        "{{DEFAULT_BRANCH}}": "main",
        "{{SETUP_COMMAND}}": "echo setup",
        "{{FORMAT_COMMAND}}": "echo format",
        "{{LINT_COMMAND}}": "echo lint",
        "{{TYPECHECK_COMMAND}}": "echo typecheck",
        "{{TEST_COMMAND}}": "echo test",
        "{{BUILD_COMMAND}}": "echo build",
        "{{VERIFY_COMMAND}}": "echo verify",
    }


def inspect_workflow(path: Path, text: str, report: Report) -> None:
    if "permissions:" not in text:
        report.error(f"workflow lacks explicit permissions: {relative(path)}")
    if re.search(r"^\s*pull_request_target\s*:", text, re.M):
        report.error(f"pull_request_target requires explicit security review: {relative(path)}")
    if re.search(r"^\s*permissions:\s*write-all\s*$", text, re.M):
        report.error(f"workflow uses write-all permissions: {relative(path)}")
    if "timeout-minutes:" not in text:
        report.error(f"workflow job lacks timeout-minutes: {relative(path)}")
    for reference in re.findall(r"uses:\s*([^\s#]+)", text):
        if "@" not in reference:
            report.error(f"action reference lacks version: {reference} in {relative(path)}")
            continue
        revision = reference.rsplit("@", 1)[1]
        if revision in WORKFLOW_MUTABLE_REFS:
            report.error(f"action reference uses mutable revision: {reference} in {relative(path)}")
        if not (
            re.fullmatch(r"v\d+(?:\.\d+){0,2}", revision)
            or re.fullmatch(r"[0-9a-fA-F]{40}", revision)
        ):
            report.warn(
                "action reference is not an exact version tag or full SHA: "
                f"{reference} in {relative(path)}"
            )


def check_blueprints(report: Report, template_state: dict[str, Any] | None) -> None:
    if not template_state:
        return
    supported = template_state.get("supportedBlueprints", [])
    if not isinstance(supported, list) or not supported or len(supported) != len(set(supported)):
        report.error("supportedBlueprints must be a non-empty unique list")
        return

    version = str(template_state.get("templateVersion", "unknown"))
    context = dummy_context(version)
    required_commands = ("setup", "format", "lint", "typecheck", "test", "build", "verify")
    for name in supported:
        if not isinstance(name, str) or not re.fullmatch(r"[a-z][a-z0-9-]*", name):
            report.error(f"invalid blueprint name: {name!r}")
            continue
        directory = ROOT / "blueprints" / name
        manifest_path = directory / "blueprint.json"
        if not manifest_path.exists():
            report.error(f"blueprint manifest missing: blueprints/{name}/blueprint.json")
            continue
        manifest = load_json(manifest_path, report)
        if not isinstance(manifest, dict):
            continue
        if manifest.get("name") != name:
            report.error(f"blueprint {name} manifest name does not match directory")
        if not manifest.get("description"):
            report.error(f"blueprint {name} lacks a description")
        commands = manifest.get("commands", {})
        missing = [
            key
            for key in required_commands
            if not isinstance(commands.get(key), str) or not commands.get(key).strip()
        ]
        if missing:
            report.error(f"blueprint {name} missing commands: {', '.join(missing)}")
        overwrites = set(manifest.get("overwrites", []))
        for expected in (".github/workflows/ci.yml", ".github/dependabot.yml"):
            if expected not in overwrites:
                report.error(f"blueprint {name} must declare intentional overwrite: {expected}")
            if not (directory / "files" / expected).exists():
                report.error(f"blueprint {name} lacks generated file: {expected}")

        files_dir = directory / "files"
        if not files_dir.is_dir():
            report.error(f"blueprint {name} lacks files directory")
            continue
        for source in sorted(path for path in files_dir.rglob("*") if path.is_file()):
            data = source.read_bytes()
            try:
                rendered = render(data.decode("utf-8"), context)
            except UnicodeDecodeError:
                continue
            unresolved = sorted(token for token in DEFAULT_PLACEHOLDERS if token in rendered)
            if unresolved:
                location = source.relative_to(directory)
                report.error(
                    f"blueprint {name} leaves unresolved tokens in {location}: "
                    f"{', '.join(unresolved)}"
                )
            rendered_name = render(source.name, context)
            if rendered_name.endswith(".json"):
                try:
                    json.loads(rendered)
                except json.JSONDecodeError as exc:
                    report.error(f"rendered blueprint JSON invalid: {relative(source)}: {exc}")
            elif rendered_name.endswith(".toml") and tomllib is not None:
                try:
                    tomllib.loads(rendered)
                except tomllib.TOMLDecodeError as exc:
                    report.error(f"rendered blueprint TOML invalid: {relative(source)}: {exc}")
            elif rendered_name.endswith(".py"):
                compile_text(rendered, relative(source), report)
            if ".github/workflows/" in source.as_posix() and source.suffix in {".yml", ".yaml"}:
                inspect_workflow(source, rendered, report)
    report.ok(f"{len(supported)} blueprints and their rendered payloads were inspected")


def check_state_and_placeholders(report: Report) -> None:
    state_path = ROOT / ".template-state.json"
    if state_path.exists():
        state = load_json(state_path, report)
        if isinstance(state, dict):
            if state.get("status") != "uninitialized":
                report.error(".template-state.json must declare status uninitialized")
            declared = set(state.get("placeholders", []))
            if DEFAULT_PLACEHOLDERS - declared:
                report.error(
                    ".template-state.json is missing declared placeholders: "
                    + ", ".join(sorted(DEFAULT_PLACEHOLDERS - declared))
                )
            check_blueprints(report, state)
            report.ok("repository is in valid uninitialized template state")
        return

    project_path = ROOT / ".project.json"
    if not project_path.exists():
        report.error("initialized repository must contain .project.json")
        return
    project = load_json(project_path, report)
    if not isinstance(project, dict) or project.get("status") != "initialized":
        report.error(".project.json must declare status initialized")

    scan_paths = [
        ROOT / "AGENTS.md",
        ROOT / "PROJECT.md",
        ROOT / "README.md",
        ROOT / ".github/CODEOWNERS",
        ROOT / "LICENSE",
        ROOT / "Makefile",
    ]
    for path in scan_paths:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        found = sorted(token for token in DEFAULT_PLACEHOLDERS if token in text)
        if found:
            report.error(f"unresolved placeholders in {relative(path)}: {', '.join(found)}")
    report.ok("initialized project metadata and placeholders were inspected")


def check_secrets(report: Report) -> None:
    problems: list[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or any(
            part in IGNORED_SCAN_PARTS for part in path.relative_to(ROOT).parts
        ):
            continue
        name = path.name.lower()
        if name in {".env.example", ".env.sample", ".env.template", "settings.local.json.example"}:
            continue
        if name in FORBIDDEN_BASENAMES or path.suffix.lower() in FORBIDDEN_SUFFIXES:
            problems.append(relative(path))
    for problem in problems:
        report.error(f"potential secret file must not be committed: {problem}")
    if not problems:
        report.ok("no common committed secret-file names were found")


def check_workflows(report: Report) -> None:
    paths = sorted((ROOT / ".github/workflows").glob("*.y*ml"))
    for path in paths:
        inspect_workflow(path, path.read_text(encoding="utf-8"), report)
    report.ok(f"{len(paths)} active GitHub workflows were inspected")


def check_python_files(report: Report) -> None:
    count = 0
    for directory in (ROOT / "scripts", ROOT / "tests", ROOT / ".claude/hooks"):
        if not directory.exists():
            continue
        for path in directory.rglob("*.py"):
            if any(part == "__pycache__" for part in path.parts):
                continue
            compile_text(path.read_text(encoding="utf-8"), relative(path), report)
            count += 1
    report.ok(f"{count} repository Python tooling files compile in memory")


def check_tree(report: Report) -> None:
    if not (ROOT / ".template-state.json").exists():
        report.ok("TREE.md freshness is not enforced after project initialization")
        return
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/render_tree.py"), "--stdout"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode:
        report.error("could not render repository tree: " + result.stderr.strip())
        return
    actual = (ROOT / "TREE.md").read_text(encoding="utf-8")
    if actual != result.stdout:
        report.error("TREE.md is stale; run python scripts/render_tree.py")
    else:
        report.ok("TREE.md matches the current template contents")


def print_report(report: Report, as_json: bool) -> None:
    if as_json:
        print(
            json.dumps(
                {
                    "ok": not report.errors,
                    "checks": report.checks,
                    "warnings": report.warnings,
                    "errors": report.errors,
                },
                indent=2,
            )
        )
        return
    for message in report.checks:
        print(f"OK: {message}")
    for message in report.warnings:
        print(f"WARNING: {message}")
    for message in report.errors:
        print(f"ERROR: {message}")
    print(
        f"\nSummary: {len(report.checks)} checks, "
        f"{len(report.warnings)} warnings, {len(report.errors)} errors"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    args = parser.parse_args()

    report = Report()
    check_required(report)
    if not report.errors:
        check_versions(report)
        check_shared_contract(report)
        check_codex(report)
        check_claude(report)
        check_mcp(report)
        check_skills(report)
        check_state_and_placeholders(report)
        check_secrets(report)
        check_workflows(report)
        check_python_files(report)
        check_tree(report)
    print_report(report, args.json)
    return 1 if report.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
