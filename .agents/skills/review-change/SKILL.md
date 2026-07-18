---
name: review-change
description: Independently review a change for correctness, security, regressions, compatibility, operations, and missing tests.
---

# Review change

Lead with concrete findings ordered by severity. For each finding include the
location, affected behavior, reasoning or reproduction, impact, and the smallest
credible correction or missing test.

Review:

- acceptance-criteria coverage;
- correctness and failure handling;
- authentication, authorization, secrets, privacy, and trust boundaries;
- data loss, migrations, concurrency, and irreversible operations;
- backward compatibility and public interfaces;
- dependency and build-chain risk;
- deployment, observability, and recovery;
- test quality and false confidence.

Do not make code changes while acting as an independent reviewer. Avoid
style-only comments unless they conceal a material defect.
