---
paths:
  - "**/*.py"
  - "pyproject.toml"
---

# Python rules

- Use type hints for public functions and non-obvious data structures.
- Prefer explicit exceptions and narrow error handling.
- Keep import-time behavior side-effect free.
- Use `pathlib` and context managers for filesystem work.
- Add pytest coverage for public behavior and regressions.
