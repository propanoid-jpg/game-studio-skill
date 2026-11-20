import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASH = shutil.which("bash")


def run(script, stdin, **env):
    return subprocess.run(
        [BASH, str(ROOT / "scripts" / script)], input=stdin, capture_output=True, text=True,
        env={**os.environ, **env},
    ).stdout


@unittest.skipUnless(BASH, "bash not available")
class HookTests(unittest.TestCase):
    def setUp(self):
        self.project = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.project, ".claude", "game-studio"))
        open(os.path.join(self.project, ".claude", "game-studio", "project.md"), "w").close()
        self.addCleanup(shutil.rmtree, self.project)

    def test_worker_return_fires_only_for_worker_reports_in_studio_projects(self):
        note = '{"prompt":"<task-notification><status>completed</status></task-notification>"}'
        self.assertIn("fill EVERY free slot", run("worker-return.sh", note, CLAUDE_PROJECT_DIR=self.project))
        self.assertEqual(run("worker-return.sh", '{"prompt":"status?"}', CLAUDE_PROJECT_DIR=self.project), "")
        self.assertEqual(run("worker-return.sh", '{"agent_id":"a","prompt":"task-notification"}', CLAUDE_PROJECT_DIR=self.project), "")
        self.assertEqual(run("worker-return.sh", note, CLAUDE_PROJECT_DIR=tempfile.gettempdir()), "")

    def test_session_start_suggests_fresh_session_only_after_compaction(self):
        self.assertIn("fresh session", run("session-start.sh", '{"source":"compact"}', CLAUDE_PROJECT_DIR=self.project))
        started = run("session-start.sh", '{"source":"startup"}', CLAUDE_PROJECT_DIR=self.project)
        self.assertIn("project.md", started)
        self.assertNotIn("fresh session", started)

    def test_engine_cap_warns_on_wasteful_waits_only(self):
        quiet = {"CLAUDE_PLUGIN_OPTION_ENGINE_PROCESS": ""}
        for cmd in ("sleep 600", "Start-Sleep -Seconds 300", "echo idle"):
            self.assertIn("wasteful wait", run("engine-cap.sh", '{"tool_input":{"command":"%s"}}' % cmd, **quiet))
        for cmd in ("sleep 5", "timeout 270 bash -c 'until grep -q DONE log; do sleep 5; done'", "ls"):
            self.assertEqual(run("engine-cap.sh", '{"tool_input":{"command":"%s"}}' % cmd, **quiet), "")

    def test_session_start_flags_a_large_instruction_file(self):
        with open(os.path.join(self.project, "AGENTS.md"), "w") as f:
            f.write("x" * 20000)
        self.assertIn("AGENTS.md is 19 KB", run("session-start.sh", '{"source":"startup"}', CLAUDE_PROJECT_DIR=self.project))

    def test_engine_cap_warns_on_recursive_delete(self):
        quiet = {"CLAUDE_PLUGIN_OPTION_ENGINE_PROCESS": ""}
        for cmd in ("rm -rf mm/addons", "Remove-Item C:/e/x -Recurse -Force"):
            self.assertIn("recursive delete", run("engine-cap.sh", '{"tool_input":{"command":"%s"}}' % cmd, **quiet))
        for cmd in ("rm evidence/x/a.png", "rm -rf C:/game/evidence/s/t/raw", "git rm -r old"):
            self.assertEqual(run("engine-cap.sh", '{"tool_input":{"command":"%s"}}' % cmd, **quiet), "")

    def test_session_start_flags_a_large_queue_doc(self):
        os.makedirs(os.path.join(self.project, "docs"))
        with open(os.path.join(self.project, "docs", "TODO.md"), "w") as f:
            f.write("x" * 40000)
        self.assertIn("TODO.md is 39 KB", run("session-start.sh", '{"source":"startup"}', CLAUDE_PROJECT_DIR=self.project))

    def test_launch_above_role_default_needs_a_reason(self):
        def launch(role, model, prompt):
            return run("worker-review.sh", '{"tool_input":{"subagent_type":"game-studio:%s","model":"%s","prompt":"%s"}}' % (role, model, prompt))
        self.assertIn("no CHUNK MODEL reason", launch("feature-dev", "opus", "fix it"))
        self.assertIn("no CHUNK MODEL reason", launch("knowledge-keeper", "sonnet", "sync"))
        self.assertIn("no CHUNK MODEL reason", launch("prep", "fable", "plan"))
        general = run("worker-review.sh", '{"tool_input":{"subagent_type":"general-purpose","model":"opus","prompt":"x"}}')
        self.assertNotIn("no CHUNK MODEL reason", general)
        for role, model, prompt in (("feature-dev", "opus", "CHUNK MODEL: opus; reason: unknown cause"),
                                    ("feature-dev", "sonnet", "fix it"), ("art-owner", "opus", "build"),
                                    ("designer", "fable", "design the endgame")):
            out = launch(role, model, prompt)
            self.assertIn("launched", out)
            self.assertNotIn("no CHUNK MODEL reason", out)

    def test_engine_cap_skips_console_launchers(self):
        self.assertIn('grep -vci -- "_console"', (ROOT / "scripts" / "engine-cap.sh").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
