# project.md (template): fill in, delete what does not apply

Save as `project.md` beside `SKILL.md`. The skill's `<placeholders>` resolve to the values here.

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

## Exclusive tool slots

| Tool | Slots | Address per slot | Launch / health check | Close rule |
|---|---|---|---|---|
| <e.g. art app> | <N> | <ports/profiles> | <commands> | <save check first> |

Shared single-owner sources: <files>

## Knowledge base (optional)

<skill or vault name, lookup and update commands, page names for decision log and status>

## Opt-in policies (delete what you do not want)

- Autonomy: user granted; never ask questions during a goal; decide, record, self-judge.
- Pre-release: no back-compat migrations, adapters or legacy tests; reject incompatible data clearly.
- Performance last: no audits or optimisation until the final step; fix concrete defects only.
- Art style rules: <style, references, what to avoid>
- Protected design decisions: <list; changes need explicit user approval>

## Standing user rules

<short list of the user's durable rules that every brief must carry>

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
- Exports: glTF 2.0 binary, metric units, origins at gameplay pivots, transforms applied.
