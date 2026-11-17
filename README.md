# devekko.bookie

Bookie is a set of [Agent Skills](https://agentskills.io) that helps a builder run a product bet with Claude Code or another agent. A bet is a product idea that gets a fast build, real users, and a go, no-go, or pivot decision on a fixed date.

You install the skills with the [`skills` CLI](https://skills.sh), like any other skill. The first skill that you run, `/setup-bookie`, then adds [pstack](https://github.com/backnotprop/pstack), which the bet skills use.

## Install bookie in a project

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
   - **Project files.** It asks for the stack and the surface. Then it writes `AGENTS.md`, `CLAUDE.md`, `PRODUCTS.md`, `DESIGN.md`, and `.gitignore`. A file that exists keeps its text and gets only its missing lines.
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

The bet skills and pstack can be in different layouts in one project. `/setup-bookie` finds pstack in both.

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
