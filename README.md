# game-studio plugin for Claude Code

A Claude Code plugin that turns one main session (the **coordinator**) and many fresh **workers**
into a small game studio. It is engine- and art-pipeline-agnostic. It bundles:

- a **coordinator agent** that runs as the main session: it plans, briefs, launches workers,
  reviews, decides and records, and delegates every task that changes files, produces content,
  researches or looks things up, however small;
- the `game-studio` **skill**: roles, model choice by task difficulty, worker briefs, handoffs, the
  coordinator review loop, parallelism caps and exclusive-tool slots (for example several art-app
  instances, one owner per instance and file), shared-tree hygiene, development, QA (layers, triage
  S0-S3), visual and release workflows, pause/resume;
- **role agents**, so workers launch as named studio roles instead of a general-purpose agent;
- **coordinator commands** for briefs, reviews, pause and resume;
- **hooks** (delegation check, engine-run cap warning, review reminder, session-start pointer);
- **options** for the queue doc, decision log, evidence folder, engine-process cap and delegation
  enforcement.

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

### Update

Refresh the marketplace, then update the plugin, then restart Claude Code (or run
`/reload-plugins`):

```bash
claude plugin marketplace update game-studio
claude plugin update game-studio@game-studio                    # auto-detects the install scope
claude plugin update game-studio@game-studio --scope project     # if it is installed for the project
```

In Claude Code: `/plugin marketplace update game-studio`, then update `game-studio` from the
`/plugin` menu.

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
agents/                           the coordinator and one agent per studio role
settings.json                     runs the main session as game-studio:coordinator
hooks/hooks.json, scripts/        hooks
```

### The coordinator (main session)

The plugin's `settings.json` sets `"agent": "game-studio:coordinator"`, so every session in a
project with the plugin enabled runs as the coordinator. Its tools are limited to managing:
Agent, SendMessage, TaskStop and Monitor for workers; Read, Glob and Grep for review; Bash and
PowerShell for read-only checks (load, logs, `git status`); Edit only for the queue doc, the
decision log, its memory and `project.md`; Skill, WebFetch, WebSearch and AskUserQuestion. It has
no Write, notebook or MCP tools (MCP tools cannot be split into read and write tools generically,
so all are excluded). Everything else goes to a worker, however small; management questions
(priorities, status, decisions, plans, reviews) are answered directly.

**Opt out.** Plugin defaults are the lowest settings layer, so your own `agent` setting wins. To
run a normal main session in one project, add to `.claude/settings.local.json` (just you) or
`.claude/settings.json` (the team):

```json
{ "agent": "claude" }
```

Put it in `~/.claude/settings.json` to opt out everywhere, or start one session with
`claude --agent claude`. The delegation hook still warns in such a session; set
`enforce_delegation` to `warn` (the default) or disable the plugin if you do not want that either.

### Agents

Launch workers with the Agent tool as `subagent_type: "game-studio:<agent>"` (or mention
`@agent-game-studio:<agent>`). Every agent preloads the `game-studio` skill, carries the hard worker
rules (targeted tests only, resource caps, off-screen windows, never kill processes it did not
start, keep the shared tree parseable, judge like a player, sketch-first visual workflow), writes a
handoff, never talks to the user and has no Agent tool, so it cannot launch sub-agents. A `model`
passed at launch overrides the default below.

Role defaults are hints: route each current chunk by complexity. Once complex design is settled, repeated validation moves to a fresh Sol/sonnet chunk; fixed named-test runs may use Luna/haiku. See the skill routing policy.

### Runtime model mapping

Choose the launch API and model for the active runtime. Keep the coordinator on its current session model.

| Task tier | Codex model | Claude model |
|---|---|---|
| Light / cheapest | `gpt-6-luna` | `haiku` |
| Medium / mid | `gpt-6.1-sol` | `sonnet` |
| Complex / strongest | `gpt-6-astra` | `opus` |

In Claude, launch `game-studio:<role>` with the Agent tool and pass the Claude model. The `model`
frontmatter in `agents/*.md` is Claude-specific. In Codex, use `collaboration.spawn_agent` with
`task_name`, a self-contained role brief in `message`, and the Codex `model`. Set `fork_turns: "none"`
(or a positive turn count when needed) when overriding the model; full-history forks inherit the
coordinator's model. Codex does not accept `subagent_type` or Claude role-agent identifiers.
Read the relevant role instructions into the brief; a Claude plugin installation does not register
role agents in Codex. Never pass `haiku`, `sonnet` or `opus` as a Codex model.

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
| `coordinator-helper` | Drafts briefs and pre-reviews handoffs (optional) | sonnet |
| `coordinator` | The main session (set by the plugin), not launched as a worker | the session's model |

### Hooks

Hooks are advisory and never block, except the delegation check when `enforce_delegation` is
`block`. They are bash scripts: on Windows they run under Git Bash
(Claude Code's default hook shell when Git for Windows is installed).

- **PreToolUse (Write, Edit, MultiEdit, NotebookEdit and write-like MCP tools):** the delegation
  check. Main session only: calls from workers carry `agent_id` in the hook input and pass
  silently. When the main session writes a file other than `queue_doc`, `decision_log`,
  `.claude/game-studio/project.md` (or the skill-folder copy) or its memory, or calls an MCP tool
  whose name starts with a write verb (write, create, update, edit, delete, set, execute, import,
  generate, ...), it adds "Coordinator: delegate this to a worker". With `enforce_delegation` =
  `block` it denies the call instead.
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
| `queue_doc` | `docs/TODO.md` | session-start and delegation hooks; reference for agents and commands |
| `decision_log` | empty | delegation hook (the coordinator may edit it directly) |
| `enforce_delegation` | `warn` | delegation hook: `warn` adds a warning, `block` denies the call |

`project.md` stays the source of truth for agents and commands; keep the options equal to it.

## Customise

1. Copy `skills/game-studio/project.example.md` to `<project>/.claude/game-studio/project.md` and
   fill it in: engine, paths, test runner, capture tool, exclusive tools, resource caps, disk
   budget, knowledge base, worker hard limits. Delete what does not apply. Keep the plugin options
   equal to it.
2. Optional policies (no back-compat migrations, performance last, autonomy, knowledge base) apply
   only if `project.md` opts in.
3. **Project rules go in `project.md`, not in a copy of the skill.** Its "Worker hard limits"
   section holds the project's own limits and the user's durable rules (real numbers, commands,
   tool addresses, engine traps). The coordinator pastes it into every brief after the skill's
   "Hard limits" block; it may tighten those limits, never loosen them. Keep one copy of the skill
   (this plugin) and update it from git; send rules any game project would want upstream.
4. A runtime without plugin support (for example Codex) reads the same skill files from the
   marketplace clone, `~/.claude/plugins/marketplaces/game-studio/skills/game-studio/`, which
   `claude plugin marketplace update game-studio` keeps current.
5. The `art-owner` agent grants `mcp__blender__*`. For another art tool or server name, copy
   `agents/art-owner.md` into `<project>/.claude/agents/`, give it a new `name`, and edit `tools`.
   Any other role can be overridden the same way.

## Example

> "Plan the inventory rework and start the first tasks."

The coordinator (the main session) reads `project.md` and the queue, splits tasks by file
ownership, writes one brief per task with `/game-studio:studio-brief`, launches `game-studio:feature-dev` and
`game-studio:ui-dev` workers, and reviews each `handoff.txt` with `/game-studio:studio-review`
before recording acceptance and launching the next task.

## Changelog

- **1.2.0**
  - Disk budget: an evidence budget per task, pruning at handoff and a free-disk check before
    launches (`<evidence_budget>`, `<min_free_disk>` in `project.md`).
  - `project.md` "Worker hard limits" section, pasted into every brief after the skill's hard
    limits, so project rules never need a forked copy of the skill.
  - Atomic asset promotion (export and import metadata together, imported at once).
  - Locking criteria on deterministic captures: a natural-variance probe pair in every before
    set, thresholds from measured noise, references never rebuilt from after pixels.
  - Deterministic capture recipe, one-off engine refresh after class or asset changes, run caps
    stated as numbers in every brief.
  - Includes the routing by current chunk complexity across Codex and Claude, which shipped
    without a version bump after 1.1.0.
- **1.1.0** Coordinator main-session agent and delegation check.

## License

MIT, see `LICENSE`.
