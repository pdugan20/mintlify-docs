# mintlify-docs

[![CI](https://github.com/pdugan20/mintlify-docs/workflows/CI/badge.svg)](https://github.com/pdugan20/mintlify-docs/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?logo=opensourceinitiative&logoColor=white)](https://opensource.org/licenses/MIT)

A Claude Code plugin for building and maintaining [Mintlify](https://mintlify.com)
documentation sites in a consistent house style.

It **layers on the official [`mintlify`](https://claude.com/plugins/mintlify)
plugin**: that plugin owns Mintlify mechanics (component syntax, `docs.json`
schema, OpenAPI). This one owns the editorial decisions — information
architecture, voice, callout discipline, scaffolding, drift-checked references,
and changelog style.

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

### For development

```bash
claude --plugin-dir /path/to/mintlify-docs
```

## Companion plugin

Install the official Mintlify plugin for the underlying mechanics this plugin
defers to:

```text
/plugin install mintlify@anthropics
```

## Requirements

No external dependencies for the skills themselves. The generator and preview
workflows assume the [Mintlify CLI](https://www.npmjs.com/package/mint)
(`npm i -g mint`) and a Python or Node toolchain in the target project.
