# game-studio plugin for Claude Code

A Claude Code plugin that turns one main session (the **coordinator**) and many fresh **workers**
into a small game studio. It is engine- and art-pipeline-agnostic. It bundles:

- the `game-studio` **skill**: roles, model choice by task difficulty, worker briefs, handoffs, the
  coordinator review loop, parallelism caps and exclusive-tool slots (for example several art-app
  instances, one owner per instance and file), shared-tree hygiene, development, QA (layers, triage
  S0-S3), visual and release workflows, pause/resume;
- **role agents**, so workers launch as named studio roles instead of a general-purpose agent;
- **coordinator commands** for briefs, reviews, pause and resume;
- advisory **hooks** (engine-run cap warning, review reminder, session-start pointer);
- **options** for the queue doc, evidence folder and engine-process cap.

## Install

In Claude Code:

```text
/plugin marketplace add propanoid-jpg/game-studio-skill
/plugin install game-studio@game-studio
```

From a shell:

```bash
claude plugin marketplace add propanoid-jpg/game-studio-skill
claude plugin install game-studio@game-studio                   # user scope (all projects)
claude plugin install game-studio@game-studio --scope project   # shared with the repo's collaborators
```

Update later with `claude plugin marketplace update game-studio` and
`claude plugin update game-studio@game-studio`.

**Skill only (no plugin):** copy `skills/game-studio/` into `<project>/.claude/skills/game-studio/`
or `~/.claude/skills/game-studio/`. You get the process, without agents, commands, hooks or options.

## What's inside

```text
.claude-plugin/plugin.json        manifest and options (userConfig)
.claude-plugin/marketplace.json   this repo is also its own marketplace
skills/game-studio/               the operating manual (SKILL.md, references/, templates/, project.example.md)
skills/studio-brief/              /game-studio:studio-brief <role> <task>
skills/studio-review/             /game-studio:studio-review <handoff>
skills/studio-pause/              /game-studio:studio-pause [reason]
skills/studio-resume/             /game-studio:studio-resume [stream ...]
agents/                           one agent per studio role
hooks/hooks.json, scripts/        advisory hooks
```

### Agents

Launch with the Agent tool as `subagent_type: "game-studio:<agent>"` (or mention
`@agent-game-studio:<agent>`). Every agent preloads the `game-studio` skill, carries the hard worker
rules (targeted tests only, resource caps, off-screen windows, never kill processes it did not
start, keep the shared tree parseable, judge like a player, sketch-first visual workflow), writes a
handoff, never talks to the user and has no Agent tool, so it cannot launch sub-agents. A `model`
passed at launch overrides the default below.

| Agent | Role | Model |
|---|---|---|
| `feature-dev` | One scoped feature or system change | sonnet (pass opus for unknown-cause debugging) |
| `ui-dev` | Interface change against a sketch and locked criteria | sonnet |
| `art-owner` | Live art-tool work on one exclusive slot; several may run in parallel | opus |
| `prep` | Captures, sketches, locked criteria, specs so exclusive tools never wait | sonnet |
| `integration` | Seed sweeps, fallbacks, campaigns, comparison near-misses | sonnet |
| `qa` | Test sweeps (only when the user asks), stale and flaky tests | sonnet |
| `balance` | Probes, tuning, before/after tables | opus |
| `visual-review` | Live-play readability review and presentation polish | opus |
| `knowledge-keeper` | Knowledge-base sync and lint | haiku |
| `release-manager` | Release checklist and packaging, only on user approval | sonnet |
| `surveyor` | Read-only inventories, grep audits, log summaries | haiku |
| `coordinator-helper` | Drafts briefs and pre-reviews handoffs (optional) | opus |

### Hooks

All hooks are advisory and never block. They are bash scripts: on Windows they run under Git Bash
(Claude Code's default hook shell when Git for Windows is installed).

- **PreToolUse (Bash, PowerShell):** counts running processes whose name contains `engine_process`
  (`tasklist` on Windows, `pgrep` on macOS/Linux) and warns when the count reaches
  `max_engine_runs`. An empty process name or a cap of 0 turns it off.
- **PostToolUse (Agent):** after the coordinator launches a `game-studio:*` or general-purpose
  worker, reminds it to review the handoff with the checklist when the worker returns and to clean
  up the worker's shells. (A SubagentStop hook is deliberately not used: its context goes to the
  finishing worker, not to the coordinator, and makes the worker take another turn.)
- **SessionStart:** if the project has `.claude/game-studio/project.md` (or
  `.claude/skills/game-studio/project.md`) or the queue doc, adds a one-line reminder to read them.
  Silent in other projects.

### Options

Set when the plugin is enabled, or later in `/config`:

| Option | Default | Used by |
|---|---|---|
| `engine_process` | `godot` | engine-cap hook (case-insensitive substring of the process name) |
| `max_engine_runs` | `10` | engine-cap hook |
| `evidence_dir` | `evidence` | reference for agents and commands (`<evidence_dir>/<stream>/<task>/`) |
| `queue_doc` | `docs/TODO.md` | session-start hook; reference for agents and commands |

`project.md` stays the source of truth for agents and commands; keep the options equal to it.

## Customise

1. Copy `skills/game-studio/project.example.md` to `<project>/.claude/game-studio/project.md` and
   fill it in: engine, paths, test runner, capture tool, exclusive tools, resource caps, knowledge
   base, standing user rules. Delete what does not apply. Keep the plugin options equal to it.
2. Optional policies (no back-compat migrations, performance last, autonomy, knowledge base) apply
   only if `project.md` opts in.
3. The `art-owner` agent grants `mcp__blender__*`. For another art tool or server name, copy
   `agents/art-owner.md` into `<project>/.claude/agents/`, give it a new `name`, and edit `tools`.
   Any other role can be overridden the same way.

## Example

> "Plan the inventory rework and start the first tasks."

The coordinator reads `project.md` and the queue, splits tasks by file ownership, writes one brief
per task with `/game-studio:studio-brief`, launches `game-studio:feature-dev` and
`game-studio:ui-dev` workers, and reviews each `handoff.txt` with `/game-studio:studio-review`
before recording acceptance and launching the next task.

## License

MIT, see `LICENSE`.
