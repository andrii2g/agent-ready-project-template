---
paths:
  - "**/*.{ts,tsx,js,mjs,cjs}"
  - "package.json"
  - "tsconfig*.json"
---

# TypeScript and JavaScript rules

- Avoid `any`; validate unknown external data before narrowing.
- Keep async errors observable and avoid unhandled promises.
- Preserve module and runtime compatibility declared by the project.
- Add tests for public behavior, validation failures, and edge cases.
