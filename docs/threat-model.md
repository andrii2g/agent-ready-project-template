# Threat Model

## Protected assets

List credentials, personal data, source code, build outputs, signing material,
production resources, hardware control surfaces, and availability requirements.

## Actors

Identify legitimate users and operators, compromised dependencies, malicious
contributors, untrusted input providers, and compromised agent tools.

## Trust boundaries

Document boundaries between users, agents, repository content, CI, package
registries, external services, devices, and production environments.

## Principal threats

- Secret disclosure through files, logs, prompts, or generated artifacts.
- Prompt injection in issues, source comments, logs, documents, or tool output.
- Dependency or build-chain compromise.
- Unauthorized code, data, infrastructure, or hardware changes.
- Destructive commands and irreversible migrations.
- Excessive network or filesystem access.
- Insecure parsing, command construction, serialization, or upload handling.

## Baseline mitigations

Use least privilege, deny common secret paths, require review for sensitive
operations, isolate untrusted input, pin and review dependencies, validate
inputs at boundaries, maintain audit evidence, and test recovery paths.

## Review triggers

Update this model when protected assets, data classes, trust boundaries,
external integrations, deployment topology, authentication, authorization, or
agent capabilities change.
