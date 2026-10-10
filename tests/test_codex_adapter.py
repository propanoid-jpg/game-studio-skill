import importlib.util
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
import tomllib

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("adapter", ROOT / "scripts/codex_adapter.py")
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)


class AdapterTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.project = Path(self.tmp.name)

    def test_install_preserves_instructions_and_is_idempotent(self):
        agents = self.project / "AGENTS.md"
        agents.write_text("User's durable instructions.\n", encoding="utf-8")
        self.assertEqual(a.install(self.project)["workers"], 12)
        first = agents.read_text(encoding="utf-8")
        a.install(self.project)
        self.assertEqual(agents.read_text(encoding="utf-8"), first)
        self.assertTrue(first.startswith("User's durable instructions.\n"))
        profiles = list((self.project / ".codex/agents").glob("*.toml"))
        self.assertEqual(len(profiles), 12)
        for path in profiles:
            profile = tomllib.loads(path.read_text(encoding="utf-8"))
            self.assertTrue(profile["name"].startswith("game-studio-"))
            self.assertNotIn("model", profile)
            self.assertIn(str(a.ROOT), profile["developer_instructions"])
        surveyor = tomllib.loads((self.project / ".codex/agents/game-studio-surveyor.toml").read_text(encoding="utf-8"))
        self.assertEqual(surveyor["sandbox_mode"], "read-only")
        self.assertEqual(len(list((self.project / ".agents/skills").glob("*/SKILL.md"))), 5)

    def test_collision_does_not_partially_install(self):
        path = self.project / ".codex/agents/game-studio-qa.toml"
        path.parent.mkdir(parents=True)
        path.write_text('name = "my-qa"', encoding="utf-8")
        with self.assertRaises(ValueError):
            a.install(self.project)
        self.assertFalse((self.project / "AGENTS.md").exists())
        self.assertEqual(list(path.parent.iterdir()), [path])

    def test_existing_project_settings_are_reused(self):
        path = self.project / ".claude/game-studio/project.md"
        path.parent.mkdir(parents=True)
        path.write_text("Existing settings", encoding="utf-8")
        a.install(self.project)
        self.assertFalse((self.project / ".codex/game-studio/project.md").exists())
        self.assertEqual(path.read_text(), "Existing settings")

    def test_brief_embeds_role_rules_and_project_limits(self):
        path = self.project / ".codex/game-studio/project.md"
        path.parent.mkdir(parents=True)
        path.write_text("Worker hard limits: run cap 2, no releases.", encoding="utf-8")
        task = self.project / "brief.txt"
        task.write_text("GOAL\nFix inventory.\nFILES\ninventory.py\nACCEPTANCE\nNamed inventory test.", encoding="utf-8")
        args = SimpleNamespace(project=self.project, task_file=task, role="feature-dev", tier="medium", task_name="inventory")
        result = a.brief(args)
        self.assertEqual(result["model"], "gpt-6.1-sol")
        self.assertEqual(result["fork_turns"], "none")
        self.assertIn("run cap 2", result["message"])
        self.assertIn("Named inventory test", result["message"])
        self.assertIn(a.read(a.ROOT / "skills/game-studio/references/worker-rules.md"), result["message"])
        task.write_text("GOAL <unfinished>", encoding="utf-8")
        with self.assertRaises(ValueError):
            a.brief(args)
        with self.assertRaises(ValueError):
            a.role("../../outside")
        with self.assertRaises(ValueError):
            a.role("coordinator")

    def test_lease_rejects_conflicts_and_wrong_owner(self):
        args = SimpleNamespace(project=self.project, action="claim", resource="blender-slot-1", owner="art1")
        a.lease(args)
        with self.assertRaises(ValueError):
            a.lease(args)
        args.action = "release"
        args.owner = "art2"
        with self.assertRaises(ValueError):
            a.lease(args)
        args.owner = "art1"
        a.lease(args)
        args.action = "claim"
        a.lease(args)

    def test_preflight_refuses_full_worker_capacity_and_low_disk(self):
        args = SimpleNamespace(project=self.project, min_free_gib=0, max_workers=3,
                               active_workers=3, engine_process="", max_engine_runs=0)
        self.assertFalse(a.preflight(args)["ok"])
        args.active_workers = 2
        self.assertTrue(a.preflight(args)["ok"])
        args.min_free_gib = 10**9
        self.assertFalse(a.preflight(args)["ok"])

    def test_release_versions_match(self):
        plugin = json.loads(a.read(a.ROOT / ".claude-plugin/plugin.json"))
        market = json.loads(a.read(a.ROOT / ".claude-plugin/marketplace.json"))
        self.assertEqual(plugin["version"], "1.3.0")
        self.assertEqual(market["plugins"][0]["version"], plugin["version"])


if __name__ == "__main__":
    unittest.main()
