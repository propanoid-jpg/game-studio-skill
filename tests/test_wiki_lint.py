"""Tests for scripts/wiki-lint.py (stdlib unittest; no pytest dependency)."""

import hashlib
import importlib.util
import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("wiki_lint", ROOT / "scripts" / "wiki-lint.py")
wiki_lint = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(wiki_lint)


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def page(title, body="", fm=""):
    return f"---\ndate: 2026-10-28\ntags: [test]\ntype: concept\nstatus: active\n{fm}---\n\n# {title}\n\n{body}\n\n## Counter-Arguments and Gaps\n"


class WikiLintTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.vault = self.root / "vault"
        self.wiki = self.vault / "wiki"
        write(self.wiki / "index.md", "# Index\n\n## Test\n- [[alpha]] -- first (2026-10-28)\n- [[beta]] -- second (2026-10-28)\n")
        write(self.wiki / "alpha.md", page("Alpha", "See [[beta]]."))
        write(self.wiki / "beta.md", page("Beta", "Linked from alpha."))

    def tearDown(self):
        self.tmp.cleanup()

    def run_lint(self, *extra):
        out = io.StringIO()
        with redirect_stdout(out):
            code = wiki_lint.main([str(self.vault), "--project-root", str(self.root), *extra])
        return code, out.getvalue()

    def test_clean_vault_passes(self):
        # beta is linked from alpha; alpha is in the index, so no orphan issue
        # blocks the run, and neither page is stale or missing a gaps section.
        code, out = self.run_lint()
        self.assertEqual(code, 0)
        self.assertIn("Pages: 3", out)

    def test_dead_link_fails_and_fix_creates_stub(self):
        write(self.wiki / "alpha.md", page("Alpha", "See [[missing-page]]."))
        code, _ = self.run_lint()
        self.assertEqual(code, 1)
        # The --fix run still reports the issue it found and fixed; the
        # following run is clean.
        code, _ = self.run_lint("--fix")
        self.assertEqual(code, 1)
        self.assertTrue((self.wiki / "missing-page.md").is_file())
        code, _ = self.run_lint()
        self.assertEqual(code, 0)

    def test_template_comment_example_is_not_an_index_entry(self):
        index = self.wiki / "index.md"
        index.write_text(index.read_text(encoding="utf-8")
                         + "\n<!--\n- [[page-name]] -- example (2026-10-28)\n-->\n",
                         encoding="utf-8")
        code, _ = self.run_lint()
        self.assertEqual(code, 0)

    def test_index_drift_fails(self):
        write(self.wiki / "gamma.md", page("Gamma"))
        code, out = self.run_lint()
        self.assertEqual(code, 1)
        self.assertIn("gamma", out)

    def test_source_hash_drift_and_missing_source(self):
        source = self.root / "docs" / "system.md"
        write(source, "system doc")
        digest = hashlib.sha256(source.read_bytes()).hexdigest()
        write(self.wiki / "alpha.md", page(
            "Alpha", "See [[beta]].",
            fm=f"source-path: docs/system.md\nsource-hash: {digest}\n"))
        code, _ = self.run_lint()
        self.assertEqual(code, 0)
        write(source, "system doc changed")
        code, _ = self.run_lint()
        self.assertEqual(code, 1)
        source.unlink()
        code, out = self.run_lint()
        self.assertEqual(code, 1)
        self.assertIn("Source missing", out)

    def test_stale_and_missing_gaps_do_not_fail_alone(self):
        write(self.wiki / "beta.md",
              "---\ndate: 2026-10-28\ntags: [test]\ntype: concept\nstatus: stale\n---\n\n# Beta\n")
        code, _ = self.run_lint()
        self.assertEqual(code, 0)


if __name__ == "__main__":
    unittest.main()
