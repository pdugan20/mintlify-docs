# Releasing

Releases run from a maintainer machine with `release-it`. CI only creates the
GitHub release from the pushed tag; it holds no tokens beyond `GITHUB_TOKEN`.

## Prerequisites

- A clean working tree on `main`, up to date with origin.
- `npm ci` has been run (release-it and the linters are devDependencies).
- `gh` is authenticated (the marketplace bump PR uses your local gh auth).
- The Claude Code CLI is installed (`npm i -g @anthropic-ai/claude-code`),
  used by the pre-release `validate:plugin` gate.

## Cut a release

```bash
npm run release
```

release-it walks the rest:

1. **Gates.** Runs `npm run lint` (claudelint + markdownlint) and
   `npm run validate:plugin` (`claude plugin validate . --strict`). Any
   failure aborts before anything is bumped.
2. **Bump.** Conventional commits since the last tag determine the suggested
   semver bump; confirm or override at the prompt. The `after:bump` hook
   syncs the new version into `.claude-plugin/plugin.json` so the manifest
   never drifts from `package.json`.
3. **Changelog.** The release section is prepended to `CHANGELOG.md`.
4. **Commit, tag, push.** `chore: release vX.Y.Z` plus tag `vX.Y.Z`.
5. **GitHub release.** The pushed tag triggers `.github/workflows/release.yml`,
   which extracts the changelog section and attaches
   `mintlify-docs-plugin.zip`.
6. **Marketplace bump.** The `after:release` hook opens a PR against
   `pdugan20/pdugan20-plugins` updating this plugin's `version` in
   `marketplace.json`. **Merge that PR to finish the release**; installs
   advertise the marketplace version.

## If something fails partway

- Failure in the gates (step 1): nothing was bumped; fix and rerun.
- Failure after the tag pushed: do not rerun release-it. Fix the GitHub
  release by hand (`gh release create vX.Y.Z --notes-file ...`) or rerun the
  marketplace bump alone:

  ```bash
  bash scripts/bump-marketplace.sh X.Y.Z
  ```
