@AGENTS.md

# Claude Code adapter

Use `.claude/rules/` for path-specific guidance and `.claude/skills/` for
repeatable workflows. Prefer the matching custom subagent for bounded work:

- `repo-mapper` for read-only code-path discovery;
- `change-worker` for small implementation tasks;
- `test-verifier` for checks and reproducible evidence;
- `risk-reviewer` for independent correctness and security review;
- `coordinator` when running an explicitly orchestrated multi-agent task.

Treat `.agents/skills/` as the canonical skill source. The copies in
`.claude/skills/` must remain byte-for-byte synchronized by
`python scripts/sync_agent_skills.py --check`.

Do not add permissions to `.claude/settings.local.json` on the user's behalf.
Do not enable external MCP servers, plugins, or network domains without an
explicit task and review of the resulting trust boundary.
