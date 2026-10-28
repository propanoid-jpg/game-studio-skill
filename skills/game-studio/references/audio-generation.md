# Audio generation (local): music, SFX, ambience and voice

Music, sound effects, ambience and voice generated locally on the shared pipeline in
[asset-pipeline.md](asset-pipeline.md), with mandatory non-AI post-processing. Licence
rules in [licences.md](licences.md) govern every engine; choices below are dated
defaults (Oct 2026), re-verified at download time. Values in `<placeholders>` come
from `project.md`. This file covers **generation**; what audio a game needs (coverage,
anatomy, mixing design) is a design question for the project's design references, not
for this pipeline file.

## 1. Engines — one per job, no substitutions

| Job | Engine (default) | Licence status | Notes |
|---|---|---|---|
| Music | ACE-Step 1.5 (turbo AIO checkpoint) | `cleared` (MIT / Apache 2.0) | Native in the backend; batch 4 seeds is cheap |
| Voice, preset | Kokoro | `cleared` (Apache 2.0) | Preset voices only, no cloning; small VRAM, CPU-capable |
| Voice, cloned | Chatterbox | `cleared-conditional` (MIT + input-rights condition, section 4) | Zero-shot cloning from a short clean reference |
| SFX / ambience | Stable Audio 3 (Small/Medium) | `gated` — USER GATE, [licences.md](licences.md) section 4 | Community licence with a revenue condition |
| Foley for silent video | MMAudio-class tools | `prototype-only` | Checkpoints under non-commercial terms; section 5 |

- **Substitution rules.** No silent substitution of engine, checkpoint or TTS voice.
  A missing model file is a named stop. Cloud audio APIs are out of scope and are
  never proposed as a substitute for a failed local step.
- Music variant: a slower, finer-detail checkpoint of the same music engine (more
  steps, same family and licence) may be allowlisted in `project.md` as an optional
  quality tier. It is a variant, not a second engine, and the manifest records which
  checkpoint produced each track.
- Install notes that bite: a current backend build ships the music and gated SFX
  nodes natively — if a template is absent, update the backend first; reinstalling
  packs is not the fix. The preset-voice pack does **not** self-download its weights:
  both the model file and its voices file must be present in its model folder, and a
  missing file typically fails silently (empty output) — check both before debugging
  anything else. The cloning engine's models download on first use into its model
  folder; verify sizes after that first run.
- Post requires `ffmpeg` on the machine. Check it in pre-flight; it is a setup
  dependency, not an optional extra.

## 2. Access route

Per [asset-pipeline.md](asset-pipeline.md), section 2:

- Interactive work (one track, one effect, auditioning variants) through MCP. Note
  that MCP audio support varies by server implementation: where the server exposes a
  dedicated audio action for the music and SFX engines, use it; TTS and other
  engines are run by executing their saved workflows through the same server.
- Batch work (variant sets, ambience sets, and above all dialogue by line ID,
  section 6) through the reusable REST batch script: one job row per item, the
  exported workflow per engine, prompt/seed/duration injected per row, outputs
  collected per item and the manifest written as items complete. A failed line in a
  dialogue batch is retried as that line only, never by re-running the scene.

## 3. Operating defaults per engine

### Music (ACE-Step class)

- Inputs: style/tags field (genre, instruments, mood, BPM, key, time signature),
  lyrics field, duration, seed. Output range per the template (short clips to
  full tracks).
- **Instrumental by default.** Never add lyrics the user did not ask for. When
  vocals are requested: structure markers (`[Verse]`, `[Chorus]`, `[Outro]`), short
  lines, the language field set to the lyrics' language, and proper names spelled
  phonetically or they will be mispronounced.
- Generate a batch of 4 seeds per request; audition and keep per section 7.

### SFX and ambience (Stable Audio class, post-gate)

- **One prompt = one sound.** The engine mixes poorly when asked for several
  unrelated sounds at once; generate separately and mix in post or in-engine.
- Write the duration inside the prompt text in the form the model expects
  (for example `… Length: 3 seconds`).
- Generate 4 variants per effect. Ambience is generated long (60–120 s) and looped
  in post (section 5).
- Use inpainting to regenerate a bad segment and outpainting to extend a clip
  before regenerating a whole clip that is mostly right.

### Voice, preset (Kokoro class)

- Voices are named presets (language + gender + name). Pick **one voice per
  character** and record it in the voice registry (section 6). Never re-pick a
  voice per line.
- Use for narrator lines, tutorial prompts and placeholder dialogue that may ship
  if the project accepts the preset voice as final — its status is `cleared`, so
  placeholder here is a production choice, not a licence limitation.

## 4. Voice, cloned (Chatterbox class) — the rights condition

Cloning is cleared **only** for voices the project has rights to. This restates
[licences.md](licences.md), section 6, because it is the rule most likely to be
pressured in practice:

- Clone only: the user's own voice, a performer's recording made for this project,
  or a licensed voice pack. Never clone a real public person's voice, a voice from
  a film or game, or a sample whose provenance is unclear. Unclear provenance:
  stop and ask. No exceptions, no prototype waiver.
- Reference standard: 5–15 s, single speaker, no music, noise or reverb, plus an
  exact transcript stored beside it. Reference files live in the project at
  `<audio_voices>/<character>/reference.wav` + `reference.txt` and are **frozen**:
  never edited, re-recorded or "improved" between sessions — a drifting reference
  is a drifting character voice. Replacing a reference is a coordinator decision
  recorded as a voice change, and all of that character's lines are candidates for
  retake.
- Emotion is controlled through the engine's exaggeration/expression parameter,
  not by adding stage directions to the line text.

## 5. Traps and prototype-only routes

- **Foley for silent video** (generated or captured cutscenes): available tools in
  this class commonly pair permissive code with **non-commercial checkpoints**.
  Their output is `prototype-only`: flag it in the manifest, use it as a timing
  reference, and produce shipped cutscene sound by placing cleared SFX in the
  editor or generating them through the gated SFX route. Never promote foley
  output to a shipped asset.
- TTS engines with non-commercial weights — whether community favourites or
  bundled examples — are not installed as voice engines here. Popularity in TTS
  comparisons is not a licence check; apply [licences.md](licences.md), section 8.
- Territory-excluded and research-only audio models are `banned`: do not install
  them to "test" them.

## 6. Dialogue production

- Input: script files at `<audio_scripts>/<scene>.txt` (or `.csv`), one record per
  line: `line_id | character | text`. Line IDs are the game's dialogue IDs; never
  renumber them.
- Output: one file per line, `<audio_generated>/voice/<scene>/<line_id>_<character>.wav`,
  generated with that character's registered voice, post-processed per section 7,
  with a per-scene manifest: line_id, character, voice/engine, reference file (if
  cloned), seed/settings, duration, loudness.
- The voice registry at `<audio_voices>/registry.md` maps character → voice id →
  engine → reference path. The registry is the source of truth; a line generated
  with an unregistered voice is not done.
- Generate the text **exactly as written** in the script file. Never paraphrase,
  punctuate-fix or "improve" a line; a script problem is a finding routed to the
  script's owner.
- Retakes regenerate only the named line IDs. A changed script line invalidates
  only its own file.

## 7. Post contract (ffmpeg, no AI) — mandatory before "done"

Every generated file passes post. Measure with loudness tooling (`loudnorm` /
ebur128 class) and record the measured values in the manifest.

### Loudness and trim, by type

| Type | Target | Additional rules |
|---|---|---|
| Music | −16 LUFS integrated, true peak ≤ −1 dBTP | Game-mix headroom; no extra limiting beyond target |
| Voice | −16 LUFS integrated | Light silence trim at both ends; no reverb added in post |
| SFX | Peak-normalise to −3 dBFS | Trim leading/trailing silence to <50 ms for UI and one-shot sounds; loudness is the in-engine mixer's job |
| Ambience | −20 LUFS integrated | Must pass the loop verification below |

### Loops (music and ambience)

- A generated track is **not** a loop. Find a musically valid loop region, apply an
  equal-power crossfade (1–3 s) at the seam, and export.
- Verify: render the file doubled (two copies joined) and check the join for clicks
  or level steps by waveform and loudness at the seam. A failed loop check means
  not done, regardless of how good one pass sounds. Record the check result in the
  manifest.
- Prompting for loopable material helps but proves nothing: request steady
  intensity, no intro, no outro, no fade — then still verify.

### Export contract

- Masters stay WAV as generated (at the engine's sample rate; do not resample
  masters).
- Engine-ready copies alongside: WAV 48 kHz 16-bit for one-shots and voice; OGG
  Vorbis q7 class for music and ambience loops. The manifest states which file is
  the master and which is the engine copy.

## 8. VRAM budgeting

- Music: mid tier, fast per track; seed batches are sequential, not parallel.
- Gated SFX engine: small tier (single-digit GB class); still obeys the one-run-at-
  a-time rule on the shared GPU ([asset-pipeline.md](asset-pipeline.md), section 5).
- Preset voice: the cheap tier — runs even on CPU, so it never queues behind heavy
  image or 3D work unless the brief says otherwise. Cloned voice: small GPU tier.
- Foley (prototype-only): budget it like any other generation run; its licence
  status does not exempt it from resource rules.

## 9. Output contract

Shared contract in [asset-pipeline.md](asset-pipeline.md), section 6, plus:

- Root: `<audio_generated>/<type>/<slug>/`, type ∈ `music | sfx | ambience | voice`
  (dialogue uses the per-scene layout in section 6 instead of `<slug>`).
- Names: `<slug>_<variant>_<seed>.wav`, plus the engine copy where section 7
  requires one.
- Manifest adds: engine and model file, settings, seed, duration, sample rate,
  channels, measured loudness, loop-check result where applicable, licence status
  and conditions, `prototype_only` flag where applicable.
- Listen-check before reporting: inspect duration, sample rate, channels and
  loudness for every delivered file, and use audio preview where available. A file
  that was never checked is not reported as done.

## 10. Test generations after setup

Each must pass or be flagged with exact errors (a gated SFX test still waiting on
the USER GATE is marked gated, not failed):

- Music loop: one instrumental loop request with BPM, key and instruments named →
  post (loop crossfade + loudness) → doubled-file seam check passes.
- SFX batch: one named effect, 4 variants → peak-normalise → files and manifest.
- Ambience: one long soundscape with exclusions stated (no voices, no music) →
  loop post and seam check.
- Voice: one narrator line on the preset engine → loudness post. Cloned-voice test
  only when a rights-cleared reference already exists in the registry; otherwise
  record `skipped — no reference provided`, which is a pass.
- Final setup report includes the gated engine's state and its revenue condition in
  plain words, per [licences.md](licences.md), section 4.
