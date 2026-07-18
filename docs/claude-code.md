# Claude Code Configuration

The repository uses Claude Code's project-scoped configuration locations while
keeping the shared engineering contract vendor-neutral.

## Instruction hierarchy

- `AGENTS.md` is the canonical repository-wide agent contract.
- Root `CLAUDE.md` imports `AGENTS.md` with `@AGENTS.md` and adds only
  Claude-specific routing guidance.
- `.claude/rules/` contains modular instructions. Language rules use `paths`
  frontmatter so they load only for matching files.
- `CLAUDE.local.md` is ignored and may contain a maintainer's private,
  machine-specific instructions. `CLAUDE.local.md.example` documents the shape.

Avoid copying shared rules into several files. Conflicting instructions waste
context and make agent behavior unpredictable.

## Settings and permissions

`.claude/settings.json` is committed project configuration. It provides:

- a conservative `default` permission mode;
- explicit allow rules for read-only Git inspection and template verification;
- approval gates for publishing, dependency mutation, infrastructure tools, and
  changes to agent-governance files;
- deny rules for common secret paths and destructive commands;
- Bash sandboxing where Claude Code supports it;
- disabled bypass-permissions mode;
- deterministic `PreToolUse` hooks; and
- disabled project auto-memory.

Personal approvals and experiments belong in `.claude/settings.local.json`,
which is ignored. Copy `.claude/settings.local.json.example` only when a local
override is genuinely needed. Do not commit the result.

Settings are a baseline, not an organization-wide enforcement mechanism.
Managed policy should impose any controls that collaborators must not be able to
override.

## Project subagents

`.claude/agents/` defines five bounded roles:

| Agent | Purpose | Default posture |
|---|---|---|
| `repo-mapper` | Trace code paths, interfaces, tests, and dependencies | Read-only planning |
| `change-worker` | Implement a small accepted change | Default permissions |
| `test-verifier` | Run checks and report reproducible evidence | Default permissions |
| `risk-reviewer` | Independently review correctness, security, and regressions | Read-only planning |
| `coordinator` | Orchestrate the other roles for genuinely multi-stage work | Planning only |

The parent agent remains accountable for scope, reconciliation, the final diff,
and validation.

## Skills

`.agents/skills/` is the canonical portable source. `.claude/skills/` contains
byte-for-byte copies for native Claude Code discovery. Run:

```bash
python scripts/sync_agent_skills.py --check
```

Use `python scripts/sync_agent_skills.py` after intentionally changing a
canonical skill.

## Hooks

The `PreToolUse` hooks in `.claude/hooks/` receive JSON on standard input and
return a structured denial only when a known high-risk command or sensitive
path is detected:

- `guard_command.py` blocks force pushes, hard resets, forced cleans,
  repository deletion, destructive infrastructure commands, host shutdown, and
  dangerous filesystem operations.
- `protect_sensitive_files.py` blocks file-tool access to environment files,
  credentials, private keys, and common secret directories while allowing
  sanitized examples.

Hooks use the exec form in `.claude/settings.json`, so project paths are passed
as exact arguments rather than shell-tokenized strings. They are tested under
`tests/template_tools/`.

## MCP and plugins

The project-scoped `.mcp.json` is active but empty. No MCP server, plugin,
credential, or remote endpoint is enabled by default. See `docs/mcp.md` before
expanding this trust boundary.

## Output styles and legacy commands

`.claude/output-styles/` documents the optional project style location but does
not install a style. `.claude/commands/` remains only as a compatibility note;
new repeatable workflows should be implemented as skills.

## Verification

After editing Claude configuration, run:

```bash
python scripts/verify_repository.py
python -m unittest discover -s tests/template_tools -v
```

Inside Claude Code, inspect `/status` to confirm the expected project settings
were loaded.
