# Knowledge vault (Obsidian, llm-wiki method, absorbed)

Attribution: this reference adapts the method of
[ekadetov/llm-wiki](https://github.com/ekadetov/llm-wiki) (MIT), which implements the
Karpathy LLM-wiki pattern inside Obsidian: ingest sources, compile them into cross-linked
pages, query the synthesis, lint for gaps. The plugin does not depend on llm-wiki, does not
install it, and does not copy its code except for the adapted deterministic lint script
(`scripts/wiki-lint.py`). What changed from upstream is listed under "Adaptations" below;
everything else follows the upstream operations.

## Vault layout

All paths come from `project.md`. Defaults preserve the upstream shape without hardcoding it:

```text
<vault_root>/<wiki_name>/              # <wiki_root>; example <vault_root> is ~/ObsidianVault
├── raw/                               # immutable source drops (external sources only)
│   ├── articles/                      # text source snapshots
│   └── attachments/                   # images and binary files
├── wiki/                              # LLM-owned synthesis pages
│   ├── index.md                       # catalog; read FIRST before any other page
│   ├── queries/                       # durable filed answers only (see "Query")
│   └── <concept>.md                   # entity and system pages
├── outputs/
│   └── reports/                       # dated lint reports
├── CLAUDE.md                          # vault schema and conventions (vault root only)
├── log.md                             # append-only operation log; never edit entries
├── .gitignore
└── qmd.yml                            # only if qmd is already installed
```

The vault schema `CLAUDE.md` at the vault root is not the project's instruction file
(`AGENTS.md` / project `CLAUDE.md`). Never confuse the two, and never write one over the other.

## Query-first rule (enforcement)

When a vault is configured in `project.md`, this rule is mandatory, not optional:

1. For any question about how the project works, what was decided, or why something is the
   way it is, read `wiki/index.md` first, then the relevant pages, following one level of
   `[[wikilinks]]` where relevant.
2. Only if the vault does not answer it, go to the raw docs or code, and say so in the
   brief or handoff. That gap is a finding for the knowledge keeper, not a reason to keep
   working around the vault.
3. Cite the wiki page (`[[page-name]]`) and the repo source path in briefs and handoffs.
   Never invent a wiki citation: if no page says it, no page is cited.
4. Exemption: a pure code task that touches no documented system, decision or constraint
   needs no vault lookup, but the moment it touches one, the rule applies to that part.

When no vault is configured, the coordinator's first task for any knowledge work is
`studio-setup-wiki`, not a workaround. A worker never sets up a vault on its own initiative
outside a setup brief.

## Entity types and frontmatter

Filenames are lowercase-kebab-case. Internal links are always `[[wikilinks]]`, never
standard markdown links to another vault page.

| Type | For | Frontmatter (all pages: `date`, `tags`, `type`, `status`) |
|---|---|---|
| `concept` | An idea, technology or event | as upstream |
| `system` | A game system and its contract | plus `source-path`, `source-hash` when derived from a repo doc |
| `mechanic` | A mechanic, skill or encounter rule | plus `source-path`, `source-hash` when derived from a repo doc |
| `decision` | A recorded decision with date and reason | plus `source-path`, `source-hash`; decisions are never rewritten to a different outcome, only superseded by a newer decision page |
| `constraint` | A hard limit, policy or protected decision | plus `source-path`, `source-hash` |
| `person` | A named individual | `tags` includes `person` |
| `source-summary` | One processed source document | plus `source-url` (external) or `source-path` (repo doc) and `source-hash` |
| `query-output` | A durable filed answer | `question`, `status: filed` until promoted |

Page body template: one-paragraph summary, Details, See Also (`[[wikilinks]]`), and
`## Counter-Arguments and Gaps`. Contradictions are flagged inline, never silently resolved:

```text
> [!WARNING] Contradiction with [[other-page]]: <what disagrees, with sources>
```

`status` values: `active`, `superseded` (with a link to the superseding page), `stale`.
A page is stale only when a human or a keeper brief marks it so, or when its repo source has
drifted and no recompile has run; age alone does not make a page stale.

## Operations

### Init

Scaffold only, run by `studio-setup-wiki` phase 1. Never initialise over a non-empty vault.
Write the schema, index and log from `templates/vault-claude.md`, `templates/vault-index.md`
and `templates/vault-log.md` with `<wiki_name>` filled in.

### Ingest

Acquire a source and save it to the raw library. Ingest does NOT create wiki pages; compile
does that. External sources (URL or file outside the repository) are saved to
`raw/articles/YYYY-MM-DD-<slug>.md` with frontmatter `date`, `source-type`
(`article` | `paper` | `transcript` | `conversation` | `image-set`), `source-url`,
`title`, `compiled: false`, then logged. A source already inside `raw/` is not re-saved.
Repo-owned docs are never ingested into `raw/`; they are inventoried and compiled in place
(see "Sweep and sync").

### Compile

Read inventoried docs and uncompiled raw sources and create or update wiki pages:

1. For each source: write or update its source-summary page (filename `<slug>.md`).
2. Entity extraction: for each system, mechanic, decision, constraint, concept or person
   mentioned, update the existing page (preserving its content, merging new facts) or
   create it from `templates/vault-page.md`.
3. Backlink audit (do not skip): grep `wiki/` for mentions of each new page title and add a
   `[[wikilink]]` at the first mention in every file that mentions it without linking it.
4. Update `wiki/index.md` under the appropriate domain heading, one line per page:
   `- [[page-name]] -- one-line description (YYYY-MM-DD)`, under 80 characters.
5. Append to `log.md` (`## [YYYY-MM-DD] compile | <N> sources -> <M> pages`), and commit
   only if the vault is already a git repository (see "Git").

One source typically touches several pages. That is normal.

### Query

Answer a question from the vault, with citations:

1. Read `wiki/index.md` first. If qmd is already installed, it may be used for candidate
   pages (`qmd query "<question>" --collection <wiki_name>`); otherwise identify pages
   from the index by title and description matching. Never install qmd as part of a query.
2. Read the relevant pages, following one level of `[[wikilinks]]` where relevant.
3. Synthesise the answer in prose with `[[wikilinks]]` as citations, or as a table when the
   question asks for a table.
4. Do NOT file routine worker lookups to `wiki/queries/`. Only a durable answer (a decision,
   a settled system description, an answer the project will reuse) is filed there by a
   knowledge-keeper brief, and promoted to a full page only by an explicit keeper brief.
   Promotion changes frontmatter `status` from `filed` to `promoted` and is logged.
5. Append to `log.md` only for filed or promoted answers, not for routine lookups.

### Sweep and sync

The one-time sweep is `studio-setup-wiki` phases 2 to 4. After setup, maintenance is
incremental sync, run by a knowledge-keeper brief after accepted work or at a milestone:

1. Recompute SHA-256 for every repo doc cited by a wiki page's `source-path`. A changed
   hash means the source drifted: recompile that source only, update the page's
   `source-hash`, and log the sync.
2. Inventory new docs in `<vault_scope>` that have no page yet and compile them.
3. Remove or supersede pages whose source doc was deleted, with a log entry; never delete
   a page silently.
4. Run lint (below) and file its report to `outputs/reports/YYYY-MM-DD-lint.md`.
5. Never re-run the full sweep to fix drift. A full rebuild is a new `studio-setup-wiki`
   brief, and only when the coordinator decides the vault itself is corrupt.

### Lint

Run `scripts/wiki-lint.py <wiki_root> [--project-root <root>] [--fix]` and report or fix:

| Check | Action |
|---|---|
| Dead links (`[[wikilinks]]` to nonexistent pages) | With `--fix`, create a stub page from the page template; otherwise report |
| Orphan pages (no inbound links, excluding `index.md`) | List; suggest the page that should link to them |
| Unlinked concept mentions | Scan pages for terms matching an existing page title without a `[[wikilink]]` at first mention; link it or flag it |
| Contradictions | List pages carrying `[!WARNING]` markers; never auto-resolve |
| Missing `## Counter-Arguments and Gaps` | With `--fix`, add the empty section; otherwise report |
| Stale pages | List pages with `status: stale` |
| Index drift | Compare `index.md` entries against actual files; add missing, remove dead |
| Source-hash drift | Recompute each page's `source-path` hash against `source-hash`; report missing sources and mismatches |

Write the lint report to `outputs/reports/`, append to `log.md`
(`## [YYYY-MM-DD] lint | <N> issues found, <M> fixed`), and commit only if the vault is
already a git repository.

### Remove

Workers never remove a vault. Deletion of a vault is a user decision, executed only on the
user's explicit instruction in that turn, with the vault path and contents listed first.

## qmd (optional, never installed by this plugin)

qmd provides hybrid BM25 plus vector search over the wiki. For small vaults (under about
50 pages) reading `index.md` is fast enough; for larger vaults qmd helps find pages without
reading everything. If qmd is already installed, use its full path, never a bare `qmd`, and
fall back to index-based search if it is absent or its collection is missing. This plugin
never installs qmd, marp or any other dependency: a SessionStart auto-install hook is
deliberately not included.

## Git

Every vault operation ends with a git commit only when the vault is already a git
repository and `<vault_git>` permits it. If the vault is not a repository, changes are saved
uncommitted and the handoff says so. A failed commit is warned about, never fatal, and never
a reason to re-run an operation. The setup worker never runs `git init` in a vault.

## Adaptations from upstream (summary)

- Vault location is parameterised in `project.md`; upstream hardcodes
  `~/ObsidianVault/03-Resources/<name>/`.
- Repo docs are compiled in place with `source-path` and `source-hash`, not copied into
  `raw/`; upstream copies every source into `raw/`.
- Routine query answers are not filed; only durable answers are filed and promoted.
- Source-hash drift is a lint check; upstream has no repo-source drift concept.
- Studio entity types (`system`, `mechanic`, `decision`, `constraint`) extend upstream
  `concept`, `person` and `source-summary`.
- No auto-install hook, no Marp export step, no worker-initiated removal, and no commit
  unless the vault is already tracked.
- Secrets are never inventoried, copied or quoted: `.env`, credentials, keys and tokens are
  in the default exclusion list and a skipped-secret entry names the path only.

## Error handling

| Situation | Action |
|---|---|
| No vault configured | Coordinator briefs `studio-setup-wiki`; workers do not invent a vault path |
| Vault path exists but is not a vault (no schema or no `wiki/`) | Gated stop; report contents, do not overwrite |
| qmd not available | Fall back to `index.md`; warn once in the handoff, not per query |
| Network error on URL ingest | Retry once; if still failing, report and suggest saving the content manually to `raw/articles/` |
| Git commit fails | Warn; changes are saved but not committed; continue |
| Wiki page already exists on compile | Update and merge, never overwrite whole |
| Raw source too large (over 50 KB) | Warn that entity extraction may be incomplete; proceed anyway |
| `log.md` missing | Recreate it from the template; warn in the handoff |
| No uncompiled sources | Report "All sources are already compiled. Nothing to do." and stop |
| Source doc deleted | Supersede or remove its pages with a log entry; report it |
