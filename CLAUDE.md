# CLAUDE.md

AGENTS.md holds the rules that every agent follows. This file adds what applies only to Claude Code.

@AGENTS.md

## Claude Code

- The five skills load from `.claude/skills/`, which links to `skills/`. A change to a `SKILL.md` applies in the next session.
- Each bet skill starts only from a slash command: `/bookie`, `/setup-bookie`, `/bet-record`, `/bet-diligence`, and `/bet-discovery`. Do not do a skill's steps another way when the Skill tool refuses it.
- The other pstack skills, such as `poteto-mode`, load from `vendor/pstack/` through links in `.claude/skills/`. Run `make pstack` when they are missing. Start a development task with `/poteto-mode`.
- Commit only when the operator asks.
