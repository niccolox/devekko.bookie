import itertools
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS: tuple[str, ...] = ("setup-bookie", "bookie", "bet-record")


class LayoutTest(unittest.TestCase):
    """The skills CLI installs a skill as a folder or as a link, and an update can change that.

    Each script must find the skills beside it in every mix of the two.
    """

    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.project = Path(self.folder.name)

    def tearDown(self):
        self.folder.cleanup()

    def install(self, linked: dict[str, bool]) -> Path:
        """Put each skill in the agent folder: as a link to the store, or as a real folder."""
        base = self.project / "-".join(name for name, link in linked.items() if link)
        agent, store = base / ".claude" / "skills", base / ".agents" / "skills"
        agent.mkdir(parents=True)
        for name, link in linked.items():
            target = (store if link else agent) / name
            shutil.copytree(
                ROOT / "skills" / name, target, ignore=shutil.ignore_patterns("__pycache__")
            )
            if link:
                (agent / name).symlink_to(Path("..") / ".." / ".agents" / "skills" / name)
        return base

    def run_script(self, base: Path, script: str, *args: str) -> subprocess.CompletedProcess[str]:
        command = [sys.executable, str(Path(".claude") / "skills" / script), *args]
        return subprocess.run(command, cwd=base, capture_output=True, text=True)

    def test_each_script_runs_in_every_mix_of_folders_and_links(self):
        for flags in itertools.product((False, True), repeat=len(SKILLS)):
            linked = dict(zip(SKILLS, flags, strict=True))
            base = self.install(linked)
            with self.subTest(linked=linked):
                bookie = self.run_script(
                    base, "bookie/scripts/bookie.py", "docs/bets.md", "BET-001", "status"
                )
                self.assertEqual(bookie.returncode, 0, bookie.stderr[-300:])
                setup = self.run_script(base, "setup-bookie/scripts/setup_bookie.py", "questions")
                self.assertEqual(setup.returncode, 0, setup.stderr[-300:])


if __name__ == "__main__":
    unittest.main()
