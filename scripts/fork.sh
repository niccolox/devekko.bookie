#!/usr/bin/env bash
# Compare the skills with a pstack checkout, or copy them into it.
# Usage: scripts/fork.sh diff|copy [path to the checkout]
# This script runs no git command in the checkout. Commit and push there yourself.
set -euo pipefail

action="${1:?give an action: diff or copy}"
root="$(cd "$(dirname "$0")/.." && pwd)"
fork="${2:-$root/../pstack-bets}"

if [ ! -d "$fork/skills" ]; then
  echo "No skills folder at $fork." >&2
  exit 1
fi

status=0
for skill in "$root"/skills/*/; do
  name="$(basename "$skill")"
  case "$action" in
    diff)
      if diff -r --exclude __pycache__ "$skill" "$fork/skills/$name" >/dev/null 2>&1; then
        echo "same     $name"
      else
        echo "differs  $name"
        status=1
      fi
      ;;
    copy)
      rsync -a --delete --exclude __pycache__ "$skill" "$fork/skills/$name/"
      echo "copied   $name"
      ;;
    *)
      echo "Unknown action: $action. Use diff or copy." >&2
      exit 2
      ;;
  esac
done
exit "$status"
