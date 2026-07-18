# Security Policy

## Supported versions

Until the project defines a release policy, security fixes are applied to the
current default branch only.

## Reporting a vulnerability

Do not open a public issue for a suspected vulnerability. Use GitHub private
vulnerability reporting when enabled, or contact the repository owner through a
private channel documented in the repository profile.

Include a concise description, affected versions or commits, reproduction
steps, impact, and any proposed mitigation. Do not include real credentials,
personal data, or destructive proof-of-concept material.

## Response expectations

The maintainer should acknowledge a report, assess severity and exposure,
coordinate remediation, add regression tests, and publish an advisory when
appropriate. Timelines depend on impact and maintainer availability.

## Agent handling rules

AI agents must not access real secret files, exfiltrate repository content, run
unreviewed exploit code, or publish vulnerability details. Security-sensitive
changes require human review and validation in an isolated environment.
