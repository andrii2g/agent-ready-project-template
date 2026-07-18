---
name: verify-change
description: Verify a repository change with reproducible commands, targeted tests, full project checks, and honest reporting of blocked validation.
---

# Verify change

1. Map acceptance criteria to observable checks.
2. Run the smallest relevant tests first.
3. Run configured format, lint, type, test, build, and policy checks.
4. Inspect failures; do not weaken checks or substitute unrelated commands.
5. Confirm the final diff contains no secrets, caches, or unrelated changes.
6. Exercise important error and boundary paths where practical.
7. Report each command, exit status, meaningful output, skipped checks, and
   remaining uncertainty.

A skipped or unavailable check is not a pass.
