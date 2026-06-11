#!/usr/bin/env node
// Keeps .claude-plugin/plugin.json in lockstep with package.json. Runs as the
// release-it after:bump hook; plugin.json silently wins over the marketplace
// entry, so it must carry the released version.
const fs = require('fs');
const path = require('path');

const { version } = require('../package.json');
const manifestPath = path.join(__dirname, '..', '.claude-plugin', 'plugin.json');

const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
manifest.version = version;
fs.writeFileSync(manifestPath, `${JSON.stringify(manifest, null, 2)}\n`);

console.log(`plugin.json version set to ${version}`);
