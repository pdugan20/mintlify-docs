# mintlify-docs

[![CI](https://github.com/pdugan20/mintlify-docs/workflows/CI/badge.svg)](https://github.com/pdugan20/mintlify-docs/actions)
[![Release](https://img.shields.io/github/v/release/pdugan20/mintlify-docs?logo=github)](https://github.com/pdugan20/mintlify-docs/releases/latest)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?logo=opensourceinitiative&logoColor=white)](https://opensource.org/licenses/MIT)

A Claude and Codex plugin for building and maintaining [Mintlify](https://mintlify.com)
documentation sites in a consistent house style.

The official [`mintlify`](https://claude.com/plugins/mintlify) plugin owns the
mechanics: component syntax, `docs.json` schema, OpenAPI. This plugin layers
on top and owns the editorial decisions: information architecture, voice,
callout discipline, scaffolding, drift-checked references, and changelog
style.

## Skills

| Skill | Claude | Codex | Description |
| ----- | ------ | ----- | ----------- |
| Scaffold a site | `/mintlify-docs:scaffold-mintlify-site` | `$mintlify-docs:scaffold-mintlify-site` | Stand up a `docs-mintlify/` tree with a topic-grouped IA, `docs.json`, generators, and sync CI |
| Review docs | `/mintlify-docs:review-docs` | `$mintlify-docs:review-docs` | Walk pages in nav order against the content playbook and pre-launch checklist |
| Write changelog | `/mintlify-docs:changelog-writer` | `$mintlify-docs:changelog-writer` | Write and audit reader-facing `<Update>` entries |
| Document a reference | `/mintlify-docs:document-reference` | `$mintlify-docs:document-reference` | Generate drift-checked CLI / MCP / API reference pages from source |

The shared editorial playbook lives in [`references/best-practices.md`](references/best-practices.md);
every skill cites it rather than restating it.

## Installation

### Skills CLI

```bash
npx skills add pdugan20/mintlify-docs
```

Pin a release when reproducibility matters:

```bash
npx skills add https://github.com/pdugan20/mintlify-docs/tree/v0.3.2
```

### Claude

```text
/plugin marketplace add pdugan20/patrick-tools
/plugin install mintlify-docs@patrick-tools
```

### Codex

```text
codex plugin marketplace add pdugan20/patrick-tools
codex plugin add mintlify@claude-plugins-official
codex plugin add mintlify-docs@patrick-tools
```

Patrick's private `agent-tooling` setup installs and refreshes both runtime
variants automatically.

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

The Codex plugin manifest lives at `.codex-plugin/plugin.json`. Validate it with
Codex's built-in `$plugin-creator` workflow before publishing changes.

## Development

```bash
npm ci
npm run verify
```

The verification gate uses the repository-pinned ClaudeLint release, validates
the marketplace manifest with its strict preset, and runs Claude Code's official
plugin validator. Before a release, also validate the Codex manifest with the
built-in `$plugin-creator` workflow.

## Requirements

The official `mintlify` plugin is a declared Claude dependency and installs
automatically there. `agent-tooling` includes it explicitly in the Codex plugin
set. The preview and
link-check workflows assume the
[Mintlify CLI](https://www.mintlify.com/docs/cli/install) (`npm i -g mint`), and
the generator scripts need a Python or Node toolchain in the target project.
