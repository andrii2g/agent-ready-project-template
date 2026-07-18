# Claude Code Project Assets

| Path | Purpose |
|---|---|
| `../CLAUDE.md` | Imports the canonical `AGENTS.md` contract and adds Claude-specific routing |
| `settings.json` | Shared permissions, sandbox configuration, and deterministic hooks |
| `settings.local.json.example` | Example personal override; the real local file is ignored |
| `agents/` | Project-scoped custom subagents for mapping, implementation, verification, review, and coordination |
| `rules/` | Modular and path-scoped project instructions |
| `skills/` | Synchronized copies of canonical `.agents/skills/` definitions |
| `hooks/` | Deterministic policy checks invoked before sensitive tool use |
| `output-styles/` | Optional project output styles; none is enabled by default |
| `commands/` | Legacy command-location guidance; skills are preferred |
| `../.mcp.json` | Active, empty project MCP registry |

`CLAUDE.md` lives at the repository root so it can import `AGENTS.md` through a
portable relative path. Do not add a second `.claude/CLAUDE.md` unless its load
and precedence effects are intentional.

For the complete operating model, read `../docs/claude-code.md` and
`../docs/mcp.md`.
