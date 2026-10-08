# Development workflow

How work goes from a user direction to accepted, recorded changes. Applies to features, systems,
content, UI, art and tuning at any stage. Paths and tools come from `project.md`.

## 1. From direction to queue (coordinator)

1. Record the user's direction in `<queue_doc>` with its date. Latest explicit corrections override
   older plans within their scope; move superseded items to history rather than restoring them.
2. Check the knowledge base (if any) for current state, owners and past decisions.
3. Break the direction into tasks that own disjoint files. For a large programme write one plan doc
   with numbered decisions and phases; reuse existing plan docs.
4. Order: data and logic before presentation; prep before exclusive-tool work; that work before its
   integration sweep. Pull non-exclusive parts of later phases forward.
5. Launch as many parallel workers as the caps allow; one owner per exclusive-tool slot.

## 2. Implementation order (every worker)

1. **Data model and deterministic logic.** Typed data, tuning values data-driven, seeded randomness,
   generators separate from rendering.
2. **Test harness.** A focused test that exercises the logic deterministically and exits non-zero on
   failure.
3. **Integration.** Wire into runtime without rewriting unrelated systems.
4. **UI and feedback.** Progressive disclosure, readable information, visual workflow below.
5. **Tuning and art polish.** Balance tables; art through the art owner.

Keep the game runnable at every step. If the project opted into the pre-release policy, remove
obsolete compatibility paths in the system you change (not unrelated ones).

## 3. Visual workflow (every UI or graphics change)

1. **Capture current state** at the target viewports with the real UI state, camera and content.
2. **Sketch before implementation**, informed by that capture (full viewport, same camera/state).
3. **Define criteria before iterating:** named regions per resolution (three or more common
   sizes) with a similarity metric for concept comparisons or an exact-pixel metric for stable
   regions. Explain what each region measures and which render differences are expected.
4. **Prove the criteria discriminate:** the before capture must fail them; self-comparison and
   stability probes (small exposure change, small shift, a second run) must pass. Coarsen grids
   rather than raise thresholds if probes are unstable, and record it. On deterministic captures,
   where a repeat run shows no noise, include a natural-variance probe pair (another frame or
   seed, same view) in every before set and derive each threshold from that measured noise; drop
   and list a check that cannot separate the before state from noise instead of clamping it.
5. **Lock** the criteria. Implement.
6. **Compare** each iteration into a new folder; inspect crops, overlay and diff at full size.
7. **Iterate the implementation** until checks pass. Never loosen thresholds, move regions or mask
   changed content. If the requirement genuinely changes, version the reference and criteria with a
   written justification. Rebuild a reference after a failure only from before-data and the spec
   (same regions and formula, written reason), never from after pixels.
8. **Manual review as a player** of the actual images, including ordinary-gameplay views:
   readability, silhouette, lighting, occlusion, text overflow, interaction. Numbers never
   establish quality. Record the review separately.

## 4. Art workflow

1. **Prep worker:** current capture, concepts, sketches, locked criteria, spec (bounds, pivot,
   clips, budgets, gameplay contract), capture cases.
2. **Art owner (live tool session):** check connection, inspect scene, build in the project's style;
   check proportions against the reference early; save sources under `<art_source_dir>`.
3. **Export** through the project's pipeline into a fresh output folder; a clean export is a
   technical pass only.
4. **Promote and wire in:** move the export and its import metadata into the runtime tree in one
   step (the project's promotion tool, if any) and import immediately, then wire in at the
   consumer named in the brief; one quick in-game capture.
5. **Integration worker:** captures and comparisons at several resolutions, acceptance checks, seed
   sweeps and campaigns for affected content, near-miss fixes.
6. **Coordinator promotion:** run the project's acceptance checklist; record accepted or
   needs-iteration with reasons.

## 5. Procedural generation work

- Seeds, layout, validation and scene instantiation stay separate and testable without rendering.
- Keep connectivity, reachability of critical content, spawn clearance, bounded size/time, limited
  retries and a known-valid fallback. Every generated result is reproducible from its seed.
- Validate with a corpus (see `qa.md`): fixed showcase seeds plus a bounded random batch.

## 6. Docs and knowledge

- Update the existing doc that owns the behaviour; do not create task reports. The handoff is the
  delivery record; the coordinator records acceptance in the queue and knowledge base.

## 7. Definition of done (worker)

- Acceptance criteria met, or an honest BLOCKED with the exact blocker.
- Changed code builds/parses; affected scenes/levels load; targeted tests pass; logs grep clean.
- Visual changes: locked criteria pass on final captures at every resolution, plus a written manual
  review as a player.
- Owning docs updated; handoff written; out-of-scope findings listed.
