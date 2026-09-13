# Threat model

Generated code, repository contents, test fixtures, compiler output, and model
responses are untrusted. Primary risks are host escape, credential theft,
network exfiltration, resource exhaustion, destructive patches, prompt
injection, dependency confusion, and sensitive data leaking into traces.

Required controls:

- Dispatch only checked-in case IDs to disposable GitHub-hosted runners.
  Workflows use read-only repository permissions and checkout with credential
  persistence disabled.
- Execute only in an ephemeral, unprivileged container with no host Docker
  socket, no secrets, no network by default, a read-only base image, dropped
  capabilities, and CPU/memory/process/time limits.
- Mount only a disposable repository copy. Never mount the home directory,
  SSH agent, cloud credentials, package-manager credentials, or production data.
- Validate patch paths, reject traversal/symlinks outside the workspace, cap
  patch size, and preserve an immutable input revision.
- Allowlist validation commands; do not pass model text through a shell.
- Enforce attempt, token, cost, wall-clock, output, and artifact-size budgets.
- Redact credentials and personal data before logs or Weave traces; use
  least-privilege, short-lived provider tokens.
- Pin trusted images and dependencies, scan them, and retain an audit trail.

The sandbox boundary reduces risk but is not proof against kernel or container
runtime vulnerabilities. GitHub Actions metadata and usage limits are also
external dependencies. Generated code never runs on a developer laptop or in
the Codespace.
