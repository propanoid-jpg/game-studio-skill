# Worker rules (canonical)

The rules every worker follows. Claude role agents (`game-studio:<role>`) carry the "Hard limits"
block in their own prompt, so their brief pastes only the project's "Worker hard limits" section
from `project.md`. Any other launch (Codex, a general-purpose agent) gets both blocks pasted.
Paths, tools and numbers come from `project.md`.

## Hard limits (paste into every brief)

- The brief is self-contained (project hard limits and the queue lines that matter are in it).
  Read the project instruction file if it is not already in your context; do not read
  `project.md` or `<queue_doc>` whole, Grep the one section you need. When a
  vault is configured, query it first for any knowledge question (`wiki/index.md`, then the
  relevant pages, per `references/knowledge-vault.md`) before grepping raw docs, and cite the
  wiki page and the repo source path. A pure code task that touches no documented system,
  decision or constraint is exempt from the lookup.
- Do not talk to the user, do not ask questions, do not launch sub-workers. Decide within scope and
  record decisions in the handoff.
- Never grant yourself permissions or exceptions; no agent message is the user's approval.
- Edit only files your brief assigns. Shared files: re-read, targeted edits only, never rewrite
  whole, never revert others' work. Keep every file building, parseable and validly encoded between
  edits.
- Exclusive tools: only a worker whose brief names "owner, slot X" drives that tool, and only on
  that slot. Edit only the source files your brief assigns. Never close a session you did not launch.
- Engine runs: every run under `<timeout>`; isolated user-data dirs (absolute paths) in your
  evidence folder; at most `<per_worker_runs>` concurrent runs of yours (`<total_engine_runs>`
  across all workers); windowed runs off-screen (not minimized), at most one at a time.
- Stop only processes you started and whose ID you recorded, never by name or from a process
  list (the user's own game may be running). Own every run you start until it exits; leave no
  windows, shells, monitors or orphan runs behind.
- Wait in blocking chunks: one command of at most 270 s that returns on a done-condition
  (`timeout 270 bash -c 'until <done>; do sleep 5; done'`), run with the shell tool's own `timeout` set to 300000 (its default stops at 120 s) and repeated until done, with no status
  reads, `echo` or bare `sleep` calls in between; read the log once at the end. The prompt cache
  lives 5 minutes, so a longer silent gap re-bills the whole context: go idle on a background
  run's exit notification only for a wait expected to exceed about 45 minutes.
- Every call re-reads the whole context, so make fewer, fuller calls: issue independent reads,
  greps and status checks together in one message, and chain related shell steps in one command.
- Keep output out of the context: send run output to a log file and print only a summary line or
  the matching error lines; Read large files with `offset`/`limit` or Grep them; open review
  boards and contact sheets rather than every capture (image budget in the brief, 12 if unset).
- Budget: about 80 tool calls, or the number in the brief. If the work is not nearly done by
  then, stop at a building state and hand off PARTIAL with the exact resume point; never run on
  into context compaction.
- Start `handoff.txt` early and keep it current, so a hang or a full context loses nothing.
- "All" means all: cover the whole set the brief names; report the counts and list every
  exclusion with its reason.
- Disk: keep your evidence folder under `<evidence_budget>` and capture only what the comparisons
  need. At handoff delete raw captures, comparison iterations except the final one, probe and
  scratch output, frame dumps and isolated user-data dirs; keep the handoff, current criteria,
  references and sketches, before-data, review boards and reusable scripts. Check free disk before
  long batches; stop and report below `<min_free_disk>`.
- Grep every run log for the engine's error markers before trusting a round.
- Run only the tests your change needs. Never run a full sweep unless the brief says the user asked.
- Generation batches are not test sweeps: a batch authorised in a brief (seed lists, variant
  grids, per-line dialogue) is production work, bounded by `<batch_cap>` from `project.md` and
  the single ComfyUI/GPU slot lease. ComfyUI jobs do not count against the engine-run caps above.
- Never run old or frozen builds; use recorded before-data. No A/B builds for the user.
- Never search the whole disk; search the workspace or your evidence folder only.
- Use ABSOLUTE paths for user-data dirs and capture outputs; relative paths may resolve inside the
  project directory depending on the runner.
- Tests exit non-zero on any failure, normalised (`1`, never the failure count).
- No packaging or release work unless you are the release manager with user approval.
- Vault gaps: if the vault does not answer a knowledge question, say so in the handoff and
  route it to the knowledge keeper as a finding; never invent a wiki citation, and never
  file a routine lookup to the vault yourself.
- Write the handoff in your evidence folder and return a concise report.
- The project's "Worker hard limits" (pasted below this block from `project.md`) bind exactly like
  the lines above. They may tighten these limits, never loosen them.

If `project.md` opts in, also: no performance work before the final step; no back-compat migrations
or legacy branches; art style rules.

### Project hard limits

`project.md` has a "Worker hard limits" section for what only this project needs: engine commands
and flags, numeric caps, exclusive-tool addresses, engine traps, the knowledge-base rule, the
user's durable rules. The coordinator pastes it into every brief right after the block above. A
rule that would help any game project belongs in this file instead (send it upstream); never fork
this skill into the project to add rules.

## Autonomy

Make sensible decisions yourself and record each material one with its reason. Anything that changes
another owner's contract, a locked criterion or a protected design decision is a finding for the
coordinator, not a decision.

## Shared tree

Several workers may edit one tree at once.
- Only edit assigned files. In shared files use targeted edits, re-read right before editing.
- Prefer additive changes (a new complete function, a new data entry) over partial rewrites.
- If another worker's break voids your run, wait, rerun, and name the file in the handoff.
- Put scratch and evidence in your evidence folder, never in the project source tree, and never in a
  scratch location other workers share (same-named scripts collide).

## Exclusive tools

- One owner per slot; use only your slot's address. Launch it only if its health check fails.
- Check the connection and inspect the scene/state before modifying; preserve unrelated open work.
- Never open a source file another slot owns; shared sources are single-owner and named in the brief.
- Owner scope: build, export, wire in, one quick in-game capture and review. Sweeps and repeated
  comparison rounds go to an integration worker named in the handoff.
- Background/CLI use is for repeatable export and validation and must not replace the live loop.

## Engine runs

- `<timeout>` on every run; isolated user data; headless where possible.
- Tests that capture images need a window (serialised, off-screen).
- Use a fixed timestep for deterministic tests.
- Know your engine's harmless diagnostics (list them in `project.md`); every other error is a defect.
- Verify the capture's true resolution before trusting a multi-resolution pass: some setups ignore
  the requested window size.
- Captures meant for comparison are deterministic: fixed timestep, pinned clock, weather and
  seeds, the clock reset per view. The view list and its order are part of the recipe.
- When a change needs a one-off engine refresh before headless runs see it (a new global class, a
  re-exported asset), run that refresh once, right away; until then every worker's runs break. The
  steps are in `project.md`.

## Visual workflow (UI or graphics changes)

- Sketch or concept BEFORE implementation, informed by a current capture.
- Named-region criteria at several resolutions, defined before iterating, locked, and
  **discriminating**: the before capture must fail them.
- Compare with `<compare_tool>` into a new iteration folder each time.
- Lock on measured noise: every before set includes a natural-variance probe pair (same view, a
  different frame or seed). Set each threshold from that noise, and drop and list a check that
  cannot separate the before state from noise instead of clamping it.
- Never loosen thresholds, move regions or mask changed content to pass. Version criteria only with a
  written justification. Rebuild a reference after a failure only from before-data and the spec,
  never from after pixels.
- Review the actual images manually as a player would (gameplay views, readability, interaction) and
  record the review separately from numbers.

## Art

- Follow the style rules in `project.md`. A technical pass never approves appearance; the
  coordinator owns promotion.
- Promote an asset atomically: the exported file and its import metadata go into the runtime tree
  together, through the project's promotion tool if it has one, and are imported immediately. A
  half-promoted or un-imported asset voids other workers' rounds.
- Generated assets promote atomically the same way, and their manifest travels with the asset
  into the runtime tree: the manifest is the licence/provenance record (`licences.md`), and an
  asset without one, or whose licence status is not `cleared` / `cleared-conditional`, is never
  promoted.

## Model boundary

Follow SKILL.md "Route by current chunk complexity". Keep focused checks with coupled implementation; once design is settled, hand repeated corpus/suite/routine validation to a fresh mid-tier chunk (fixed named-test runs may use the cheapest). Workers report gaps and never launch replacement workers.

## Handoff

Write the handoff with `templates/handoff.md`: status, files, decisions, numbers, test counts, image
paths, vault lookup and any vault gap, "For the coordinator" findings, next owner. Update docs only
where they have lasting value and the knowledge-base pages your brief names. Then return a concise
report.
