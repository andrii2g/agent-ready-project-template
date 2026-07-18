# Testing rules

- Add regression coverage for defects and behavior-focused tests for new work.
- Run targeted checks before the full configured verification command.
- Do not weaken, skip, or rewrite a check merely to obtain a pass.
- Isolate time, randomness, network, filesystem, and external services where
  they would make tests nondeterministic.
- Report unavailable or skipped checks as residual risk, not success.
