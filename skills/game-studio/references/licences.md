# Licence rules for generated assets

This file is the single licence source for every generation pipeline in this skill:
[asset-pipeline.md](asset-pipeline.md), [image-and-textures.md](image-and-textures.md),
[models-3d.md](models-3d.md) and [audio-generation.md](audio-generation.md). If another
reference, a tutorial, a model card summary or a worker's memory disagrees with this file,
stop and re-check the primary licence text. Do not resolve a conflict by picking the more
permissive reading.

Licence facts change. The model choices named in the pipeline references are dated
defaults (checked Oct 2026). A dated default is a starting point, not a clearance:
re-verify the licence at download time and again before a release that ships the asset.

## 1. The allowlist pattern

- Generation for shipped assets uses **allowlisted engines only**. An engine is
  allowlisted for a project when `project.md` records, per engine: name and version,
  model files, licence name, licence status (see section 2), any conditions, the date
  checked and the source (licence text or official model card, not a blog summary).
- Anything not on the project's allowlist is not used for shipped assets, however
  convenient, however good the output, and however many tutorials recommend it.
- Adding an engine to the allowlist is a coordinator decision recorded in `project.md`.
  A worker who wants a new engine files a finding with the licence text attached; the
  worker does not self-allowlist by downloading it.
- One engine per job, no silent substitution. If the allowlisted engine is missing,
  broken or out of VRAM, stop and name the exact engine and problem. Never fall back to
  a different architecture, a cloud API or a partner node without explicit approval in
  that turn.
- Cloud generation services and paid partner nodes are out of scope for the local
  pipelines by default. Proposing one as a fallback for a failed local step is a
  finding for the coordinator, not a workaround.

## 2. Licence statuses

Every engine, model file and asset carries exactly one status. The status goes in the
manifest (see [asset-pipeline.md](asset-pipeline.md), output contract) and is never
omitted, guessed or upgraded silently.

| Status | Meaning | May ship? |
|---|---|---|
| `cleared` | Licence permits commercial use in the shipped product, conditions met and recorded | Yes |
| `cleared-conditional` | Commercial use permitted only while a stated condition holds (revenue threshold, attribution, territory, rights to input material) | Yes, while the condition holds; re-check before release |
| `gated` | Weights or access sit behind a licence the user must accept personally (section 4) | Not until the gate completes, then re-classify |
| `prototype-only` | Licence is non-commercial, research-only or otherwise excludes shipped use | Never. Flag, contain, replace before shipping |
| `banned` | Licence excludes the project's territory or use, or terms are research-only / void for this project | Never install or use |

- A model family is not a status. Different variants, sizes and checkpoints of one
  family routinely carry different licences. Classify the exact file used.
- Code licence and weights licence are separate. Permissive code does not clear
  non-commercial weights, and permissive weights do not clear a non-commercial
  dependency in the pipeline that produced them. Check every layer that touches the
  output: model, encoder, VAE, custom node pack, post tool.
- Conditions travel with the asset. If an engine is `cleared-conditional`, its
  condition is written in the asset manifest, not only in `project.md`.

## 3. Jurisdiction check (duty, not a footnote)

- Some licences exclude territories by name. Before allowlisting any engine, read the
  licence text for territory, field-of-use and entity restrictions, and check them
  against the project's location and distribution territories in `project.md`
  (`<project_territories>`).
- A licence that does not apply in a project territory makes the engine `banned` for
  that project, even if it is popular, preinstalled in templates, or cleared for other
  projects. Record the excluding clause as the reason.
- Distribution widens the check. An engine cleared for the developer's territory is
  re-checked when the game ships into a new territory, sells through a new storefront
  or is localised under a different publisher.
- When in doubt, treat the engine as not cleared and ask. A delayed asset is
  recoverable; a shipped asset under a void licence is not.

### Worked example: a rejected engine

An image-to-3D family with wide tutorial coverage was rejected during the Oct 2026
review, before any install:

- Its community licence stated it did not apply in several named territories,
  including major European markets. For a project based and selling there, use would
  have been unauthorised regardless of the model's quality or fit.
- It was therefore recorded `banned` with the clause as evidence, and the pipeline
  standardised on a permissively licensed engine available natively in the generation
  backend instead (see [models-3d.md](models-3d.md)).
- Lesson, applied generally: check territory clauses **before** comparing quality,
  speed or VRAM. Popularity is not evidence of licence fitness.

## 4. The USER GATE pattern (gated models)

Some useful models are distributed behind a licence click-through on the model host.
That acceptance is personal. No agent accepts it on the user's behalf.

1. Coordinator records the engine as `gated` in `project.md`, with the licence name,
   the condition in plain words (for example a revenue ceiling for free commercial
   use) and the page the user must open.
2. Brief a worker to prepare everything else — folders, workflow, post steps — and to
   stop at the gate. Other pipelines proceed; a gate never blocks unrelated work.
3. The worker tells the user, in one message: which page to open, that they must log
   in and accept the licence themselves, the condition in plain words, and to say
   "done" when access is granted. No stored, shared or borrowed credential is used to
   bypass the gate.
4. After the user's word: download or place files per the official template, verify
   each file by size, record file names and sizes, and re-classify the engine
   (`cleared` or `cleared-conditional`, with the condition written out).
5. If the user declines or does not answer, record the engine `skipped by user` for
   that project and finish without it. A gated engine is never required for setup
   completion unless `project.md` says so explicitly.

## 5. Truth in labelling

- **Draft is not production.** Raw generator output is a draft until it passes the
  pipeline's post contract and verification, and its licence status is `cleared` or
  `cleared-conditional`. Call it a draft in folders, manifests and handoffs.
- Never upgrade a label to make a handoff look complete: an unviewed render, an
  unchecked loop, an unmeasured loudness value and an unverified tile are not done,
  whatever the file looks or sounds like.
- `prototype-only` output is labelled in its manifest (`prototype_only: true`),
  stored outside the shippable asset folders where the pipeline defines them, and
  never promoted. Its legitimate uses are timing, composition and feasibility
  references that a cleared pipeline then replaces.
- If an asset's engine is later re-classified (licence change, condition breached,
  territory added), every asset from that engine inherits the new status until
  re-checked. List affected assets as a finding; do not leave them labelled cleared.
- A manifest without a licence field is incomplete. See the shared output contract in
  [asset-pipeline.md](asset-pipeline.md).

## 6. Input rights (the licence of what goes in)

Output clearance does not cure bad inputs.

- **Voice reference audio:** clone or imitate a voice only with proven rights — the
  user's own voice, a recording made for the project by a consenting performer, or a
  licensed voice pack. Never clone a public person's voice, a performer's voice from
  a film or game, or any sample whose provenance is unclear. Unclear provenance means
  stop and ask; there is no prototype waiver. Detail in
  [audio-generation.md](audio-generation.md).
- **Image and 3D inputs:** use project-owned, generated or licensed reference images.
  A scraped or third-party artwork input is a finding, not an input.
- **Prompts and lyrics:** do not instruct an engine to reproduce a living artist's
  protected work verbatim as a shipped asset. Style direction in the project's own
  words is the project's decision, recorded in `project.md`.
- Keep the input next to the output (the pipeline references state the per-type rule)
  so provenance can be audited later from the manifest alone.

## 7. Per-pipeline summary (Oct 2026 defaults)

Detail and operating rules live in the pipeline references. This table is an index,
not a substitute for re-checking at download time.

| Pipeline | Cleared / conditional | Prototype-only | Banned examples |
|---|---|---|---|
| Image | Z-Image-Turbo, FLUX.2 [klein] 4B (Apache 2.0); SDXL checkpoint (OpenRAIL, per-checkpoint check) | — | Non-commercial dev-tier image models for shipped assets |
| Texture / PBR | CHORD expansion from a cleared base texture | — | Any expansion of a prototype-only base |
| 3D | Pixal3D, TRELLIS.2, TripoSR (MIT) | — | Territory-excluded 3D families (section 3); cloud 3D services by default |
| 3D drafts | Stable Fast 3D (`gated`; community licence, revenue condition) | — | As above |
| Music | ACE-Step 1.5 (MIT / Apache 2.0) | — | Cloud music services by default |
| Voice | Kokoro (Apache 2.0); Chatterbox (MIT, input-rights condition) | — | Non-commercial TTS weights for shipped lines |
| SFX / ambience | Stable Audio 3 Small/Medium (`gated`; community licence, revenue condition) | Video-foley checkpoints under non-commercial terms | Research-only / territory-excluded audio models |

## 8. Download-time checklist (every engine, every install)

1. Open the official template or model repository file listing at download time. Use
   the files named there; do not guess file names from memory or from this file.
2. Open and read the licence text itself. Record status, conditions and territory
   check in `project.md` before the download starts (section 4 if gated).
3. Check the download size expectation in `project.md` (`<download_budget>`) and free
   disk (`<min_free_disk>`). A download that would exceed the budget is a gated stop.
4. After download, verify every file by size. A multi-GB model arriving as a few KB
   of HTML is a failed download: redo it once, then report the exact error.
5. Record file name, size, licence status and date in the setup state file (see
   [asset-pipeline.md](asset-pipeline.md), setup).
