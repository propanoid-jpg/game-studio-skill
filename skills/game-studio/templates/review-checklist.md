# Coordinator review checklist (every handoff)

Run through this before accepting. Accepting takes minutes, not a re-run of the worker's job; if
something needs re-running, that is a follow-up brief.

## Evidence

- [ ] Handoff exists at the stated path; status is explicit (COMPLETE / PARTIAL / BLOCKED).
- [ ] Opened the key images myself (final captures, overlays), including one ordinary-gameplay view
      for visual work. They show what the handoff claims.
- [ ] Numbers are traceable: results files, corpus tables, balance tables exist.
- [ ] Logs grep clean for the engine's error markers; timeouts are explained, not counted as passes.

## Scope and rules

- [ ] Only assigned files edited; shared files changed with targeted edits; nothing reverted.
- [ ] Tests exit non-zero on failure; no coverage deleted without a note.
- [ ] No old/frozen build runs; before-data came from records.
- [ ] No full test sweep (unless the user asked); no unrequested performance work, migrations or
      packaging (per the project's opt-in policies).
- [ ] Resource caps respected; windows off-screen; no leftover shells, monitors or processes.
- [ ] Evidence folder within the disk budget and pruned (raw captures, old iterations, scratch and
      user-data dirs gone; handoff, criteria, references and boards kept).
- [ ] Exclusive tools: only the named owner used its slot, within scope.

## Quality

- [ ] Visual work: sketch predates implementation; criteria locked before iteration and
      discriminating; nothing loosened or masked; versioning justified; manual player-view review
      written. Judged as a player, not by metrics.
- [ ] Art: matches the project's style rules; technical pass is not treated as approval; promotion
      checklist items addressed or routed; asset and import metadata promoted together and imported.
- [ ] Procedural: corpus with invalid-seed and fallback counts and showcase hash stability.
- [ ] Protected design decisions and project policies intact.
- [ ] Owning docs updated; no task-report docs created.

- [ ] Next model follows remaining chunk complexity; settled routine validation leaves Astra/opus, with exact checks and ownership handed to fresh Sol/sonnet or fixed-run Luna/haiku. Escalations cite concrete complexity/failure.

## Decide and record

- [ ] Verdict: accept / accept with follow-ups / follow-up brief (same worker if running, else fresh).
- [ ] `<queue_doc>`: targeted edit marking acceptance with date and handoff path, plus decisions.
- [ ] Knowledge base (if configured): update owning pages and the decision log.
- [ ] Each "For the coordinator" finding routed (S0 now; S1 next brief; S2/S3 polish list).
- [ ] Finished worker cleaned up (shells, monitors, idle tools); next task(s) launched immediately;
      freed exclusive-tool slot refilled first; load and free disk checked.
