#!/bin/bash
# Copies the post skill in from plugins/vamos before an eval run. A symlink doesn't do: the eval's sandbox blocks
# reads outside the plugin under test, so the skill's references and plan.py must sit inside this folder.
set -e
cd "$(dirname "$0")"
rm -rf skills/post
cp -R ../../../plugins/vamos/skills/post skills/post
echo "skills/post copied from plugins/vamos"
