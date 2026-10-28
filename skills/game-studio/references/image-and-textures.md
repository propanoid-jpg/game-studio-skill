# Image and texture generation (local)

Sketches, concept art, sprites and seamless PBR textures, generated locally on the
shared pipeline in [asset-pipeline.md](asset-pipeline.md). Licence rules in
[licences.md](licences.md) govern every engine here; engine choices below are dated
defaults (Oct 2026), re-verified at download time. Values in `<placeholders>` come
from `project.md`.

## 1. Engines — one primary per task

| Job | Engine (default) | Licence status | Notes |
|---|---|---|---|
| Draft / sketch / fast concept | Z-Image-Turbo | `cleared` (Apache 2.0) | Distilled; locked sampler below |
| Refine / edit / multi-reference | FLUX.2 [klein] 4B | `cleared` (Apache 2.0) | Change described in sentences |
| Stylised / LoRA / ControlNet | One SDXL checkpoint | `cleared-conditional` (OpenRAIL; check the exact checkpoint) | Tag prompts, real negatives |
| Texture → PBR expansion | Ubisoft CHORD nodes | `cleared` when the base texture is cleared | BaseColor in, material maps out |
| Optional maximum quality | One large Apache-licensed image model from `project.md` | Per `project.md` | One image at a time, free memory around it |

- **Substitution rules.** No silent substitution of architecture, checkpoint or
  engine family, ever. A substitute is allowed only when: the primary is missing or
  has failed under the failure rules in [asset-pipeline.md](asset-pipeline.md), the
  substitute is allowlisted in `project.md` for the same job, its licence status is
  recorded, and the handoff names the swap and why. Within a family, a quantised
  build (for example FP8 instead of BF16) of the same model is a size decision, not
  a substitution, and is recorded in the manifest.
- **Banned for shipped assets:** non-commercial dev-tier variants of otherwise
  cleared families. A family being partly cleared does not clear its dev variants;
  classify the exact file (see [licences.md](licences.md), section 2). Prototype-only
  use of a banned variant requires the user's explicit word in that turn and the
  `prototype_only` manifest flag.
- Model placement follows the backend's model folders by type (diffusion models,
  text encoders, VAEs, checkpoints, ControlNet models). At download time use the file
  list from the official workflow template or model repository; verify sizes and
  record file names in the setup state file.

## 2. Locked settings per architecture

Sampler settings are architecture properties. Carrying settings across architectures
is the most common silent quality failure in this pipeline.

- **Z-Image-Turbo (distilled):** steps 8 (range 6–9), cfg 1.0, euler, simple
  schedule, native size up to `<draft_max_size>` (1024×1024 class). **cfg above ~1
  destroys output on a distilled model** — never raise it to fix a weak image. No
  negative-prompt lists; write sentence prompts. ControlNet via its union model
  (canny, HED, depth, pose, line as available).
- **FLUX.2 [klein] 4B (refine/edit):** few-step generation (~4 steps per its
  template), sentence prompts describing the desired end state or the change.
  Negative prompts are largely ignored; do not spend iterations tuning them.
- **SDXL:** ~20 steps, cfg 5–7, 1024×1024 native, tag-style prompts with weights
  where needed, and a real negative prompt. This is the LoRA and ControlNet route:
  Lineart, Canny and Depth ControlNet models at minimum in `project.md` if the
  project uses sketch-to-art.
- Record the full settings block in the manifest for every approved asset. A result
  that cannot be reproduced from its manifest is not an approved asset.

## 3. Node packs (baseline)

Install through the backend's manager, verify each in the node list, and record
versions in the setup state file (setup rules in [asset-pipeline.md](asset-pipeline.md)):

- Seamless tiling pack (seamless tile + circular VAE decode) — mandatory for textures.
- CHORD nodes — PBR estimation from a single base image.
- ControlNet preprocessors (lineart / canny / depth / pose).
- IP-Adapter — style and subject reference guidance for refine work.

A project that does not use a pack omits it in `project.md`; a missing pack that a
workflow needs is a named stop, not a rebuild of the workflow.

## 4. Prompting

- One prompt, one asset. Order: subject, action or pose, environment, explicit view
  (`side view`, `top-down orthographic`, `isometric`, `turnaround front side back`),
  style anchor, lighting, palette.
- State the background: `isolated on plain white background` for props and sprites,
  `full-bleed environment` for concepts. Add `no text, no watermark, no UI` unless
  text is the asset.
- Match the prompt dialect to the architecture (section 2): sentences for the
  distilled and refine engines, tags plus weights for SDXL.
- Append the project's style anchor verbatim when it holds approved content
  ([asset-pipeline.md](asset-pipeline.md), section 6). Change one variable at a time
  between variants of an approved draft.

## 5. Pipelines

Choose the access route per task as in [asset-pipeline.md](asset-pipeline.md),
section 2: interactive drafting through MCP; batches, variant grids and sweeps
through the reusable REST batch script, with the exported workflow JSON per pipeline
below.

### Sketch

- Text-to-sketch in batches of 4 on the draft engine (or SDXL with a sketch LoRA
  where the project has one). A sketch request gets a sketch: monochrome line art,
  construction lines acceptable — never a coloured render presented as a sketch.
- Hand sketch to art: load the drawing, guide with Lineart ControlNet on SDXL
  (strength 0.7–0.9 faithful, 0.4–0.6 loose) or HED/Canny on the draft engine.
  Preserve the user's composition; guidance strength is the only looseness control.

### Concept

1. Draft batch of 4–8 on the draft engine.
2. View all of them. Show the user the viable ones with their seeds.
3. Refine only the **one approved draft**: img2img or IP-Adapter refine on the
   refine engine, denoise 0.35–0.55.
4. Upscale 2× only after approval. Upscaling an unapproved draft is wasted GPU time
   and is not done.

### Texture (seamless is a verified property, not a prompt hope)

- Prompt must include, in substance: `seamless tiling texture, orthographic
  top-down, flat even lighting, no shadows, no perspective, no objects, full-frame
  material`, plus the material's microstructure in concrete words.
- Seamless Tile node and Circular VAE Decode are mandatory in the workflow; a
  texture workflow without them is not a texture workflow.
- Verify before delivery: tile the output 2×2 and view it. A visible seam is a
  fail: regenerate once with a different seed; a second fail is recorded as failed
  with the 2×2 image path in the report. Never deliver an unverified texture as
  seamless.

### PBR expansion (CHORD)

- Input: one verified seamless base texture (BaseColor). CHORD estimates Normal,
  Height, Roughness and Metalness.
- Default map size 1024; upscale the set to 2K for standard shipping surfaces, 4K
  only for hero surfaces named in the brief.
- Naming: `<slug>_basecolor`, `<slug>_normal`, `<slug>_height`, `<slug>_roughness`,
  `<slug>_metalness`. The set ships together or not at all; a partial PBR set is a
  finding, not a delivery.
- Sanity-view the Normal and Roughness maps. Inverted-looking normals or a uniformly
  flat roughness on a varied material means re-run or flag, not ship.

## 6. VRAM budgeting

- Draft engine: the cheap tier; batches are fine within `<batch_cap>`.
- Refine engine and SDXL with ControlNet: mid tier; free memory before a run after
  heavy work, batch one for refine iterations.
- PBR expansion: run per texture, after the base is verified — never expand a batch
  of unverified bases.
- Optional maximum-quality model, if the project allowlists one: one image at a
  time, free memory before and after, never inside a sweep.
- General OOM and sequencing rules: [asset-pipeline.md](asset-pipeline.md), section 5.

## 7. Output contract

Shared contract in [asset-pipeline.md](asset-pipeline.md), section 6, plus:

- Root: `<generated_dir>/<type>/<slug>/`, type ∈ `sketch | concept | texture |
  sprite`.
- PBR maps use the suffixes in section 5; the base texture's manifest lists the full
  map set and the CHORD workflow used.
- Report: viewed images, paths, seeds, one recommended variant with a one-line
  reason. Sketch, concept and texture test generations after setup follow the pass
  criteria of their pipelines above (right type, viewed, texture tiles clean).

## 8. Failures specific to this pipeline

- Bad anatomy or composition: change seed or model tier within the same job's
  allowlist. Do not pile on adjectives, and do not raise cfg on a distilled engine.
- A draft that only works at settings outside section 2 is a finding about the
  workflow, not a new house style; record it and route it to the coordinator.
- Background removal for downstream use (3D inputs, sprites) uses the project's
  approved removal step and is recorded in the manifest; see the input-prep rules in
  [models-3d.md](models-3d.md) when the image feeds 3D generation.
