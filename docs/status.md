# Status

Written on 2026-11-17, when the skills moved here from the saasx2x project. Change this file when the state changes.

## Where the skills are

| Place | State |
| --- | --- |
| This repository, `skills/` | The source. Edit the skills here. |
| GitHub, `niccolox/devekko.bookie`, branch `main` | The published copy. It is public. `npx skills add niccolox/devekko.bookie` and `npx skills update` read it. A push to `main` publishes. |
| `~/Projects/pstack-bets` (fork `niccolox/pstack-bets`) | A second public copy. PR #5 holds the setup stage, the stage commits, the saved prompts, and `setup-bookie`. It was open on 2026-11-17. |
| `~/Projects/saasx2x.59/.claude/skills/` | The copies that saasx2x uses. Commit `6c4a25b` on the branch `feat/bookie-skill`, not pushed. |

## How this repository differs from the fork and from saasx2x

- Two type fixes that change no behavior. `skills/bookie/scripts/bookie.py`: the JSON results and the progress entries use `Any`, and the answers merge is one expression. `skills/bet-record/scripts/bet_dialog.py`: `Question` is `dict[str, Any]`.
- The pstack step of `setup-bookie`.

`make fork-diff` shows `bookie`, `bet-record`, and `setup-bookie` as different until these changes are copied to the fork.

## Upstream pstack

- `pstack.lock` names `backnotprop/pstack` on `main`. The first pull was on 2026-11-17 at commit `f2772d5`, with 58 skills. `setup-bookie` installs pstack from the same source in a user project.
- That source does not have the `poteto-mode` trigger that runs `bet-record` when a project names a bet record. That trigger is one line in `skills/poteto-mode/SKILL.md` of the fork `niccolox/pstack-bets`. A project does not need it: the `AGENTS.md` that bookie writes tells each agent to do the bet steps before `/poteto-mode`.

## Open work

1. Install the published version with `npx` in an empty folder, and run a full `/setup-bookie` and `/bookie` session there. Only the script steps were run so far. The model step and the operator questions were not run.
2. Decide what the fork `niccolox/pstack-bets` is for, now that users install from this repository.
3. Decide what saasx2x does with its copies: keep them, or install with `npx skills add niccolox/devekko.bookie`.

## What was verified on 2026-11-17

- `make check` on Python 3.11: lint, types, and 95 tests passed. Six tests cover the pstack sync, with a local repository as the upstream. Four cover the install script. Two cover the pstack check of `setup-bookie`, and two check that the sources and the skill names agree. Nine cover the register, and two cover the order of the bet steps in `AGENTS.md`.
- The register from a copy of a real bet record showed the correct row: the status word only, the decision date, and `5 open`. That record is in `.local/`, and the script added `BOOKIE.md` to `.gitignore`.
- The checker command in the generated `AGENTS.md` ran in both install layouts: `.claude/skills/` for a copy and `.agents/skills/` for links.
- The commands of the FastAPI and React stack ran on a real project with the default layout, `app/main.py` and `web/` from the Vite `react-ts` template: `uv sync`, `uv run pytest`, `uv run ruff check .`, `uv run pyright`, `uv run fastapi dev`, and the `npm --prefix web` commands `install`, `test`, `run lint`, `run typecheck`, and `run dev`. The test showed three facts that the stack notes now hold: `tsc` must run as a `typecheck` script and not through `npm exec`, the Vite template has no `test` and no `typecheck` script, and pytest needs `pythonpath = ["."]` to import `app`.
- `npx skills add niccolox/devekko.bookie -l` found the five skills, with no second copy from the links in `.claude/skills/`.
- `npx skills add niccolox/devekko.bookie --skill '*' -a claude-code -y` in an empty folder put the five skills in `.claude/skills/` and wrote `skills-lock.json` at `59c711c`. The scripts ran there.
- With the working copy installed by `npx skills add <this folder>`: the pstack check printed `missing`, its `install` command added 58 skills, the check then printed `present`, and the setup steps made one commit on `setup/bookie` that holds `skills-lock.json`. This passed with the bet skills in `.agents/skills/` and also with the bet skills in `.claude/skills/`.
- After the push of commit `874c337`: `npx skills add niccolox/devekko.bookie --skill '*' -a claude-code -y` in an empty folder pinned that commit in `skills-lock.json`. The pstack check printed `missing`, its `install` command added 58 skills, and the check then printed `present`.
- `npx skills update -y` in a project with both sources fetched 2 sources and reported that all skills were up to date.
- After the push of commit `a1d70ff`: `npx skills update -y` in a project installed at `874c337` updated `bet-record`, `bookie`, and `setup-bookie`, and left the other 60 skills. The lock file then named `a1d70ff` for those three. The installed `bookie` was the same as the source.
- That update moved the three updated skills from real folders in `.claude/skills/` to `.agents/skills/` with links, because the project was installed with `-a claude-code`. An update that moves only one of two skills that work together broke the import between them. `tests/test_layouts.py` now runs both entry scripts in all 8 mixes of folders and links. 4 mixes failed before the fix, and all 8 pass now.
- `make pstack` pulled 58 skills on the first run. A second run reported `current` and did not rewrite the local copy.
- `make bookie REPO=<an empty folder>` installed 58 pstack skills, the 5 bet skills, and 2 agent definitions.
- `make sandbox NAME=demo` created a project with 63 skills and its own git repository. This repository stayed on `main` with no change.
