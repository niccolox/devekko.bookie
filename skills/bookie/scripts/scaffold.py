"""Write the project files that a bet needs: AGENTS.md, CLAUDE.md, PRODUCTS.md, DESIGN.md."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

TEMPLATES = Path(__file__).resolve().parents[1] / "references" / "templates"
FILES = ("AGENTS.md", "CLAUDE.md", "PRODUCTS.md", "DESIGN.md")
TODO = "{{TODO"
DEFAULT_SKILLS = ".claude/skills"
ALIASES = {"PRODUCTS.md": "PRODUCT.md"}
RECOMMENDED = " (Recommended)"


@dataclass(frozen=True)
class Stack:
    """One stack that a project can use, and what each project file gets for it."""

    hint: str
    commands: tuple[tuple[str, str], ...]
    notes: tuple[str, ...]
    ignore: tuple[str, ...]


PYTHON_IGNORE = (
    "# Python",
    "__pycache__/",
    "*.pyc",
    ".venv/",
    ".pytest_cache/",
    ".ruff_cache/",
    "dist/",
)
NODE_IGNORE = ("# TypeScript", "node_modules/", "dist/", "coverage/", "*.tsbuildinfo")

# The first stack is the one that the setup question recommends.
STACKS: dict[str, Stack] = {
    "FastAPI and React": Stack(
        hint="A FastAPI API on Python with uv, and a React UI with TypeScript in web/.",
        commands=(
            ("Install", "`uv sync` and `npm --prefix web install`"),
            ("Test", "`uv run pytest` and `npm --prefix web test`"),
            ("Lint", "`uv run ruff check .` and `npm --prefix web run lint`"),
            ("Types", "`uv run pyright` and `npm --prefix web run typecheck`"),
            ("Run the API", "`uv run fastapi dev`"),
            ("Run the UI", "`npm --prefix web run dev`"),
        ),
        notes=(
            "**API.** FastAPI on Python, managed with `uv`. The app is in `app/main.py`, so "
            "`uv run fastapi dev` finds it with no path. The dependency is `fastapi[standard]`. "
            "Pydantic models are the typed domain model.",
            "**UI.** React with TypeScript, built with Vite, in `web/`. Its `package.json` has "
            "the scripts `dev`, `lint`, `typecheck`, and `test`. The Vite template gives `dev` "
            "and `lint`. Add `typecheck` as `tsc -b` and `test` as `vitest run`.",
            "**Contract.** The UI gets its types from the OpenAPI schema of the API, made with "
            "`openapi-typescript`. Do not write the same type by hand on both sides.",
            "**Rules.** The business rules are in the API. The UI shows state and sends "
            "actions, and it holds no rule that the API also holds.",
            "**Tools.** `pytest`, `ruff`, and `pyright` check the API, as development "
            'dependencies. In `pyproject.toml`, set `pythonpath = ["."]` under '
            "`[tool.pytest.ini_options]`, so that the tests in `tests/` can import `app`. "
            "`vitest` tests the UI. A browser test covers each flow that a user depends on.",
        ),
        ignore=(*PYTHON_IGNORE, *NODE_IGNORE),
    ),
    "Python": Stack(
        hint="Python with uv, pytest, ruff, and pyright. No UI package.",
        commands=(
            ("Install", "`uv sync`"),
            ("Test", "`uv run pytest`"),
            ("Lint", "`uv run ruff check .`"),
            ("Types", "`uv run pyright`"),
            ("Run", "{{TODO: the command that starts the app}}"),
        ),
        notes=(
            "Python, managed with `uv`. Pydantic models are the typed domain model.",
            "`pytest`, `ruff`, and `pyright` check the code.",
        ),
        ignore=PYTHON_IGNORE,
    ),
    "TypeScript": Stack(
        hint="TypeScript with npm, and the scripts test, lint, and typecheck.",
        commands=(
            ("Install", "`npm install`"),
            ("Test", "`npm test`"),
            ("Lint", "`npm run lint`"),
            ("Types", "`npm run typecheck`"),
            ("Run", "{{TODO: the command that starts the app}}"),
        ),
        notes=(
            "TypeScript, managed with `npm`. The types are the domain model. Parse outside "
            "data at the boundary into typed values.",
            "The `package.json` has the scripts `test`, `lint`, and `typecheck`.",
        ),
        ignore=NODE_IGNORE,
    ),
    "Other": Stack(
        hint="Another stack. You fill in the commands and the stack notes.",
        commands=(
            ("Install", "{{TODO}}"),
            ("Test", "{{TODO}}"),
            ("Lint", "{{TODO}}"),
            ("Types", "{{TODO}}"),
            ("Run", "{{TODO}}"),
        ),
        notes=(
            "{{TODO: The language, the framework, and the package manager, with the reason "
            "for the choice.}}",
        ),
        ignore=(),
    ),
}

SURFACES: dict[str, str] = {
    "Web UI": (
        "A web UI. Each screen shows the items, the state of each item, and what waits for a "
        "person. An action that a person approves shows the change before it happens. Each "
        "screen has a loading, an empty, and an error state."
    ),
    "API only": (
        "An API with no UI. Each endpoint validates its input at the boundary and returns typed "
        "errors that say what to fix. The API publishes its schema, and clients use types made "
        "from it."
    ),
    "Command line": (
        "A command-line tool. Each command that changes data prints what it will change and has "
        "a dry-run flag. Output for people is plain text; output for scripts is JSON."
    ),
    "Email or chat": (
        "No UI of its own. The agent works in email or chat. Each message that it sends says "
        "what it did, what it did not do, and how to reach a person."
    ),
}

IGNORE_BASE = (
    "# Private notes, saved prompts, and decision trails",
    ".local/",
    ".audit/",
    "# Secrets",
    ".env",
    ".env.*",
    "!.env.example",
    "*.pem",
    "*.key",
    "# Editors and systems",
    ".DS_Store",
    ".idea/",
    ".vscode/",
)


def stack_key(answer: str) -> str:
    """The stack that an answer names. The question marks the first stack as recommended."""
    key = answer.strip().removesuffix(RECOMMENDED)
    if key not in STACKS:
        raise SystemExit(f"--stack must be one of: {', '.join(STACKS)}")
    return key


def commands_table(stack: str) -> str:
    lines = ["| Task | Command |", "| --- | --- |"]
    lines += [f"| {task} | {command} |" for task, command in STACKS[stack].commands]
    return "\n".join(lines)


def stack_notes(stack: str) -> str:
    notes = STACKS[stack].notes
    return notes[0] if len(notes) == 1 else "\n".join(f"- {note}" for note in notes)


def setup_questions(prefix: str = "") -> list[dict[str, object]]:
    """The two questions for the question tool that set the stack and the surface."""
    first = next(iter(STACKS))
    return [
        {
            "question": f"{prefix}which stack does the project use?",
            "header": "Stack",
            "multiSelect": False,
            "options": [
                {"label": name + (RECOMMENDED if name == first else ""), "description": stack.hint}
                for name, stack in STACKS.items()
            ],
        },
        {
            "question": f"{prefix}what does a person use to work with the product?",
            "header": "Surface",
            "multiSelect": False,
            "options": [
                {"label": k, "description": v.split(". ")[0] + "."} for k, v in SURFACES.items()
            ],
        },
    ]


CLAUDE_IMPORT = "\n## Shared agent rules\n\n@AGENTS.md\n"
RECORD_LINE = (
    "\n## Bet record\n\nThe bet record is `{record}`. The `bet-record` skill reads and checks "
    "it, and `/bookie BET-NNN` continues a bet at its current stage.\n"
)


def existing(root: Path, name: str) -> Path | None:
    for candidate in (name, ALIASES.get(name)):
        if candidate and (root / candidate).exists():
            return root / candidate
    return None


def write_ignore(root: Path, stack: str) -> str:
    """Create .gitignore, or add the missing default lines to it."""
    path = root / ".gitignore"
    wanted = list(dict.fromkeys([*IGNORE_BASE, *STACKS[stack].ignore]))
    if not path.exists():
        path.write_text("\n".join(wanted) + "\n", encoding="utf-8")
        return "created"
    lines = path.read_text(encoding="utf-8").splitlines()
    have = {line.strip() for line in lines}
    missing = [line for line in wanted if not line.startswith("#") and line not in have]
    if not missing:
        return "kept"
    path.write_text("\n".join([*lines, "", "# Added by bookie", *missing]) + "\n", encoding="utf-8")
    return f"added {len(missing)} lines"


def skills_folder(root: Path, here: Path | None = None) -> str:
    """The folder that holds the installed skills, as a path from the project root.

    The folder differs between agents, so take it from the place of this script. A script
    that runs from outside the project gives the usual folder for Claude Code.
    """
    here = here or Path(__file__).absolute().parents[2]
    relative = os.path.relpath(here, os.path.abspath(root))
    return DEFAULT_SKILLS if relative.startswith("..") else relative


def render(name: str, project: str, record: str, stack: str, surface: str, skills: str) -> str:
    text = (TEMPLATES / name).read_text(encoding="utf-8")
    return (
        text.replace("{{project}}", project)
        .replace("{{record}}", record)
        .replace("{{skills}}", skills)
        .replace("{{commands}}", commands_table(stack))
        .replace("{{stack}}", stack_notes(stack))
        .replace("{{surface}}", SURFACES[surface])
    )


def scaffold(root: Path, record: Path, stack: str, surface: str) -> list[tuple[str, str]]:
    """Create each missing file. Add only the missing links to an existing one."""
    stack = stack_key(stack)
    if surface not in SURFACES:
        raise SystemExit(f"--surface must be one of: {', '.join(SURFACES)}")
    relative = os.path.relpath(record.resolve(), root.resolve())
    actions = [(".gitignore", write_ignore(root, stack))]
    for name in FILES:
        path = existing(root, name)
        if path is None:
            (root / name).write_text(
                render(name, root.resolve().name, relative, stack, surface, skills_folder(root)),
                encoding="utf-8",
            )
            actions.append((name, "created"))
            continue
        text = path.read_text(encoding="utf-8")
        if name == "CLAUDE.md" and "AGENTS.md" not in text:
            path.write_text(text.rstrip("\n") + "\n" + CLAUDE_IMPORT, encoding="utf-8")
            actions.append((name, "added the AGENTS.md import"))
        elif name == "AGENTS.md" and relative not in text:
            path.write_text(
                text.rstrip("\n") + "\n" + RECORD_LINE.format(record=relative), encoding="utf-8"
            )
            actions.append((name, "added the bet record line"))
        else:
            actions.append((name, f"kept {path.name}" if path.name != name else "kept"))
    return actions


def check(root: Path, record: Path) -> str | None:
    """Return the first problem with the project files, or None."""
    paths = {name: existing(root, name) for name in FILES}
    missing = [name for name, path in paths.items() if path is None]
    if missing:
        return f"missing in {root}: {', '.join(missing)}"
    relative = os.path.relpath(record.resolve(), root.resolve())
    texts = {path.name: path.read_text(encoding="utf-8") for path in paths.values() if path}
    if not any(relative in texts.get(name, "") for name in FILES[:2]):
        return f"neither AGENTS.md nor CLAUDE.md names the bet record {relative}"
    for name, text in texts.items():
        for number, line in enumerate(text.splitlines(), 1):
            if TODO in line:
                return f"{name}:{number} still has a {TODO} marker"
    return None
