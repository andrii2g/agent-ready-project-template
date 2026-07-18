---
name: implement-change
description: Implement an accepted repository change with narrow scope, tests, documentation, and explicit validation evidence.
---

# Implement change

1. Confirm the accepted criteria and applicable plan.
2. Inspect affected files before editing.
3. Make the smallest change that satisfies the criteria.
4. Preserve public contracts unless change is explicitly authorized.
5. Validate input and error behavior at trust boundaries.
6. Add or update behavior-focused tests.
7. Update documentation and examples when observable behavior changes.
8. Run targeted checks and inspect the diff.
9. Hand off exact files changed, tests added, commands run, and residual risk.

Stop and request a decision before adding a production dependency, changing a
public contract, applying a migration, or expanding permissions.
