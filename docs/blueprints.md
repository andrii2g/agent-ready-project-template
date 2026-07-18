# Blueprints

A blueprint is a declarative manifest plus a file tree copied into the project
by `scripts/template/init_project.py`.

## Manifest fields

- `name`: stable command-line identifier.
- `description`: human-facing purpose.
- `commands`: exact setup, format, lint, type-check, test, build, and verify
  commands inserted into project metadata and `AGENTS.md`.
- `overwrites`: paths the initializer may intentionally replace.

## File substitution

The initializer replaces declared tokens in UTF-8 text files and in path names.
The primary tokens are project name, slug, package name, description, owner,
author, email, year, license identifier, and project commands.

## Adding a blueprint

1. Copy an existing blueprint directory.
2. Use a unique lowercase name.
3. Add a valid `blueprint.json`.
4. Keep the generated baseline minimal and independently useful.
5. Add or update template-tool tests.
6. Run `make verify-template`.
7. Document runtime and package-manager assumptions.

Do not embed credentials, organization-specific endpoints, or mutable production
configuration in a blueprint.
