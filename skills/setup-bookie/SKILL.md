---
name: setup-bookie
description: "Set up a project for pstack and bookie in one pass, in place of setup-pstack: install pstack when it is missing, write the pstack model settings into the project, write AGENTS.md, CLAUDE.md, PRODUCTS.md, DESIGN.md, and .gitignore, turn off setup-pstack, and commit the result. Use for /setup-bookie, 'set up bookie', 'set up this project for bets', 'configure pstack models' in a project that uses bookie, or a new project that will run /bookie."
disable-model-invocation: true
---

# Setup bookie

This skill replaces `/setup-pstack` in a project that runs bets with **bookie**. It installs pstack when the project does not have it, does the pstack model setup, writes the project files that bookie needs, turns `setup-pstack` off for the project, and commits. After it, `/bookie` starts with its setup stage already passed.

Run each command from the project root. `<scripts>` is the `scripts` folder beside this file, for example `.claude/skills/setup-bookie/scripts`.

## 1. Pstack

The bet skills use pstack skills such as `setup-pstack` and `poteto-mode`. Check that the project has them:

```sh
python3 <scripts>/setup_bookie.py pstack
```

When `state` is `present`, go to step 2. When `state` is `missing`:

1. Tell the operator that pstack is missing and that you install it from the `source` in the result.
2. Run the `install` command from the result, unchanged, from the project root. It uses the same `skills` CLI that installed this skill, and it records the source and its commit in `skills-lock.json`.
3. Run the check again. It must print `present`.

If `npx` is not available or the network fails, stop. Give the operator the `install` command to run, and continue when the check prints `present`. Never copy pstack files from another project by hand.

## 2. Models

Read [`../setup-pstack/SKILL.md`](../setup-pstack/SKILL.md) and do its steps 1 to 6, with these changes:

- **Write to the project, not the home folder.** Claude Code: `.claude/rules/pstack-models.md`. Cursor: `.cursor/rules/pstack-models.mdc`. Other harnesses: `.agents/pstack-models.md`. The pstack skills read the project file because `CLAUDE.md` names it in step 3.
- **Panels with one vendor.** When the detected models are all Anthropic models, set each panel role (`arena runners`, `arena cross-judge pool`, `architect runners`, `interrogate reviewers`) to one Fable, one Opus, and one Sonnet slug at `high`. Tell the operator that arena runs no cross-judge, because a cross-judge needs another vendor.
- **Budget.** Offer `large` first. It matches the pstack defaults.
- **Speed.** Claude Code subagents have no fast mode. Write each slug without `-fast` there.

Do not do steps 7 and 8 here. Bookie's gates and the build stage cover verification.

## 3. Project files

1. Print the questions and send them to the question tool (`AskUserQuestion` in Claude Code) unchanged:

   ```sh
   python3 <scripts>/setup_bookie.py questions
   ```

2. Write the files with the answers. The record path is `docs/bet-process.md` unless the operator wants the record out of git, then `.local/bet-process.md`:

   ```sh
   python3 <scripts>/setup_bookie.py project --stack <answer> --surface <answer> --record <path>
   ```

   The script writes `AGENTS.md`, `CLAUDE.md`, `PRODUCTS.md`, `DESIGN.md`, and `.gitignore` from the **bookie** templates, and adds `"setup-pstack": "off"` to `.claude/settings.json`. It never replaces a file. An existing file gets only its missing lines, as the **Project files** section of [`../bookie/SKILL.md`](../bookie/SKILL.md) says.

3. Add one line to `CLAUDE.md` that names the model settings file from step 2, for example: "The pstack model settings are in `.claude/rules/pstack-models.md`. Read them from this project, not from the home folder."

4. Fill each `{{TODO}}` as the **Project files** section of the bookie skill says. Ask the operator in chat for one paragraph about the product when you do not have one: the problem, who has it, what they do today, and who pays. Write `Open:` and a question for each fact that is not known. Keep the files anonymous.

5. Check the files. Fix each problem that it prints:

   ```sh
   python3 <scripts>/setup_bookie.py check --record <path>
   ```

## 4. Commit

```sh
python3 <scripts>/setup_bookie.py commit --record <path>
```

The script refuses while `check` fails. It runs `git init` in a folder with no repository. On `main`, `master`, or a new repository, it switches to the branch `setup/bookie`, and it commits every change under the project root. Files named like secrets stay out; the result lists them in `left_out`, and you tell the operator about each one. It never pushes.

## 5. Report

Tell the operator:

- Whether pstack was present or installed, with its source.
- The model settings file and the budget.
- Each project file and what happened to it: created, lines added, or kept.
- That `/setup-pstack` is off in this project, and that `/setup-bookie` changes the models from now on.
- The commit and its branch.
- The next step: `/bookie` starts the first bet.
- How to update later: the `update` command from step 1 checks each source and updates the skills that changed.

## Rules

- Never write a model slug that you did not detect, as `setup-pstack` says.
- Never write a name, an email, or a company name into the project files.
- Never push. A push, a PR, and a merge need the operator's words.
