# game-studio skill for Claude Code

A process skill that turns one main Claude Code session (the **coordinator**) and many fresh
**workers** into a small game studio. It is engine- and art-pipeline-agnostic. It defines:

- roles and model choice by task difficulty;
- worker briefs, handoffs and a coordinator review checklist;
- the coordinator loop (review, decide, record, route, launch);
- parallelism caps, serial slots for exclusive tools, resource limits, shared-tree hygiene;
- development, QA (layers, triage S0-S3), visual and release workflows, pause/resume.

## Install

Copy `skills/game-studio/` into either:

- `<project>/.claude/skills/game-studio/` (one project), or
- `~/.claude/skills/game-studio/` (all projects).

## Customise

1. Copy `project.example.md` to `<project>/.claude/skills/game-studio/project.md` (or keep the name)
   and fill it in: engine, paths, test runner, capture tool, exclusive tools, resource caps,
   knowledge base, standing user rules. Delete what does not apply.
2. Optional policies (no back-compat migrations, no performance work until last, autonomy,
   knowledge base) apply only if `project.md` opts in.
3. Edit the `description` in `SKILL.md` frontmatter to name your game so the skill triggers reliably.

## Example

> "Plan the inventory rework and start the first tasks."

The coordinator reads `project.md`, queues tasks with disjoint file ownership, writes one brief per
task from `templates/worker-brief.md` (with the worker rules pasted), launches fresh workers on the
cheapest adequate model, and reviews each `handoff.md` with `templates/review-checklist.md` before
recording acceptance and launching the next task.

## License

MIT, see `LICENSE`.
