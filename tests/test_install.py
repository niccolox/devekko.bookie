import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INSTALL = ROOT / "scripts" / "install.sh"


class InstallTest(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        base = Path(self.folder.name)
        self.pstack = base / "pstack"
        for name, text in (("how", "upstream how"), ("bookie", "upstream bookie")):
            (self.pstack / "skills" / name).mkdir(parents=True)
            (self.pstack / "skills" / name / "SKILL.md").write_text(text)
        (self.pstack / "agents").mkdir()
        (self.pstack / "agents" / "poteto-agent.md").write_text("agent")
        (self.pstack / ".commit").write_text("abcdef1234567\n")
        self.project = base / "project"
        self.project.mkdir()

    def tearDown(self):
        self.folder.cleanup()

    def install(self, target=None, **env):
        return subprocess.run(
            [str(INSTALL), str(target or self.project)],
            capture_output=True,
            text=True,
            env={**os.environ, "PSTACK": str(self.pstack), "BOOKIE_NO_SYNC": "1", **env},
        )

    def skill(self, name):
        return (self.project / ".claude" / "skills" / name / "SKILL.md").read_text()

    def test_a_new_project_gets_pstack_the_bet_skills_and_the_agents(self):
        result = self.install()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.skill("how"), "upstream how")
        self.assertEqual(
            self.skill("bookie"), (ROOT / "skills" / "bookie" / "SKILL.md").read_text()
        )
        self.assertTrue(
            (self.project / ".claude" / "skills" / "setup-bookie" / "SKILL.md").exists()
        )
        self.assertTrue((self.project / ".claude" / "agents" / "poteto-agent.md").exists())
        self.assertIn("/setup-bookie", result.stdout)
        self.assertIn("pstack commit abcdef1", result.stdout)
        self.assertFalse((self.project / ".git").exists())

    def test_a_pstack_skill_that_the_project_changed_stays_unless_update_is_set(self):
        mine = self.project / ".claude" / "skills" / "how"
        mine.mkdir(parents=True)
        (mine / "SKILL.md").write_text("my how")
        self.install()
        self.assertEqual(self.skill("how"), "my how")
        self.install(BOOKIE_UPDATE="1")
        self.assertEqual(self.skill("how"), "upstream how")

    def test_an_old_bet_skill_is_replaced_and_its_stale_files_are_removed(self):
        old = self.project / ".claude" / "skills" / "bookie"
        (old / "scripts").mkdir(parents=True)
        (old / "scripts" / "omni.py").write_text("old")
        self.install()
        self.assertFalse((old / "scripts" / "omni.py").exists())
        self.assertTrue((old / "scripts" / "bookie.py").exists())

    def test_a_missing_folder_and_this_repository_are_refused(self):
        self.assertNotEqual(self.install(self.project / "none").returncode, 0)
        self.assertIn("this repository", self.install(ROOT).stderr)


if __name__ == "__main__":
    unittest.main()
