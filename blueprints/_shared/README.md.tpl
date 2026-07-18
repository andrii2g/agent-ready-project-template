# {{PROJECT_NAME}}

{{PROJECT_DESCRIPTION}}

## Status

This repository was initialized from Agent-Ready Project Template `v{{TEMPLATE_VERSION}}`
using the `{{PROJECT_SLUG}}` project identity and the selected stack blueprint.

## Quick start

```bash
{{SETUP_COMMAND}}
{{VERIFY_COMMAND}}
```

## Project commands

| Operation | Command |
|---|---|
| Setup | `{{SETUP_COMMAND}}` |
| Format check | `{{FORMAT_COMMAND}}` |
| Lint | `{{LINT_COMMAND}}` |
| Type check | `{{TYPECHECK_COMMAND}}` |
| Test | `{{TEST_COMMAND}}` |
| Build | `{{BUILD_COMMAND}}` |
| Full verification | `{{VERIFY_COMMAND}}` |

## Working with AI coding agents

- `AGENTS.md` is the canonical repository-wide engineering contract.
- `CLAUDE.md` imports that contract and adds Claude Code routing guidance.
- `.codex/` contains Codex configuration, custom agents, and command rules.
- `.claude/` contains Claude Code settings, subagents, path-scoped rules,
  portable skills, and deterministic hooks.
- `PROJECT.md` defines the product contract and should be completed before
  substantial implementation work.
- Architecture decisions belong in `docs/adr/`; execution plans belong in
  `docs/plans/`.

Repository configuration is a baseline, not a substitute for human review or
organization-level managed policy. Do not place credentials in project files or
agent configuration.

## Documentation

- [Project contract](PROJECT.md)
- [Architecture](docs/architecture.md)
- [Quality model](docs/quality.md)
- [Threat model](docs/threat-model.md)
- [Contributing](CONTRIBUTING.md)
- [Security policy](SECURITY.md)

## License

{{LICENSE_ID}}. See `LICENSE`.
