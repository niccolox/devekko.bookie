import datetime as dt
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from pstack_sync import VENDOR, local_hash, remote_url, status, sync

TODAY = dt.date(2026, 11, 17)

for key in ("GIT_AUTHOR", "GIT_COMMITTER"):
    os.environ[f"{key}_NAME"] = "Sync Test"
    os.environ[f"{key}_EMAIL"] = "sync@example.invalid"


def git(folder, *args):
    return subprocess.run(
        ["git", "-C", str(folder), *args], capture_output=True, text=True, check=True
    ).stdout.strip()


class SyncTest(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        base = Path(self.folder.name)
        self.upstream = base / "upstream"
        self.root = base / "project"
        (self.root / "skills" / "bookie").mkdir(parents=True)
        self.upstream.mkdir()
        git(self.upstream, "init", "-q", "-b", "main")
        self.publish({"how": "v1", "bookie": "upstream copy"})
        lock = {"source": str(self.upstream), "branch": "main"}
        (self.root / "pstack.lock").write_text(json.dumps(lock))

    def tearDown(self):
        self.folder.cleanup()

    def publish(self, skills, remove=()):
        for name, text in skills.items():
            path = self.upstream / "skills" / name
            path.mkdir(parents=True, exist_ok=True)
            (path / "SKILL.md").write_text(text)
        for name in remove:
            git(self.upstream, "rm", "-r", "-q", f"skills/{name}")
        git(self.upstream, "add", "-A")
        git(self.upstream, "commit", "-q", "-m", "change")
        return git(self.upstream, "rev-parse", "HEAD")

    def skill(self, name):
        return (self.root / ".claude" / "skills" / name / "SKILL.md").read_text()

    def test_the_first_sync_pulls_and_links_the_upstream_skills(self):
        result = sync(self.root, TODAY)
        self.assertEqual(result["state"], "updated")
        self.assertEqual(self.skill("how"), "v1")
        lock = json.loads((self.root / "pstack.lock").read_text())
        self.assertEqual(lock["commit"], git(self.upstream, "rev-parse", "HEAD"))
        self.assertEqual(lock["synced"], "2026-11-17")

    def test_a_local_skill_wins_over_the_upstream_skill_of_the_same_name(self):
        result = sync(self.root, TODAY)
        self.assertEqual(result["links"]["local"], ["bookie"])
        self.assertFalse((self.root / ".claude" / "skills" / "bookie").exists())

    def test_no_pull_happens_while_the_hash_is_the_same(self):
        sync(self.root, TODAY)
        marker = self.root / VENDOR / "skills" / "how" / "SKILL.md"
        marker.write_text("edited locally")
        result = sync(self.root, TODAY)
        self.assertEqual(result["state"], "current")
        self.assertEqual(marker.read_text(), "edited locally")

    def test_a_new_hash_replaces_the_files_and_removes_a_deleted_skill(self):
        self.publish({"why": "v1"})
        sync(self.root, TODAY)
        new = self.publish({"how": "v2"}, remove=("why",))
        self.assertEqual(status(self.root)["state"], "changed")
        result = sync(self.root, TODAY)
        self.assertEqual((result["state"], result["to"]), ("updated", new))
        self.assertEqual(self.skill("how"), "v2")
        self.assertEqual(result["links"]["removed"], ["why"])
        self.assertFalse((self.root / ".claude" / "skills" / "why").is_symlink())
        self.assertEqual(local_hash(self.root), new)

    def test_an_unreachable_upstream_keeps_the_local_copy(self):
        sync(self.root, TODAY)
        (self.root / "pstack.lock").write_text(
            json.dumps({"source": str(self.upstream / "gone"), "branch": "main"})
        )
        result = sync(self.root, TODAY)
        self.assertEqual(result["state"], "offline")
        self.assertEqual(self.skill("how"), "v1")

    def test_an_owner_and_name_becomes_a_github_url(self):
        self.assertEqual(remote_url("owner/name"), "https://github.com/owner/name.git")
        self.assertEqual(
            remote_url("https://example.invalid/x.git"), "https://example.invalid/x.git"
        )


if __name__ == "__main__":
    unittest.main()
