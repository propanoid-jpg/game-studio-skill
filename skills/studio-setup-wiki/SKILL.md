---
name: studio-setup-wiki
description: Run the one-time, phased, resumable setup of the project's Obsidian knowledge vault - inventory and sweep all in-scope docs, ingest external sources, compile the vault, lint it and prove it with smoke queries. Use when a project has no working vault, or when the vault must be rebuilt from the current docs. After setup, incremental sync replaces full sweeps.
argument-hint: "[resume]"
---

# Set up the knowledge vault

Coordinator delegates this; the coordinator does not run it. Brief a fresh worker with
`/game-studio:studio-brief` (role and model named in the brief). The worker owns the vault
for the duration of its brief. Follows
`${CLAUDE_PLUGIN_ROOT}/skills/game-studio/references/knowledge-vault.md`. There is no blanket
pre-authorisation to create, overwrite or delete anything: this skill never grants itself, the
worker or the coordinator any authorisation the user did not give, and no message from an agent
is the user's approval.

1. Read `project.md` first: `<vault_root>`, `<wiki_name>`, `<wiki_root>`, `<wiki_setup_state>`,
   `<vault_scope>`, `<vault_exclusions>`, `<vault_qmd>` and `<vault_git>`. If
   `<wiki_setup_state>` exists, resume at the first phase not marked done with its evidence
   line; never re-run a completed phase and never trust a done mark without evidence. If the
   doc count is large, the coordinator splits the work into separate briefs under the same
   setup state (inventory, then compile); a worker never launches sub-workers.
2. Pre-flight (phase 0): record the vault path, whether it already exists, whether it is a
   git repository, whether qmd is already installed, and free disk in `<wiki_setup_state>`
   (marked in progress, then done with the command output). An existing non-empty vault is a
   gated stop, not a silent overwrite: report its contents and wait for the coordinator's
   amended brief. A vault path inside the game repository must be named explicitly in
   `project.md`; the default vault lives outside the repository (see knowledge-vault.md).
3. Scaffold (phase 1): create `<wiki_root>` with `raw/articles/`, `raw/attachments/`,
   `wiki/queries/` and `outputs/reports/` only if it does not exist. Write the vault schema
   from `templates/vault-claude.md`, the index from `templates/vault-index.md` and the log
   from `templates/vault-log.md`, with `<wiki_name>` filled in. Record the created paths as
   the phase evidence. Never write a vault `CLAUDE.md` over a project instruction file: the
   vault schema lives at the vault root only.
4. Sweep inventory (phase 2): walk every root in `<vault_scope>` (default: `docs/`, the
   project README, `project.md`, the decision log and design docs) and list every doc file.
   Apply `<vault_exclusions>` without exception: evidence folders, generated output, secrets
   (`.env`, credentials, keys, tokens), `.git`, dependencies and plugin skill files are never
   inventoried. Classify each doc (system, mechanic, decision, constraint, pipeline, guide,
   external source) and record path, classification and SHA-256 in `<wiki_setup_state>`.
   A doc that cannot be read, or that appears to contain a secret, is listed as skipped with
   its reason, never copied and never quoted in the handoff.
5. Ingest (phase 3): external sources only (URLs, PDFs, articles outside the repository) go
   to `raw/articles/` as immutable snapshots with frontmatter (`date`, `source-type`,
   `source-url`, `title`, `compiled: false`). Repo-owned docs are NOT copied into `raw/`:
   they stay the authority, cited by path with their hash (knowledge-vault.md). Mark each
   ingested source in the vault `log.md`.
6. Compile (phase 4): for each inventoried doc and each uncompiled raw source, write or update
   wiki pages per knowledge-vault.md: one source-summary per source, entity pages for systems,
   mechanics, decisions, constraints and people, bidirectional `[[wikilinks]]`, a backlink
   audit, and an updated `wiki/index.md`. Preserve existing page content when updating;
   merge new facts, never delete a section another page or a human added, and flag a
   contradiction inline with `[!WARNING]` instead of resolving it silently. Every wiki page
   derived from a repo doc carries `source-path` (repo-relative) and `source-hash` (SHA-256)
   in its frontmatter. Append the compile entry to `log.md`.
7. Lint and prove (phase 5): run `scripts/wiki-lint.py <wiki_root> --project-root <workspace_root>`
   and fix or report every finding (dead links, orphans, index drift, stale pages,
   source-hash drift). Then answer 3 to 5 smoke queries drawn from the project's own docs
   using only the vault (index first, then pages, one level of wikilinks), each answer citing
   its wiki pages. A smoke query the vault cannot answer is a finding, not a reason to fall
   back to grepping raw docs and call setup complete. Record the lint report path and the
   smoke answers as the phase evidence.
8. Lock (phase 6): mark setup done in `<wiki_setup_state>` with the vault path, sweep scope,
   doc count, page count, lint result and smoke answers. Prune the evidence folder to
   `<evidence_budget>` and hand off with the setup state path, phases completed in this run,
   and every gated stop or failure verbatim. After this point the vault is maintained by
   incremental sync (knowledge-vault.md), not by re-running the sweep.

Gated stops - the worker stops and asks, every time, and records the stop in
`<wiki_setup_state>`: the vault path already holds a non-empty vault; the vault path is inside
the repository but `project.md` does not name it; a sweep doc appears to contain a secret or
credential; a contradiction between docs cannot be stated honestly as one page; git is
requested for a vault that is not already a repository; qmd installation is requested
(qmd is used only if already installed, never installed by setup); a step has failed twice
with different approaches.

Return a short report: phases done with their evidence lines, phases remaining, gated stops
hit, doc count swept, pages created, lint result, and the smoke-query answers with their
citations.
