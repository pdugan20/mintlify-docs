---
name: scaffold-mintlify-site
description: This skill should be used when the user asks to "scaffold a docs site", "set up Mintlify", "create a docs-mintlify directory", "stand up docs", "bootstrap documentation", or wants a new Mintlify docs site for a project. Generates a docs-mintlify/ tree with a topic-grouped IA, docs.json, page stubs, generators, Makefile targets, and the mirror sync + drift CI, all in house style.
argument-hint: '[project root]'
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash(ls *)
  - Bash(cat *)
  - Bash(mkdir *)
  - Bash(test *)
---

# Scaffold Mintlify Site

Stand up a new Mintlify docs site for a project in the house style. The output is
a `docs-mintlify/` tree authored in the **product repo** (so generators and
anti-drift CI sit next to the code), wired for the org/mirror hosting model.

This skill owns the editorial shape (IA, page set, house defaults). For component
syntax and `docs.json` schema details, defer to the official `mintlify` plugin.
The authority for every decision here is
`${CLAUDE_PLUGIN_ROOT}/references/best-practices.md`; read it first.

## Usage

Invoke with `/scaffold-mintlify-site [project root]`. The skill runs in three
phases: detect and decide (below), generate the tree, then wire the toolchain.
It is non-destructive: it never overwrites an existing `docs-mintlify/`.

## Instructions: detect and decide

### Step 1: Don't clobber

Check for an existing `docs-mintlify/` (or `docs/`, `website/`). If found, offer
to **review/extend** it (hand off to `review-docs`) rather than scaffold over it.

### Step 2: Detect project type

Run [scripts/detect-project-type.sh](./scripts/detect-project-type.sh) (or read
`pyproject.toml` / `package.json` / look for an OpenAPI spec). Determine which of
these the project has, since they drive the IA and the reference tab:

- **CLI** (a `console_scripts` / `bin` entry point)
- **MCP server** (a FastMCP or MCP SDK server module)
- **HTTP API** (an OpenAPI/AsyncAPI spec)

**If the project is an MCP server, the `Claude (MCP)` nav group is mandatory.**

### Step 3: Decide the brand and IA, options-first

Present 2 to 3 options plus a recommendation (best-practices section 5) for:

- **Brand primary color.** Do not default to the generic indigo `#6366f1`;
  pick a deliberate color with AA contrast in light and dark (section 6).
- **The differentiator hook** for the introduction (section 4).
- **The how-to topic groups** for this project (e.g. Getting started / Everyday
  use / Integrations / Claude (MCP) / Concepts / Help), section 3.

Confirm before writing files.

## Generate the tree

Create `docs-mintlify/` from the templates, substituting the decided values:

```text
docs-mintlify/
  docs.json              from templates/docs.json (fill name, color, nav groups)
  introduction.mdx       from templates/introduction.mdx
  quickstart.mdx         from templates/quickstart.mdx
  requirements.mdx       from templates/requirements.mdx
  troubleshooting.mdx    from templates/troubleshooting.mdx
  changelog.mdx          from templates/changelog.mdx
  guides/                one stub per decided how-to
  concepts/              architecture (+ design / mcp-server if relevant)
  reference/             cli.mdx / mcp-tools.mdx / configuration.mdx as relevant
  logo/                  placeholder light.svg / dark.svg (note: replace in visual pass)
  favicon.svg            placeholder adaptive favicon
```

The `docs.json` template already encodes the canonical IA: a **Guides** tab with
topic groups and a **Reference** tab split into CLI / MCP groups. Delete the
groups the project does not need; never leave a flat how-to list longer than ~5
entries (section 3).

## Wire the toolchain

- **Makefile targets** from [templates/Makefile-docs.mk](./templates/Makefile-docs.mk):
  `docs` (preview), `docs-reference` (regenerate), `docs-links` (broken-links).
- **Reference generators:** hand off to the `document-reference` skill to add
  `gen_cli_reference.py` / `gen_mcp_reference.py` and the drift CI.
- **Mirror sync:** the org/mirror hosting recipe (best-practices sections 1-2)
  is a one-time, mostly-browser setup. Add the pull-based sync workflow to the
  *mirror* repo from [templates/sync-docs.yml](./templates/sync-docs.yml). Walk
  the user through the launch recipe steps that require the browser (org creation,
  app install, domain) rather than attempting them.

## Hand off

After scaffolding, the natural next steps are:

1. `document-reference` to generate the CLI/MCP/API reference and drift CI.
2. `review-docs` to do the first content pass once stubs have real content.
3. `changelog-writer` for the first changelog entry at first release.

## Scope

This skill creates the initial tree, `docs.json`, stubs, and toolchain wiring. It
does not write finished page content (that is an authoring pass) and does not
perform the browser-only hosting steps (it guides them).
