# devekko.bookie

Bookie is a set of [Agent Skills](https://agentskills.io) that helps a builder run a product bet with Claude Code or another agent. A bet is a product idea that gets a fast build, real users, and a go, no-go, or pivot decision on a fixed date.

## Why a bookie

Each product idea is a bet. You put in time and money. On the decision date, the bet is settled: go, no-go, or pivot. A bookie takes the bet, writes down the terms before the start, and pays out on the result, not on how the backer feels about it. This skill does the same job for a product.

A builder who is excited about an idea is a bad judge of it. The builder sees a demo that works, three friends who say "nice", and one person who will "probably pay". So the builder moves the decision date by two weeks, then again. Bookie stops that:

- **The terms come first.** Before the first line of code, you write the core question, 3 to 6 kill criteria, and a decision date. Each criterion has a number and names the evidence that counts. For example: "4 of 10 trial users run the report a second time in week 2."
- **The terms do not move.** After the frame stage, no agent changes a criterion, a threshold, or the date. Only you can, and the record shows that you did.
- **Bookie counts acts, not words.** A compliment is not usage. A promise is not a payment. The Customer evidence table logs only what a person did.
- **The bet is settled on the date.** At the score stage, the agent runs the commands that make the evidence again and sets each criterion to `met` or `not met`. Then you write the memo and make the call.

A no-go is a good result. It costs two to four weeks, not two years.

## The register

`BOOKIE.md` at the project root is the register of the bets. It shows every bet in the project in one table, so you and each agent can see the state at a glance:

```markdown
| Bet | Name | Status | Stage | Decision date | Criteria | Updated |
| --- | --- | --- | --- | --- | --- | --- |
| BET-001 | Invoice match | Decided: no-go | finished | 2026-09-30 | 1 met, 3 not met | 2026-09-30 |
| BET-002 | Weekly cash report | With users | iterate (9 of 11) | 2026-12-04 | 2 met, 2 open | 2026-11-16 |
| BET-003 | Supplier risk alerts | Framing | frame (2 of 11) | | none | 2026-11-17 |
```

- **Bookie writes it, not you.** The script writes the register again after each stage, so each stage commit holds the current state. An edit by hand is replaced at the next stage.
- **Agents read it first.** Before a task, an agent finds the bet in the register. When the bet is not yet at the build stage, the agent writes no code. It asks you to type `/bookie BET-NNN`.
- **It keeps old bets.** A bet with the status `Decided: no-go` stays in the table. The next idea starts with a record of what failed and why.
- **It is as private as the record.** When git ignores the bet record, git also ignores `BOOKIE.md`.

## Install bookie in a project

You install the skills with the [`skills` CLI](https://skills.sh), like any other skill. The first skill that you run, `/setup-bookie`, then adds [pstack](https://github.com/backnotprop/pstack), which the bet skills use.

You need Node.js for `npx`, `git`, and Python 3.11 or later.

1. Install the skills. Run this from the root of your project:

   ```bash
   npx skills add niccolox/devekko.bookie
   ```

   The CLI lists the five skills. Select all five, then select your agents. `bookie` and `setup-bookie` use scripts from the skill folders beside them, so install the five skills together.

   To install with no questions, name the skills and the agent:

   ```bash
   npx skills add niccolox/devekko.bookie --skill '*' -a claude-code -y
   ```

2. Set up the project. Start your agent in the project and type the command:

   ```text
   /setup-bookie
   ```

   The skill does these steps in order:

   - **Pstack.** It checks that the project has the pstack skills. When they are missing, it installs them from `backnotprop/pstack` with the same `skills` CLI.
   - **Models.** It picks the pstack models and writes them into the project.
   - **Project files.** It asks for the stack and the surface. FastAPI and React is the recommended stack: a FastAPI API on Python with `uv`, and a React UI with TypeScript in `web/`. Then it writes `AGENTS.md`, `CLAUDE.md`, `PRODUCTS.md`, `DESIGN.md`, and `.gitignore`. A file that exists keeps its text and gets only its missing lines. It also writes `BOOKIE.md`, the register of the bets.
   - **Commit.** It turns `/setup-pstack` off for the project and makes one commit on the branch `setup/bookie`. In a folder with no git repository, it runs `git init` first. It never pushes.

3. Start the first bet:

   ```text
   /bookie
   ```

   The skill asks for one paragraph about the problem, then runs the stages in order. Later, `/bookie BET-001` continues at the stage where the last run stopped.

### What the install adds to your project

| Path | What it is |
| --- | --- |
| `.claude/skills/<name>` | Each skill, where Claude Code reads it. |
| `.agents/skills/<name>/` | Present when the CLI installs for several agents. It then holds the files, and `.claude/skills/<name>` is a link to them. |
| `skills-lock.json` | The source and the commit of each skill. Commit this file. |

The skills can be in different layouts in one project. An update can also move a skill from a folder to a link. The scripts find the skills beside them in every mix of the two.

### Update

```bash
npx skills update
```

The CLI checks each source in `skills-lock.json` and updates the skills that changed. This covers the bet skills and pstack. Read `git diff` after an update, because an update can replace a change that you made to an installed skill.

### Install pstack yourself

You can install pstack before `/setup-bookie`. The skill then finds it and installs nothing:

```bash
npx skills add backnotprop/pstack --skill '*' -y
```

### What bookie does in your project

- **It runs eleven stages:** setup, frame, build-or-buy, scope, evals, build, harden, users, iterate, score, memo. Each stage must pass a gate before the next stage starts.
- **It asks you each product call** through the question tool: the kill criteria, the decision date, the scope, the human step, and the decision.
- **It keeps a register.** `BOOKIE.md` has one row for each bet. See [The register](#the-register).
- **It puts the bet before the build.** `AGENTS.md` tells each agent to read `BOOKIE.md` and run the record checker before a task. An agent writes no code for a bet that is not framed or is not yet at the build stage. `/poteto-mode` starts after those steps.
- **It commits.** Each finished or skipped stage is one local commit, `bookie(BET-NNN): <stage> done`, on the branch `bet/bet-nnn`. Files named like secrets stay out of the commit. It never pushes.
- **It saves prompts.** Each filled prompt goes to `.local/bookie/BET-NNN/prompts/`, which git ignores.

## Skills

| Skill | What it does |
| --- | --- |
| [`setup-bookie`](skills/setup-bookie/SKILL.md) | Sets up a project in one pass, in place of `setup-pstack`: pstack, model settings, project files, `.gitignore`, and a commit. |
| [`bookie`](skills/bookie/SKILL.md) | Runs one bet from setup to the memo. |
| [`bet-record`](skills/bet-record/SKILL.md) | Keeps the bet record: core question, kill criteria, decision date, build log, score, and memo. |
| [`bet-diligence`](skills/bet-diligence/SKILL.md) | Writes a diligence memo on a dependency, product, or company, with evidence for each finding. |
| [`bet-discovery`](skills/bet-discovery/SKILL.md) | Plans customer interviews and logs only what people did. |

Each skill starts only from its slash command.

## Develop the skills

This part is for a person who changes the skills. It needs `uv`, `make`, and `rsync`.

```text
skills/<name>/           The source of each skill: SKILL.md, scripts/, references/
.claude/skills/<name>    A link to skills/<name>, so a session here loads the source
vendor/pstack/           The upstream pstack skills (git ignores this folder)
pstack.lock              The upstream source, branch, and commit hash
scripts/, tests/         The scripts that the Makefile runs, and their tests
sandbox/                 Test projects (git ignores this folder)
docs/status.md           The current state and the open work
```

```bash
make install     # the development tools
make pstack      # the upstream skills
make check       # lint, types, and tests on Python 3.11
```

Run `make help` for every command. [AGENTS.md](AGENTS.md) holds the rules for a change to a skill.

### Upstream pstack in this repository

A session in this repository, and each sandbox, uses the pstack skills from `vendor/pstack/`. `pstack.lock` names their source:

```json
{
  "source": "backnotprop/pstack",
  "branch": "main",
  "commit": "<the hash of the last pull>",
  "synced": "<the date of the last pull>"
}
```

| Command | What it does |
| --- | --- |
| `make pstack` | Asks GitHub for the branch's current hash. Pulls the files into `vendor/pstack/` only when that hash differs from the hash of the local copy. |
| `make pstack-check` | Compares the two hashes and pulls nothing. |

With no network, each command keeps the local copy. `setup-bookie` installs pstack from the same source, and a test fails when the two differ. To use another source, change `source` in `pstack.lock` and `PSTACK_SOURCE` in `skills/setup-bookie/scripts/setup_bookie.py`.

### Test a change before you publish it

`npx skills add` installs the version on GitHub. To test the working copy, use one of these:

```bash
make sandbox NAME=demo            # a new test project in sandbox/demo
make bookie REPO=../my-project    # an existing project
```

Both copy the working copy of the five bet skills, and the pstack skills from `vendor/pstack/`, into the project's `.claude/skills/`. `make bookie` keeps a pstack skill that the project already has. It runs no git command in the project.

Then start a session in the project and type `/setup-bookie`, then `/bookie`. A sandbox has its own git repository, so the bookie commits stay inside it. The skills in a project are copies, so install again after a change to the source. `make sandbox-clean` removes every sandbox.

### Publish

A push to `main` of this repository publishes the skills, because `npx skills add` and `npx skills update` read it. Run `make check` first.

A second public copy is in the fork [`niccolox/pstack-bets`](https://github.com/niccolox/pstack-bets), with a checkout at `../pstack-bets`. [docs/status.md](docs/status.md) says which version that copy holds.

```bash
make fork-diff     # shows which skills differ from the checkout
make fork-copy     # copies the skills into ../pstack-bets/skills
```

`fork-copy` runs no git command. Make the branch, the commit, and the PR in the checkout.
