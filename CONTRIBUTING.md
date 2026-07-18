# Contributing

## Before starting

Open or select an issue with clear acceptance criteria. For substantial work,
create a plan under `docs/plans/` before implementation.

## Development workflow

1. Create a focused branch.
2. Read `AGENTS.md`, `PROJECT.md`, and applicable nested instructions.
3. Make the smallest coherent change.
4. Add or update tests.
5. Run the commands listed in `AGENTS.md`.
6. Complete the pull-request template with validation evidence.

## Commits

Use concise imperative subjects. Keep unrelated changes in separate commits.
Do not include secrets, generated caches, editor state, or local agent settings.
AI-assisted commits remain the human author's responsibility.

## Pull requests

Pull requests should map changes to acceptance criteria, identify compatibility
and security effects, disclose dependency changes, and show exact verification
commands and results.

## Agent-governance changes

Changes under `.codex/`, `.claude/`, `.agents/`, `scripts/verify_repository.py`,
or protected GitHub workflows require explicit review from the configured code
owner. Explain why the policy is changing and how it was tested.
