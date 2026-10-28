# project.md (template): fill in, delete what does not apply

Save as `<project>/.claude/game-studio/project.md` (plugin install) or as `project.md` beside
`SKILL.md` (skill copied into the project). The skill's `<placeholders>` resolve to the values here.

Plugin options (`/config`, section game-studio) mirror some of these values for the hooks and
agents: `queue_doc`, `decision_log` (the coordinator may edit both directly), `evidence_dir`,
`engine_process` (process-name substring counted by the engine-cap warning) and `max_engine_runs`
(the total cap). `enforce_delegation` (`warn` or `block`) sets what the delegation check does when
the main session writes other files. Keep them equal to the values below.

## Project

- Name: <project>
- Workspace root: <workspace_root>   Engine project root: <engine_root>
- Instruction file: <e.g. AGENTS.md or CLAUDE.md>
- Task queue doc (`<queue_doc>`): <path>   Decision log: <path or knowledge-base page>
- Evidence folder (`<evidence_dir>`): <path>/<stream>/<task>/
- Art sources (`<art_source_dir>`): <path>   Runtime assets: <path>   Release output (`<release_dir>`): <path>

## Engine and commands

- Engine and version: <engine>
- Test runner (`<test_runner>`): <command, args for split suites, headless and windowed modes>
- Timeout (`<timeout>`): <e.g. 240 s; 300 s for long captures>
- Fixed timestep flag: <flag>   Isolated user-data: <env vars/flags, absolute paths>
- Error markers to grep in logs: <strings>   Harmless known diagnostics: <strings>
- Capture tool (`<capture_tool>`) and window-size gotchas: <command, notes>
- Comparison tool (`<compare_tool>`): <command and criteria format>
- Packaging: <script, preset, checks>

## Resource caps

- Total engine runs across all workers: <N>   Per worker: <N>   Windowed overall: <N>
- Windowed runs off-screen at: <position flag>
- Load check command: <process count / CPU>
- Disk: evidence budget per task (`<evidence_budget>`): <e.g. 1 GB>   Minimum free disk
  (`<min_free_disk>`): <e.g. 100 GB>   Free-disk check command: <e.g. df -h>

## Exclusive tool slots

| Tool | Slots | Address per slot | Launch / health check | Close rule |
|---|---|---|---|---|
| <e.g. art app> | <N, e.g. 4 parallel instances> | <ports/profiles> | <commands> | <save check first> |
| ComfyUI / GPU | 1 (always exactly one) | <comfyui_url> | <health check command> | <one queue, one owner; lease named in queue doc> |

Shared single-owner sources: <files>

Art-tool MCP server name (for the `art-owner` agent's tools; default `blender`): <name>

## Asset pipelines (local generation; delete if the project does not generate)

Pipeline operating specifics live HERE, in `project.md` (the one-copy rule): do NOT create
separate per-pipeline docs in the project. The general rules are the skill references
`asset-pipeline.md`, `image-and-textures.md`, `models-3d.md`, `audio-generation.md` and
`licences.md`; setup is run by the `studio-setup-assets` command and its state file.

- GPU (`<gpu>` / `<gpu_vram>`): <e.g. model, VRAM GB>   RAM: <GB>
- ComfyUI server (`<comfyui_url>`): <http://127.0.0.1:8188 — localhost only, never exposed>
  Install root (`<comfyui_root>`): <path>   MCP server name (`<comfyui_mcp_server>`): <name>
- Model roots: <checkpoints / diffusion models / LoRA / VAE / audio model paths>
- Generated output (`<generated_dir>`): <path, e.g. art/generated/> — one folder per asset,
  each with its `manifest.json`
- Batch cap (`<batch_cap>`): <max jobs in one authorised generation batch, e.g. 32>
  Download budget (`<download_budget>`): <max GB for model downloads without asking again>
- Access routes: MCP for interactive work; a reusable REST batch script for batch work
  (both equal standing, chosen per task — see `asset-pipeline.md`)
- Licence policy: follow `references/licences.md`. Per-engine status recorded here:
  <engine/model — status `cleared` / `cleared-conditional` (condition) / `gated` / `prototype-only`, date>
  Gated engines awaiting the user's personal licence acceptance: <list or none>
- Cloud generation APIs: <off (default) / on for: ...> — no cloud image or audio APIs and no
  paid partner nodes unless the user approves in that specific turn.
- Model storage lives OUTSIDE the evidence budget: model files sit under `<comfyui_root>` and
  are not counted against `<evidence_budget>`; generated outputs and evidence still are.

## Design parameters (used by the design-guide references)

- Combat model (`<combat_model>`): <e.g. cooldowns / mana with no cooldowns / stamina — drives
  the repetition rules in `skill-animation.md` and the resource pressure in `boss-encounters.md`>
- Camera modes (`<camera_modes>`): <e.g. third person only / first + third person — every skill
  effect is authored per mode in `skill-animation.md`>
- Engine audio buses (`<engine_audio_buses>`): <bus names and loudness targets per bus — used by
  `audio-generation.md` post and `audio-design.md` mixing>

## Knowledge base (optional)

<skill or vault name, lookup and update commands, page names for decision log and status>

## Opt-in policies (delete what you do not want)

- Autonomy: user granted; never ask questions during a goal; decide, record, self-judge.
- Pre-release: no back-compat migrations, adapters or legacy tests; reject incompatible data clearly.
- Performance last: no audits or optimisation until the final step; fix concrete defects only.
- Art style rules: <style, references, what to avoid>
- Protected design decisions: <list; changes need explicit user approval>

## Worker hard limits (pasted into every brief)

<The project's own limits and the user's durable rules, as short imperative bullets with real
numbers and commands: run caps and timeout, user-data isolation, off-screen position,
exclusive-tool addresses, error markers, engine traps, the knowledge-base rule, release and
compatibility policy. The coordinator pastes this section after the "Hard limits" block of
`references/worker-rules.md`. It may tighten those limits, never loosen them. Do not copy the
skill into the project to add rules: project rules go here, general ones upstream.>

## Engine notes (worked example: Godot 4 + Blender)

- Engine project root `game/`; scripts, scenes, data, tests under it; art sources in `art_source/`,
  exported GLBs in `game/assets/models/`.
- Tests: `tools/run_tests.sh -j 4 test_a 'test_b_*'`; windowed capture tests with `-w`, serialised.
  Runs use `timeout 240`, `--fixed-fps 60`, and absolute isolated `APPDATA`/`LOCALAPPDATA` in the
  evidence folder. Windowed runs use `--position -4000,-4000`.
- Error markers: `Parse Error`, `SCRIPT ERROR`, `Failed to load script`. Harmless: the Windows
  root-certificate-store diagnostic. Exit 124/137 is a timeout.
- Relative paths are resolved from the project root when `--path` is used; use absolute paths.
- After adding or renaming a `class_name`, refresh the class cache once with an editor `--quit`
  run, otherwise headless runs fail to parse scripts using it.
- Replaced GLB textures are ignored until extracted textures and `.glb.import` are deleted and the
  project is reimported.
- Exclusive tool: Blender GUI slots, one per port (for example 9876-9879), slot A through the MCP
  tools and the others through a small socket client; ping before launch; check `bpy.data.is_dirty`
  is False before quitting a slot. Background CLI (`blender --background`) only for export and
  validation. Sources single-owner per `.blend`.
- Exports: glTF 2.0 binary, metric units, origins at gameplay pivots, transforms applied. Promote
  the GLB and its `.import` together, then import at once.
