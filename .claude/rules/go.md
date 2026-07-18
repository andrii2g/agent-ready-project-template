---
paths:
  - "**/*.go"
  - "go.mod"
  - "go.sum"
---

# Go rules

- Return or wrap errors with useful context; do not silently discard them.
- Pass `context.Context` through operations that can block or be cancelled.
- Keep package APIs small and avoid unnecessary interfaces.
- Run gofmt, go vet, and relevant tests.
