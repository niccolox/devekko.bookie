# devekko.bookie

This repository is where the bookie and bet skills are written and tested. The skills help a builder run a product bet: a fast build, real users, and a go, no-go, or pivot decision on a fixed date.

[README.md](README.md) has the layout and the commands. [docs/status.md](docs/status.md) has the current state and the open work.

## Layout

- `skills/<name>/` holds the source of each skill. Edit the skills only here.
- `.claude/skills/<name>` is a link to `skills/<name>`. A Claude Code session in this folder loads the files that you edit.
- `vendor/pstack/` holds the upstream pstack skills. `make pstack` pulls them. Git ignores the folder, and `pstack.lock` records the source and the commit hash.
- `sandbox/` holds test projects from `make sandbox`. Git ignores it.
- `scripts/` holds the scripts that the Makefile runs. `tests/` holds their tests.

## Commands

| Task | Command |
| --- | --- |
| Install | `make install` |
| Test | `make test` |
| Lint | `make lint` |
| Types | `make types` |
| All checks | `make check` |
| Apply the format | `make format` |
| Pull upstream pstack on a new hash | `make pstack` |
| Compare the pstack hash, pull nothing | `make pstack-check` |
| Install the working copy into a project | `make bookie REPO=<folder>` |
| Create a test project | `make sandbox NAME=<name>` |
| Compare with the fork checkout | `make fork-diff` |

Run `make check` before you say that a change works.

## Upstream pstack

The other pstack skills, such as `poteto-mode` and `setup-pstack`, come from the repository that `pstack.lock` names.

- `make pstack` asks GitHub for the branch's commit hash with `git ls-remote`. That call downloads no files. It pulls the files only when the hash differs from the hash of the local copy, or when there is no local copy.
- A pull replaces `vendor/pstack/` and links each upstream skill into `.claude/skills/`. A skill in `skills/` wins over an upstream skill of the same name.
- Never edit a file in `vendor/`. The next pull replaces it. Change an upstream skill in its own repository.
- To use another source, change `source` in `pstack.lock`, then run `make pstack`. Change `PSTACK_SOURCE` in `skills/setup-bookie/scripts/setup_bookie.py` to the same value. A test in `tests/test_sources.py` fails when the two differ.
- A user project does not use `vendor/` or `pstack.lock`. There, `/setup-bookie` installs pstack with `npx skills add`, and `skills-lock.json` records its commit.
- After a clone of this repository, run `make pstack` once.

## Skill rules

- A skill is a folder with a `SKILL.md`. Rules that a script can check go in a script with tests, not in the text.
- The scripts run on Python 3.11 with the standard library only. Do not add a dependency to a skill script.
- `bookie` and `setup-bookie` import scripts from the skill folders beside them. Keep the five skills in one folder. When you add a skill to `skills/`, add its link in `.claude/skills/` and its line in `.gitignore`.
- Each skill script change needs a test for the behavior that a user of the script can observe.
- Write skill text in short sentences, one instruction in each. Name a thing by what it does.
- The skills and their templates name no company and no person. A test in `skills/bookie/scripts/test_bookie.py` checks the templates.
- Run the skill tests in a temporary folder. A test must never commit to this repository.

## Test a skill by hand

1. Run `make sandbox NAME=<name>`.
2. Start a session in `sandbox/<name>`.
3. Type `/setup-bookie`, then `/bookie`.

`make sandbox` and `make bookie` both run `scripts/install.sh`, so a sandbox gets the same files as a real project. The sandbox has its own git repository, so the bookie commits stay inside it. Never run `bookie.py done` or `setup_bookie.py commit` with this repository as the root.

## Publish

Users install the skills with `npx skills add niccolox/devekko.bookie`, which reads `main` of this repository on GitHub. So a push to `main` publishes the skills to every user's next install and update.

1. Run `make check`.
2. Test the change in a sandbox.
3. Commit and push only when the operator asks.

A second public copy is in the fork `niccolox/pstack-bets`, in a checkout at `../pstack-bets`. `make fork-copy` copies the skills there and runs no git command. In the checkout, make a branch, commit, push, and open a PR only when the operator asks.

## Always ask first

Ask the operator before a push, a PR, a merge, a force-push, or a deletion of a branch.
