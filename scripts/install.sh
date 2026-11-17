#!/usr/bin/env bash
# Install bookie into a project: the upstream pstack skills, then the bet skills.
# Usage: scripts/install.sh <project folder>
#
# Environment:
#   PSTACK=<folder>     The folder that holds the pstack skills folder. Default: vendor/pstack
#   BOOKIE_NO_SYNC=1    Do not ask GitHub for a new pstack hash first
#   BOOKIE_UPDATE=1     Replace the pstack skills that the project already has
#
# The script runs no git command in the project.
set -euo pipefail

target="${1:?give the project folder, for example: scripts/install.sh ../my-project}"
root="$(cd "$(dirname "$0")/.." && pwd)"
pstack="${PSTACK:-$root/vendor/pstack}"

if [ ! -d "$target" ]; then
  echo "$target is not a folder. Create the project folder first." >&2
  exit 1
fi
target="$(cd "$target" && pwd)"
if [ "$target" = "$root" ]; then
  echo "The project is this repository. Its skills load through links already." >&2
  exit 1
fi

if [ "${BOOKIE_NO_SYNC:-0}" != "1" ]; then
  python3 "$root/scripts/pstack_sync.py" sync >/dev/null
fi
if [ ! -d "$pstack/skills" ]; then
  echo "No pstack skills at $pstack. Run 'make pstack' first." >&2
  exit 1
fi

skills="$target/.claude/skills"
mkdir -p "$skills"
added=0
kept=0
replaced=0

# The pstack skills come first. A pstack skill that the project has stays as it is,
# because the project can hold its own changes to it.
for skill in "$pstack"/skills/*/; do
  name="$(basename "$skill")"
  [ -d "$root/skills/$name" ] && continue
  if [ -e "$skills/$name" ] && [ "${BOOKIE_UPDATE:-0}" != "1" ]; then
    kept=$((kept + 1))
    continue
  fi
  [ -e "$skills/$name" ] && replaced=$((replaced + 1)) || added=$((added + 1))
  rsync -a --delete --exclude __pycache__ "$skill" "$skills/$name/"
done

# The bet skills always come from this repository.
bets=0
for skill in "$root"/skills/*/; do
  rsync -a --delete --exclude __pycache__ "$skill" "$skills/$(basename "$skill")/"
  bets=$((bets + 1))
done

# The subagent definitions that poteto-mode uses.
if [ -d "$pstack/agents" ]; then
  mkdir -p "$target/.claude/agents"
  for agent in "$pstack"/agents/*.md; do
    [ -e "$target/.claude/agents/$(basename "$agent")" ] || cp "$agent" "$target/.claude/agents/"
  done
fi

commit="unknown"
[ -f "$pstack/.commit" ] && commit="$(cut -c1-7 "$pstack/.commit")"
echo "Installed into $skills"
echo "  bet skills:    $bets installed"
echo "  pstack skills: $added added, $replaced replaced, $kept kept (pstack commit $commit)"
echo "Next: start your agent in $target and type /setup-bookie"
