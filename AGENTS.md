# devekko.bookie

This repository is where the bookie and bet skills are written and tested. The skills help a builder run a product bet: a fast build, real users, and a go, no-go, or pivot decision on a fixed date.

[README.md](README.md) has the layout and the commands. [docs/status.md](docs/status.md) has the current state and the open work.

## Layout

- `skills/<name>/` holds the source of each skill. Edit the skills only here.
- `.claude/skills/<name>` is a link to `skills/<name>`. A Claude Code session in this folder loads the files that you edit.
- `sandbox/` holds test projects from `make sandbox`. Git ignores it.
- `scripts/` holds the shell scripts that the Makefile runs.

## Commands

| Task | Command |
| --- | --- |
| Install | `make install` |
| Test | `make test` |
| Lint | `make lint` |
| Types | `make types` |
| All checks | `make check` |
| Apply the format | `make format` |
| Create a test project | `make sandbox NAME=<name>` |
| Compare with the fork checkout | `make fork-diff` |

Run `make check` before you say that a change works.

## Skill rules

- A skill is a folder with a `SKILL.md`. Rules that a script can check go in a script with tests, not in the text.
- The scripts run on Python 3.11 with the standard library only. Do not add a dependency to a skill script.
- `bookie` and `setup-bookie` import scripts from the skill folders beside them. Keep the five skills in one folder.
- Each skill script change needs a test for the behavior that a user of the script can observe.
- Write skill text in short sentences, one instruction in each. Name a thing by what it does.
- The skills and their templates name no company and no person. A test in `skills/bookie/scripts/test_bookie.py` checks the templates.
- Run the skill tests in a temporary folder. A test must never commit to this repository.

## Test a skill by hand

1. Run `make sandbox NAME=<name>`.
2. Start a session in `sandbox/<name>`.
3. Type `/setup-bookie`, then `/bookie`.

The sandbox has its own git repository, so the bookie commits stay inside it. Never run `bookie.py done` or `setup_bookie.py commit` with this repository as the root.

## Publish

The public copy of the skills is in the fork `niccolox/pstack-bets`, in a checkout at `../pstack-bets`.

1. Run `make check`.
2. Run `make fork-copy`. It copies the skills and runs no git command.
3. In the checkout, make a branch, commit, push, and open a PR. Do this only when the operator asks.

## Always ask first

Ask the operator before a push, a PR, a merge, a force-push, or a deletion of a branch.
