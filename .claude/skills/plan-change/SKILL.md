---
name: plan-change
description: Produce a concise, evidence-based implementation plan for a risky, ambiguous, or multi-file repository change.
---

# Plan change

1. Restate the objective, acceptance criteria, and non-goals.
2. Inspect the real execution paths, interfaces, tests, and relevant decisions.
3. Identify assumptions and requirement conflicts.
4. Propose the smallest coherent change, naming affected files and interfaces.
5. Identify security, compatibility, data, operational, and dependency risks.
6. State human decisions or approvals required before implementation.
7. Define targeted and full verification commands.
8. Record rollback or recovery for irreversible or operational changes.

Write substantial plans from `docs/plans/TEMPLATE.md`. Do not edit product code
while operating in planning mode.
