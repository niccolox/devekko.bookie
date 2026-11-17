import json
import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "skills" / "setup-bookie" / "scripts"))

from setup_bookie import PSTACK_SKILLS, PSTACK_SOURCE

ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME = re.compile(r"\*\*([a-z][a-z0-9-]*)\*\*")


class SourcesTest(unittest.TestCase):
    def test_the_skill_and_the_lock_name_the_same_pstack_source(self):
        lock = json.loads((ROOT / "pstack.lock").read_text())
        self.assertEqual(PSTACK_SOURCE, lock["source"])

    def test_the_pstack_check_covers_each_skill_that_a_bet_skill_names(self):
        local = {path.name for path in (ROOT / "skills").iterdir() if path.is_dir()}
        named = set()
        for skill in local:
            named |= set(SKILL_NAME.findall((ROOT / "skills" / skill / "SKILL.md").read_text()))
        covered = local | set(PSTACK_SKILLS)
        not_covered = {n for n in named if n not in covered and f"principle-{n}" not in covered}
        self.assertEqual(not_covered, set())


if __name__ == "__main__":
    unittest.main()
