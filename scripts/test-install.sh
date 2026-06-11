#!/usr/bin/env bash
# Install smoke test: verifies that installing this plugin auto-installs its
# declared dependency (mintlify@claude-plugins-official) with no plugin
# errors. Wraps the working tree in a throwaway local marketplace that
# mirrors the pdugan20-plugins cross-marketplace allowlist, so the test
# covers this repo's plugin.json and the CLI behavior; the marketplace
# repo's own CI covers the production marketplace.json.
#
# Needs the claude CLI on PATH and network access (clones the official
# marketplace). No login required: plugin management is local.
set -euo pipefail

repo="$(cd "$(dirname "$0")/.." && pwd)"
CLAUDE_CONFIG_DIR="$(mktemp -d)"
export CLAUDE_CONFIG_DIR
work="$(mktemp -d)"
trap 'rm -rf "$CLAUDE_CONFIG_DIR" "$work"' EXIT

mkdir -p "$work/mkt/.claude-plugin" "$work/mkt/mintlify-docs"
cp -R "$repo/.claude-plugin" "$repo/skills" "$repo/references" \
  "$repo/LICENSE" "$repo/README.md" "$work/mkt/mintlify-docs/"
cat > "$work/mkt/.claude-plugin/marketplace.json" <<'EOF'
{
  "name": "local-test",
  "owner": { "name": "ci" },
  "allowCrossMarketplaceDependenciesOn": ["claude-plugins-official"],
  "plugins": [{ "name": "mintlify-docs", "source": "./mintlify-docs" }]
}
EOF

claude plugin marketplace add anthropics/claude-plugins-official
claude plugin marketplace add "$work/mkt"
claude plugin install mintlify-docs@local-test

list="$(claude plugin list --json)"
echo "$list" | jq -e \
  '.[] | select(.id == "mintlify@claude-plugins-official")' > /dev/null \
  || { echo "FAIL: dependency mintlify@claude-plugins-official was not auto-installed"; exit 1; }
echo "$list" | jq -e \
  '[.[] | select((.errors // []) | length > 0)] | length == 0' > /dev/null \
  || { echo "FAIL: plugin errors present:"; echo "$list" | jq '.[] | {id, errors}'; exit 1; }

echo "PASS: dependency auto-installed, no plugin errors"
