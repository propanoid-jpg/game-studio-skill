# 3D model generation (local, image-to-3D)

Single-image-to-3D generation plus a scripted game-ready post pass, on the shared
pipeline in [asset-pipeline.md](asset-pipeline.md). Licence rules in
[licences.md](licences.md) govern every engine; choices below are dated defaults
(Oct 2026), re-verified at download time. Values in `<placeholders>` come from
`project.md`.

## 1. Honest constraints — state them before promising anything

- Generator output is a high-poly, messy triangle mesh with generated UVs and
  textures. It is a sculpt / blockout, **not** a finished asset. Any claim of
  production-ready output straight from the generator is false; the post contract in
  section 5 exists because of this.
- Static props, items, architecture and vegetation: this pipeline can take them to
  game-ready automatically through post.
- Characters and anything that must deform (rigging, facial animation, cloth): the
  generated topology is not suitable. Deliver as static posed meshes flagged
  `needs_manual_retopo: true`, or as blockout for a modeller. Never promise a
  rig-ready character from this pipeline.
- One input image means the generator invents the unseen sides. Back and occluded
  views are approximations; the render check in section 6 must include them, and
  inventions are flagged, never hidden by showing only the input-side view.

## 2. Engines — fixed choices, no substitutions

| Job | Engine (default) | Licence status | Notes |
|---|---|---|---|
| Textured 3D, default | Pixal3D | `cleared` (MIT) | Pixel-aligned to the input view; best fidelity to an approved concept image |
| Textured 3D, fallback | TRELLIS.2 | `cleared` (MIT, ComfyUI-native route only) | Use when the default drifts from the input silhouette, or for hollow / complex structures |
| Fast shape draft | TripoSR | `cleared` (MIT) | Sub-second class, untextured, vertex colours only |
| Fast textured draft | Stable Fast 3D (SF3D) | `gated` — USER GATE, [licences.md](licences.md) section 4 | Community licence with a revenue condition; optional, never required |

- Use **only the backend-native route** for Pixal3D / TRELLIS.2 (official templates
  and core nodes). The native implementation is part of the licence clearance: a
  third-party pipeline build can reintroduce dependencies the native route avoids.
  Do not hand-assemble model files from third-party repositories; the official
  template's file list is the source of truth.
- **Substitution rules.** No substitution beyond the default/fallback pair above
  without a coordinator decision recorded in `project.md`. Cloud 3D services and
  partner/API 3D nodes are out of scope and are never proposed as a fallback for a
  failed local run. Territory-excluded engine families are `banned` (see the worked
  example in [licences.md](licences.md), section 3) — do not install them even when
  tutorials push them.
- TripoSR output is a shape check only. Never texture it up and call it an asset;
  if the user promotes a TripoSR shape, it goes through the full textured route and
  section 5 like any other asset.
- SF3D, when the gate completes: its licence condition is written into every SF3D
  asset's manifest. When the gate is declined or unanswered, the pipeline is
  complete without it.

## 3. Access route

Per [asset-pipeline.md](asset-pipeline.md), section 2: interactive single-asset
generation through MCP; repeated generation over a list of approved inputs
(prop sets, variant inputs) through the reusable REST batch script, which queues
the exported image-to-3D workflow per input, injects the input path and resolution,
polls to completion and copies the GLB into the asset folder with its manifest.
3D runs are heavy-tier: one at a time, never in parallel with image or audio
generation on the same GPU.

## 4. Input preparation (mandatory before every generation)

Input quality is the largest quality lever — larger than any sampler setting.

1. Source: an approved concept/prop image from the image pipeline
   ([image-and-textures.md](image-and-textures.md)) or a user-supplied image with
   provenance recorded. One object per image.
2. Compose: object centred, filling ~80% of frame, not cropped. A 3/4 view is
   preferred for props — a pure front view starves depth, extreme angles distort.
3. Background removal with the project's approved removal step: object on
   transparency or a plain background. Busy backgrounds leak into geometry.
4. Square canvas, ≥1024×1024 where the source allows. Save the prepared input next
   to the output as `<slug>_input.png`.
5. Known weak classes — characters intended for rigging, thin structures (chains,
   wires, foliage cards), transparent or mirror objects: warn the user **before**
   generating, every time, and expect manual cleanup. The warning is part of the
   brief's acceptance, not a post-hoc excuse.

## 5. Post contract — game-ready means post output

Raw output goes to the generated tier and is labelled DRAFT. Only post output may
be called game-ready. Post is one reusable scripted tool in the project
(`<mesh_prep_tool>`, headless DCC scripting — for example a Blender Python script),
parameterised by input file, output folder and asset class. Write it once, reuse it
for every asset; a per-asset hand cleanup in a GUI session is not the contract.

The tool performs, in order, and logs each step:

1. **Import and report:** raw triangle count, dimensions, material and texture sizes.
2. **Fix:** apply transforms; set real-world scale (1 unit = 1 m; target size per
   class or explicit size argument); merge by distance; delete loose/floating
   geometry and tiny disconnected islands (under ~0.1% of volume); fill small holes;
   recalculate normals; make manifold where achievable. Report what was removed.
3. **Budget pass:** decimate (planar for hard-surface, collapse for organic) or
   voxel-remesh plus decimate to the class budget (table below). Never remesh a
   non-manifold mesh — fix first; if still non-manifold, decimate only.
4. **UV:** keep generated UVs if they pass checks (no overlaps beyond tolerance,
   reasonable texel density); otherwise smart-project and pack. A second UV channel
   for lightmaps is the engine's import job, not post's — do not bake it here.
5. **Textures:** keep embedded PBR maps; downscale to the class texture size; name
   maps `<slug>_basecolor / _normal / _roughness / _metallic` alongside the GLB.
6. **LOD chain:** LOD0 is the budgeted mesh; LOD1 at 50% of LOD0 triangles, LOD2 at
   25%, each a decimate of LOD0, exported as separate named objects in the same
   file (engine-specific LOD grouping is the engine's import job).
7. **Collision:** one simplified mesh — convex hull of LOD2 or a decimate to
   ≤500 triangles — exported as `<slug>_collision.glb`. Never derive collision from
   the raw mesh.
8. **Export:** origin at bottom-centre, forward axis per the target engine's glTF
   convention from `project.md`, one self-contained `.glb` (textures embedded) per
   LOD set plus the collision file. Report final triangle counts per LOD.

### Budgets by asset class

| Class | LOD0 budget | Texture | Examples |
|---|---|---|---|
| `hero_prop` | 30,000 tris | 2048 | Centrepiece furniture, signature items, hero weapons |
| `prop` | 10,000 tris | 1024 | Barrels, crates, chairs, tools |
| `small_item` | 3,000 tris | 512 | Bottles, books, food, loot items |
| `background` | 1,500 tris | 512 | Rocks, distant architecture filler, vegetation |
| `character_static` | 40,000 tris | 2048 | Statues, posed blockout — always `needs_manual_retopo: true` if it will ever be rigged |

An asset that cannot reach its budget without visible silhouette damage: stop,
report the lowest acceptable count found, and let the user reclass it. Never ship
over-budget silently.

## 6. Verification — the render check

- With the DCC in headless mode, render the game-ready mesh from front, side, back
  and 3/4 at a fixed neutral setup (grey background, one key light, one fill) to
  `preview_*.png` in the asset folder, and **view all four**.
- Compare silhouette and proportions against `<slug>_input.png`. Obvious invention
  or collapse on the back or sides is flagged in the manifest and the handoff; the
  asset is not called verified.
- Shape-draft check (TripoSR): confirm the runtime class and a recognisable
  silhouette from the input. Drafts get the same honesty rule at lower depth: a
  wrong silhouette is reported as wrong, not presented as a pass.

## 7. VRAM budgeting

- This is the heavy tier. The default engines state a high-VRAM minimum class
  (e.g. a 24 GB card); treat that tier as the floor, not headroom.
- Run stages sequentially (structure → shape → texture). Before every run, free
  memory / unload models.
- Default effective resolution `1024³`. The step above (`1536³` class) is
  hero-asset-only, one at a time, after freeing memory and closing other GPU work.
- OOM: drop one resolution step and retry once. Second OOM: stop and report, per
  [asset-pipeline.md](asset-pipeline.md), section 5.

## 8. Output contract

Shared contract in [asset-pipeline.md](asset-pipeline.md), section 6, plus:

- Per asset: generated tier at `<assets3d_generated>/<slug>/` (prepared input, raw
  GLB, manifest); game-ready tier at `<assets3d_game_ready>/<slug>/` (LOD GLB,
  collision GLB, extracted PBR maps, four preview renders, manifest).
- Manifest adds: input image and its own image-manifest reference, engine and model
  files, resolution setting, seed if the engine exposes one, raw and final triangle
  counts, texture sizes, asset class, flags (`needs_manual_retopo`, back-view
  notes, SF3D licence condition where applicable).
- No manifest plus no viewed render check means not an asset, whatever the mesh
  looks like from the front.

## 9. Failures specific to this pipeline

- Broken topology after the fix pass (non-manifold, holes beyond small): take the
  decimate-only path or regenerate with a different seed or input angle.
- Two failed generations of the same object: stop, show the user the previews, and
  say plainly that the object is a manual-modelling candidate. Route it as a finding
  to the art queue; do not keep spending GPU time on it.
- Silhouette drift from the approved input on the default engine: that is the
  stated trigger for the fallback engine (section 2), once, with the swap recorded.
