#!/usr/bin/env bash
# Create a test project in sandbox/<name> with the skills installed as copies.
# Usage: scripts/sandbox.sh <name> [path to a pstack checkout]
set -euo pipefail

name="${1:?give a name, for example: scripts/sandbox.sh demo}"
pstack="${2:-../pstack-bets}"
root="$(cd "$(dirname "$0")/.." && pwd)"
target="$root/sandbox/$name"

if [ -e "$target" ]; then
  echo "sandbox/$name exists. Remove it first, or use another name." >&2
  exit 1
fi

mkdir -p "$target/.claude/skills"

# The other pstack skills come first, so that the local skills replace their copies.
if [ -d "$root/$pstack/skills" ]; then
  rsync -a --exclude __pycache__ "$root/$pstack/skills/" "$target/.claude/skills/"
  echo "Copied the pstack skills from $pstack."
else
  echo "No pstack checkout at $pstack. The sandbox gets only the bet skills." >&2
fi

for skill in "$root"/skills/*/; do
  rsync -a --delete --exclude __pycache__ "$skill" "$target/.claude/skills/$(basename "$skill")/"
done

# The sandbox needs its own repository. Without one, bookie commits to this repository.
git -C "$target" init -q -b main

echo "Created sandbox/$name. Start a session there:"
echo "  cd $target && claude"
echo "Then type /setup-bookie, and after it /bookie."
