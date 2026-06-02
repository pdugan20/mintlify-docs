# Claude Code Instructions

## Architecture

This is a pure-skill Claude Code plugin. No npm package, no build step — just
skill definitions with supporting templates, scripts, and reference files.

```text
.claude-plugin/     Plugin manifest
references/         Shared editorial playbook (best-practices.md)
skills/             One directory per skill, each with SKILL.md + supporting files
```

## Skills

| Skill | Directory |
|-------|-----------|
| scaffold-mintlify-site | `skills/scaffold-mintlify-site/` |
| review-docs | `skills/review-docs/` |
| changelog-writer | `skills/changelog-writer/` |
| document-reference | `skills/document-reference/` |

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
claudelint check-all
```
