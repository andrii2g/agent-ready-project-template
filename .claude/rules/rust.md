---
paths:
  - "**/*.rs"
  - "Cargo.toml"
  - "Cargo.lock"
---

# Rust rules

- Avoid `unsafe` unless the task explicitly requires it and the safety
  invariants are documented and tested.
- Use structured error types at library boundaries.
- Do not use `unwrap` or `expect` on recoverable production paths.
- Run rustfmt, Clippy with warnings denied, and tests.
