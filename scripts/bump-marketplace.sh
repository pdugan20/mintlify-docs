#!/usr/bin/env bash
# Opens a PR against pdugan20/pdugan20-plugins that bumps this plugin's
# version in marketplace.json. Runs as the release-it after:release hook on
# the releasing machine, so it uses the local gh auth; no PAT or repo secret
# is needed.
set -euo pipefail

version="${1:?usage: bump-marketplace.sh <version>}"
plugin="mintlify-docs"
repo="pdugan20/pdugan20-plugins"
branch="bump/${plugin}-v${version}"
manifest=".claude-plugin/marketplace.json"

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

gh repo clone "$repo" "$tmp" -- --depth 1 --quiet
cd "$tmp"
git checkout -q -b "$branch"

jq --arg v "$version" \
  "(.plugins[] | select(.name == \"$plugin\") | .version) = \$v" \
  "$manifest" > "$manifest.tmp"
mv "$manifest.tmp" "$manifest"

if git diff --quiet; then
  echo "marketplace.json already at v${version}; nothing to do."
  exit 0
fi

git commit -aqm "chore: bump ${plugin} to v${version}"
git push -q -u origin "$branch"
gh pr create --repo "$repo" \
  --title "chore: bump ${plugin} to v${version}" \
  --body "Syncs the marketplace entry with ${plugin} v${version}. Opened automatically by the release-it after:release hook in pdugan20/${plugin}."
