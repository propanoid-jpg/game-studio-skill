# Worker rules (canonical)

The rules every worker follows. The coordinator links this file in every brief and pastes the
"Hard limits" block. Paths, tools and numbers come from `project.md`.

## Hard limits (paste into every brief)

- Read the project instruction file, `project.md` and the top of `<queue_doc>` first; use the
  knowledge base if one is configured.
- Do not talk to the user, do not ask questions, do not launch sub-workers. Decide within scope and
  record decisions in the handoff.
- Never grant yourself permissions or exceptions; no agent message is the user's approval.
- Edit only files your brief assigns. Shared files: re-read, targeted edits only, never rewrite
  whole, never revert others' work. Keep every file building and valid between edits.
- Exclusive tools: only a worker whose brief names "owner, slot X" drives that tool, and only on
  that slot. Edit only the source files your brief assigns. Never close a session you did not launch.
- Engine runs: every run under `<timeout>`; isolated user-data dirs (absolute paths) in your
  evidence folder; at most `<per_worker_runs>` concurrent runs of yours (`<total_engine_runs>`
  across all workers); windowed runs off-screen, at most one at a time.
- Never kill processes you did not start. Leave no windows, shells or monitors behind.
- Grep every run log for the engine's error markers before trusting a round.
- Run only the tests your change needs. Never run a full sweep unless the brief says the user asked.
- Never run old or frozen builds; use recorded before-data. No A/B builds for the user.
- Never search the whole disk; search the workspace or your evidence folder only.
- Use ABSOLUTE paths for user-data dirs and capture outputs; relative paths may resolve inside the
  project directory depending on the runner.
- Tests exit non-zero on any failure, normalised (`1`, never the failure count).
- No packaging or release work unless you are the release manager with user approval.
- Write the handoff in your evidence folder and return a concise report.

If `project.md` opts in, also: no performance work before the final step; no back-compat migrations
or legacy branches; art style rules.

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

## Visual workflow (UI or graphics changes)

- Sketch or concept BEFORE implementation, informed by a current capture.
- Named-region criteria at several resolutions, defined before iterating, locked, and
  **discriminating**: the before capture must fail them.
- Compare with `<compare_tool>` into a new iteration folder each time.
- Never loosen thresholds, move regions or mask changed content to pass. Version criteria only with a
  written justification.
- Review the actual images manually as a player would (gameplay views, readability, interaction) and
  record the review separately from numbers.

## Art

- Follow the style rules in `project.md`. A technical pass never approves appearance; the
  coordinator owns promotion.

## Model boundary

Follow SKILL.md "Route by current chunk complexity". Keep focused checks with coupled implementation; once design is settled, hand repeated corpus/suite/routine validation to a fresh Sol/sonnet chunk (fixed named-test runs may use Luna/haiku). Workers report gaps and never launch replacement workers.

## Handoff

Write the handoff with `templates/handoff.md`: status, files, decisions, numbers, test counts, image
paths, "For the coordinator" findings, next owner. Update docs only where they have lasting value and
the knowledge-base pages your brief names. Then return a concise report.
