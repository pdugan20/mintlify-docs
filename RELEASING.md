# Releasing

Releases run from a maintainer machine with `release-it`. CI only creates the
GitHub release from the pushed tag; it holds no tokens beyond `GITHUB_TOKEN`.

## Prerequisites

- A clean release branch based on the latest `main` and pushed with an upstream.
- `npm ci` has been run (release-it and the linters are devDependencies).
- `gh` is authenticated (the marketplace bump PR uses your local gh auth).
- `npm ci` provides the pinned Claude Code CLI used by the pre-release
  `validate:plugin` gate.

## Prepare the release pull request

```bash
VERSION=0.4.0
git switch main
git pull --ff-only
git switch -c "release/v$VERSION"
git push -u origin "release/v$VERSION"
npm run release -- "$VERSION" --ci
git push
```

release-it prepares the reviewable release commit:

1. **Gates.** Runs `npm run lint` (claudelint + markdownlint) and
   `npm run validate:plugin` (`claude plugin validate . --strict`). Any
   failure aborts before anything is bumped.
2. **Bump.** Conventional commits since the last tag determine the suggested
   semver bump. Pass the intended version explicitly in CI mode. The
   `after:bump` hook syncs the new version into `.claude-plugin/plugin.json` so
   the manifest never drifts from `package.json`.
3. **Changelog.** The release section is prepended to `CHANGELOG.md`.
4. **Commit.** Creates `chore: release vX.Y.Z` locally. It intentionally does
   not tag or push, because `main` requires a pull request and passing checks.

Open a pull request for the release branch, wait for required checks, and merge
it.

## Publish after merge

Tag the merged release commit, wait for the GitHub release, and then open the
marketplace bump:

```bash
VERSION=0.4.0
git switch main
git pull --ff-only
git tag -a "v$VERSION" -m "v$VERSION"
git push origin "v$VERSION"
gh run watch "$(gh run list --workflow Release --event push --limit 1 --json databaseId --jq '.[0].databaseId')" --exit-status
bash scripts/bump-marketplace.sh "$VERSION"
```

The tag triggers `.github/workflows/release.yml`, which extracts the changelog
section and attaches `mintlify-docs-plugin.zip`. The final command opens a pull
request against `pdugan20/patrick-tools`; merge it so both marketplace
entries advertise the released version.

## If something fails partway

- Failure in the preparation gates: nothing was bumped; fix and rerun.
- Failure before the release PR merges: fix the branch and rerun its checks.
- Failure after the tag is pushed: do not rerun release-it. Fix the GitHub
  release by hand (`gh release create vX.Y.Z --notes-file ...`) or rerun the
  marketplace bump alone:

  ```bash
  bash scripts/bump-marketplace.sh X.Y.Z
  ```
