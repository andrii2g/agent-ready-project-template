---
paths:
  - ".github/workflows/**/*.yml"
  - ".github/workflows/**/*.yaml"
---

# GitHub Actions rules

- Set explicit least-privilege `permissions`.
- Do not expose secrets to untrusted pull-request code.
- Prefer immutable action references or exact release tags approved by policy.
- Keep required job names stable when branch rules depend on them.
- Add timeouts to jobs that can hang.
- Treat workflow changes as security-sensitive and require owner review.
