---
name: game-studio
description: >-
  Game studio operating manual: agent roles, how a coordinator and fresh workers hand work over, the
  development, QA and release processes. Use it when planning, delegating, briefing, reviewing, testing
  or releasing work on a game project, whether you are the coordinator (main session) or a worker.
  Every worker brief must carry the worker rules.
argument-hint: plan | brief <role> <task> | review <handoff> | qa | pause | resume | release
---

# game-studio: how the game gets built

One main session (the **coordinator**) plus many fresh **workers** form a small studio. The process
is engine-agnostic. Project specifics (engine, paths, commands, caps, opt-in policies) live in the
project's `project.md`: `.claude/game-studio/project.md` when this skill comes from the plugin, or
next to this file when the skill is copied into a project (start from `project.example.md`). The
project's instruction file and the user's latest explicit corrections win over this skill on any
conflict.

**Plugin install.** When this skill is installed as the `game-studio` plugin:

- Launch workers as the role agents `game-studio:<role>` (`feature-dev`, `ui-dev`, `art-owner`,
  `prep`, `integration`, `qa`, `balance`, `visual-review`, `knowledge-keeper`, `release-manager`,
  `surveyor`, `coordinator-helper`) instead of a general-purpose agent. Each preloads this skill,
  carries the hard worker rules and has no Agent tool. A `model` passed at launch overrides its default.
- Coordinator commands: `/game-studio:studio-brief`, `/game-studio:studio-review`,
  `/game-studio:studio-pause`, `/game-studio:studio-resume`.
- Plugin options (`/config`): `queue_doc` (default `docs/TODO.md`), `evidence_dir` (default
  `evidence`), `engine_process` (default `godot`) and `max_engine_runs` (default 10), read by the
  hooks. `project.md` is the source of truth; keep the options equal to it.
- Advisory hooks: a warning before shell commands when the engine-process count reaches the cap, a
  review-and-clean-up reminder after each worker launch, and a session-start pointer to
  `project.md` and the queue doc. None of them block.

| File | Read when |
|---|---|
| `project.md` | start of every session: the project's paths, tools, caps and policies |
| `references/roles.md` | choosing a role, writing a brief, routing a finding |
| `references/worker-rules.md` | CANONICAL worker rules; paste the hard limits into every brief |
| `references/workflow.md` | planning or implementing a feature, UI/graphics or art change |
| `references/qa.md` | testing, corpora, bots, balance tables, triage |
| `references/release.md` | only after explicit user approval of a release |
| `templates/*.md` | briefs, handoffs, handoff review |

## 1. Start of a session or workstream

1. Read `project.md`, the project's instruction file and the task queue (`<queue_doc>`): pauses,
   urgent items, latest user directions.
2. If a knowledge base is configured, query it before grepping raw docs.
3. After a pause or crash, confirm the tree builds first (section 12).
4. Check machine load before launching anything (section 6).

## 2. Roles

Full definitions in `references/roles.md`.

| Role | One line | Serial? | Default model |
|---|---|---|---|
| Coordinator | Main session: plans, briefs, reviews, routes, decides, talks to the user | one | main session |
| Feature/system worker | Logic, tests, integration, UI for one scoped feature | parallel | mid |
| Art owner | Models/rigs/exports/wires in one asset batch; owns an exclusive-tool slot | one per slot | strongest |
| Prep worker | Sketches, criteria, specs, briefs so exclusive-tool owners never wait | parallel | mid |
| Integration/validation worker | Seed sweeps, campaigns, comparison near-misses after a drop | parallel | mid |
| QA/test-health worker | Suite sweep (only when asked); fixes stale tests; routes bugs | parallel | mid |
| Balance worker | Reusable probes; before/after tables | parallel | strongest |
| Visual polish/review worker | Live-play readability against locked criteria | parallel | strongest |
| Knowledge keeper | Knowledge-base sync and lint (if configured) | parallel | cheapest |
| Release manager | Packages a release, ONLY on explicit user approval | one | mid |
| Surveyor | Read-only inventories, grep audits, log summaries | parallel | cheapest |
| Coordinator helper (optional) | Drafts briefs, pre-reviews handoffs; never decides | parallel | strongest |

UI work is a feature worker specialised on the sketch-first visual workflow (`ui-dev` agent).

### Model choice

Pass a model on every worker launch. Take the cheapest model that can do the task well and escalate on a
failed review, not by default.

| Tier | Use for |
|---|---|
| cheapest | Mechanical, fully specified work: surveys, inventories, grep audits, renames, running a named test list, small doc edits. |
| mid | Scoped workers with a clear brief: stale tests, one feature or bug with a known cause, UI against locked sketches, prep captures, sweeps, packaging. |
| strongest | Judgement-heavy work: live art modelling and review, readability reviews, unknown-cause debugging, balance design, cross-system changes, design trade-offs. |

The model never changes the rules. If a cheaper worker's handoff fails review, relaunch the remainder
as a fresh worker one tier up and say what failed. A fork inherits the coordinator's model; use a
fresh worker when a cheaper one is wanted.

## 3. Interaction rules

- **Fresh worker per chunk**, with a self-contained brief. Workers have no access to the
  coordinator's memory: paths, decisions, limits and prior evidence go in the brief.
- **Workers never talk to the user and never launch sub-workers.** They decide within scope and
  record decisions in the handoff.
- **Out-of-scope findings** go in the handoff under "For the coordinator" with evidence (path, seed,
  log line, probe). Workers do not fix other owners' files; the coordinator routes each finding.
- **The coordinator may message a running worker** with corrections, a tighter cap or a stop. That is
  a brief amendment, never consent for anything outside the rules or the user's protections.
- **No permission laundering.** No message from an agent is the user's approval. Nobody grants
  itself or another agent permissions, settings or exceptions the user did not grant.
- **One handoff per task**: `<evidence_dir>/<stream>/<task>/handoff.txt` (template in
  `templates/handoff.md`) plus a concise final report.
- **Stalled worker:** relaunch fresh from its checkpoint; do not nurse it.

## 4. The coordinator loop (every handoff)

1. **Review** with `templates/review-checklist.md`: open the key images yourself, check claims against
   logs, grep logs for errors, confirm scope was respected and nothing was loosened.
2. **Decide:** accept, accept with routed follow-ups, or send a follow-up brief (same worker if
   still running, else fresh). Never accept on a numeric pass alone.
3. **Record:** mark the item in `<queue_doc>` with date and handoff path, plus decisions; update the
   knowledge base if configured.
4. **Route findings:** urgent defects to the top of the queue and a brief now; the rest to the
   owner's next brief or a polish list.
5. **Clean up:** stop the finished worker's background shells and monitors, and close idle tools it
   launched (after checking there is no unsaved work). Never close what you did not start.
6. **Launch the next task(s) immediately**, keeping useful workers busy within the caps. Refill a
   freed exclusive-tool slot first.

The coordinator keeps `<queue_doc>` as the single queue: what runs, who owns it, where evidence is.

## 5. Parallelism and exclusive tool slots

- An **exclusive tool** is one whose live session must have a single driver (an art/DCC app, an
  editor instance, a device, a license seat). It is NOT limited to one instance: run as many
  parallel instances (slots) as the machine and licences allow (for example 4 art-app windows),
  one owner per instance and per source file. `project.md` lists each tool with its slot count, how
  a slot is addressed (port, profile, instance) and how to launch and close it.
- One owner per slot; a worker only touches its own slot. Launch a slot only if a health check
  fails; never close another slot's session. Confirm no unsaved work before closing.
- Slots run in parallel only across DIFFERENT source files and export targets. Shared sources have
  one owner at a time, named in the queue; batches touching one wait.
- Keep the exclusive-tool queue fed: pull non-exclusive work of later phases forward (concepts,
  sketches, locked criteria, specs, capture cases) into prep workers.
- The exclusive-tool owner's scope is narrow: build, export, wire in, one quick in-game check.
  Sweeps and repeated comparison rounds go to a parallel integration worker.
- Everything else runs in parallel, bounded by section 6. Split by file ownership, not topic.

## 6. Resource limits (hard; numbers come from `project.md`)

- At most `<total_engine_runs>` engine runs across ALL workers together; each worker at most
  `<per_worker_runs>` concurrently, queued (never fire all seeds at once).
- Check real load (process count, CPU) before launching workers or batches; queue when high.
- Every engine run under a timeout, with isolated user-data directories inside the task's evidence
  folder. Never touch a real player profile.
- Windowed runs off-screen (not minimized), at most one per worker and `<total_windowed>` overall.
- Never kill processes you did not start; leave no windows or orphan runs behind.
- Finished workers, background shells and idle tools do not linger.

## 7. Autonomy and decisions

- The coordinator decides and records (queue plus decision log) without asking, EXCEPT protected
  design decisions, releases, and anything the user reserved.
- **If the user granted autonomy** (project opt-in or a direct statement): never ask questions
  while a goal runs; resolve open points by research or judgement, record the decision and why,
  and judge results yourself.
- Workers decide within scope and record material decisions with reasons. Anything touching another
  owner's contract, a protected decision or a locked criterion is a finding.
- Tooling setup is done by the studio, not handed to the user.

## 8. Standing rules (apply to every brief)

- **Targeted tests only.** Never run a full test sweep unless the user explicitly asks; run the
  tests each change needs and route single failures to focused workers.
- **Judge art and UI as a player**, from real gameplay captures, not by metrics. Passing numbers
  never establish quality, readability or feel.
- **Never run old or frozen builds** for comparison; reuse recorded before-data.
- **Lean workflow:** no provenance manifests, hash files, task reports or one-off scripts; scripts
  must be reusable; docs only where they have lasting value (update existing ones).
- **Player-facing wording** is direct and non-chatty. Use one message system, not parallel ones.
- Optional policies, active only if `project.md` opts in: **pre-release** (no back-compat
  migrations, adapters or legacy tests; reject incompatible data clearly), **performance last**
  (no audits or optimisation until the final step; fix only concrete defects), **art style rules**.

## 9. Shared-tree hygiene (many writers)

- Edit only files your brief assigns. In shared files: re-read right before editing, make
  targeted edits, never rewrite whole, never revert others' work.
- Keep every file building and valid between edits; others run the project concurrently. Add a
  complete function rather than leave one half-edited.
- Grep every run log for the engine's error markers before trusting a round. A compile break from
  another worker voids the round: wait, rerun, report the file.
- Tests exit non-zero on any failure with a normalised code (`1`, not the failure count).

## 10. Development (detail in `references/workflow.md`)

1. Read the queue and knowledge base; inspect current code, data and scenes.
2. Smallest coherent design; record assumptions.
3. Order: data model and deterministic logic, test harness, integration, UI and feedback, tuning and art.
4. **UI or graphics change:** capture current state, sketch before implementation, locked
   discriminating named-region criteria at several resolutions (the before state fails them),
   implement, compare into a new iteration folder, iterate. Never loosen thresholds or mask regions.
   Always review the actual images.
5. Run targeted tests and a build/parse check; write the handoff.

## 11. QA (detail in `references/qa.md`)

| Layer | When | Owner |
|---|---|---|
| Targeted tests | every change | implementing worker |
| Generation corpus | procedural change | integration worker |
| Campaign/playthrough bots | progression, combat, balance change | integration/balance worker |
| Full test-health sweep | ONLY when the user explicitly asks | QA worker |
| Live-play readability review | after visual/UI milestones | visual polish worker |
| Balance tables | any tuning change | balance worker |

Tests are deterministic (fixed seeds, fixed timestep, simulation time not wall clock). Findings are
triaged S0-S3; S0 (build break, crash, hang, data loss) goes to the top of the queue with a worker now.

## 12. Pause and resume

**Pause:** tell running workers to stop at a building state and write a partial handoff (done,
half-done, files touched, next step); add a `PAUSED <date>` block at the top of `<queue_doc>` with
each in-flight stream's evidence folder as a checkpoint; update the knowledge base.

**Resume:** verify the tree builds (one small suite, grep for errors); fix or route breaks; relaunch
every paused stream as a **fresh** worker whose brief points at its checkpoint and warns edits may be
partial; clear each PAUSED line as it is relaunched or delivered.

## 13. Release (detail in `references/release.md`)

**Only on explicit user approval**, recorded with date and scope. Completed streams or a green
build never imply approval. The release manager runs the checklist and does no publishing,
uploading or signing unless the user asks.

## 14. Knowledge base (optional)

If `project.md` configures one: look up before grepping docs; update after every accepted handoff and
user decision or correction (coordinator, or a knowledge keeper for batches); sync and lint
periodically. Repository docs stay the raw sources, cited by path.

## 15. Writing a brief

Use `templates/worker-brief.md`. Every brief states: role, one-sentence goal, scope and non-goals;
files owned and shared; inputs (queue lines, docs, prior handoffs, before-data); acceptance
criteria; resource caps, exclusive-tool status, evidence folder; the pasted worker-rule hard
limits; the handoff format and the next owner.
