#!/usr/bin/env python3
"""Keep a local copy of the upstream pstack skills. Pull only when the upstream hash changes."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

LOCK = "pstack.lock"
VENDOR = Path("vendor") / "pstack"
MARKER = ".commit"
KEEP = ("skills", "agents", "LICENSE")
LINKS = Path(".claude") / "skills"


def run(*args: str, cwd: Path | None = None) -> str:
    result = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or f"{' '.join(args)} failed")
    return result.stdout.strip()


def read_lock(root: Path) -> dict[str, str]:
    path = root / LOCK
    if not path.exists():
        raise SystemExit(f"{path} is missing; it names the upstream source and branch")
    return json.loads(path.read_text(encoding="utf-8"))


def write_lock(root: Path, lock: dict[str, str]) -> None:
    (root / LOCK).write_text(json.dumps(lock, indent=2) + "\n", encoding="utf-8")


def remote_url(source: str) -> str:
    """A GitHub owner/name becomes its URL. A URL or a local path stays as it is."""
    if "://" in source:
        return source
    if source.startswith(("/", ".", "~")):
        return str(Path(source).expanduser())
    return f"https://github.com/{source}.git"


def remote_hash(url: str, branch: str) -> str:
    """Ask the remote for the branch's commit hash. This downloads no files."""
    line = run("git", "ls-remote", url, f"refs/heads/{branch}")
    if not line:
        raise RuntimeError(f"{url} has no branch {branch}")
    return line.split()[0]


def local_hash(root: Path) -> str | None:
    marker = root / VENDOR / MARKER
    return marker.read_text(encoding="utf-8").strip() if marker.exists() else None


def pull(root: Path, url: str, branch: str) -> str:
    """Replace the local copy with the branch's files. Return the commit hash that was pulled."""
    with tempfile.TemporaryDirectory() as folder:
        clone = Path(folder) / "pstack"
        run("git", "clone", "--quiet", "--depth", "1", "--branch", branch, url, str(clone))
        pulled = run("git", "rev-parse", "HEAD", cwd=clone)
        if not (clone / "skills").is_dir():
            raise RuntimeError(f"{url} has no skills folder")
        target = root / VENDOR
        if target.exists():
            shutil.rmtree(target)
        target.mkdir(parents=True)
        for name in KEEP:
            source = clone / name
            if source.is_dir():
                shutil.copytree(source, target / name, symlinks=True)
            elif source.exists():
                shutil.copy2(source, target / name)
        (target / MARKER).write_text(pulled + "\n", encoding="utf-8")
    return pulled


def link(root: Path) -> dict[str, list[str]]:
    """Link each upstream skill into .claude/skills. A skill in skills/ wins over upstream."""
    links = root / LINKS
    links.mkdir(parents=True, exist_ok=True)
    upstream = root / VENDOR / "skills"
    names = sorted(p.name for p in upstream.iterdir() if p.is_dir()) if upstream.is_dir() else []
    local = {p.name for p in (root / "skills").iterdir() if p.is_dir()}
    prefix = Path("..") / ".." / VENDOR / "skills"
    removed = []
    for entry in sorted(links.iterdir()):
        points_upstream = entry.is_symlink() and Path(entry.readlink()).parent == prefix
        if points_upstream and (entry.name not in names or entry.name in local):
            entry.unlink()
            removed.append(entry.name)
    added = []
    for name in names:
        entry = links / name
        if name in local or entry.is_symlink() or entry.exists():
            continue
        entry.symlink_to(prefix / name)
        added.append(name)
    return {"added": added, "removed": removed, "local": sorted(local & set(names))}


def status(root: Path) -> dict[str, str | None]:
    lock = read_lock(root)
    have = local_hash(root)
    remote = remote_hash(remote_url(lock["source"]), lock["branch"])
    return {
        "source": lock["source"],
        "branch": lock["branch"],
        "local": have,
        "remote": remote,
        "state": "current" if have == remote else "changed" if have else "missing",
    }


def sync(root: Path, today: dt.date, force: bool = False) -> dict[str, Any]:
    lock = read_lock(root)
    url = remote_url(lock["source"])
    have = local_hash(root)
    try:
        remote = remote_hash(url, lock["branch"])
    except RuntimeError as error:
        if have:
            return {"state": "offline", "local": have, "reason": str(error), "links": link(root)}
        raise SystemExit(f"cannot reach {url}, and there is no local copy: {error}") from error
    if have == remote and not force:
        return {"state": "current", "local": have, "links": link(root)}
    pulled = pull(root, url, lock["branch"])
    lock.update(commit=pulled, synced=today.isoformat())
    write_lock(root, lock)
    return {"state": "updated", "from": have, "to": pulled, "links": link(root)}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("check", "sync"))
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--force", action="store_true", help="pull even when the hash is the same")
    parser.add_argument("--today", type=dt.date.fromisoformat, default=dt.date.today())
    args = parser.parse_args(argv)
    if args.command == "check":
        try:
            print(json.dumps(status(args.root), indent=1))
        except RuntimeError as error:
            print(
                json.dumps(
                    {"state": "offline", "local": local_hash(args.root), "reason": str(error)},
                    indent=1,
                )
            )
    else:
        print(json.dumps(sync(args.root, args.today, args.force), indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
