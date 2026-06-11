# Claude Code Instructions

## Architecture

This is a pure-skill Claude Code plugin. No build step and nothing published
to npm: the root `package.json` is private dev tooling only (linters and
release-it). This file lives at `.claude/CLAUDE.md` rather than the repo root
because `claude plugin validate --strict` rejects a root CLAUDE.md (it is
not shipped as plugin context; this file is contributor context).

```text
.claude-plugin/     Plugin manifest
references/         Shared editorial playbook (best-practices.md)
skills/             One directory per skill, each with SKILL.md + supporting files
scripts/            Release tooling (version sync, marketplace bump, packaging)
```

## Skills

| Skill                  | Directory                        |
| ---------------------- | -------------------------------- |
| scaffold-mintlify-site | `skills/scaffold-mintlify-site/` |
| review-docs            | `skills/review-docs/`            |
| changelog-writer       | `skills/changelog-writer/`       |
| document-reference     | `skills/document-reference/`     |

## Design principles

- **Layer, don't duplicate.** Mintlify mechanics (component syntax, `docs.json`
  schema, OpenAPI) belong to the official `mintlify` plugin. This plugin encodes
  only editorial decisions. When a skill needs a component's syntax, it points
  at the official plugin instead of restating it.
- **One source of truth for the playbook.** Skills cite sections of
  `references/best-practices.md`; they do not copy its rules inline.
- **House voice is non-negotiable.** No em dashes. No emojis. Benefit-led,
  second person, present tense. These rules apply to the docs the skills
  produce *and* to this repo's own files.

## File conventions

- Skill definitions: `skills/<name>/SKILL.md`
- Templates: `skills/<name>/templates/*`
- Scripts: `skills/<name>/scripts/*`
- Reference docs: `skills/<name>/references/*.md`

## Validation

```bash
npm run lint              # claudelint + markdownlint
npm run validate:plugin   # claude plugin validate . --strict
```

CI also runs shellcheck, ruff, and actionlint over the bundled scripts and
workflows.

## Releasing

See [RELEASING.md](../RELEASING.md). Short version: `npm run release` on a
clean main; release-it bumps, syncs `.claude-plugin/plugin.json`, tags, and
opens the marketplace bump PR. `CHANGELOG.md` is generated; never hand-edit.
