# QA process

QA is layered; each layer has a trigger, an owner and a required output. All runs obey the resource
caps in `worker-rules.md`. Commands come from `project.md`.

## Determinism rules (all tests)

- Fixed seeds; record every seed used. Session seeds are exposed for reproduction.
- Fixed timestep. Outcome-affecting logic uses simulation time, never wall clock.
- Every test exits non-zero on any failure, normalised to `1`, on every code path.
- Isolated user-data directories per run; never a real player profile.
- A test is flaky until repeated runs agree; fix the cause (race, wall clock, window setup) rather
  than retrying until green.

## Layer 1: targeted tests (every change)

- Owner: the implementing worker.
- Run the suites that cover the change plus a build/parse check. Split long suites by argument.
- Output: command lines, pass/fail counts and the results file path in the handoff.

## Layer 2: generation corpus (procedural changes)

- Owner: the feature worker for its area, or the integration worker after an art drop.
- Fixed showcase seeds plus a bounded random batch (typically 16-32 per area), queued within the
  caps, plus a forced-fallback run.
- Report per area: seeds passed/failed, **invalid-seed count**, **fallback count**, generation time
  (max and typical), **showcase-seed hash stability** (same seed, same layout hash before and after
  an unrelated change, or the change is explained).
- A generator that errors without retry or fallback is an S0/S1 defect.

## Layer 3: campaign and playthrough bots

- Owner: integration or balance worker. Several seeds, bounded time, real game flow (no shortcuts
  the player lacks).
- A bot pass is an engineering check, never proof of feel, pacing or balance.

## Layer 4: full test-health sweep

> Never launch this layer on the studio's own initiative, including before a release. Only when
> the user explicitly asks. Otherwise use targeted suites and route single failing tests to
> focused workers.

- Owner: QA/test-health worker. Run the whole suite (headless where possible, windowed serial for
  capture tests).
- For each failure decide: **stale test** (update to current authorised behaviour, dated comment, no
  coverage deleted), **flaky** (fix the cause), **too long** (bound or split), or **real bug** (fix
  only if trivial and unowned; else route with evidence).
- Output: per-test table (exit, time, errors, verdict) and a handoff with the routed list.

## Layer 5: live-play readability review

- Owner: visual polish/review worker. Trigger: after visual, UI or encounter milestones.
- Captures from ordinary gameplay cameras and states at the supported resolutions; review as a
  player: threat telegraphs, friend/foe distinction, text, occlusion, clutter. Findings go to polish
  lists or fixes. Metrics never replace this review.

## Layer 6: balance tables

- Owner: balance worker. Trigger: any tuning or progression change.
- Reusable probe (arithmetic from live formulas, or bot scenarios over 8+ seeds). The "before"
  column comes from recorded data or from evaluating the old table on the current build, **never
  from running an old build**.
- Output: before/after tables per level and encounter type, plus the data diff.

## Severity triage and routing

| Severity | Examples | Action |
|---|---|---|
| S0 blocker | parse/build error, crash, hang, save or data loss, generator error without fallback | top of `<queue_doc>`; fix worker now; message affected running workers |
| S1 major | feature broken, progression blocked, real test failure, visual regression failing locked criteria | owner's next brief (or a new worker now if the owner is idle) |
| S2 moderate | balance deviation, readability issue, comparison near-miss, over-long test | polish list or balance/polish queue |
| S3 minor | cosmetic, doc drift, nice-to-have | polish list or knowledge keeper |

Every routed finding carries evidence: path, seed, command, log line or probe.

## Log hygiene

- Before trusting a round, grep all logs for the engine's error markers (`project.md`). A hit fails
  the test.
- A timeout exit is a hang to investigate, not a pass.
- A round voided by another worker's build break is rerun after the fix; the break is reported.

## What QA never does

- Run old or frozen builds for comparison.
- Loosen thresholds, delete coverage or label failures "pre-existing" to get green.
- Performance audits before the final performance step, if the project opted into that policy.
