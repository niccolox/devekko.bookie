# Status

Written on 2026-11-17, when the skills moved here from the saasx2x project. Change this file when the state changes.

## Where the skills are

| Place | State |
| --- | --- |
| This repository, `skills/` | The source. Edit the skills here. |
| `~/Projects/pstack-bets` (fork `niccolox/pstack-bets`) | The public copy. PR #5 holds the setup stage, the stage commits, the saved prompts, and `setup-bookie`. It was open on 2026-11-17. |
| `~/Projects/saasx2x.59/.claude/skills/` | The copies that saasx2x uses. Commit `6c4a25b` on the branch `feat/bookie-skill`, not pushed. |

## How this repository differs from the other two

Two type fixes were made here after the copy. They change no behavior:

- `skills/bookie/scripts/bookie.py`: the JSON results and the progress entries use `Any`, and the answers merge is one expression.
- `skills/bet-record/scripts/bet_dialog.py`: `Question` is `dict[str, Any]`.

`make fork-diff` shows `bookie` and `bet-record` as different until these fixes are published.

## Not in this repository

- The `poteto-mode` trigger that runs `bet-record` when a project names a bet record. It is one line in `skills/poteto-mode/SKILL.md` of the fork.
- The other pstack skills. `setup-bookie` reads `../setup-pstack/SKILL.md`, so a project needs `setup-pstack` installed beside it. A sandbox gets it from the fork checkout.

## Open work

1. Run a full `/setup-bookie` and `/bookie` session in a sandbox. Only the script steps were run so far. The model step and the operator questions were not.
2. Publish the two type fixes to the fork.
3. Decide what saasx2x does with its copies: keep them, or install from the fork with `npx skills`.
4. Decide whether this repository gets a remote on GitHub.

## What was verified on 2026-11-17

- `make check` on Python 3.11: lint, types, and 64 tests passed.
- `make sandbox NAME=demo` created a project with 63 skills. In it, `setup_bookie.py project` and `commit` made one commit on `setup/bookie` in the sandbox's own repository, and `bookie.py next` returned the setup stage. This repository stayed on `main` with no change.
