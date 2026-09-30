---
name: studio-resume
description: Resume the game studio after a pause or crash - verify the tree builds, then relaunch every paused stream as a fresh worker from its checkpoint and clear the PAUSED lines. Use when the user says resume, continue or carry on after a pause.
argument-hint: "[stream ...]"
---

# Resume the studio

Coordinator only. Follows section 12 of the `game-studio` skill
(`${CLAUDE_PLUGIN_ROOT}/skills/game-studio/SKILL.md`).

1. Read `project.md`, the project instruction file and the PAUSED block at the top of the queue doc
   (named in `project.md`; plugin option `queue_doc`). With arguments, resume only the
   named streams.
2. Verify the tree builds: one small targeted test or parse check under the project's timeout, then
   grep the log for the engine's error markers (a worker runs it; the coordinator only reads the log).
   Route any break, however small, to a fresh fix worker first. Check machine load and the engine-run cap.
3. For each paused stream, read its checkpoint handoff and write a fresh brief with
   `/game-studio:studio-brief` (template `${CLAUDE_PLUGIN_ROOT}/skills/game-studio/templates/worker-brief.md`).
   Add the resume line: "Your predecessor was stopped mid-task; edits may be partial. Checkpoint:
   <path>. Verify the tree builds and your files are consistent before continuing."
4. Launch each as a FRESH worker of its role agent (`game-studio:<role>`), refilling exclusive-tool
   slots first, within the caps. Never resume the old worker's context.
5. Replace each PAUSED line with "resumed <date> -> <new evidence folder>" as it is relaunched or
   delivered; remove the block when it is empty.
