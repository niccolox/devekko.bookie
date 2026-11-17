# devekko.bookie

Development repository for the bookie and bet skills. It has two purposes:

1. It holds the source of the skills.
2. It tests them, with automated tests and with test projects.

The skills are [Agent Skills](https://agentskills.io) for Claude Code and other agents. They help a builder run a product bet: frame it with kill criteria and a decision date, build a thin slice, put it in front of users, and write an honest go, no-go, or pivot memo.

## Skills

| Skill | What it does |
| --- | --- |
| [`setup-bookie`](skills/setup-bookie/SKILL.md) | Sets up a project in one pass, in place of `setup-pstack`: model settings, `AGENTS.md`, `CLAUDE.md`, `PRODUCTS.md`, `DESIGN.md`, `.gitignore`, and a commit. |
| [`bookie`](skills/bookie/SKILL.md) | Runs one bet through eleven stages, from setup to the memo. It asks the operator each product call, checks a gate before each next stage, commits each stage, and saves each prompt to `.local/`. |
| [`bet-record`](skills/bet-record/SKILL.md) | Keeps the bet record: core question, kill criteria, decision date, build log, score, and memo. |
| [`bet-diligence`](skills/bet-diligence/SKILL.md) | Writes a diligence memo on a dependency, product, or company, with evidence for each finding. |
| [`bet-discovery`](skills/bet-discovery/SKILL.md) | Plans customer interviews and logs only what people did. |

## Layout

```text
skills/<name>/           The source of each skill: SKILL.md, scripts/, references/
.claude/skills/<name>    A link to skills/<name>, so a session here loads the source
vendor/pstack/           The upstream pstack skills (git ignores this folder)
pstack.lock              The upstream source, branch, and commit hash
scripts/, tests/         The scripts that the Makefile runs, and their tests
sandbox/                 Test projects (git ignores this folder)
docs/status.md           The current state and the open work
```

## Start

You need `uv`, `git`, and `make`.

```bash
make install
make pstack
make check
```

`make check` runs the lint, the type check, and the tests on Python 3.11. Run `make help` for every command.

## Upstream pstack

The bet skills work with the other pstack skills, such as `poteto-mode` and `setup-pstack`. Those come from the repository in `pstack.lock`:

```json
{
  "source": "backnotprop/pstack",
  "branch": "main",
  "commit": "<the hash of the last pull>",
  "synced": "<the date of the last pull>"
}
```

`make pstack` asks GitHub for the branch's current hash. It pulls the files into `vendor/pstack/` only when that hash differs from the hash of the local copy. `make pstack-check` compares the hashes and pulls nothing. With no network, both keep the local copy.

To use another source, such as the fork, change `source` and run `make pstack`.

## Test a skill by hand

```bash
make sandbox NAME=demo
cd sandbox/demo && claude
```

In the session, type `/setup-bookie`, then `/bookie`.

The sandbox is a new project with its own git repository. It gets the upstream pstack skills from `vendor/pstack/`, and then the five skills from this repository as copies. A copy does not change when you edit the source, so make a new sandbox after a change. `make sandbox-clean` removes every sandbox.

## Publish to the fork

The public copy is in [`niccolox/pstack-bets`](https://github.com/niccolox/pstack-bets), which also holds the rest of pstack. Projects install the skills from there:

```bash
npx skills add niccolox/pstack-bets -s setup-bookie -s bookie -s bet-record -s bet-diligence -s bet-discovery -s setup-pstack --copy
```

To publish a change:

```bash
make check
make fork-diff     # shows which skills differ from the checkout
make fork-copy     # copies the skills into ../pstack-bets/skills
```

`fork-copy` runs no git command. Make the branch, the commit, and the PR in the checkout.
# devekko.bookie
