# Local asset pipeline (ComfyUI): topology, access routes and shared contracts

The shared foundation for local generation: [image-and-textures.md](image-and-textures.md),
[models-3d.md](models-3d.md) and [audio-generation.md](audio-generation.md) all run on the
server described here and obey the contracts in this file. Licence rules are in
[licences.md](licences.md) and override anything here. Values in `<placeholders>` come
from `project.md`.

## 1. Topology and fixed rules

- Backend: one local ComfyUI server at `<comfyui_url>` (default `http://127.0.0.1:8188`),
  installed **outside** the game repository at `<comfyui_dir>`. Never vendor the server
  into the game repo.
- ComfyUI has no authentication. Bind to localhost only: never `0.0.0.0`, never expose
  the server to the LAN or the internet, never tunnel it out as a workaround.
- Hardware is project data, not an assumption: GPU and VRAM in `<gpu>` / `<gpu_vram>`,
  RAM in `project.md`. Every engine default in the pipeline references was verified on
  a consumer high-VRAM tier (e.g. a 24 GB card); a smaller card re-budgets per section 5
  before any download, it does not discover limits by crashing mid-queue.
- No cloud generation APIs and no paid partner nodes unless the user approves them
  explicitly in that specific turn. A failed local step is reported, not routed around.
- Local generation is an **exclusive-tool slot**. The GPU and the server have one owner
  at a time (see `worker-rules.md` and `roles.md`): the brief names the slot owner,
  other workers prepare inputs and criteria while they wait, and no worker launches a
  second server instance against the same GPU without a coordinator decision recorded
  in `<queue_doc>`.

## 2. Two access routes — equal standing, chosen per task

The worker chooses the route per task and records the choice in the handoff. Neither
route is a fallback for the other; both drive the same server, workflows and outputs.

### Route A: MCP server

- Use when: interactive, exploratory or single-asset work; drafting and viewing
  iterations with the coordinator or user in the loop; running a saved workflow once
  with hand-picked parameters.
- The MCP server name and registration come from `project.md` (`<comfyui_mcp_server>`).
  Before a session, confirm its tools are callable and list which server implementation
  is active; two implementations exist in the ecosystem and their tool shapes differ.
- High-level generate/view actions are preferred over hand-built node graphs when the
  server offers them. View every output through the route's view/return mechanism
  before judging it (section 7).

### Route B: reusable batch script over the REST API

- Use when: batch, repeatable or sweep work — seed lists, variant grids, per-line
  dialogue, per-asset texture sets, regeneration of a named set, anything that must
  run identically again. Batch work **prefers this route**.
- The script is a reusable project tool at `<asset_tools_dir>` (for example a single
  batch runner committed with the project tools), parameterised by arguments or a job
  file. It is not a one-off: a script written for one batch and discarded violates the
  standing lean-workflow rule. One general runner serves all pipelines; per-pipeline
  behaviour comes from the workflow JSON and the job file, not from script copies.
- The runner must implement, at minimum:
  1. **Workflow loading:** read an API-format workflow JSON exported from ComfyUI
     (section 3). Never hand-author a node graph in code when a workflow can be
     exported; never edit the exported JSON by string replacement.
  2. **Parameter injection:** parse the JSON and set named node inputs by node id /
     title from the job file — prompt, negative prompt where the architecture uses
     one, seed, steps, size or duration, input image path, output prefix. The mapping
     of job fields to nodes is declared at the top of the job file or in a small
     sidecar, so a renamed node fails loudly instead of silently generating defaults.
  3. **Queueing:** POST the workflow to the server's prompt endpoint, record the
     returned prompt id for every item, and queue items sequentially unless
     `project.md` states a safe concurrency for this GPU (default: one at a time).
  4. **Polling:** poll the server's history endpoint per prompt id with a timeout
     from `project.md` (`<generation_timeout>`). A timeout is a failure to report with
     the prompt id, not a silent skip. Handle queue-interruption and server-restart
     as failures, not as empty successes.
  5. **Output collection:** download or copy outputs from the server's output
     location / view endpoint into the asset folder (section 6), rename to the
     naming contract, and never leave the only copy inside the server's output tree.
  6. **Manifest writing:** write or update the folder `manifest.json` as items
     complete (section 6), including failures, so a long batch is auditable mid-run
     and resumable after interruption: completed items are not regenerated on resume
     unless the job file says so.
  7. **Failure and retry:** on a generation error, record the server error verbatim,
     the workflow and the parameters. Retry an out-of-memory failure once after
     freeing memory (section 5); retry no other class automatically more than once.
     A second failure stops that item, the batch continues only if the job file marks
     items independent, and the handoff lists every failed item with its error.
- Test the runner on a two-item job before trusting it with a sweep. Sweep size is
  capped by `project.md` (`<batch_cap>`); larger sweeps are split by the coordinator.

## 3. Workflows

- Workflows live in the project at `<workflows_dir>`, named by pipeline and purpose
  (for example `texture-seamless.json`). The UI-format and API-format exports are
  different files: the batch script consumes the API format. Export both when a
  workflow changes, in the same commit.
- A workflow is locked once its pipeline's test generation passes. Changing a locked
  workflow is a briefed change with a new test generation, not an in-passing tweak
  during a batch.
- Missing node or failed import inside a workflow: name the exact pack and node,
  attempt one fix (install the pack's requirements or update the backend), then
  record the exact import error and continue without that workflow if the brief
  allows. Do not rebuild a user's workflow as a workaround and do not loop on fixes.
- Session pre-flight for either route: confirm the server answers, report free and
  total VRAM, list installed models and node packs relevant to the task. A missing
  model or node is a stop that names the exact file or pack — never a silent
  substitution (see [licences.md](licences.md)).

## 4. Setup (gated, resumable)

Initial installation and later engine additions follow the same gated phases. There is
no blanket pre-authorisation to install or download.

- Maintain a setup state file in the project (`<setup_state>`, one per pipeline area
  if the project prefers). Before each phase mark it in progress; after verified
  completion mark it done **with evidence** (command output, file names and sizes,
  server URL, VRAM numbers). Resume from the first unfinished phase; never re-run a
  completed phase and never trust a done mark without its evidence line.
- Phase order, each gated by its verification: environment detection (OS, GPU and
  VRAM, runtime versions, free disk) → backend install → server start and verify
  (root/system endpoint answers, reported device matches `<gpu>`) → custom node packs
  → model downloads per pipeline → access-route connection (MCP registration and/or
  batch runner smoke test) → persisted operating brief in the project → test
  generations per pipeline.
- **Gated stops — stop and ask, every time:** administrator/root rights or a reboot
  is required; a licence click-through or account creation is demanded (apply the
  USER GATE in [licences.md](licences.md)); the engine is gated; a download would
  exceed `<download_budget>` or free disk would fall below `<min_free_disk>`; a step
  has failed twice with different approaches.
- Node packs and models are installed per the pipeline references only. Verify each
  pack appears in the server's node list and each model file by size; record both in
  the setup state file.
- Connecting the MCP route may require a full restart of the calling application.
  That restart is a phase boundary: mark the state file, tell the user in one short
  message that a restart is needed to continue setup, and resume from the state file
  in the next session by verifying the tools are callable.

## 5. VRAM and resource budgeting

- One generation at a time per GPU by default. Stages inside one engine run
  sequentially; do not run an image generation in parallel with a 3D or audio
  generation on the same server instance.
- Before every heavy run, free memory / unload models through the access route, and
  check free VRAM against the engine's stated tier in its pipeline reference.
- Budget by tier, recorded in `project.md`: draft engines are cheap and batchable;
  refine and 3D engines are the heavy tier and run singly; the largest optional
  models run one at a time with a free-memory call before and after.
- Out of memory: free memory, drop batch size to one, retry once. Second OOM: stop
  and report VRAM, model and size — do not propose a bigger GPU, a cloud GPU or CPU
  offloading as the first fix.
- Obey the shared resource rules in `worker-rules.md`: check machine load and free
  disk before launching batches, keep evidence under `<evidence_budget>`, and leave
  no orphan server or runner processes behind.

## 6. Shared output and manifest contract

Pipeline references add per-type fields; this contract is the common floor.

- Generated output goes to the pipeline's generated root from `project.md` (for
  example `<generated_dir>/<type>/<slug>/`). Never write generated output directly
  into engine source asset folders; promotion is a separate, reviewed step owned as
  in `workflow.md`.
- Naming: `<slug>_<variant>_<seed>.<ext>`, with per-type suffixes where a pipeline
  defines them (PBR maps, LODs, engine copies). The prepared input that produced an
  asset is saved beside it; provenance starts at the input.
- One `manifest.json` per asset folder: prompt (and negative where applicable),
  engine and exact model files, workflow name, sampler/settings or generation
  parameters, seed, size/duration as applicable, date, licence status and conditions
  (from [licences.md](licences.md)), post steps applied, and flags (for example
  `prototype_only`, known-weakness notes). No manifest means not final.
- A style anchor, where the project keeps one (`<style_anchor>`), is appended to
  prompts verbatim once the user has approved its content, and the manifest records
  that it was applied. Variants change one variable at a time; approved assets have
  their seed recorded before variants are made.

## 7. Verification (all pipelines)

- View, render or listen-check every output yourself before judging or reporting it,
  using the pipeline's own check: tile view for textures, multi-view renders for
  meshes, doubled-file seam and loudness measurement for loops. A numeric pass never
  replaces the check.
- Report viewed outputs with paths and seeds, one recommended variant and a one-line
  reason. Report failures with exact errors and paths; never fake a pass, relabel a
  failure as a pass, or show only the flattering view of an asset.
- Test generations after setup (per pipeline reference) must all pass or be flagged
  with exact errors before setup is reported complete.
