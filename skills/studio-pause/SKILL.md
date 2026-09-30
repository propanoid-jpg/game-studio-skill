---
name: studio-pause
description: Pause the game studio cleanly - tell every running worker to stop at a building state and write a partial handoff, then add a PAUSED block with checkpoints at the top of the queue doc. Use when the user says pause, stop for now or end of session.
argument-hint: "[reason]"
---

# Pause the studio

Coordinator only. Follows section 12 of the `game-studio` skill
(`${CLAUDE_PLUGIN_ROOT}/skills/game-studio/SKILL.md`).

1. List every running worker, background shell and monitor you launched, and which exclusive-tool
   slot each worker owns.
2. Message each running worker: "Pause now. Stop at a building, parseable state; do not start new
   runs; write a PARTIAL handoff in your evidence folder (done, half-done, files touched, files
   mid-edit, exact next step); save and keep your exclusive-tool session open unless your brief says
   otherwise; then return." Wait for the reports. A worker that does not answer: stop it and note
   that its files may be mid-edit.
3. Add at the TOP of the queue doc (named in `project.md`; plugin option `queue_doc`):

   ```text
   PAUSED <YYYY-MM-DD> - <reason>
   - <stream/task> - <role> - checkpoint: <evidence folder>/handoff.txt - state: <one line> - files mid-edit: <paths or none>
   ```

4. Stop the background shells and monitors you started. Close only tools you launched, and only
   after checking there is no unsaved work. Never kill processes you did not start.
5. Update the knowledge base's status page if one is configured.
6. Report to the user: what was paused, the checkpoints, anything left running and why.

Resume later with `/game-studio:studio-resume`.
