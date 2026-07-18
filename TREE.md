# Repository Tree

```text
agent-ready-project-template/
├── .agents/
│   ├── skills/
│   │   ├── bootstrap-project/
│   │   │   └── SKILL.md
│   │   ├── implement-change/
│   │   │   └── SKILL.md
│   │   ├── plan-change/
│   │   │   └── SKILL.md
│   │   ├── review-change/
│   │   │   └── SKILL.md
│   │   ├── verify-change/
│   │   │   └── SKILL.md
│   │   └── write-adr/
│   │       └── SKILL.md
│   └── README.md
├── .claude/
│   ├── agents/
│   │   ├── change-worker.md
│   │   ├── coordinator.md
│   │   ├── repo-mapper.md
│   │   ├── risk-reviewer.md
│   │   └── test-verifier.md
│   ├── commands/
│   │   └── README.md
│   ├── hooks/
│   │   ├── guard_command.py
│   │   ├── protect_sensitive_files.py
│   │   └── README.md
│   ├── output-styles/
│   │   └── README.md
│   ├── rules/
│   │   ├── 00-security.md
│   │   ├── 10-testing.md
│   │   ├── docs.md
│   │   ├── github-actions.md
│   │   ├── go.md
│   │   ├── python.md
│   │   ├── rust.md
│   │   └── typescript.md
│   ├── skills/
│   │   ├── bootstrap-project/
│   │   │   └── SKILL.md
│   │   ├── implement-change/
│   │   │   └── SKILL.md
│   │   ├── plan-change/
│   │   │   └── SKILL.md
│   │   ├── review-change/
│   │   │   └── SKILL.md
│   │   ├── verify-change/
│   │   │   └── SKILL.md
│   │   └── write-adr/
│   │       └── SKILL.md
│   ├── README.md
│   ├── settings.json
│   └── settings.local.json.example
├── .codex/
│   ├── agents/
│   │   ├── change-worker.toml
│   │   ├── repo-mapper.toml
│   │   ├── risk-reviewer.toml
│   │   └── test-verifier.toml
│   ├── rules/
│   │   └── default.rules
│   ├── config.toml
│   └── README.md
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── agent-task.yml
│   │   ├── bug.yml
│   │   ├── config.yml
│   │   └── feature.yml
│   ├── workflows/
│   │   ├── ci.yml
│   │   ├── codeql.yml.disabled
│   │   ├── dependency-review.yml.disabled
│   │   ├── policy.yml
│   │   └── release.yml.disabled
│   ├── CODEOWNERS
│   ├── dependabot.yml
│   ├── pull_request_template.md
│   └── release.yml
├── blueprints/
│   ├── _shared/
│   │   └── README.md.tpl
│   ├── generic/
│   │   ├── files/
│   │   │   ├── .github/
│   │   │   │   ├── workflows/
│   │   │   │   │   └── ci.yml
│   │   │   │   └── dependabot.yml
│   │   │   ├── src/
│   │   │   │   └── README.md
│   │   │   └── tests/
│   │   │       └── README.md
│   │   └── blueprint.json
│   ├── go/
│   │   ├── files/
│   │   │   ├── .github/
│   │   │   │   ├── workflows/
│   │   │   │   │   └── ci.yml
│   │   │   │   └── dependabot.yml
│   │   │   ├── cmd/
│   │   │   │   └── {{PROJECT_SLUG}}/
│   │   │   │       └── main.go
│   │   │   ├── internal/
│   │   │   │   └── app/
│   │   │   │       ├── greet.go
│   │   │   │       └── greet_test.go
│   │   │   ├── scripts/
│   │   │   │   └── check_gofmt.py
│   │   │   └── go.mod
│   │   └── blueprint.json
│   ├── python/
│   │   ├── files/
│   │   │   ├── .github/
│   │   │   │   ├── workflows/
│   │   │   │   │   └── ci.yml
│   │   │   │   └── dependabot.yml
│   │   │   ├── src/
│   │   │   │   └── {{PACKAGE_NAME}}/
│   │   │   │       ├── __init__.py
│   │   │   │       ├── cli.py
│   │   │   │       └── py.typed
│   │   │   ├── tests/
│   │   │   │   └── test_cli.py
│   │   │   ├── .python-version
│   │   │   └── pyproject.toml
│   │   └── blueprint.json
│   ├── rust/
│   │   ├── files/
│   │   │   ├── .github/
│   │   │   │   ├── workflows/
│   │   │   │   │   └── ci.yml
│   │   │   │   └── dependabot.yml
│   │   │   ├── src/
│   │   │   │   ├── lib.rs
│   │   │   │   └── main.rs
│   │   │   ├── tests/
│   │   │   │   └── greet.rs
│   │   │   ├── Cargo.toml
│   │   │   └── rust-toolchain.toml
│   │   └── blueprint.json
│   └── typescript/
│       ├── files/
│       │   ├── .github/
│       │   │   ├── workflows/
│       │   │   │   └── ci.yml
│       │   │   └── dependabot.yml
│       │   ├── docs/
│       │   │   └── package-lock.md
│       │   ├── src/
│       │   │   └── index.ts
│       │   ├── tests/
│       │   │   └── index.test.ts
│       │   ├── .nvmrc
│       │   ├── .prettierignore
│       │   ├── eslint.config.mjs
│       │   ├── package.json
│       │   ├── tsconfig.build.json
│       │   └── tsconfig.json
│       └── blueprint.json
├── docs/
│   ├── adr/
│   │   ├── 0000-template.md
│   │   └── README.md
│   ├── plans/
│   │   ├── README.md
│   │   └── TEMPLATE.md
│   ├── runbooks/
│   │   ├── incident-response.md
│   │   ├── README.md
│   │   └── release.md
│   ├── agent-configuration-matrix.md
│   ├── agent-operating-model.md
│   ├── architecture.md
│   ├── blueprints.md
│   ├── claude-code.md
│   ├── codex.md
│   ├── mcp.md
│   ├── quality.md
│   ├── repository-governance.md
│   ├── repository-structure.md
│   └── threat-model.md
├── licenses/
│   ├── Apache-2.0.txt
│   ├── MIT.txt
│   └── Proprietary.txt
├── ops/
│   └── github/
│       ├── labels.yml
│       ├── main-ruleset.json
│       └── README.md
├── scripts/
│   ├── template/
│   │   └── init_project.py
│   ├── configure_github.py
│   ├── render_tree.py
│   ├── sync_agent_skills.py
│   ├── validate_blueprints.py
│   └── verify_repository.py
├── tests/
│   └── template_tools/
│       ├── __init__.py
│       ├── test_claude_hooks.py
│       ├── test_initializer.py
│       ├── test_sync_agent_skills.py
│       └── test_verify_repository.py
├── .editorconfig
├── .env.example
├── .gitattributes
├── .gitignore
├── .mcp.json
├── .template-state.json
├── AGENTS.md
├── CHANGELOG.md
├── CLAUDE.local.md.example
├── CLAUDE.md
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── LICENSE
├── Makefile
├── PROJECT.md
├── README.md
├── ROADMAP.md
├── SECURITY.md
├── TREE.md
└── VERSION
```
