---
name: studio-brief
description: Write a self-contained worker brief for one task from the game-studio worker-brief template, choosing the role agent and model tier, with the worker hard limits pasted in. Use before launching any studio worker.
argument-hint: "<role> <task>"
---

# Write a worker brief

Coordinator (or `game-studio:coordinator-helper`). Follows section 15 of the `game-studio` skill
(`${CLAUDE_PLUGIN_ROOT}/skills/game-studio/SKILL.md`).

1. Pick the role and its agent: `game-studio:feature-dev`, `ui-dev`, `art-owner`, `prep`,
   `integration`, `qa`, `balance`, `visual-review`, `knowledge-keeper`, `release-manager`,
   `surveyor` or `coordinator-helper` (definitions in
   `${CLAUDE_PLUGIN_ROOT}/skills/game-studio/references/roles.md`). Keep the agent's default model
   unless the task needs another tier; pass `model` on launch to override.
2. Copy `${CLAUDE_PLUGIN_ROOT}/skills/game-studio/templates/worker-brief.md` and fill every `<...>`
   from `project.md`, the queue doc (from project.md; plugin option `queue_doc`), prior handoffs and recorded
   before-data. The worker sees none of your conversation: paths, decisions and limits go in the brief.
3. Name owned and shared files so parallel workers never overlap; name the exclusive-tool slot for an
   art owner ("owner, slot X") or state that the worker owns none.
4. Evidence folder: `<evidence_dir>/<stream>/<task>/` (from project.md; plugin option `evidence_dir`). Engine caps from `project.md`.
5. Paste the "Hard limits" block from
   `${CLAUDE_PLUGIN_ROOT}/skills/game-studio/references/worker-rules.md` verbatim, plus the project's
   standing user rules from `project.md`.
6. Add the role-specific lines from the template, then launch the worker with the Agent tool using
   `subagent_type: "game-studio:<role>"` and record the launch in the queue doc.

Return the brief text (or launch it, if asked to).
