# Codex adapter

Use this reference when running the studio in Codex. The plugin's Claude manifest,
settings and hooks remain Claude-specific. The adapter uses the same canonical roles,
worker rules and templates; it does not require an API key or an MCP orchestration server.

## Install and update

Requires Python 3.11+ and a persistent plugin clone. Run from that clone:

```text
python scripts/codex_adapter.py install --project /absolute/path/to/game
```

This installs 12 standalone role files into the project's .codex/agents/, skill pointers into
.agents/skills/, and a managed coordinator block in AGENTS.md. Existing unrelated instructions
are preserved; unmanaged destination collisions fail before writing. Re-running updates adapter
files and its block. The installer does not edit global Codex configuration or permissions.
Generated pointers use the clone's absolute path: keep the clone available and rerun installation
after moving it or updating the plugin. Install only in projects where studio coordination is wanted.

Fill .codex/game-studio/project.md if the installer created it. An existing Claude studio project
file is reused instead. Read paths in this order: .codex/game-studio/project.md,
.claude/game-studio/project.md, .claude/skills/game-studio/project.md. Keep the queue, evidence
locations, numeric caps and worker hard limits configured before starting work.

Restart Codex and confirm discovery of game-studio-feature-dev, game-studio-surveyor and the
other roles. Standalone .codex/agents/*.toml is the current documented format. Older clients
may need an update; do not silently claim that native roles loaded. See
https://learn.chatgpt.com/docs/agent-configuration/subagents for current discovery and controls.

## Launch and review

Use a named custom role when the exposed launch API supports it. The generated names are
 game-studio-<role>, with no Claude namespace colon. Keep the coordinator's session model.
Generated profiles deliberately omit model and effort: explicit current-chunk routing must
remain effective rather than being overridden by a fixed profile model.

If the launch tool has no agent-type field, fill templates/worker-brief.md and compose its
self-contained message with the adapter:

```text
python scripts/codex_adapter.py brief --project /absolute/path/to/game --role feature-dev --tier medium --task-name inventory_logic --task-file /absolute/path/to/filled-brief.txt
```

The result is JSON for collaboration.spawn_agent: task_name, fork_turns="none", model and message.
The message embeds role instructions, canonical worker rules, project settings and the task brief.
The adapter prints a request; the coordinator invokes the available spawn tool. It does not create
agents through a shell or send messages by itself. Only "none" and "all" are supported fork modes
in this collaboration API. Choose light (gpt-6-luna), medium (gpt-6.1-sol), or complex
(gpt-6-astra) per current chunk. Check the available model list; report unavailable models rather
than substituting silently. Respect actual runtime concurrency, including the coordinator slot.

Record returned worker IDs and ownership in the queue. Use the available agent messaging, wait,
follow-up and interrupt tools to steer workers. Interrupting a turn does not necessarily free its
thread slot: consult live status and supported close controls before refilling. Workers never spawn
sub-workers or grant approval. Use templates/review-checklist.md after every handoff, inspect
images and logs, record acceptance or a new brief, then release ownership after work has stopped.
A native surveyor requests a read-only sandbox and returns its handoff in the agent reply; it
cannot persist handoff.txt. Assign a writer when the queue needs a saved copy.

## Resource checks and ownership

Before a launch, use project-configured numeric limits, bounded by the runtime's actual cap:

```text
python scripts/codex_adapter.py preflight --project /absolute/path/to/game --min-free-gib 5 --max-workers 3 --active-workers 1 --engine-process godot --max-engine-runs 10
python scripts/codex_adapter.py lease claim --project /absolute/path/to/game --resource blender-slot-1 --owner art_task_1
python scripts/codex_adapter.py lease release --project /absolute/path/to/game --resource blender-slot-1 --owner art_task_1
```

The numbers above are examples; use project values. Preflight returns a failing exit status when
a cap is reached or disk is low. Check machine load separately with available read-only tools.
Pass current live worker counts; preflight does not query the host agent registry. Engine counting
is an advisory snapshot, not an atomic reservation. Check per-worker timeouts, evidence budgets,
isolated user-data directories, and off-screen window requirements in every brief and review.

Leases use atomic directory creation and reject a second claimant. Claim every exclusive tool and
shared source before launch, using the same resource spelling across all coordinators. Use a resolved
absolute source path for file resources (case-normalized on case-insensitive filesystems). A lease
only coordinates participants using this adapter; it cannot block Blender or arbitrary file writes.
Never expire a lease automatically: after a crash, inspect live workers and unsaved work, then use
the recorded owner to release it. Temporary leases live in .codex/game-studio/locks/; exclude that
folder from version control in the target game project.

## Enforcement boundaries

Claude tool allowlists and hook events are not translated into invented Codex settings. The native
surveyor profile requests sandbox_mode="read-only"; parent runtime overrides can still affect
permissions, so confirm effective behavior. Other roles inherit current runtime permissions.
Available tools, MCP connections, approvals and sandbox controls remain host-owned. The art worker
uses only its assigned server/slot, even if other connectors are visible.

Coordinator delegation, role tool discipline, engine caps and the review loop are instructions
plus explicit checks in this adapter, not automatic PreToolUse/PostToolUse hooks. Do not advertise
Claude-level tool filtering or a hard engine cap in a brief-only runtime. If the host cannot enforce
a required restriction, report that limitation and use its supported sandbox/control options.
