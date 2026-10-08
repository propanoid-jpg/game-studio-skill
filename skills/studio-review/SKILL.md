---
name: studio-review
description: Review a worker's handoff before accepting it, using the game-studio review checklist - evidence, scope, caps, visual and art quality judged as a player, then verdict, queue record, routed findings, cleanup and next launch. Use whenever a worker returns or a handoff path is given.
argument-hint: "<handoff path | stream/task>"
---

# Review a handoff

Coordinator only (a `game-studio:coordinator-helper` may pre-review, but the coordinator decides).
Reviewing is reading: fixes the review finds go to a worker, not into your own edits.
Follows section 4 of the `game-studio` skill (`${CLAUDE_PLUGIN_ROOT}/skills/game-studio/SKILL.md`).

1. Open the handoff (`$ARGUMENTS`, or `<evidence_dir>/<stream>/<task>/handoff.txt`).
2. Go through `${CLAUDE_PLUGIN_ROOT}/skills/game-studio/templates/review-checklist.md` item by item:
   - open the key images yourself, including one ordinary-gameplay view for visual work;
   - check claims against results files and logs; grep logs for the engine's error markers;
   - check scope (only assigned files), caps, no full sweep, no old-build runs, nothing loosened;
   - judge art and UI as a player; a numeric pass alone never accepts.
3. Verdict: accept, accept with routed follow-ups, or a follow-up brief (same worker if it is still
   running, otherwise a fresh one; reassess remaining chunk complexity and cite a concrete reason for any escalation).
   Once complex design is settled, route repeated validation to fresh Sol/sonnet; fixed named runs may use Luna/haiku. Preserve focused implementation checks and one quick gameplay review.
4. Record the verdict in the queue doc with the date and handoff path, and decisions in the decision
   log; brief a knowledge-keeper worker for knowledge-base updates if one is configured. Route each "For the coordinator" finding (S0 now, S1 next brief, S2/S3 polish list).
5. Clean up the worker's background shells and monitors, then launch the next task immediately,
   refilling a freed exclusive-tool slot first.

Reply with a short verdict: status, what was checked, decisions, routed findings, next launch.
