# game-studio plugin for Claude Code and Codex

A Claude Code plugin that turns one main session (the **coordinator**) and many fresh **workers**
into a small game studio. It is engine- and art-pipeline-agnostic. It bundles:

- a **coordinator agent** that runs as the main session: it plans, briefs, launches workers,
  reviews, decides and records, and delegates every task that changes files, produces content,
  researches or looks things up, however small;
- the `game-studio` **skill**: roles, model choice by task difficulty, worker briefs, handoffs, the
  coordinator review loop, parallelism caps and exclusive-tool slots (for example several art-app
  instances, one owner per instance and file), shared-tree hygiene, development, QA (layers, triage
  S0-S3), visual and release workflows, pause/resume;
- **local generation pipelines**: one ComfyUI/GPU slot for images, seamless textures and PBR sets,
  image-to-3D models, and music, SFX, ambience and voice — driven interactively over MCP or in
  batches by a reusable REST script, with a licence gate before any download or generation and a
  licence/provenance manifest travelling with every generated asset;
- **design guides** as skill references: audio design (audit, coverage matrix, nine-slot skill
  anatomy), skill animation and VFX identity (fingerprints and the distance rule), boss encounters
  (movement portfolio, attack coverage, adds law) and the fun profile (moment targets, playtests);
- **role agents**, so workers launch as named studio roles instead of a general-purpose agent;
- **coordinator commands** for briefs, reviews, pause, resume, asset setup and vault setup;
- **knowledge vault**: an Obsidian vault built by a one-time sweep of all project docs, then maintained by incremental sync, with a query-first rule for every worker and a deterministic lint script for dead links, orphans, index drift and source-hash drift (adapted llm-wiki method, no external plugin);
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

### Codex installation

From a persistent clone of this repository (Python 3.11+):

```text
python scripts/codex_adapter.py install --project /absolute/path/to/game
```

This installs 14 native Codex worker roles, discoverable skill pointers and coordinator instructions
into the target project. Fill the generated studio project file, restart Codex, and verify role
discovery. Re-run installation after updating or moving the clone. Existing project instructions
are preserved; global Codex settings and permissions are not changed.

See [the Codex adapter reference](skills/game-studio/references/codex.md) for launch requests,
model routing, resource preflight, exclusive-tool leases and runtime limits. Sessions without
named-agent spawning use self-contained role briefs. Claude hooks and tool allowlists do not
automatically apply in Codex; the adapter documents which checks are explicit and advisory.

## What's inside

```text
.claude-plugin/plugin.json        manifest and options (userConfig)
.claude-plugin/marketplace.json   this repo is also its own marketplace
skills/game-studio/               the operating manual (SKILL.md, references/, templates/, project.example.md)
skills/studio-brief/              /game-studio:studio-brief <role> <task>
skills/studio-review/             /game-studio:studio-review <handoff>
skills/studio-pause/              /game-studio:studio-pause [reason]
skills/studio-resume/             /game-studio:studio-resume [stream ...]
skills/studio-setup-assets/       /game-studio:studio-setup-assets — gated, resumable local pipeline setup
skills/studio-setup-wiki/         /game-studio:studio-setup-wiki — gated, resumable one-time vault sweep, then incremental sync
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

**Main session model.** Run the coordinator on the strongest tier (`opus` in Claude, Sol in
Codex). Its briefs and reviews set the ceiling for every worker, so the mid tier is a false
saving; the top tier is wasted on its many routine turns (accept, record, launch). For the rare
hard management problem (scoping a release, splitting a large goal, a stream that keeps failing
review) the coordinator briefs a top-tier worker to write the plan and then executes it.

**Sessions.** Use one main session per goal or release. All state lives in files (the queue doc,
the decision log, `project.md`, handoffs, the coordinator's memory), so a fresh session loses
nothing, while a long one re-reads its whole history on every turn and drifts after
compactions. At a goal boundary, or once a session has been compacted, let the running workers
return (or run `/game-studio:studio-pause`), start a new session and run
`/game-studio:studio-resume`. The session-start hook reminds the coordinator of this after each
compaction.

### Agents

Launch workers with the Agent tool as `subagent_type: "game-studio:<agent>"` (or mention
`@agent-game-studio:<agent>`). Only the coordinator preloads the `game-studio` skill; every worker agent carries the hard worker
rules (targeted tests only, resource caps, off-screen windows, never kill processes it did not
start, keep the shared tree parseable, judge like a player, sketch-first visual workflow), writes a
handoff, never talks to the user and has no Agent tool, so it cannot launch sub-agents. A `model`
passed at launch overrides the default below.

Role defaults are hints: route each current chunk by complexity. Once complex design is settled, repeated validation moves to a fresh mid-tier chunk; fixed named-test runs may use the cheapest. The top tier (`fable` in Claude) is for the hardest chunks only. See the skill routing policy.

### Runtime model mapping

Choose the launch API and model for the active runtime. Keep the coordinator on its current session model.

| Task tier | Codex model | Claude model |
|---|---|---|
| Light / cheapest | `gpt-6-luna` | `haiku` |
| Medium / mid | `gpt-5.6-terra` | `sonnet` |
| Complex / strongest | `gpt-6.1-sol` | `opus` |
| Hardest / top | `gpt-6-astra` | `fable` |

In Claude, launch `game-studio:<role>` with the Agent tool and pass the Claude model. The `model`
frontmatter in `agents/*.md` is Claude-specific. In Codex, use `collaboration.spawn_agent` with
`task_name`, a self-contained role brief in `message`, and the Codex `model`. Set `fork_turns: "none"`
when overriding the model; `"all"` full-history forks inherit the
coordinator's model. Codex does not accept `subagent_type` or Claude role-agent identifiers.
Read the relevant role instructions into the brief; a Claude plugin installation does not register
role agents in Codex. Never pass `haiku`, `sonnet` or `opus` as a Codex model.

| Agent | Role | Model |
|---|---|---|
| `feature-dev` | One scoped feature or system change | sonnet (pass opus for unknown-cause debugging) |
| `ui-dev` | Interface change against a sketch and locked criteria | sonnet |
| `art-owner` | Live art-tool work on one exclusive slot; several may run in parallel | opus |
| `asset-gen` | Image, texture/PBR and 3D generation on the single ComfyUI/GPU slot | opus |
| `audio-gen` | Music, SFX, ambience and voice generation on the single ComfyUI/GPU slot | opus |
| `prep` | Captures, sketches, locked criteria, specs so exclusive tools never wait | sonnet |
| `integration` | Seed sweeps, fallbacks, campaigns, comparison near-misses | sonnet |
| `qa` | Test sweeps (only when the user asks), stale and flaky tests | sonnet |
| `balance` | Probes, tuning, before/after tables | opus |
| `visual-review` | Live-play readability review and presentation polish | opus |
| `knowledge-keeper` | Vault setup, sync, compile and lint | haiku |
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
  worker, reminds it to fill the remaining free slots with independent queue items.
- **UserPromptSubmit:** when a background worker reports back to the main session, reminds the
  coordinator to review the handoff with the checklist, clean up, refill every free slot and
  relaunch stalled workers. Silent on typed prompts and outside studio projects. (A SubagentStop
  hook is deliberately not used: its context goes to the finishing worker.)
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
4. A runtime using the manual without an adapter reads the same skill files from the
   marketplace clone, `~/.claude/plugins/marketplaces/game-studio/skills/game-studio/`, which
   `claude plugin marketplace update game-studio` keeps current.
5. The `art-owner` agent grants `mcp__blender__*`. For another art tool or server name, copy
   `agents/art-owner.md` into `<project>/.claude/agents/`, give it a new `name`, and edit `tools`.
   Any other role can be overridden the same way. The generation agents (`asset-gen`, `audio-gen`)
   grant `mcp__comfyui__*` the same way; the server name is set in `project.md`.

## Example

> "Plan the inventory rework and start the first tasks."

The coordinator (the main session) reads `project.md` and the queue, splits tasks by file
ownership, writes one brief per task with `/game-studio:studio-brief`, launches `game-studio:feature-dev` and
`game-studio:ui-dev` workers, and reviews each `handoff.txt` with `/game-studio:studio-review`
before recording acceptance and launching the next task.

## Changelog

- **1.7.0** (token efficiency, from an analysis of 2,046 worker runs)
  - Workers no longer preload the skill and lose the Skill and Monitor tools: a smaller prompt on
    every call. Briefs for role agents paste only the project's "Worker hard limits" and name the
    skill directory.
  - Wait rule replaced: blocking chunks of at most 270 s on a done-condition (the prompt cache
    lives 5 minutes); idle waits only beyond about 45 minutes. The shell hook warns on long bare
    sleeps and idle echoes.
  - New worker rules: batch independent lookups in one message, keep run output in log files,
    an image budget, and a budget of about 80 tool calls with a PARTIAL handoff beyond it.
  - Routing: a model above the role default needs a reason in the brief; surveyor and
    knowledge-keeper run at low effort.
  - Coordinator: one queue Edit per review, vault updates batched through a "Vault pending" list,
    a fresh session at the first compaction, and a session-start warning when the project
    instruction file exceeds 10 KB.

- **1.6.0** (fixes from a month of real studio sessions)
  - Codex tiers are now Luna, Terra, Sol, Astra (cheapest to top); Sol and Astra each moved up one tier.
  - Top model tier: `fable` in Claude and `gpt-6-astra` in Codex, for the hardest chunks only (a documented strongest-tier
    failure, or foundational design many workers build on). No role defaults to it.
  - Claude-facing text names tiers, not Codex models; the coordinator prompt no longer opens with
    Codex instructions.
  - Engine-cap hook counts one Windows engine run once (skips the `_console` launcher).
  - Queue starvation and stalls: new worker-return hook (review, refill every free slot, stall
    check), launch-time reminder to fill remaining slots, `<stall_minutes>` in `project.md`.
  - Worker rules: stop only recorded process IDs, own runs until they exit, wait without polling,
    start the handoff early, "all" means all with exclusions listed.
  - The queue doc holds open work only: accepted items are deleted, not annotated.
  - Main-session guidance: strongest tier for the coordinator, one session per goal, and a
    reminder after each compaction to move to a fresh session at the next quiet point.

- **1.5.0**
  - Knowledge vault: absorbed llm-wiki method (MIT, attributed) as `references/knowledge-vault.md`
    with no external plugin dependency — Obsidian layout, query-first enforcement in the core
    skill, worker rules, brief and review templates, and the knowledge-keeper role.
  - New command `studio-setup-wiki`: phased, resumable, gated one-time sweep of all in-scope
    docs, external-source ingest to immutable `raw/`, compile to cross-linked wiki pages with
    source-path and source-hash frontmatter, lint and smoke-query proof, then incremental sync.
  - New deterministic `scripts/wiki-lint.py` (stdlib only) and tests: dead links, orphans,
    index drift, stale pages, missing gaps sections, contradiction warnings and source-hash
    drift, with `--fix` for stubs and missing sections. Repo docs are never copied into `raw/`;
    qmd is used only if already installed, never installed; vault git commits only if the
    vault is already tracked; workers never delete a vault.
  - Codex adapter now installs 7 skill pointers (game-studio plus six commands); worker count
    stays at 14.

- **1.4.0**
  - Local generation pipelines: ComfyUI topology with a single GPU slot, MCP and reusable REST
    batch routes, licence gating (`licences.md`) and a mandatory per-asset manifest; references
    for image/textures, 3D models and audio generation, plus the gated, resumable
    `studio-setup-assets` setup command and templates for manifests and audits.
  - Two new worker roles, `asset-gen` and `audio-gen` (14 Codex worker roles in total).
  - Design guides as references: audio design, skill animation identity, boss encounters and
    the fun profile, wired into the QA layers, the art workflow and release readiness
    (licence manifest audit).
  - Contradiction fixes: the lean-workflow ban on provenance manifests now excepts the
    generated-asset manifest; authorised generation batches are production work, not test
    sweeps; ComfyUI jobs are bounded by the slot lease and `<batch_cap>`, not engine-run caps.

- **1.3.0**
  - Codex project adapter: 12 native worker roles, skill discovery and coordinator activation.
  - Self-contained spawn-request composer with Luna/Sol/Astra routing and correct fork modes.
  - Resource preflight and atomic exclusive-tool/shared-source leases.
  - Documented runtime permissions, hook and concurrency limits; installer and lease regression checks.

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
