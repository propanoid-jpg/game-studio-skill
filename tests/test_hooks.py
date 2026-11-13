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

    def test_engine_cap_skips_console_launchers(self):
        self.assertIn('grep -vci -- "_console"', (ROOT / "scripts" / "engine-cap.sh").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
