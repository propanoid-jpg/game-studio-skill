# <wiki_name> Wiki Schema

Vault schema for the knowledge keeper. This file lives at the vault root only. It is not
the project's instruction file (AGENTS.md / project CLAUDE.md).

## Directory Layout

- raw/              -- immutable source drops. Never edit files here.
- raw/articles/     -- external text source snapshots (articles, papers, transcripts).
- raw/attachments/  -- images and binary attachments.
- wiki/             -- LLM-owned synthesis pages. The keeper has full write access here.
- wiki/index.md     -- catalog. Read this FIRST before opening any other page.
- wiki/queries/     -- durable filed answers. Promote to wiki/ when settled.
- outputs/reports/  -- dated lint reports and other artifacts.
- log.md            -- append-only operation log. Never edit existing entries.

## Repo sources

Repo-owned docs are NOT copied into raw/. They are compiled in place and cited by path.
Every wiki page derived from a repo doc carries `source-path` (repo-relative path) and
`source-hash` (SHA-256 of that file at compile time) in its frontmatter. Sync recomputes
the hash; a mismatch means the source drifted and the page must be recompiled.

## Entity Types and Templates

See `templates/vault-page.md` in the game-studio skill for the page templates. Types:
`concept`, `system`, `mechanic`, `decision`, `constraint`, `person`, `source-summary`,
`query-output`.

## Naming Conventions

- All filenames: lowercase-kebab-case.md
- Wikilinks: [[filename-without-extension]]
- Never use standard markdown links for internal links

## Log Format

Append to log.md after every operation. Format:

```text
## [YYYY-MM-DD] <operation> | <title>
One-line description.
```

Operations: init | ingest | compile | query | promote | sync | lint

## Index Format

wiki/index.md is a human- and LLM-readable catalog. Format:

```text
## Domain Name
- [[page-name]] -- one-line description (YYYY-MM-DD)
```

Keep entries under 80 chars. Update after every compile.

## Cross-Reference Rules

- Every page must link to at least one other page when content warrants it
- When creating or updating a page, scan index.md for related entities and add [[wikilinks]]
- Flag contradictions inline: > [!WARNING] Contradiction with [[other-page]]

## Ingest Rules

1. Acquire the source (URL or file outside the repository)
2. Classify the source type
3. Save to raw/articles/ with frontmatter (compiled: false)
4. Append to log.md
5. Commit only if the vault is already a git repository

Ingest does NOT create wiki pages. Use compile for that.

## Compile Rules

1. Identify uncompiled raw sources (no matching source-summary in wiki/) and repo docs whose
   source-hash has changed
2. For each source: write source-summary, extract entities, create/update pages
3. Backlink audit: grep existing pages for mentions of new titles
4. Update wiki/index.md
5. Append to log.md
6. Commit only if the vault is already a git repository

## Query Rules

1. Read wiki/index.md first
2. Open relevant pages
3. Synthesise answer with [[wikilinks]] as citations
4. File only durable answers to wiki/queries/ (routine lookups are not filed)
5. Offer promotion to wiki/ as a full page only in a keeper brief
6. Append to log.md for filed and promoted answers only
7. Commit only if the vault is already a git repository

## Lint Rules

Scan all pages in wiki/ and report:

- Contradictions between pages
- Orphan pages (no inbound [[links]], excluding index.md)
- Pages with status: stale
- Missing Counter-Arguments and Gaps section
- Index entries pointing to missing files
- Source-hash drift against source-path files

After fixing, append to log.md and commit only if the vault is already a git repository.
