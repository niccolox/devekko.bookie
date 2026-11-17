"""Render and write BOOKIE.md, the register of the bets in a project."""

from __future__ import annotations

from pathlib import Path

REGISTER = "BOOKIE.md"
COLUMNS = ("Bet", "Name", "Status", "Stage", "Decision date", "Criteria", "Updated")
Row = dict[str, str]

INTRO = (
    "This file is the register of the bets in this project. Bookie writes it after each "
    "stage, from the bet record and from the progress of each bet. Do not edit it. "
    "Change the bet record, then run `/bookie`."
)
LEGEND = (
    "- **Status** is the status in the bet record.",
    "- **Stage** is the bookie stage that the bet is at. "
    "`not started` means that bookie has not run for the bet.",
    "- **Criteria** counts the kill criteria by result.",
    "- **Updated** is the date of the last finished or skipped stage.",
)
NO_BETS = "No bets yet. `/bookie` starts the first bet."
CONTINUE = "`/bookie BET-NNN` continues a bet at its stage. `/bookie` starts a new bet."


def cell(text: str) -> str:
    """One table cell: one line, with each pipe escaped."""
    return " ".join(text.replace("|", "\\|").split()) or "-"


def render(rows: list[Row], record: str) -> str:
    """The text of the register. The same rows always give the same text."""
    lines = [
        "# Bookie",
        "",
        INTRO,
        "",
        f"The bet record is [`{record}`]({record.replace(' ', '%20')}).",
        "",
        "| " + " | ".join(COLUMNS) + " |",
        "| " + " | ".join("---" for _ in COLUMNS) + " |",
    ]
    lines += [
        "| " + " | ".join(cell(row.get(column, "")) for column in COLUMNS) + " |" for row in rows
    ]
    lines += ["", CONTINUE if rows else NO_BETS, "", *LEGEND]
    return "\n".join(lines) + "\n"


def write(root: Path, text: str) -> str:
    """Write the register when its text changed. Return what happened."""
    path = root / REGISTER
    if not path.exists():
        path.write_text(text, encoding="utf-8")
        return "created"
    if path.read_text(encoding="utf-8") == text:
        return "kept"
    path.write_text(text, encoding="utf-8")
    return "updated"
