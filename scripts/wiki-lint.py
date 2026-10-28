#!/usr/bin/env python3
"""Lint a game-studio knowledge vault (Obsidian, llm-wiki method, adapted).

Checks, over <wiki_root>/wiki/ (the vault's wiki directory, not the vault root):
  dead links, orphan pages, index drift, stale pages,
  missing "Counter-Arguments and Gaps" sections, and source-hash drift
  (a page's source-path file whose SHA-256 no longer matches its source-hash).

Adapted from the deterministic lint step of ekadetov/llm-wiki (MIT): the
upstream checks are dead links, orphans, missing sections, contradictions,
stale pages and index drift. Source-hash drift is a studio addition, because
repo docs are compiled in place and cited by path rather than copied to raw/.

Usage:
  python3 scripts/wiki-lint.py <wiki_root> [--project-root <root>]
                                     [--fix] [--report <path>]

<wiki_root> is the vault root containing wiki/index.md (for example
~/ObsidianVault/03-Resources/<wiki_name>/). --project-root resolves relative
source-path values; it defaults to the current working directory.

Exit code is 0 when no hard issue is found (dead links, index drift or
source-hash drift) and 1 otherwise. Orphan, stale and missing-section findings
are reported but do not change the exit code on their own. Unlinked mentions
are informational only. A --fix run still exits 1 for the issues it found and
fixed; re-run it to confirm a clean result. With --fix, stub pages are created for dead links and
the missing gaps section is appended to pages that lack it; index drift (other
than the index entry for a newly created stub) and source-hash drift are never
auto-fixed, because they need keeper judgement.
Standard library only.
"""

import argparse
import hashlib
import re
import sys
from datetime import date
from pathlib import Path

WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:\|[^\]]*)?\]\]")
INDEX_ENTRY_RE = re.compile(r"^\s*-\s*\[\[([^\]|#]+)", re.MULTILINE)
FENCED_RE = re.compile(r"```.*?```", re.DOTALL)
COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
GAPS_HEADING = "## Counter-Arguments and Gaps"
GAP_TYPES = {"concept", "system", "mechanic", "decision", "constraint"}


def strip_code(text):
    return FENCED_RE.sub("", text)


def strip_comments(text):
    # Template comment blocks carry example [[page-name]] entries; they are
    # not real index entries or links.
    return COMMENT_RE.sub("", text)


def parse_frontmatter(text):
    """Return (frontmatter dict, body). Frontmatter is a flat key: value block."""
    if not text.startswith("---\n") and not text.startswith("---\r\n"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    raw = text[3:end].strip()
    body = text[end + 4 :].lstrip("\n")
    data = {}
    for line in raw.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data, body


def page_title(body, stem):
    match = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
    return match.group(1).strip() if match else stem


def collect_pages(wiki_dir):
    """All wiki pages: top-level pages plus queries/, keyed by stem."""
    pages = {}
    for path in sorted(wiki_dir.rglob("*.md")):
        rel = path.relative_to(wiki_dir)
        if rel.parts[0] == "queries" and len(rel.parts) > 1:
            # Filed answers are pages for link targets, but not index entries.
            pages[path.stem] = {"path": path, "in_queries": True}
        else:
            pages[path.stem] = {"path": path, "in_queries": False}
    return pages


def main(argv=None):
    parser = argparse.ArgumentParser(description="Lint a knowledge vault.")
    parser.add_argument("wiki_root", type=Path, help="Vault root containing wiki/")
    parser.add_argument("--project-root", type=Path, default=Path.cwd(),
                        help="Root for relative source-path values (default: cwd)")
    parser.add_argument("--fix", action="store_true",
                        help="Create stubs for dead links and add missing gaps sections")
    parser.add_argument("--report", type=Path, default=None,
                        help="Write the markdown report to this path as well")
    args = parser.parse_args(argv)

    wiki_dir = args.wiki_root / "wiki"
    if not wiki_dir.is_dir():
        print(f"wiki-lint: no wiki/ directory under {args.wiki_root}", file=sys.stderr)
        return 2
    index_path = wiki_dir / "index.md"
    if not index_path.is_file():
        print(f"wiki-lint: no wiki/index.md under {args.wiki_root}", file=sys.stderr)
        return 2

    pages = collect_pages(wiki_dir)
    # Index covers top-level pages only; queries/ answers are not index entries.
    indexable = {stem for stem, p in pages.items() if not p["in_queries"] and stem != "index"}

    links = {}          # stem -> set of target stems
    frontmatter = {}
    titles = {}
    for stem, info in pages.items():
        text = info["path"].read_text(encoding="utf-8")
        fm, body = parse_frontmatter(text)
        frontmatter[stem] = fm
        titles[stem] = page_title(body, stem)
        links[stem] = set(WIKILINK_RE.findall(strip_code(strip_comments(body))))

    dead = sorted(
        (src, tgt) for src, targets in links.items() for tgt in targets if tgt not in pages
    )
    inbound = {stem: 0 for stem in pages}
    for targets in links.values():
        for tgt in targets:
            if tgt in inbound:
                inbound[tgt] += 1
    orphans = sorted(
        stem for stem, info in pages.items()
        if stem != "index" and not info["in_queries"] and inbound[stem] == 0
    )
    stale = sorted(stem for stem, fm in frontmatter.items() if fm.get("status") == "stale")
    missing_gaps = sorted(
        stem for stem, fm in frontmatter.items()
        if fm.get("type") in GAP_TYPES
        and GAPS_HEADING not in (pages[stem]["path"].read_text(encoding="utf-8"))
    )
    warnings = sorted(
        stem for stem, info in pages.items()
        if "[!WARNING]" in info["path"].read_text(encoding="utf-8")
    )

    index_text = index_path.read_text(encoding="utf-8")
    index_entries = set(INDEX_ENTRY_RE.findall(strip_comments(index_text)))
    index_missing = sorted(indexable - index_entries)
    index_dead = sorted(index_entries - set(pages))

    # Source-hash drift: source-path is repo-relative unless absolute.
    source_missing = []
    source_drift = []
    for stem, fm in frontmatter.items():
        source = fm.get("source-path")
        expected = fm.get("source-hash")
        if not source or not expected:
            continue
        candidate = Path(source)
        if not candidate.is_absolute():
            candidate = args.project_root / source
        if not candidate.is_file():
            source_missing.append((stem, source))
            continue
        actual = hashlib.sha256(candidate.read_bytes()).hexdigest()
        if not (actual == expected or actual.startswith(expected) or expected.startswith(actual)):
            source_drift.append((stem, source))

    # Unlinked mentions: an existing page's title appears in prose without a link.
    unlinked = []
    for stem, info in pages.items():
        if stem == "index":
            continue
        body = strip_code(info["path"].read_text(encoding="utf-8"))
        for other, title in titles.items():
            if other == stem or len(title) < 3:
                continue
            if title.lower() in body.lower() and other not in links[stem]:
                unlinked.append((stem, other))

    fixed = 0
    if args.fix:
        for _src, tgt in dead:
            stub = wiki_dir / f"{tgt}.md"
            if stub.exists():
                continue
            stub.write_text(
                f"---\ndate: {date.today().isoformat()}\ntags: [stub]\n"
                f"type: concept\nstatus: active\n---\n\n# {tgt}\n\n"
                f"Stub created by wiki-lint for a dead link. Replace with real content.\n\n"
                f"## See Also\n\n## {GAPS_HEADING[3:]}\n",
                encoding="utf-8",
            )
            fixed += 1
            # A new stub page must also enter the index, or the fix itself
            # creates index drift on the next run.
            index_text = index_path.read_text(encoding="utf-8")
            if f"[[{tgt}]]" not in index_text:
                if not index_text.endswith("\n"):
                    index_text += "\n"
                index_text += (
                    f"- [[{tgt}]] -- stub created by wiki-lint "
                    f"({date.today().isoformat()})\n"
                )
                index_path.write_text(index_text, encoding="utf-8")
        for stem in missing_gaps:
            path = pages[stem]["path"]
            text = path.read_text(encoding="utf-8")
            if not text.endswith("\n"):
                text += "\n"
            path.write_text(text + f"\n{GAPS_HEADING}\n", encoding="utf-8")
            fixed += 1

    def section(title, items):
        if not items:
            return f"## {title}\n\nNone.\n"
        lines = "\n".join(f"- {item}" for item in items)
        return f"## {title}\n\n{lines}\n"

    report = (
        f"# Wiki Lint Report\n\nVault: {args.wiki_root}\nPages: {len(pages)}\n\n"
        + section("Dead links (page -> target)", [f"{s} -> {t}" for s, t in dead])
        + section("Orphan pages", orphans)
        + section("Index drift: pages missing from index", index_missing)
        + section("Index drift: index entries with no page", index_dead)
        + section("Stale pages", stale)
        + section("Missing Counter-Arguments and Gaps", missing_gaps)
        + section("Pages with contradiction warnings", warnings)
        + section("Source missing", [f"{s} ({p})" for s, p in source_missing])
        + section("Source-hash drift", [f"{s} ({p})" for s, p in source_drift])
        + section("Unlinked mentions (informational)",
                  [f"{s} mentions [[{t}]] without linking" for s, t in unlinked])
        + (f"\nFixed with --fix: {fixed} items.\n" if args.fix else "")
    )
    print(report, end="")
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(report, encoding="utf-8")

    hard = bool(dead or index_missing or index_dead or source_missing or source_drift)
    return 1 if hard else 0


if __name__ == "__main__":
    raise SystemExit(main())
