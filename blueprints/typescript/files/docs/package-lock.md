# Package lock

Run `npm install` once after initialization, review the dependency graph, and
commit the generated `package-lock.json`. CI intentionally uses `npm ci` and
will fail until the lockfile is present, preserving reproducibility.
