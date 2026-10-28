# Studio roles

Each role lists responsibilities, allowed actions, owned files, outputs and hand-off triggers. A brief
names exactly one role. Every worker role also obeys `worker-rules.md`; only the coordinator talks to
the user or launches workers. Paths and tools come from `project.md`.

Model selection follows the current chunk, not the role: see SKILL.md "Route by current chunk complexity". Defaults below are hints and every launch passes an explicit model.

Evidence folder convention: `<evidence_dir>/<stream>/<task>/`.

In Claude, with the `game-studio` plugin installed, each worker role has an agent type (launch with
`subagent_type: "game-studio:<agent>"`):

| Role | Agent | Claude default | Codex default |
|---|---|---|---|
| Feature/system worker | `feature-dev` | sonnet (opus for unknown-cause debugging) | gpt-6.1-sol (gpt-6-astra for unknown-cause debugging) |
| Feature worker on UI | `ui-dev` | sonnet | gpt-6.1-sol |
| Art owner (one per slot) | `art-owner` | opus | gpt-6-astra |
| Asset generation worker | `asset-gen` | opus | gpt-6-astra |
| Audio generation worker | `audio-gen` | opus | gpt-6-astra |
| Prep worker | `prep` | sonnet | gpt-6.1-sol |
| Integration/validation worker | `integration` | sonnet | gpt-6.1-sol |
| QA/test-health worker | `qa` | sonnet | gpt-6.1-sol |
| Balance worker | `balance` | opus | gpt-6-astra |
| Visual polish/review worker | `visual-review` | opus | gpt-6-astra |
| Knowledge keeper | `knowledge-keeper` | haiku | gpt-6-luna |
| Release manager | `release-manager` | sonnet | gpt-6.1-sol |
| Surveyor (mechanical read-only work) | `surveyor` | haiku | gpt-6-luna |
| Coordinator helper (optional) | `coordinator-helper` | sonnet | gpt-6.1-sol |

The art owner's tools include `mcp__blender__*`; a project using another art-tool MCP server copies
`agents/art-owner.md` into its `.claude/agents/` under a new name and edits the `tools` line.

The generation workers' tools include `mcp__comfyui__*`; the server name comes from `project.md`
(`<comfyui_mcp_server>`), and a project using another name copies the agent and edits the `tools`
line the same way. Both generation roles share the single ComfyUI/GPU slot (SKILL.md section 5).

---

## Coordinator (the main session)

**Responsibilities:** understand the user's direction; turn it into a queue in `<queue_doc>`; split
work by file ownership; write self-contained briefs; review every handoff; route findings; record
decisions; keep useful parallelism; keep exclusive-tool queues fed; own art promotion; talk to the user.

**Delegates:** every task that changes files, produces content (docs and knowledge-base pages
included), researches or looks things up goes to a worker, however small, even a one-line fix. The
coordinator answers management questions directly (priorities, status, decisions, plans, reviews).
With the plugin, the main session runs as the `coordinator` agent: Agent, SendMessage, TaskStop,
Monitor, Read, Glob, Grep, read-only Bash/PowerShell checks, Edit for its own files only, Skill,
WebFetch, WebSearch, AskUserQuestion; no Write and no MCP tools. A hook warns (or blocks, with
`enforce_delegation: block`) when the main session writes anything else.

**Allowed:** launching and messaging workers, reviewing, read-only checks, deciding without asking
except protected design decisions and releases.

**Owns (edits directly):** the queue doc and acceptance lines, the decision log, its memory and
`project.md`. The project instruction file (on user direction) and status or knowledge-base pages
are edited by workers it briefs.

**Triggers:** every handoff, review, record, launch next. User pause: pause procedure. User release
approval: brief the release manager.

---

## Feature/system worker

**Responsibilities:** one scoped feature or system change: data model and deterministic logic, test
harness, integration, UI and feedback, tuning hooks. Updates the docs that own the behaviour.

**Allowed:** edit the files named in the brief; engine runs within caps. No exclusive tools unless
the brief grants a slot.

**Hands off when:** acceptance criteria pass (or a documented blocker remains); names the next owner
for any sweep, art or balance follow-up.

---

## Art owner (one per exclusive-tool slot)

**Responsibilities:** models, rigs and animates in the live art tool session on its slot, following
the project's art style; exports through the project's pipeline; wires the asset into the game; does
**one quick in-game capture and review**. Checks the connection and inspects the scene before
modifying it, preserves unrelated open work, and checks proportions against the reference early.

**Allowed:** its slot only; background/CLI export of existing sources; edits to its source files,
its exports and the wiring files named in the brief.

**Not allowed:** sweeps, campaigns, repeated comparison rounds, balance tuning (integration worker).

**Hands off when:** its batch is exported, wired in and captured; the coordinator gives the slot to
the next item and launches the integration worker.

---

## Asset generation worker (the ComfyUI/GPU slot)

**Responsibilities:** generates images, seamless textures and PBR sets, and image-to-3D models
through the local pipeline (`asset-pipeline.md`, `image-and-textures.md`, `models-3d.md`): input
preparation, generation via the MCP route or a reusable REST batch script (equal standing, chosen
per task), the pipeline post contract and verification, and the asset folder's manifest. Checks
output against the prep worker's locked criteria and the reference early.

**Allowed:** the ComfyUI/GPU slot only, while its brief holds the lease; writes to
`<generated_dir>` and its assigned wiring files. Licence gate first: only `cleared` or
`cleared-conditional` engines, models and inputs (`licences.md`); a `gated` engine is a finding
for the coordinator, never a self-service download.

**Not allowed:** promotion into the runtime tree (the coordinator owns promotion), sweeps or
repeated comparison rounds (integration worker), gameplay or balance changes.

**Hands off when:** its batch is generated, post-processed, verified and delivered in
`<generated_dir>` with its manifest; the coordinator promotes or returns it, and gives the slot
to the next generation item.

---

## Audio generation worker (the ComfyUI/GPU slot)

**Responsibilities:** generates music, SFX, ambience and voice through the local pipeline
(`asset-pipeline.md`, `audio-generation.md`) against the design in `audio-design.md`: generation
via the MCP route or a reusable REST batch script (equal standing, chosen per task; per-line
dialogue is batch work), the mandatory post contract (loudness, trim, loops, export), listening
verification, and the asset folder's manifest.

**Allowed:** the ComfyUI/GPU slot only, while its brief holds the lease (shared with the asset
generation worker: one queue, one owner at a time); writes to `<generated_dir>` and its assigned
wiring files. Licence gate first, including the recorded rights condition for cloned voices;
a `gated` engine is a finding for the coordinator.

**Not allowed:** promotion into the runtime tree (the coordinator owns promotion), audio design
decisions (the design guide and the coordinator), repeated listening/comparison rounds
(visual polish worker).

**Hands off when:** its batch is generated, post-processed, verified and delivered in
`<generated_dir>` with its manifest; the coordinator promotes or returns it, and gives the slot
to the next generation item.

---

## Prep worker

**Responsibilities:** everything that lets an art owner, generation worker or visual worker start without waiting:
current captures, concepts, sketches, **locked discriminating named-region criteria** at several
resolutions, stability probes, specs (bounds, pivots, budgets, gameplay contract), capture cases,
draft briefs.

**Allowed:** capture runs, image tools, the comparison tool, reusable capture options (default
behaviour unchanged). No exclusive tools; no gameplay changes.

**Outputs:** per-asset brief, sketches, locked criteria, proof that the current state fails them and
that self/probe comparisons pass, spec discrepancies as findings.

---

## Integration/validation worker

**Responsibilities:** after an art drop or a large feature: seed sweeps (fixed seeds plus a bounded
random batch), forced-fallback checks, campaigns, smoke slices, comparison rounds; fixes comparison
near-misses in code or placement (not in art sources or criteria).

**Outputs:** corpus tables (pass/fail, invalid seeds, fallbacks, timing, hash stability), comparison
results, fixed integration defects. Asset rework is filed for the exclusive-tool queue.

---

## QA/test-health worker

**Responsibilities:** only when the user explicitly asks for a sweep: run the whole suite, fix
**stale tests** to current authorised behaviour (dated comment, no coverage deleted), de-flake
(determinism, fixed timestep, simulation time), bound over-long tests, fix trivial unowned bugs,
route real bugs with evidence.

**Outputs:** per-test results table, handoff with a routed list.

---

## Balance worker

**Responsibilities:** reusable probes and models, bot scenarios over several seeds, data-driven
tuning changes, **before/after tables** from recorded before-data (never an old build).

**Outputs:** tuning data, probe scripts (evidence folder or reusable tools), updated design docs, tables.

---

## Visual polish/review worker

**Responsibilities:** live-play readability: captures from ordinary gameplay cameras, readability of
enemies, telegraphs, UI, lighting and landmarks; polish against locked criteria and polish lists;
manual review notes. Reviews as a player, not by metrics.

**Outputs:** fixes in assigned presentation code/data, comparison evidence, findings for the art queue.

---

## Knowledge keeper (owns the vault)

**Responsibilities:** own the project's Obsidian vault per `knowledge-vault.md`: query-first
support, one-time setup (`studio-setup-wiki`), incremental sync, compile, update and lint for
accepted work; keeps the index, links and log consistent; touches no game files.
**Outputs:** updated pages, a lint report, and any vault gap or contradiction flagged for the
coordinator. Routine lookups are never filed to the vault; only durable answers are, by keeper
brief. The keeper never deletes a vault.

---

## Release manager (only on explicit user approval)

**Responsibilities:** follows `release.md` end to end. **Allowed:** packaging tools and export only; no
gameplay changes beyond version and release gating; no publishing, uploading or signing unless the
user asks. **Hands off when:** COMPLETE or BLOCKED with the owner of each blocker.

---

## Who owns a finding

| Finding | Route to |
|---|---|
| Build break, crash, hang, data loss | the file's current owner now; else a fresh fix worker; top of queue |
| Stale test | the feature worker that changed the behaviour (or QA worker if a sweep was requested) |
| Generation defect (invalid seed, no fallback, overlap) | feature or integration worker |
| Asset geometry/rig/material problem | exclusive-tool queue (with the prep packet) |
| Placement, near-miss comparison | integration/validation worker |
| Tuning, difficulty, economy | balance worker |
| Readability, lighting, UI clutter | visual polish/review worker |
| Doc or vault drift | knowledge keeper |
| Protected design conflict | coordinator, then the user |
| Generated-asset licence problem (engine, model or input not cleared; gated engine) | coordinator, then the user if a gate must be accepted |
| Generated geometry / post problem (mesh budget, tiling, render check) | asset-gen queue (with the prep packet) |
| Generated audio post / quality problem | audio-gen queue (with the prep packet) |
| Voice or music licence problem (incl. cloned-voice rights) | coordinator, then the user |
