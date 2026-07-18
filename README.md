# Agent-Ready Project Template

A secure, language-agnostic GitHub template for projects that will be designed,
implemented, tested, and reviewed with AI coding agents.

The template provides one shared engineering contract in `AGENTS.md`, a thin
Claude Code adapter in `CLAUDE.md`, tool-specific controls under `.codex/` and
`.claude/`, portable skills, GitHub governance, and selectable project
blueprints.

## Included agent environments

| Environment | Project assets |
|---|---|
| OpenAI Codex | `.codex/config.toml`, custom agents, command rules, `AGENTS.md`, `.agents/skills/` |
| Claude Code | `CLAUDE.md`, `.claude/settings.json`, custom agents, rules, hooks, and mirrored skills |
| Other agents | `AGENTS.md`, `PROJECT.md`, architecture and quality documentation |

No external MCP server, plugin, credential, or network endpoint is enabled by
default. The committed `.mcp.json` registry is intentionally empty.

## Create a project from the template

1. Create a repository from this GitHub template or extract the ZIP.
2. Run the initializer from the repository root:

```bash
python scripts/template/init_project.py \
  --name "Example Service" \
  --description "A concise description of the project" \
  --owner your-github-handle \
  --blueprint python \
  --license MIT
```

3. Review `PROJECT.md`, `AGENTS.md`, `.claude/settings.json`, and the generated
   stack files.
4. Run the repository checks:

```bash
python scripts/verify_repository.py
```

5. Optionally preview GitHub repository settings:

```bash
python scripts/configure_github.py --repo owner/repository
```

Add `--apply` only after reviewing the printed operations.

## Blueprint choices

| Blueprint | Intended use | Generated baseline |
|---|---|---|
| `generic` | Documentation, hardware, research, infrastructure, mixed projects | `src/` and `tests/` guidance plus policy CI |
| `python` | Libraries, CLIs, services, automation | `pyproject.toml`, Ruff, mypy, pytest, build |
| `typescript` | Node.js libraries, CLIs, services | TypeScript, ESLint, Prettier, Vitest |
| `go` | CLIs and services | Go modules, `go vet`, tests, build |
| `rust` | CLIs, libraries, systems tools | Cargo, rustfmt, Clippy, tests |

The initializer is non-destructive by default. It refuses to overwrite
unexpected files unless `--force` is supplied. Use `--dry-run` to inspect the
planned changes and `--keep-template-assets` to retain the blueprints and
template-tool tests.

## Important files

- `AGENTS.md`: canonical repository instructions for coding agents.
- `CLAUDE.md`: imports `AGENTS.md` and adds Claude-specific routing guidance.
- `PROJECT.md`: product and technical contract.
- `.codex/`: Codex sandbox, approvals, custom agents, and command rules.
- `.claude/`: Claude permissions, sandbox settings, agents, rules, skills, hooks, and optional output-style guidance.
- `.mcp.json`: active but empty project-scoped MCP registry.
- `.agents/skills/`: canonical portable skill definitions.
- `docs/repository-structure.md`: path-by-path lifecycle and responsibility reference.
- `docs/agent-configuration-matrix.md`: maps shared policy to Codex, Claude, and GitHub enforcement.
- `TREE.md`: generated full repository tree.

## Template development

Run the policy, skill synchronization, and unit tests, then validate every
blueprint in isolated generated repositories:

```bash
make verify-template
make validate-blueprints
```

The template tooling and its CI checks use only the Python standard library;
stack dependencies are installed only after a project blueprint is selected.

## Security posture

This repository is deliberately conservative:

- agents cannot read common secret files;
- destructive commands are denied or require approval;
- Codex network access is disabled inside its workspace-write sandbox;
- Claude Bash commands are sandboxed when the platform supports it;
- force pushes, repository deletion, infrastructure destruction, releases,
  deployments, and merges remain human-controlled operations;
- local settings and personal memories are ignored by Git.

Review all project-level settings before trusting a repository. Repository
configuration supplements, but does not replace, organization-level policy.

## License

The template defaults to MIT and can generate MIT, Apache-2.0, or proprietary
license text during initialization.
