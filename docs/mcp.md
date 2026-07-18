# Model Context Protocol Configuration

The repository contains an active, empty `.mcp.json`:

```json
{
  "mcpServers": {}
}
```

This makes the project-scoped MCP location explicit while granting no external
tool or data access. MCP servers expand the trust boundary and must be reviewed
before they are added.

## Review checklist

Before enabling a server, document and review:

1. the server owner, source, license, and pinned version;
2. the exact executable or remote endpoint;
3. every tool, resource, and prompt the server exposes;
4. filesystem, process, network, and credential access;
5. whether tool results can contain untrusted instructions;
6. data classification, retention, and transmission behavior;
7. least-privilege credentials and their rotation procedure;
8. timeout, failure, revocation, and incident-response behavior;
9. the human approvals required for state-changing tools; and
10. a reproducible test proving the configuration works as intended.

Use environment-variable references rather than literal secrets. Never commit
API keys, access tokens, private keys, passwords, or cloud credentials to
`.mcp.json`, `.claude/settings.json`, or any other repository file.

## Example shape

The following is documentation only and is not enabled by the template:

```json
{
  "mcpServers": {
    "example-read-only": {
      "command": "example-mcp-server",
      "args": ["--read-only"],
      "env": {
        "EXAMPLE_TOKEN": "${EXAMPLE_TOKEN}"
      }
    }
  }
}
```

After adding a server, update `docs/threat-model.md`, verify the server in an
isolated environment, and require owner review for the resulting `.mcp.json`
change.
