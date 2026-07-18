# Repository Structure

The repository separates product intent, shared agent behavior, vendor runtime
controls, delivery governance, reusable project generation, and stack-specific
implementation files. `TREE.md` is the authoritative exhaustive path listing;
this document explains why each area exists.

## Root contracts

| Path | Responsibility |
|---|---|
| `README.md` | Human-facing setup, blueprint selection, and security posture |
| `PROJECT.md` | Product problem, users, requirements, constraints, interfaces, data, operations, and success criteria |
| `AGENTS.md` | Canonical repository-wide operating contract for coding agents |
| `CLAUDE.md` | Thin Claude Code adapter that imports `AGENTS.md` |
| `CLAUDE.local.md.example` | Non-committed personal instruction example |
| `.mcp.json` | Active, empty project-scoped MCP registry |
| `CONTRIBUTING.md` | Contribution, review, and validation workflow |
| `SECURITY.md` | Vulnerability reporting and supported-security expectations |
| `CODE_OF_CONDUCT.md` | Collaboration standards |
| `CHANGELOG.md`, `ROADMAP.md`, `VERSION` | Release history, planned evolution, and template version |
| `.template-state.json` | Declares the repository is an uninitialized template and lists supported blueprints/placeholders |
| `TREE.md` | Deterministically generated full path tree |

## Shared and vendor-specific agent configuration

### `.agents/`

The canonical portable Agent Skills source. Each skill lives at
`.agents/skills/<skill-name>/SKILL.md`. The synchronization script mirrors these
files to Claude Code's native project-skill location and the verifier rejects
drift.

### `.codex/`

- `config.toml`: project-scoped approvals, workspace-write sandbox, disabled
  sandbox network access, and bounded multi-agent settings.
- `agents/`: mapper, implementation, verification, and independent-review roles.
- `rules/default.rules`: explicit prompts or denials for publishing,
  destructive Git operations, privilege escalation, infrastructure deletion,
  repository deletion, and local resource pruning.

### `.claude/`

- `settings.json`: project permissions, sandbox settings, hooks, and disabled
  bypass-permissions mode.
- `settings.local.json.example`: non-committed personal override example.
- `agents/`: five bounded project subagents.
- `rules/`: always-on security/testing rules plus path-scoped documentation,
  workflow, Python, TypeScript, Go, and Rust rules.
- `skills/`: synchronized Claude-native copies of portable skills.
- `hooks/`: tested `PreToolUse` checks for destructive commands and sensitive
  file access.
- `output-styles/`: optional style location, intentionally empty except for
  guidance.
- `commands/`: compatibility note for the legacy command location.

Root `.mcp.json` is deliberately empty. `docs/mcp.md` defines the review process
for any future server.

## Delivery governance

### `.github/`

- `ISSUE_TEMPLATE/`: structured agent task, bug, and feature forms.
- `pull_request_template.md`: acceptance-criteria mapping, validation evidence,
  security impact, compatibility impact, dependency review, and AI-assistance
  disclosure.
- `CODEOWNERS`: owner review for agent governance, workflows, project contracts,
  ADRs, and repository-policy tooling.
- `dependabot.yml`: dependency updates for GitHub Actions in template state; the
  initializer adds the selected stack ecosystem.
- `workflows/policy.yml`: repository policy, configuration, skill-sync, and
  secret-name checks.
- `workflows/ci.yml`: template-tool test suite; replaced with stack CI during
  initialization.
- disabled workflow examples: opt-in CodeQL, dependency review, and release
  automation that require repository-specific review before activation.

### `ops/github/`

Declarative labels and a default-branch ruleset plus a README explaining how to
preview or apply them through `scripts/configure_github.py`. Settings are kept
separate because creating a repository from a GitHub template does not imply
that all repository-level settings were copied.

## Project knowledge

- `docs/architecture.md`: system context, components, data flow, interfaces, and
  deployment model.
- `docs/quality.md`: quality attributes and required evidence.
- `docs/threat-model.md`: assets, actors, trust boundaries, threats, and
  mitigations.
- `docs/agent-operating-model.md`: role selection, delegation, handoffs, and
  human-control boundaries.
- `docs/claude-code.md`, `docs/codex.md`, `docs/mcp.md`: vendor runtime and tool
  integration details.
- `docs/repository-governance.md`: ownership, protected changes, and required
  checks.
- `docs/blueprints.md`: manifest contract and extension procedure.
- `docs/adr/`: durable architectural decisions.
- `docs/plans/`: substantial implementation plans.
- `docs/runbooks/`: repeatable release and incident-response procedures.

## Blueprints

Every stack directory under `blueprints/` contains:

1. `blueprint.json`, declaring its name, purpose, exact setup/format/lint/type
   check/test/build/verify commands, and intentional overwrite paths; and
2. `files/`, a project-root-relative tree rendered by the initializer.

Included blueprints:

| Blueprint | Generated implementation baseline |
|---|---|
| `generic` | Language-neutral source and verification guidance |
| `python` | `pyproject.toml`, `src` layout, typed CLI, Ruff, mypy, pytest, build, CI, Dependabot |
| `typescript` | strict TypeScript, ESLint, Prettier, Vitest, build config, CI, Dependabot |
| `go` | module, CLI, internal package, tests, gofmt checker, CI, Dependabot |
| `rust` | Cargo package, library and binary, tests, rustfmt, Clippy, CI, Dependabot |

`blueprints/_shared/README.md.tpl` becomes the initialized project's README.
`licenses/` supplies rendered MIT, Apache-2.0, and proprietary choices.

## Tooling and tests

| Path | Purpose |
|---|---|
| `scripts/template/init_project.py` | Guarded interactive/non-interactive project initialization, dry-run, placeholder rendering, blueprint application, and template-asset cleanup |
| `scripts/verify_repository.py` | Validates template and initialized states, Codex/Claude controls, skills, MCP registry, workflows, secret-file names, and Python tooling |
| `scripts/validate_blueprints.py` | Initializes every blueprint in an isolated temporary copy and validates generated metadata and files |
| `scripts/sync_agent_skills.py` | Synchronizes or checks canonical and Claude skill copies |
| `scripts/configure_github.py` | Previews or applies labels and a ruleset through GitHub CLI |
| `scripts/render_tree.py` | Regenerates `TREE.md` deterministically |
| `tests/template_tools/` | Hook, initializer, blueprint, synchronization, and repository-verifier tests |

## Generated project lifecycle

1. The user selects a blueprint and runs the initializer.
2. The initializer refuses unexpected overwrites unless `--force` is explicit.
3. Paths and UTF-8 content are rendered from declared placeholders.
4. CI, Dependabot, license, README, Makefile, commands, and project metadata are
   generated.
5. `.template-state.json` is replaced by `.project.json`.
6. Template-only blueprints, license sources, initializer tests, and initializer
   code are removed unless `--keep-template-assets` is supplied.
7. The initialized repository is verified without installing dependencies or
   publishing Git/GitHub changes.
