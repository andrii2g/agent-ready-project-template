# Repository Governance

## Ownership

`CODEOWNERS` assigns explicit review responsibility for agent settings,
workflows, policy scripts, and project contracts. Replace the template owner
during initialization.

## Default branch

The recommended ruleset blocks deletion and force pushes, requires pull
requests, at least one approving review, resolved conversations, and successful
`Policy` and `CI` checks. Review the JSON before applying it because feature
availability varies by GitHub plan and repository type.

## Automation

Workflows use read-only permissions unless a job requires more. Optional
security and release workflows are shipped with a `.disabled` suffix to avoid
surprising failures or publication. Enable them only after reviewing languages,
permissions, billing, and branch protections.

## Agent governance

Changes to agent instructions or permissions are code changes. They require an
issue or clear task, an explanation of the new capability or restriction,
validation of the configuration, and human review by the configured owner.
