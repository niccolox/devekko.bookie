#!/usr/bin/env bash
# Create a test project in sandbox/<name> and install bookie into it.
# Usage: scripts/sandbox.sh <name>
set -euo pipefail

name="${1:?give a name, for example: scripts/sandbox.sh demo}"
root="$(cd "$(dirname "$0")/.." && pwd)"
target="$root/sandbox/$name"

if [ -e "$target" ]; then
  echo "sandbox/$name exists. Remove it first, or use another name." >&2
  exit 1
fi

mkdir -p "$target"
# The sandbox needs its own repository. Without one, bookie commits to this repository.
git -C "$target" init -q -b main
"$root/scripts/install.sh" "$target"
