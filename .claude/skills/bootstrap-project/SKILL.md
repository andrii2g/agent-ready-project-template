---
name: bootstrap-project
description: Initialize an unconfigured repository created from this template using explicit project metadata and a selected blueprint.
---

# Bootstrap project

Use this skill only while `.template-state.json` exists.

1. Read `README.md`, `docs/blueprints.md`, and the selected blueprint manifest.
2. Collect explicit project name, description, owner, author, license, and
   blueprint values. Do not guess identity or licensing decisions.
3. Preview with `python scripts/template/init_project.py ... --dry-run`.
4. Review paths that will be overwritten or removed.
5. Run initialization without `--dry-run` only after the values are accepted.
6. Review `PROJECT.md`, `AGENTS.md`, `.project.json`, CI, Dependabot, and
   CODEOWNERS.
7. Run `python scripts/verify_repository.py`.
8. Report generated files and any manual decisions still required.

Never create a remote repository, commit, push, install dependencies, or apply
GitHub settings as part of initialization unless explicitly requested.
