#!/usr/bin/env bash
# Bundles the plugin into mintlify-docs-plugin.zip so the release workflow
# can attach it to the GitHub release. Users can then trial the plugin with
# `claude --plugin-url .../releases/latest/download/mintlify-docs-plugin.zip`
# without registering the marketplace.
set -euo pipefail

cd "$(dirname "$0")/.."
out="mintlify-docs-plugin.zip"

rm -f "$out"
zip -qr "$out" .claude-plugin skills references LICENSE README.md \
  -x '*/__pycache__/*' -x '*.pyc'
echo "wrote $out"
