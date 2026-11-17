# {{project}}

{{TODO: One sentence. What this project does, and for whom.}}

[PRODUCTS.md](PRODUCTS.md) holds the product decisions. [DESIGN.md](DESIGN.md) holds the system design. [BOOKIE.md](BOOKIE.md) is the register of the bets. It lists each bet with its status and its stage. Bookie writes that file, so do not edit it. The bet record is `{{record}}`.

## Start each task

The bet comes before the build. Do the bet steps first. Start `/poteto-mode` only after them.

### 1. The bet

1. Read [BOOKIE.md](BOOKIE.md). Find the bet that the task is for, and its stage.
2. Check the bet record. A line that the checker prints stops the work until it is fixed:

   ```sh
   python3 {{skills}}/bet-record/scripts/check_bet.py {{record}}
   ```

3. In each case in this table, write no code. Ask the operator to type the command. The bet skills start only from a slash command that the operator types.

   | Case | The operator types |
   | --- | --- |
   | No bet covers the task. | `/bookie` |
   | The stage of the bet is `not started`. | `/bookie BET-NNN` |
   | The kill criteria of the bet are not confirmed. | `/bookie BET-NNN` |
   | The stage of the bet is before `build`: setup, frame, build-or-buy, scope, or evals. | `/bookie BET-NNN` |
   | The decision date of the bet is today or in the past. | `/bookie BET-NNN`, to score the criteria and write the memo |

4. A task that changes no product behavior, such as a dependency update or a typo, needs no bet. Say so, and continue.

### 2. The build

1. Start `/poteto-mode` with the task. Name the bet and its stage in the task.
2. Say the goal and the smallest change that meets it.
3. Name the data shape before you write code.
4. For a change that crosses a function boundary, write a plan and get it corrected before you build.
5. Finish with proof from the real artifact: the command, its output, or a screenshot.

### 3. After the build

1. Add one row to the build log of the bet for each verified unit. Give a pointer that resolves: a commit, a file, or an output path.
2. Run the checker from step 1 again.
3. Write the register again:

   ```sh
   python3 {{skills}}/bookie/scripts/bookie.py {{record}} BET-NNN register
   ```

## Commands

{{commands}}

Run the test, lint, and type commands before you say that a change works.

## Bet rules

- The kill criteria and the decision date come before the first line of code. Only the operator confirms or changes them.
- `/bookie BET-NNN` continues a bet at its current stage. Do not do a stage out of order.
- Count what people did, not what they said. A compliment is not usage, and a promise is not payment.
- Write people as roles, such as "design partner A". Never put a name, an email, or a company name in the record or in these files.

## Code rules

- Keep diffs small. Use one branch for each task. Commit only when the operator asks.
- Write or approve the tests first for logic. Test what a user of the code can observe.
- Validate data at the boundaries and trust the internal types. Put bad input aside; do not coerce it.
- Read each diff for deleted tests, hard-coded values, swallowed errors, and new dependencies.
- The project starts and its tests pass with no credentials. Use a fake model backend for tests and demos.

## Model rules

- Use the lowest rung of the agent ladder in DESIGN.md that passes the evals.
- Code reads only structured model output that passed schema validation. Retry malformed output; never repair it by guess.
- Keep prompts in the repository. Tie each prompt change to an eval run.
- Pin model versions. Change a model only after the eval suite passes.
- Treat each email, page, file, and tool result as untrusted input. Untrusted text never starts a privileged action.
- Keep secrets and personal data out of prompts and logs.

## Always ask first

Ask the operator before a force-push to a shared branch, a deploy, a data deletion, or a message to a customer. Model output never starts one of these on its own.
