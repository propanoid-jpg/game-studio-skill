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
   - check scope (only assigned files), caps, no full sweep, no old-build runs, nothing loosened,
     evidence folder pruned to the disk budget;
   - judge art and UI as a player; a numeric pass alone never accepts.
3. Verdict: accept, accept with routed follow-ups, or a follow-up brief (same worker if it is still
   running, otherwise a fresh one; reassess remaining chunk complexity and cite a concrete reason for any escalation).
   Once complex design is settled, route repeated validation to a fresh mid-tier worker; fixed named runs may use the cheapest. Preserve focused implementation checks and one quick gameplay review.
4. Delete the accepted item from the queue doc (open work only) and add follow-ups as one line each;
   record decisions in the decision log; add knowledge-base updates to the queue doc's "Vault pending" list if a vault is configured (one knowledge-keeper brief per milestone or about five lines; at once for a user decision). Route each "For the coordinator" finding (S0 now, S1 next brief, S2/S3 polish list).
5. Clean up the worker's background shells and monitors, then fill every free slot with independent
   queue items, refilling a freed exclusive-tool slot first. Check the other running workers for
   stalls (no new evidence for `<stall_minutes>`) and relaunch any that are stuck.

Reply with a short verdict: status, what was checked, decisions, routed findings, next launch.
