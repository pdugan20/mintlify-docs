#!/usr/bin/env bash
# Opens a PR against pdugan20/plugins that advances both runtime
# catalogs to the same tagged plugin release. Runs as the release-it
# after:release hook on the releasing machine, so it uses the local gh auth;
# no PAT or repo secret is needed.
set -euo pipefail

version="${1:?usage: bump-marketplace.sh <version>}"
plugin="mintlify-docs"
repo="pdugan20/plugins"
branch="bump/${plugin}-v${version}"
claude_manifest=".claude-plugin/marketplace.json"
codex_manifest=".agents/plugins/marketplace.json"

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

gh repo clone "$repo" "$tmp" -- --depth 1 --quiet
cd "$tmp"
git checkout -q -b "$branch"

jq --arg v "$version" --arg ref "v${version}" \
  "(.plugins[] | select(.name == \"$plugin\") | .version) = \$v |
   (.plugins[] | select(.name == \"$plugin\") | .source.ref) = \$ref" \
  "$claude_manifest" >"$claude_manifest.tmp"
mv "$claude_manifest.tmp" "$claude_manifest"

jq --arg ref "v${version}" \
  "(.plugins[] | select(.name == \"$plugin\") | .source.ref) = \$ref" \
  "$codex_manifest" >"$codex_manifest.tmp"
mv "$codex_manifest.tmp" "$codex_manifest"

if git diff --quiet; then
  echo "marketplace.json already at v${version}; nothing to do."
  exit 0
fi

git add "$claude_manifest" "$codex_manifest"
git commit -qm "chore: bump ${plugin} to v${version}"
git push -q -u origin "$branch"
# --head is required: gh cannot infer the head branch in this throwaway
# depth-1 clone.
gh pr create --repo "$repo" --head "$branch" \
  --title "chore: bump ${plugin} to v${version}" \
  --body "Syncs the Claude and Codex marketplace entries with ${plugin} v${version}. Opened automatically by the release-it after:release hook in pdugan20/${plugin}."
