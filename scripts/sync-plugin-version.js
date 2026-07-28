#!/usr/bin/env node
// Keeps both runtime manifests in lockstep with package.json. Runs as the
// release-it after:bump hook; plugin manifests silently win over marketplace
// entries, so both must carry the released version.
const fs = require('fs');
const path = require('path');

const { version } = require('../package.json');
const manifestPaths = [
  path.join(__dirname, '..', '.claude-plugin', 'plugin.json'),
  path.join(__dirname, '..', '.codex-plugin', 'plugin.json'),
];

for (const manifestPath of manifestPaths) {
  const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
  manifest.version = version;
  fs.writeFileSync(manifestPath, `${JSON.stringify(manifest, null, 2)}\n`);
  console.log(`${path.relative(path.join(__dirname, '..'), manifestPath)} version set to ${version}`);
}
