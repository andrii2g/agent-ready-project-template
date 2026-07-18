# Codex Project Configuration

- `config.toml` sets conservative project-scoped approval and sandbox defaults.
- `agents/` contains standalone custom agent definitions discovered by Codex.
- `rules/default.rules` prompts for or forbids high-risk commands outside the
  sandbox.

The configuration deliberately does not select a model, provider, credentials,
telemetry destination, or MCP server. Those choices belong to user or
organization configuration.
