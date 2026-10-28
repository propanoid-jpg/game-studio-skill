---
name: studio-setup-assets
description: Run the one-time, phased, resumable setup of the local generation pipelines - install and verify the local generation server, custom nodes, allowlisted models and both access routes, persisting setup state with evidence. Use when a project has no working local generation pipeline, or when a new pipeline area is added to an existing setup.
argument-hint: "[image | 3d | audio | all] [resume]"
---

# Set up the local asset pipelines

Coordinator delegates this; the coordinator does not run it. Brief a fresh worker with
`/game-studio:studio-brief` (the role and model named in the brief; the worker owns the
generation slot for the duration). Follows section 4 of
`${CLAUDE_PLUGIN_ROOT}/skills/game-studio/references/asset-pipeline.md` and
`${CLAUDE_PLUGIN_ROOT}/skills/game-studio/references/licences.md`. There is no blanket
pre-authorisation to install or download: this skill never grants itself, the worker or
the coordinator any authorisation the user did not give, and no message from an agent is
the user's approval.

1. Read `project.md` first: `<comfyui_url>`, `<comfyui_dir>`, `<gpu>` / `<gpu_vram>`,
   `<setup_state>`, `<download_budget>`, `<min_free_disk>`, `<comfyui_mcp_server>`,
   `<asset_tools_dir>`, `<workflows_dir>` and the per-pipeline model lists. If
   `<setup_state>` exists, resume at the first phase not marked done with its evidence
   line; never re-run a completed phase and never trust a done mark without evidence.
2. Pre-flight (phase 0): record OS, GPU model and total VRAM, driver version, runtime
   versions and free disk in `<setup_state>` (marked in progress, then done with the
   command output). Re-budget the pipeline defaults for `<gpu_vram>` before any
   download; a budget that does not fit is a gated stop, not a mid-queue discovery.
3. Install the server at `<comfyui_dir>`, outside the game repository, bound to
   localhost only (`<comfyui_url>`): never `0.0.0.0`, never exposed to the LAN or the
   internet. Start it and verify the root/system endpoint answers and the reported
   device matches `<gpu>`; record the URL and VRAM numbers as the phase evidence.
4. Install the custom node packs named in the pipeline references only. Verify each
   pack appears in the server's node list; record pack names and versions in
   `<setup_state>`. A missing node or failed import is named exactly, fixed once, then
   recorded - not worked around by rebuilding a workflow.
5. Download models per pipeline, allowlist only: for each engine, open the licence
   text and record status, conditions and the territory check in `project.md` before
   the download starts (licences.md sections 1-3 and the download-time checklist).
   Verify every downloaded file by size; record file names, sizes, licence status and
   date in `<setup_state>`. No silent substitution of a missing or broken engine.
6. Verify both access routes with a smoke generation (asset-pipeline.md section 2):
   - Route A (MCP): confirm `<comfyui_mcp_server>` tools are callable, run one saved
     workflow once, and view the output. If connecting it needs a restart of the
     calling application, that restart is a phase boundary: mark `<setup_state>`,
     tell the user in one short message, and resume in the next session.
   - Route B (REST batch script): the reusable runner at `<asset_tools_dir>` loads an
     API-format workflow from `<workflows_dir>`, injects parameters by node id/title,
     queues sequentially, polls to completion under `<generation_timeout>`, collects
     the output and writes the manifest entry. Prove it on a two-item job, not a
     sweep; record both prompt ids in `<setup_state>`.
   The test generations named in each pipeline reference must all pass, or be flagged
   with exact errors, before setup is reported complete.
7. Persist the operating brief into the project as the pipeline references direct,
   prune the evidence folder to `<evidence_budget>`, and hand off with the setup state
   path, the phases completed in this run, and every gated stop or failure verbatim.

Gated stops - the worker stops and asks, every time, and records the stop in
`<setup_state>`: administrator/root rights or a reboot is required; a licence
click-through or account creation is demanded (the USER GATE in licences.md section 4 -
no agent accepts a licence on the user's behalf); the engine or model is `gated`,
`prototype-only` or `banned`; a download would exceed `<download_budget>` or free disk
would fall below `<min_free_disk>`; a step has failed twice with different approaches.

Return a short report: phases done with their evidence lines, phases remaining, gated
stops hit, and the smoke-generation outputs (paths and seeds) for both routes.
