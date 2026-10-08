---
name: studio-brief
description: Write a self-contained worker brief for one task from the game-studio worker-brief template, choosing the role agent and model tier, with the worker hard limits pasted in. Use before launching any studio worker.
argument-hint: "<role> <task>"
---

# Write a worker brief

Coordinator (or `game-studio:coordinator-helper`). Follows section 15 of the `game-studio` skill
(`${CLAUDE_PLUGIN_ROOT}/skills/game-studio/SKILL.md`).

1. Select the active runtime using the game-studio skill's "Runtime model mapping". In Claude, pick the role and its agent: `game-studio:feature-dev`, `ui-dev`, `art-owner`, `prep`,
   `integration`, `qa`, `balance`, `visual-review`, `knowledge-keeper`, `release-manager`,
   `surveyor` or `coordinator-helper` (definitions in
   `${CLAUDE_PLUGIN_ROOT}/skills/game-studio/references/roles.md`). Choose the current chunk's complexity, never simply retain the role default;
   pass the mapped runtime `model` on every launch and record the concrete reason. In Codex,
   use a self-contained role brief with `collaboration.spawn_agent`, not Claude agent identifiers.
2. Fill `${CLAUDE_PLUGIN_ROOT}/skills/game-studio/templates/worker-brief.md` in as the Agent prompt
   (the coordinator does not save briefs to disk; a worker writes any brief file) and fill every `<...>`
   from `project.md`, the queue doc (from project.md; plugin option `queue_doc`), prior handoffs and recorded
   before-data. The worker sees none of your conversation: paths, decisions and limits go in the brief.
3. Name owned and shared files so parallel workers never overlap; name the exclusive-tool slot for an
   art owner ("owner, slot X") or state that the worker owns none.
4. Evidence folder: `<evidence_dir>/<stream>/<task>/` (from project.md; plugin option `evidence_dir`). Engine caps
   (as numbers) and the disk budget from `project.md`.
5. Paste the "Hard limits" block from
   `${CLAUDE_PLUGIN_ROOT}/skills/game-studio/references/worker-rules.md` verbatim, then the
   "Worker hard limits" section of `project.md` verbatim.
6. Add the role-specific lines from the template. In Claude, launch with the Agent tool using
   `subagent_type: "game-studio:<role>"`. In Codex, use `collaboration.spawn_agent` with `task_name`,
   `message`, the mapped `model`, and `fork_turns: "none"` for a fresh worker. Record the launch in the queue doc.

Return the brief text (or launch it, if asked to).
