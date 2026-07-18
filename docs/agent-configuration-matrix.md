# Agent Configuration Matrix

This matrix shows where each concern is expressed and which layer can actually
enforce it. Prose guides model behavior; deterministic controls and repository
policy provide stronger boundaries.

| Concern | Shared contract | Codex | Claude Code | GitHub / deterministic layer |
|---|---|---|---|---|
| Product requirements | `PROJECT.md` | Reads shared files | `CLAUDE.md` imports `AGENTS.md`; reads project docs | Issue forms and PR acceptance mapping |
| Working method | `AGENTS.md` | Native instruction discovery | Imported through `CLAUDE.md` | PR template and review |
| Repeatable workflows | `.agents/skills/` | Portable skill discovery | Mirrored `.claude/skills/` | CI executes exact checks |
| Specialized roles | Role guidance in `AGENTS.md` | `.codex/agents/*.toml` | `.claude/agents/*.md` | CODEOWNERS keeps humans accountable |
| Filesystem boundary | Least-privilege instruction | Workspace-write sandbox | Sandbox and file permission rules | Runner/workstation OS controls |
| Network boundary | Ask before trust expansion | Sandbox network disabled | No MCP/plugin/server configured by default | Firewall, managed policy, CI permissions |
| Secret access | Never read or expose secrets | Sandbox plus repository instructions | Deny rules plus sensitive-file hook | Gitignore, secret scanning, environment controls |
| Destructive commands | Explicit prohibitions | `.codex/rules/default.rules` | `guard_command.py` hook and deny rules | Branch rules, repository permissions, human approval |
| Test requirements | Definition of done | Verification subagent | Verification subagent and testing rules | CI status checks |
| Security review | Trigger list and threat model | Risk reviewer | Risk reviewer and security rule | CODEOWNERS, PR review, optional CodeQL |
| Publishing / merge / deploy | Human-controlled | Prompt/forbidden rules | Ask/deny rules and hook | GitHub rulesets and environment approvals |
| Personal preferences | Not committed | User-level Codex configuration | `CLAUDE.local.md` and `.claude/settings.local.json` | Local machine only |
| Organization policy | Referenced, not embedded | Managed requirements/configuration | Managed settings/hooks | Organization rulesets and enterprise controls |

## Precedence and duplication policy

- Shared engineering rules are written once in `AGENTS.md`.
- Claude-specific behavior is additive in `CLAUDE.md` and `.claude/`.
- Portable procedures are authored once under `.agents/skills/` and synchronized.
- Tool permission files should contain only tool-runtime controls, not a second
  product specification.
- A mandatory rule should have an enforceable counterpart where practical:
  permissions, hooks, CI checks, branch rules, or operating-system policy.
