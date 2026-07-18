# Quality Strategy

## Verification layers

- Static formatting and linting.
- Type or compile-time checks where applicable.
- Fast unit tests for local behavior.
- Integration tests at component boundaries.
- End-to-end or hardware-in-the-loop checks for critical user journeys.
- Security and dependency review for relevant changes.

## Test qualities

Tests should be deterministic, isolated, readable, and proportional to risk.
Prefer stable public behavior over private implementation details. Record
required external services and fixtures explicitly.

## CI expectations

CI runs with least-privilege permissions, avoids repository secrets on
untrusted pull-request code, and treats skipped required checks as failures.
Generated projects should keep the `Policy` and `CI` job names stable when the
GitHub ruleset requires them.

## Release quality

A release should have a reviewed change set, passing required checks, updated
changelog and documentation, rollback or recovery guidance, and explicit human
approval.
