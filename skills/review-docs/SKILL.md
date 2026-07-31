---
name: review-docs
description: Deprecated compatibility skill from the archived mintlify-docs repository. Direct users to install pdugan20/skills and use review-mintlify-docs; do not run this historical copy for new work.
argument-hint: '[path to docs-mintlify | single page]'
---

# Review Docs

**Deprecated:** Do not execute this historical workflow for new work. Direct the
user to install `pdugan20/skills` and use `review-mintlify-docs`.

Run the house-style content and polish pass on a Mintlify docs site. This is the
editorial review, not the mechanics. For Mintlify component syntax and `docs.json`
schema questions, defer to the official `mintlify` plugin.

The authority for every rule cited here is the shared playbook:
[references/best-practices.md](../../references/best-practices.md). Read it
first. This skill is the procedure that applies it; the operational rubric is in
[references/review-rubric.md](./references/review-rubric.md).

## The two non-negotiable habits

1. **Holistic read before edits.** For each page, first answer "what should this
   page do, and what is wrong, redundant, or missing?" Then recommend, then edit.
   Not every page needs work; say so when a page is already strong.
2. **Options-first.** For any wording or structure choice, present 2 to 3 options
   plus a recommendation and let the maintainer pick. Do not unilaterally rewrite
   while riffing. (best-practices section 5.)

## Instructions

### Step 1: Locate the site and read the nav

Find `docs-mintlify/docs.json` (or the path requested by the user). Read its
`navigation` to get the canonical page order. **The review walks pages in nav
order**, not file order. If `$ARGUMENTS` names a single page, review just that
page but still load the nav for cross-link context.

### Step 2: IA check first, before any page edits

Before walking pages, audit the navigation itself against best-practices
section 3:

- **Is any group a flat list longer than ~5 entries?** If so, it should be split
  into topic groups (Getting started / Everyday use / Integrations / Concepts /
  Help, plus domain-specific groups).
- **Is this an MCP server?** (Check for an `mcp-server`/`mcp-tools` page or an MCP
  reference.) If so, a dedicated **Claude (MCP)** group is mandatory, not folded
  into a generic guides list.
- **Are the "pages every project needs" present?** Quickstart, Requirements (or
  supported-X), Troubleshooting. Flag any that are missing.
- **Is the Reference tab split by domain** (CLI / MCP groups with per-domain
  pages plus an overview landing) once it has more than a couple of pages?

Report the IA findings and proposed nav reorg first. Reorganizing the nav is
step one of the pass; pages are then walked in the new order.

### Step 3: Per-page punch list

For each page in nav order, run the rubric in
[references/review-rubric.md](./references/review-rubric.md). Produce a per-page
punch list grouped by category (Frametitle / Voice / Callouts / Links / Code /
Components / Verify). Mark each item as a recommendation, not a done deal.

### Step 4: Apply, options-first

After the maintainer picks from the options, make targeted edits. Commit per page
if the user wants commits (small, logical commits). Never hand-edit generated
pages (reference, changelog); change the generator instead (see the
`document-reference` and `changelog-writer` skills).

### Step 5: Link check and build

Run `mint broken-links` in `docs-mintlify/` after the pass (or after each page on
a long review). Also boot `mint dev` once: `broken-links` does **not** parse
frontmatter, so a malformed `title:`/`description:` passes the link check but
fails the build. `mint dev` reports it as "syntax error in your frontmatter".

### Step 6: Pre-launch checklist

Before declaring done, run the pre-launch checklist (best-practices section 8).
Report each item as pass/fail with the specific offending page or value.

## Brand red flags to always catch

These recur and are quick wins:

- **Generic indigo primary** (`#6366f1` or the Mintlify default) chosen by
  accident rather than deliberately (best-practices section 6).
- **Em dashes in body prose** (grep the em-dash character; section 4). When
  fixing these, watch the frontmatter: a colon-space in an unquoted `title:`/
  `description:` breaks the build, so quote any value that gains a colon.
- **`<Tip>` callouts** or stacked callouts (section 4).
- **Pages with no `description` or no `icon`** (section 4).
- **Hardcoded drift-prone counts** ("37 tools") in hand-written prose
  (section 4).
- **Implementation jargon** on user-facing pages (section 4).

## Scope

This skill reviews and edits hand-authored MDX pages and the `docs.json` nav. It
does not touch generated reference/changelog output, the mirror repo, or CI
config.
