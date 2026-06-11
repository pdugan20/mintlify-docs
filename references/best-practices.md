# Mintlify docs best-practices playbook

The portable playbook for building and shipping a Mintlify docs site for a
single-maintainer OSS project. Captured while building `docs.clickwheel.fm` and
generalized so the next site is a fast-follow, not a re-derivation.

This file is the shared backbone for the `mintlify-docs` plugin. Each skill cites
sections here rather than restating them. It covers editorial and operational
decisions only; for Mintlify component syntax, `docs.json` schema, and OpenAPI
setup, defer to the official `mintlify` plugin.

Status labels in headings: `proven` (used in practice), `recipe` (repeatable
steps), `validate` (worth re-checking per project).

## 1. Hosting and infrastructure (proven, recipe)

The free-tier constraints and the workaround proven end-to-end:

- **Mintlify free (Hobby) is one site per Mintlify account.** Multi-site is
  gated to paid/Enterprise. A second free site needs a second Mintlify account
  (use a `you+<project>@gmail.com` alias).
- **The Mintlify GitHub App installs once per GitHub owner**, bound to one
  workspace. A personal account already bound to one site shows no selectable
  repos for a second account, which is the symptom that blocks the naive path.
- **Fix: connect each additional site to a repo owned by its own GitHub org.**
  An org gives a clean app-installation surface.
- **Free tier:** custom domain works, private source repo works; the published
  site is always public (password protection is Pro; auth/SSO is Enterprise).

### Per-site launch recipe

1. **Create a dedicated GitHub org** (browser only, no API):
   `github.com/account/organizations/new`, Free plan. Name it after the docs
   domain (e.g. `clickwheel-fm`). Org names are global; check availability with
   `gh api /users/<name>` (404 means free).
2. **Create the mirror repo** in the org (e.g. `<org>/docs`), public.
3. **Enable workflow write permissions on the org** (browser): Org, Settings,
   Actions, General, Workflow permissions, "Read and write". New orgs ship
   read-only, which blocks the sync push. (API needs `admin:org`:
   `gh api --method PUT /orgs/<org>/actions/permissions/workflow -f default_workflow_permissions=write`.)
4. **Seed the mirror** with the source `docs-mintlify/` contents at the repo
   **root** (so `docs.json` is top-level, no subdirectory toggle in Mintlify).
5. **Add the pull-based sync workflow** to the mirror (see section 2).
6. **Install the Mintlify App** on the org, scoped to the mirror repo.
7. **Connect** from the project's `+alias` Mintlify account: org, mirror, `main`,
   subdirectory off.
8. **Add the custom domain** in Mintlify; create the DNS CNAME it shows
   (`docs` to Mintlify's target).

## 2. Source to mirror sync, drift-proof (proven, recipe)

Docs are authored in the **product repo** (`<owner>/<project>/docs-mintlify`) so
the generators and anti-drift CI sit next to the code. Mintlify needs a repo
under a **different owner** (the org), so a one-way mirror bridges them.

- **Pull, do not push.** A workflow in the mirror clones the public source,
  `rsync --delete`s `docs-mintlify/` to the mirror root, and self-pushes with the
  built-in `GITHUB_TOKEN`. This needs no cross-repo credentials: reading a public
  repo is auth-free and a repo's own token can push to itself. (Deploy keys and
  PATs both required extra setup or were org-disabled; the pull model sidesteps
  all of it.)
- **Triggers:** `schedule` (30-min safety net) plus `workflow_dispatch` (manual)
  plus optional `repository_dispatch: docs-changed` (near-instant trigger from
  the source repo, if a cross-repo token is added).
- **Preserve mirror-only files** in the rsync excludes: `.git`, `.github`,
  `README.md` (the "generated, do not edit" banner).
- **Pin `permissions: contents: write`** in the workflow and set the repo token
  to write.

### Anti-drift, two layers (proven)

1. **Content correctness** lives in the source repo: generators
   (`gen-cli-reference`, `gen-mcp-reference`, `gen-changelog`) plus a CI job that
   regenerates and **fails on drift**. Reference and changelog pages cannot go
   stale.
2. **Mirror fidelity:** the mirror is overwritten every sync, so it is always
   byte-equal to source `docs-mintlify/`. Never hand-edit the mirror.

## 3. Information architecture, Diátaxis (proven)

Keep the four modes distinct; do not blur them:

- **Tutorial** (`quickstart`): zero to first win, linear, no detours.
- **How-to guides:** task-focused; assume the quickstart is done.
- **Reference:** generated, exhaustive, dry (`cli`, `mcp-tools`, `configuration`).
- **Explanation/concepts:** the *why* (`architecture`, `design`).

**Navigation: group how-tos by topic, not by Diátaxis label, once you have more
than a few.** A single flat "How-to guides" list stops scanning well past
about 5 entries. A proven shape for a CLI + MCP project:

```text
Guides (tab)
  Getting started   introduction, quickstart, requirements
  Everyday use      the core task guides
  Integrations      per-service setup guides
  Claude (MCP)      the MCP server concept + remote-MCP guide
  Concepts          architecture, design
  Help              troubleshooting, changelog

Reference (tab)
  CLI               overview + per-domain pages
  MCP               overview + per-domain pages
  configuration
```

If the project is an MCP server, the **Claude (MCP)** group is mandatory, not
optional. Surface the AI story as its own group.

## 4. Content standards (proven)

### Frontmatter and nav

- **Every page sets `title` plus a real-sentence `description`** (it is the SEO
  and search snippet; write a sentence, not a label).
- **Add an `icon:` to every page in a tab**, uniformly (half-iconed groups look
  unfinished). Reuse the homepage card icons so nav and cards match.
- **Use `sidebarTitle` to keep nav labels short** when the page `title` is long.

### Framing and voice

- **Lead with the differentiator, not the crowded category.** Find the project's
  rare hook and lead with it.
- **A short "what it does" in 2 to 4 capability pillars**, not a feature dump.
- **Second person, present tense, imperative.** Short paragraphs.
- **No em dashes.** Hard rule for shipped docs. Use commas, colons, or
  parentheses. (Grep for the em-dash character before shipping.) **Frontmatter
  caveat:** a colon followed by a space inside an unquoted YAML `title:` or
  `description:` starts a nested mapping and breaks the build. When you replace
  an em dash with a colon in frontmatter, wrap the whole value in quotes
  (`description: "Two ways: local or remote."`). `mint dev` surfaces these as
  "syntax error in your frontmatter"; a link check won't.
- **No hardcoded, drift-prone counts** ("37 tools") unless programmatically
  derived. Illustrative sample-output blocks are fine; keep one consistent
  fictional example across pages.
- **Strip implementation jargon from user-facing pages**: keep the capability,
  drop the mechanism. Reference and concepts pages may be more technical.

### Callouts, minimal consistent palette

- **`<Note>` (blue) is the default** for any advisory or important info.
- **`<Warning>` (yellow) is reserved for the genuinely irreversible** (data loss,
  cannot-undo).
- **Avoid `<Tip>` (green).** It just adds a third color; demote nice-to-knows to
  prose.
- **Do not stack callouts.** One per concept, and prefer prose unless it is a
  real gate or caution. Two colored boxes back-to-back is a smell.

### Links

- **Link once, on first meaningful mention.** Do not double-link the same target
  in close proximity.
- **Link to the most specific relevant page** (a per-domain reference beats a
  generic overview), and always forward to the canonical page: one source of
  truth per fact.

### Code examples

- Always language-tagged; use **code-block titles** for config and `.env` blocks
  (filename in the title bar).
- **Align inline `#` comments and keep them short** so the block does not scroll
  horizontally.
- **Prefer runnable copy-paste over shell plumbing** in a quickstart.
- **Realistic-but-clean paths**; drop volume prefixes and noise.
- **Real values where safe; placeholders for secrets and domains**
  (`<your-token>`, `mcp.example.com`). Keep secrets in a mode-`600` env file;
  inline the env var in prose rather than a sparse `KEY=...` block; treat tokens
  like passwords and link the provider's official "find your token" page.

### Components by shape

- Linear setup: `<Steps>`; **set `titleSize="h3"`** so the steps populate the
  right-rail TOC (default `p` leaves a step page with an empty TOC).
- Client/OS/shell variants: `<Tabs>`.
- Optional / troubleshooting / advanced detail: `<Accordion>` /
  `<AccordionGroup>` (progressive disclosure). Link to a full repo runbook rather
  than inlining long ops.
- Next steps / cross-sell: `<CardGroup>`.

### Verify before you document

- **Check command names, arg names, flags, and limits against the source.** Do
  not guess; read the code, and verify tool behavior against the official docs.
- **Generated pages (reference, changelog) are never hand-edited**: change the
  generator and regenerate.

### Pages every project needs

- **Quickstart**, **Requirements / supported-X**, **Troubleshooting.**
- **Requirements:** present "what each integration needs" as a **table**
  (`Extra | Credentials`), and surface gotchas at the requirements level, not
  buried in a guide.
- **Troubleshooting:** bucket by area, and **point at self-diagnostic tools**
  (the `doctor` commands) rather than re-explaining setup.

### The MCP / AI cross-reference pattern

On each feature or integration guide, add a single **one-line "From Claude"
nudge** that links (a) MCP setup and (b) the per-domain tool reference:

> You can also drive this from Claude. Set up the [MCP server](...), then the
> [Plex tools](/reference/mcp-tools/plex) are yours.

Do **not** dump tool names inline (the reference owns them) and do **not** repeat
a gating/permission note on every page; document client-side gating **once** on
the MCP server page.

## 5. The content and polish pass, process (recipe)

1. **Reorg the nav first** (topic groups, section 3), then walk pages **in nav
   order** (Welcome to Changelog).
2. **Per page: holistic read first.** "What should this page do? What is wrong,
   redundant, or missing?" Recommend, then make targeted edits. Not every page
   needs heavy editing; say so when a page is already strong.
3. **Options-first iteration.** For any wording or structure choice, present 2 to
   3 options plus a recommendation and let the maintainer pick. Do not
   unilaterally rewrite while riffing.
4. **Verify against source as you go** (commands, args, flags, limits).
5. **Commit per page** (small, logical commits). Apply pre-commit hooks manually
   first on the changed files to dodge the stash-conflict dance.
6. **Run `mint broken-links` after each page.**
7. **Park tangents** in a `DEFERRED.md`. When you reach the page they belong to,
   check whether it already covers them before re-adding.

## 6. Visual and brand standards (proven)

The system carries across sites; the values are per-project.

- **`docs.json` controls:** `theme`, `colors` (`primary`/`light`/`dark`), `logo`
  (light+dark), `favicon`, `appearance.default`, optional `fonts`.
- **One brand primary**, AA contrast in both light and dark. Avoid the default
  generic indigo unless chosen deliberately.
- **Logo:** provide light + dark. Constrain size in custom CSS **and set
  `aspect-ratio` on the logo `img`** so it does not flash at intrinsic size on
  client-side navigation.
- **Favicon:** a single **adaptive SVG** (dark default plus a
  `prefers-color-scheme: dark` override) reads in both modes. Mintlify generates
  PNG derivatives at server start, so restart `mint dev` to see favicon changes.
- **Page icons:** uniform within a tab, reused from the homepage cards.
- **OG/social image and landing hero:** per-project, deferred to a visual pass.
  Prefer designed SVG diagrams over Mermaid (Mermaid reads too generic).
- **Per-project, not shared:** logo, colors, OG image, domain. **Shared:**
  component patterns, page structure, voice, the callout palette, the checklist.

## 7. Mintlify mechanics and gotchas (validate per theme)

Verified against `mintlify.com/docs` and in practice. Theme-specific notes call
out the theme.

- **Theme toggle is all-or-nothing.** `appearance.strict: true` hides every
  toggle; there is no per-location control.
- **`footer.links` adds an extra footer tier** (in maple) above "Powered by
  Mintlify"; with only a couple of links it reads as a confusing second footer.
  Watch for GitHub appearing three times (navbar primary + footer social +
  footer link); keep it to the navbar button plus footer icon.
- **Step titles only hit the right-rail TOC with `titleSize="h2"/"h3"`**; use
  this for a step-based page instead of `mode: "wide"` (which hides the TOC).
- **`mode`:** `wide` hides the right-rail TOC; `center` removes sidebar + TOC;
  `custom` strips chrome. Section `##`/`###` headings feed the right rail; keep
  them short.
- **maple has no top navbar bar:** `navbar.primary` renders at the **bottom of
  the left sidebar**, and `navbar.links` near it.

## 8. Pre-launch checklist (recipe)

- [ ] `mint broken-links` passes (CI: "Docs Links").
- [ ] Generated reference + changelog regenerated; drift CI green.
- [ ] Every page has a real `description` and an `icon`; nav labels short.
- [ ] No em dashes anywhere (grep the em-dash character).
- [ ] Callout palette consistent (Note default; Warning only for irreversible; no
      stray Tips).
- [ ] Commands, args, flags, and limits verified against source.
- [ ] Example domains/secrets genericized (`mcp.example.com`, `<your-token>`).
- [ ] Quickstart works copy-paste on a clean machine.
- [ ] Light + dark both legible; logo/favicon correct in both (logo does not
      flash on navigation).
- [ ] OG image set; link preview checked.
- [ ] Custom domain resolves; HTTPS valid.
- [ ] Mirror sync verified (dispatch once, confirm success).
- [ ] README of the product repo points to the live docs.

## 9. Tooling

- **Local preview:** `mint dev` in `docs-mintlify/` (live reload; favicon
  needs a restart).
- **Link check:** `mint broken-links`.
- **Make targets:** `make docs` (preview), `make docs-reference` (regenerate),
  `make docs-links` (check).

## 10. Mintlify features to leverage (proven)

- `<ParamField>` for params (type/required/default badges; descriptions wrap as
  paragraphs instead of cramped table cells).
- Synopsis line per command (`<tool> <cmd> [OPTIONS] ...`).
- Per-group reference pages (CLI + MCP) with an overview landing.
- Generated, drift-checked reference + changelog; `sidebarTitle`; a real
  `description` per page.
- Contextual menu (Copy page / View as Markdown / Open in Claude or ChatGPT) via
  the `docs.json` `contextual` block.
- Feedback thumbs (`docs.json` `feedback`).
- CLI examples per command; MCP "Try asking" prompts per domain.
- Code-block titles for config and `.env` blocks.
- `llms.txt` / `llms-full.txt` (auto-generated).

### Reconsidered

- **Reusable snippets:** use `snippets/` only for genuinely repeated,
  page-agnostic boilerplate. Client-side MCP gating is general behavior; document
  it once on the MCP server page, do not repeat it per guide.

### Decided against

- **Mermaid diagrams.** The shapes/arrows read too generic and cannot be styled
  to "designed" quality. Park diagrams and add them back as polished SVGs in the
  visual pass.
