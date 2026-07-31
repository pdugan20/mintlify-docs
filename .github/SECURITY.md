# Security Policy

## Supported Versions

No standalone release receives security updates. This repository is retained
only as migration and release history. The maintained skills live in
[`pdugan20/skills`](https://github.com/pdugan20/skills).

## Reporting a Vulnerability

Please do not report security vulnerabilities through public GitHub issues.

Report vulnerabilities against the maintained collection through its
[GitHub Security Advisories](https://github.com/pdugan20/skills/security/advisories/new).

Scope note: this plugin ships skill instructions, templates, and small
generator scripts that run in the user's own environment. The most relevant
vulnerability classes are prompt-injection vectors in skill content and
unsafe patterns in the bundled scripts (command injection, path traversal).
Reports in either category are welcome.

## What to Expect

Fixes are released from `pdugan20/skills`; this archived repository will not
receive patched standalone releases.
