# Codex Configuration

`AGENTS.md` contains shared behavioral guidance. `.codex/config.toml` contains
project runtime defaults, while `.codex/agents/` defines narrow custom roles and
`.codex/rules/` contains command policies for execution outside the sandbox.

The project configuration intentionally omits a model and provider. Users and
organizations should select those in their own Codex configuration. The
workspace-write sandbox permits repository edits but disables outbound network
access. Approval remains on request, and login-shell behavior is disabled.

Codex project configuration is loaded only after the repository is trusted.
Rules are an additional guardrail and should not be treated as a replacement
for sandboxing, GitHub protections, or human review.
