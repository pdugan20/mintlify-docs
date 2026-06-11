# mintlify-docs

[![CI](https://github.com/pdugan20/mintlify-docs/workflows/CI/badge.svg)](https://github.com/pdugan20/mintlify-docs/actions)
[![Release](https://img.shields.io/github/v/release/pdugan20/mintlify-docs?logo=github)](https://github.com/pdugan20/mintlify-docs/releases/latest)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?logo=opensourceinitiative&logoColor=white)](https://opensource.org/licenses/MIT)

A Claude Code plugin for building and maintaining [Mintlify](https://mintlify.com)
documentation sites in a consistent house style.

It **layers on the official [`mintlify`](https://claude.com/plugins/mintlify)
plugin**, declared as a manifest dependency: that plugin owns Mintlify
mechanics (component syntax, `docs.json` schema, OpenAPI). This one owns the
editorial decisions: information architecture, voice, callout discipline,
scaffolding, drift-checked references, and changelog style.

## Skills

| Skill | Command | Description |
| ----- | ------- | ----------- |
| Scaffold a site | `/scaffold-mintlify-site` | Stand up a `docs-mintlify/` tree with a topic-grouped IA, `docs.json`, generators, and sync CI |
| Review docs | `/review-docs` | Walk pages in nav order against the content playbook and pre-launch checklist |
| Write changelog | `/changelog-writer` | Write and audit reader-facing `<Update>` entries |
| Document a reference | `/document-reference` | Generate drift-checked CLI / MCP / API reference pages from source |

The shared editorial playbook lives in [`references/best-practices.md`](references/best-practices.md);
every skill cites it rather than restating it.

## Installation

### From the marketplace

```text
/plugin marketplace add pdugan20/pdugan20-plugins
/plugin install mintlify-docs@pdugan20-plugins
```

### Trial without the marketplace

Each release attaches the plugin as a zip, so you can try it for a single
session without registering anything:

```bash
claude --plugin-url https://github.com/pdugan20/mintlify-docs/releases/latest/download/mintlify-docs-plugin.zip
```

### For development

```bash
claude --plugin-dir /path/to/mintlify-docs
```

## Requirements

- **The official `mintlify` plugin** (a Claude Code plugin, distinct from the
  CLI below). Declared as a manifest dependency, so Claude Code flags it on
  install if it is missing; it does not install automatically. To install it:

  ```text
  /plugin install mintlify@claude-plugins-official
  ```

- **The [Mintlify CLI](https://www.npmjs.com/package/mint)** (`npm i -g mint`)
  for the preview and link-check workflows the skills wire up (`mint dev`,
  `mint broken-links`).
- **A Python or Node toolchain** in the target project, for the generated
  reference scripts.

The skills themselves have no other dependencies.
