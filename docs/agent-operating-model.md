# Agent Operating Model

## Roles

The template uses four execution roles and one optional coordinator:

1. **Repository mapper** traces relevant code paths and dependencies without
   making changes.
2. **Change worker** implements a narrow, accepted plan.
3. **Test verifier** runs checks, adds narrowly scoped missing coverage when
   requested, and reports reproducible evidence.
4. **Risk reviewer** independently reviews correctness, security, compatibility,
   operations, and test gaps.
5. **Coordinator** delegates bounded tasks and reconciles their results.

## Recommended sequence

For a risky feature or defect:

```text
repo-mapper -> change-worker -> test-verifier -> risk-reviewer
```

Small documentation changes do not require a multi-agent workflow. Delegation
should reduce context noise or enable independent parallel analysis, not create
ceremony.

## Handoffs

Each role should return a compact structured handoff containing relevant files,
findings or changes, assumptions, commands run, observed results, and unresolved
risk. The parent agent must inspect the final diff and remains accountable for
the final response.

## Human control points

Humans retain control of permission expansion, new production dependencies,
public contract changes, migrations, release publication, merges, deployments,
destructive operations, and changes to agent governance.
