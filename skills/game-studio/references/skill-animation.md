# Skill animation and VFX identity

How every skill in a game gets a distinct, provable visual identity: fingerprints, controlled vocabularies, timing truth, a reserved danger grammar, and acceptance tests. Read when authoring, generating, rigging or reviewing skill animations and VFX, or briefing a worker to do so. The sound twin is `audio-design.md` (nine-slot anatomy); encounter use of enemy skills is in `boss-encounters.md`. Project specifics — schools, rig, `<camera_modes>`, `<combat_model>`, budgets — come from `project.md`.

## 0. The problem and the three rules

Made skill by skill, by feel, a large skill set collapses: ten skills in one school become one explosion at ten sizes, every projectile a glowing ball in a new colour, every area skill a coloured circle, every cast the same arm wave at a new speed. Colour is not identity. Size is not identity. Speed is not identity. A recoloured, rescaled copy is a defect with a second filename.

1. **Audit before animation.** Extract the real skill registry first (§4). Never animate a skill that is not in the registry; never leave a registry skill without a fingerprint.
2. **Identity is combinatorial, never a single trait.** Body gesture + primary shape + motion + trail + ground mark + timing rhythm + light behaviour, combined. Reuse components freely. Never reuse a combination.
3. **The animation must never lie.** The frame damage applies, the area that is dangerous, the moment a channel can be interrupted, the instant a buff expires — what the player sees is exactly what the game does.

Per-system DO/DON'T material is binding. An exception is recorded in the skill's spec sheet as a project decision, never taken on the author's judgement. `MUST` = does not ship without it. `MUST NOT` = does not ship with it.

## 1. Pillars, forbiddens, readability hierarchy

- **Readability beats spectacle.** The player reads the screen while moving, aiming, managing resources and watching enemy telegraphs.
- **The body speaks first.** In a third-person-style view the pose identifies the skill family before particles appear; in a first-person-style view the hands, weapon or viewmodel do the same job (per `<camera_modes>`). Particles confirm; they do not replace.
- **One skill, one silhouette moment.** Every skill contains a **signature frame** that, printed as a black silhouette, still identifies it. No signature frame, no identity yet.
- **Effects belong to the world** the project defines: its materials and registers, as recorded in `project.md`. Registers the project has not adopted do not appear.

Global MUST NOT (no exceptions by default): a recoloured copy as a new skill; a generic glowing orb as the primary projectile of more than one skill family; a coloured ground circle as the *only* representation of an area skill; a full-screen flash or white-out for a non-ultimate skill; any effect hiding an enemy telegraph, a danger boundary, the player character's position or a loot drop for longer than the project's stated cap (starting default: 150 ms); any light source added per particle, per projectile copy or per summon copy (budgets in §15).

**Readability hierarchy** — when effects stack, higher wins (brighter core, sharper edge, drawn later, never fully occluded); every spec sheet assigns its skill a rank: 1 Enemy danger telegraphs and imminent-damage areas. 2 Player damage state (being hit, low health, shield about to break). 3 Player skill impacts on the current target. 4 Player cast/release. 5 Active ground danger, either side. 6 Friendly lingering effects and constructs/summons, as applicable. 7 Loot, interactables, progression-relevant world objects. 8 Ambient and cosmetic particles — always culled, dimmed or dropped first.

## 2. Visual Identity Fingerprints

### 2.1 The fields

Every registry skill is assigned exactly one value in each field, from the controlled vocabularies of §6. Inventing a value means adding it to §6's project vocabulary first, with a definition — never inline in one skill's spec.

| # | Field | Decides |
|---|---|---|
| F1 | Body gesture family | What the body / viewmodel does |
| F2 | Primary shape | The one geometric shape the skill is remembered by |
| F3 | Colour pair | Core colour + edge colour; never one colour alone |
| F4 | Motion vector | How the effect mainly moves through space |
| F5 | Particle behaviour | How particles are born, live and die, and their count class |
| F6 | Trail type | What a moving effect leaves behind, if anything |
| F7 | Ground mark | What it writes on the ground, if anything |
| F8 | Timing rhythm | Its anticipation / release / linger pattern |
| F9 | Light behaviour | None / steady / pulse / rationed strobe / shadow off — every emissive skill |
| F10 | Construct silhouette | Every summon, placed construct, trap and placed object, as applicable |

### 2.2 The Distance Rule

- Any two skills **MUST differ in at least 3 of F1–F8**.
- Any two sharing **school AND delivery archetype MUST differ in at least 4**, and at least one difference **MUST** be F2 or F4. Colour and timing alone do not separate siblings.
- Any two a build can equip **at the same time MUST differ in at least 4**, regardless of school. The player must never confuse two buttons they alternate between.
- A skill and its rank/modifier variant **MUST keep the same F2 and F4** and may change size, density, a secondary shape and exactly one other field (§9).
- An **enemy** skill **MUST differ from every player skill in F4 or F7 plus the danger grammar** (§13), even in the same school.

Maintain a fingerprint matrix, one row per skill; check every new row against every existing row. Resolve a collision by changing the *new* skill, never the shipped one.

### 2.3 The five identity tests — on paper, before animating

1. **Silhouette.** Signature and release frames in flat black on white: a tester who knows the skill list names the skill.
2. **Grayscale.** The full effect desaturated: still identifiable by shape, motion, timing.
3. **Palette-Swap.** Recoloured to another school's palette: if it now looks exactly like an existing skill of that school, it was always a palette swap. Fail.
4. **Freeze.** Stills at anticipation end, release, mid-travel, impact and shortly after impact: each phase distinguishable from the same skill's other phases and from siblings' same phase.
5. **Muffled.** At reduced size, at maximum view distance for `<camera_modes>`, in the project's worst visibility context and on its worst-case background (named in `project.md` from the audit): still identifiable. The worst case is chosen because builds travel, not because the skill belongs there.

### 2.4 Components vs identities

Reusable components (encouraged): an emitter shape, a trail setting, a decal base, a body gesture *with a different F2/F4 on top*, an impact material layer shared with hit feedback. Identities (each primary only once per school + delivery group): a primary shape (F2), a signature pose held beyond the project's threshold, a unique ground mark (F7), a unique projectile silhouette including its trail read as one object.

## 3. The coverage matrix

Distinctness for most skills is not completeness. Completeness is a matrix: **Axis A** — every registry skill, plus enemy skills, boss skills, passive procs and construct/summon abilities, as applicable. **Axis B** — the eight phases of §5. **Axis C** — every context in `<camera_modes>`, low/reduced-effects modes, low-spec LOD, crowded fights, boss arenas, and the project's bright/dark extremes. Each cell is `animate`, `derive` (state the rule), `parameter` (state the range) or `none` (state the reason; forbidden for release, impact and expire on any damaging or defensive skill). **A skill is complete only when every cell in its row has a disposition.**

## 4. Step zero — the audit

Extract from code, data, trees and design notes; report counts to the coordinator before animating. A count that contradicts the game's known scope means the audit failed.

1. **Skill registry** — id, class/school, delivery archetype, geometry, target type, damage profile, resource cost, repeatability, channel behaviour, ultimate status (project-marked only), current animation state.
2. **Enemy skill registry** — every enemy and boss ability with telegraph, damage type and expected player response. Separate registry, separate grammar (§13).
3. **Passive proc registry** — every passive that can proc, stack, trigger or expire visibly.
4. **Construct registry** — every summon/construct/trap type, as applicable: silhouette, size class, attack delivery, lifetime, replacement behaviour at cap.
5. **Weapon/stance registry** — every weapon type and stance that changes the hands, because F1 gestures are performed *with* something.
6. **Camera/view registry** — the real viewmodel setup, camera distances, FOV range and lowest shipped resolution/effects setting for each mode in `<camera_modes>`. All readability tests use these real values.

## 5. Anatomy of one skill — eight phases, layer stack

### 5.1 The eight phases

Aligned with the nine audio slots in `audio-design.md` §6: where a phase and a slot describe the same moment, they share the same frame in the spec sheet.

| # | Phase | What the player must learn | Failure if generic |
|---|---|---|---|
| 1 | Anticipation / wind-up | Which skill, and whether the decision can still change | All skills start identically |
| 2 | Cast | The skill is committed; resource is spent here unless design says otherwise | A cancelled cast looks like a fired one |
| 3 | Release | The exact frame the effect leaves / the damage path starts | Dodges and interrupts feel unfair |
| 4 | Travel | Where it is going, how fast, whether it can still be avoided | Effects "teleport" from hand to target |
| 5 | Impact | It landed, on what, and how the shape reports the result class | One impact for every material; a miss looks like a hit |
| 6 | Linger / tick | The effect is still active, its area still live, its age readable | A long zone identical at its start and just before expiry |
| 7 | Expire / end | It is over, now | Players dodge dead zones and re-cast live buffs |
| 8 | Fail | It did not happen, and why | One generic fizzle for different decisions |

A phase that does not apply is `none` with a reason. Fail is plural: each fail type the game has (for example resource, range/line-of-sight, interrupted) gets a distinct form — body first — because each implies a different next player action.

### 5.2 The layer stack

Each layer may be `none` with a reason; layers are where reuse lives. 1. **Body** (carries F1) — full body, or hands/weapon viewmodel per `<camera_modes>`. 2. **Weapon/focus** — a defined point and pattern reacts; never a uniform whole-weapon glow for every skill. 3. **Core** (F2, F3) — the layer the Silhouette and Grayscale tests judge. 4. **Secondary** — the material the core is made of; school-coloured, skill-shaped. 5. **Trail/residue** (F6). 6. **Ground** (F7), conforming to terrain per §14. 7. **Light** (F9) — at most one dynamic light per effect, budgeted. 8. **Distortion/air** — rationed; at most one per skill, never full strength on a repeatable skill. 9. **Reaction** — what the target does; shared systems, tuned per skill. A heavy skill with a light flinch lies about its weight. 10. **UI echo** — identical grammar across skills. The bar confirms; the world identifies.

DO/DON'T, anatomy: record the signature frame number; align release, impact and expire frames with the audio slots; make a miss visibly different from a hit; show linger age (thins, slows, cracks, sinks or cools — a stated rule per skill); end lingering effects with a readable expire phase (starting default: at least 150 ms at combat distance); never invent per-skill HUD animations.

## 6. Controlled vocabularies

Finite lists force combinations, and combinations create distinctness. Use the game's real schools from the registry; delete rows it lacks, add rows it has, in this format.

### 6.1 School/element language

Per school record: core/edge colours (actual values in the implementation file, never prose like "orange-ish"), material and particle character, motion character, and what is forbidden for that school. Binding rules: a school is recognised by how it moves as much as by colour; two schools must not share both colour neighbours and motion character; any colour the project reserves for danger (§13) is not a player school's core.

### 6.2 Delivery archetypes — visual grammar

Every archetype must be recognisable from travel + impact alone, body hidden.

| Archetype | MUST | MUST NOT |
|---|---|---|
| Melee strike | Arc follows the weapon's real swing; contact frame = impact frame | A detached slash arc ahead of the weapon, or one that lingers |
| Cleave / arc | One wide ground-hugging sweep; the edge is the dangerous part | A full ring pretending to be a cleave (it lies about where is safe) |
| Movement (dash/leap) | The body is the projectile; trail behind; landing marked at the true point | A separate projectile effect while the body also moves |
| Single projectile | One traveller, one silhouette, trail unique within its school | Traveller below the readability minimum at max distance |
| Multi-projectile | A pattern (fan, spiral, staggered line, ring) that is itself the identity; count visible at release | A shapeless spray of identical orbs |
| Nova / point-blank | Expands outward; the expanding edge is the dangerous moment | Instant full-radius appearance with no expansion |
| Ground area (targeted) | Placement, arrival and active zone are three distinct states | Zone at full strength in one frame, far from the caster |
| Beam / channel | Continuous connection for exactly the channel's life; stages visible; break instant and total | Rendering through obstacles it cannot damage through; persisting after the channel ends |
| Summon / construct | A materialise phase with a family construction grammar | A fade-in |
| Buff / ward | Applied to the body: defined location, pattern, settle state | A generic ring at the feet as the whole buff |
| Curse / mark | Applied to the target's body, readable at mob and boss scale, with live and about-to-expire states | A tiny head icon as the only representation |
| Heal | Motion travels toward and into the healed body; the healed body owns the signature frame | Looking like a buff, or like a damage skill aimed at a friend |
| Shield / guard | A surface with location, facing and damage states | The same bubble for every shield regardless of school |
| Trap / mine | Placed-unarmed, armed-live and triggered/spent always distinguishable | An unarmed trap that looks armed to its owner |

### 6.3 Body gesture families (F1)

A finite set, sharply differentiated, beats many similar bespoke gestures. Default families — replace with the real rig's capabilities after the audit, keeping the structure: overhead cast/strike; thrust/point; sweep left / sweep right (direction is part of the family); cross/gather; plant/kneel; throw/release; stomp/slam; shout/command; dual/asymmetric (hands do two different things); step-cast (gesture completed while moving).

Per skill state: family, hand(s), weapon involvement, and whether the lower body is rooted, stepping or free — under `<combat_model>` the lower-body answer is a balance fact and animation and design must agree on it in writing. Two skills on the same probable skill bar must not share family + hand pattern + timing rhythm. No full-body gesture for a skill designed to be cast while moving; no subtle gesture for a heavy commitment. Author upper/lower-body separation from the start; rooted skills are the explicit exception list. Each family needs a distinct first 150 ms — identification happens at the start, under repetition, in peripheral vision.

### 6.4 Shape, colour, motion, particle, trail, ground

- **F2 primary shapes (controlled list):** sphere/orb, shard/crystal, spear/lance, disc/ring, cone, fan/arc, column/pillar, wall/plane, dome, spiral/helix, branching tree, pool/splat, inscribed ring-set, swarm, wave/crest, cross/sigil, chain, cloud/volume. A shape is primary for at most one skill per school + delivery group; as a secondary it is unrestricted but visibly subordinate. A sphere primary needs a written justification in the spec sheet.
- **F3 colour pairs:** core + edge, both from the school's row, varied in value — never hue family — to separate siblings; siblings also differ in core-to-edge direction. Dangerous information is never carried by colour alone.
- **F4 motion vectors:** outward radial, inward/imploding, rising, falling/descending, forward ballistic, arcing ballistic, orbiting, spiralling, ground-creeping, branching, pulsing in place, sweeping arc, draining to a point, oscillating, teleport-snap (only where design says instant — the absence of travel is then its identity).
- **F5 particle behaviour:** state birth (burst/stream/growth/assembly/condensation), life (ballistic/floating/seeking/ground-bound/attached), death (fade/shatter/burn-out/sink/pop — rationed) and count class (project bands in `project.md`). Siblings differ in at least one of birth, life or death, not only in count.
- **F6 trail types:** none (stated), continuous ribbon, segmented dashes, ember/spark shedding, smoke/vapour wake, ground line, after-image ghosts (rationed), dripping residue, ordered mark sequence, debris field. A trail is part of the projectile's silhouette; distinctness by trail must be tested at max distance, not asserted.
- **F7 ground marks:** none, scorch, frost/rime, pool, inscribed ward (ordered schools only), cracks, overgrowth, ash/drain, residue slick, path line for moving effects. A mark outlives its damage only by a stated amount and, while it remains, is visually weaker than any live effect. Never the same mark for a damaging and a beneficial zone.

## 7. Timing — anticipation, release truth, rhythm

Per spec sheet, in milliseconds (never frames alone): `anticipation_ms` (the animation shows whether it is cancellable — open posture — or committed — closed posture), `release_frame`, `active_ms`, `recovery_ms` (under `<combat_model>`, alongside resource cost, recovery may be the cast-rate limiter: it is a balance number owned by design; the animator does not stretch it for beauty), `cancel_windows`, `interrupt_behaviour` per layer.

**Timing rhythms (F8):** Snap (very short anticipation, instant release); Cast (standard single release); Heavy (long anticipation, weighty release, long recovery); Staged (2–3 readable steps); Channel (short anticipation, sustained active, stated tick rhythm); Pulse (repeated releases from one cast); Delayed (release, stated fuse, effect). Siblings must not share a rhythm *and* a gesture family. DO: make anticipation identifiable before release at combat distance; keep the release frame identical across views, modes and LODs; let recovery read as recovery (a settle pose); give staged skills a readable change at every stage. DON'T: front-load identity into impact only; end animations abruptly at the cancel window; hide the player's own commitment from the player.

## 8. Per-archetype rules (condensed)

- **Projectiles:** silhouette readable at max distance; travel states speed honestly; impact per material class or a stated shared layer; near-miss/pass-by read in first-person-style views; an end-of-life form for a projectile that hits nothing — never a silent vanish. No homing visuals on a non-homing projectile; no trail longer than typical combat distance. Siblings separate first by pattern/silhouette, second by trail, only third by colour value.
- **Melee/cleave/slam:** the weapon's real path is the effect's path; weight comes from anticipation, commitment and recovery, not shake alone; ground interaction on contact; a whiff is visibly thinner than a hit. No arc wider than the damage geometry.
- **Nova/ground/rain:** three states distinct; boundary judgeable to within a character width while moving; expansion travel for novas; overlapping instances show instance boundaries or a stated merge behaviour.
- **Beams/channels:** §6.2, plus a hero body that shows the cost of channelling.
- **Movement skills:** start, travel, landing are three events; a failed form is visibly a failure; direction and verticality are honest; no false body that reads as targetable.
- **Buffs/shields/heals:** buff live state quieter than its apply moment, with an expiry warning state for long player-applied effects; shields show intact/strained/breaking; heals differ by target type (self, ally, construct, as applicable).
- **Curses/marks:** on the target's body at every scale; tick and expiry states present.
- **Traps/mines:** the three states of §6.2, readable by the owner at a glance.

## 9. Rank, modifiers and build variation

Variation changes expression, never identity: keep F2 and F4; scale size, density, a secondary shape and exactly one other field (§2.2). A modifier that changes geometry, targeting or delivery follows the project's design rules for conversions — the visual follows the new delivery's grammar and the spec sheet records the change. A modifier, rank or proc that changes gameplay with no visual delta and no stated `none` reason is a defect. Re-run the identity tests on the maximum modified form.

## 10. Repetition — animation under rapid casting

Applies in full if `<combat_model>` has no or low cooldowns; apply the overlap and clutter rules regardless.

- A repeatable skill has a reduced repeat form (fewer particles, no distortion layer, no camera effects) beyond a stated cast rate, produced by rule, not by dropping frames.
- **Settle rule:** every repeatable animation ends in a settle pose that loops cleanly into its own anticipation, so sustained casting reads as rhythm, not glitching.
- **Fail is a first-class animation** — the most seen one in a resource-gated game. §5's distinct fail forms are mandatory, readable muted, in every camera mode.
- **Overlap:** simultaneous instances of one skill cap at a stated count, then merge, dim secondaries or reuse the reduced form per a stated rule. Friendly effects never outrank the hierarchy of §1.

## 11. Camera modes — two views, one skill

For each mode in `<camera_modes>`: the view is authored, not derived by hiding the body. Timing is identical in every mode — the view may differ, the clock may not. A centred or self skill needs a non-blinding form in a first-person-style view; a third-person-style view needs readability at its real maximum distance. Behind-the-player information gets a stated carrier (directional edge cue, sound per `audio-design.md`, or both). Test both the earliest and latest shipped forms of each mode.

## 12. Body, rig and weapons

Upper-body gestures blend over locomotion by default; rooting is explicit per skill. Weapon involvement is stated per gesture (registry 5); a gesture that only works with one weapon type is flagged, not shipped silently. Facing agrees with aim within the project's stated tolerance; feet do not slide on rooted casts; weapons do not vanish in any phase, view or LOD. Hit reactions, flinch families and knockback direction are shared systems tuned per skill (§5.2, layer 9).

## 13. Enemy and boss skills — the danger grammar

### 13.1 The danger grammar — reserved, exclusive, never borrowed

The project reserves a fixed signal set for "you are about to take damage", recorded in `project.md` once all player fingerprints exist and then frozen: a reserved colour value, a reserved shape family, a reserved motion character and a reserved telegraph fill pattern (project chooses the concrete values). Player-beneficial effects MUST NOT use any of them, in any school, at any rank. Enemy effects MUST use them consistently. Safe ground in an enemy pattern is a visual fact — telegraphed as clearly as danger — never merely the absence of the danger signal. See `boss-encounters.md` §8 for how bosses combine these signals fairly.

### 13.2 Telegraph law

- Area shown = area damaged. A telegraph smaller than the real area is a lie; larger is a stated, consistent margin, if the project uses one at all.
- Telegraph duration is by response type (dodge, interrupt, brace, kill-first, endure), with project floors recorded in `project.md` (starting defaults are set with the boss work in `boss-encounters.md` §17). An enemy telegraph is never shorter than its regular-enemy counterpart for the same response type.
- Every telegraph states its response type in its form: what the player is expected to do must be readable on first sight, attemptable on first sight and achievable by the third (acceptance test 9).
- Telegraphs survive overlap: two simultaneous enemy telegraphs remain separately readable by pattern, not only by colour.

### 13.3 DO / DON'T — enemy skills

DO: give boss and elite skills their own fingerprint discipline (an enemy signature is as unique as a player one); carry telegraph information in shape and motion as well as colour; test telegraphs muted and in every camera mode. DON'T: reuse a player skill's effect with a colour change as an enemy skill; use player school signatures for enemy arrivals; let an enemy effect read as loot, a buff or a safe zone.

## 14. Constructs, lingering states and special systems

As applicable to the project's systems; where a system does not exist, record `none` in the audit rather than omitting the section.

- **Buff/ward body states:** apply, settle, expiry warning — on the body, per §8.
- **Ground effects and terrain:** marks conform to slope within the project's stated limits; effects on stairs, water or broken ground keep a judgeable boundary or state the exception per zone type.
- **Channels and sustained effects:** stage changes are visible in width, texture or segmentation; a sustained effect's intensity states its remaining life or stage.
- **Summons and creatures:** full lifecycle, each state a distinct form — materialise, idle, move, attack, damage states, death, despawn, and replaced-at-cap. Silhouette (F10) is unique per type within its family.
- **Placed and built constructs:** assembly/build states distinct from the finished state; load/aim/fire/reload cycle where it has one, each readable; damage states; destruction as its own event form (collapse or the design's stated form), never a generic explosion borrowed from a skill.
- **Traps and placed objects:** §8 lifecycle; build phases never read as finished.
- **Camera and screen effects — a rationed budget:** shake in a small set of classes with stated caps (a skill names its class or `none`); FOV kicks, aberration, vignette pulses, slow motion and hit-stop are game-wide rations, off for ordinary skills by default and project-marked where used. Identity must survive with camera effects disabled in settings — for some players, they will be.
- **Passive procs and triggered effects:** a proc is a whisper, not a cast — one family form per school at the body location the family owns; stacks read at thresholds only (max, loss), mirroring `audio-design.md`. A triggered full skill renders its real fingerprint, with the body layer of its trigger source, stated per trigger.

## 15. Clutter, performance and accessibility

- **Readability minimums, stated then measured** in the implementation file from the audit's real camera/resolution data: minimum projectile silhouette at max distance; minimum ground-boundary contrast on the worst-case background; minimum telegraph size and duration per response type; maximum frame share for one ordinary skill at its signature frame (starting default: 25%; ultimates are project-marked exceptions).
- **Clutter budget:** stated concurrent caps in `project.md` (dynamic lights, particles in frame, full-form lingering ground effects). Over-budget trim order follows §1: ambient first, then friendly secondaries, then reduced repeat forms, then LOD swaps. Danger, impacts and the current target are never trimmed. Shipping without numbers is forbidden; the numbers themselves are set from measured crowd-test frame times on target hardware, not guessed in advance.
- **Accessibility — MUST:** no information by hue alone (boundaries, expiry, friendly/enemy, school identity all have shape or motion carriers); no strobe above the project's photosensitivity cap at any cast rate (starting default: 3 flashes/second), including fast schools under repetition — a reduced form replaces strobe with a single strike plus after-image; a reduced-effects mode that changes no timing, area read or identity field except F5 count class and F9; camera effects individually disableable.
- **Performance — MUST:** per-skill particle and light classes in the spec sheet, checked in the crowded-fight test, not in an empty room; pooling for projectiles, impacts and ground effects (per-cast allocation under rapid casting hitches exactly when it reads as unfairness); a stated distance LOD per lingering and construct effect, with F2/F4 surviving; no visual lifetime beyond the gameplay lifetime plus a short stated cosmetic tail.

## 16. Deliverables and engine rules

Per skill, the author delivers: the spec sheet (fingerprint, timings in ms, phase dispositions, hierarchy rank); body/blend definitions for anticipation, cast, release, recovery, settle, each fail form and interrupt; VFX per phase built from the layer stack, each layer separately toggleable; the coverage-matrix row; each camera-mode form, reduced-effects form and LOD — or their `derive` rules; and the §18 test evidence (screenshots are files, not claims). One naming scheme without exception, built from skill id, phase and variant; shared components live in one shared library and are referenced, never copied per skill. Timings are data, read from the skill's definition, so design can re-price without re-authoring; release events fire from one signal path shared by damage, spawns and audio. Emissive/bloom interaction is stated per material and tested in the brightest shipped scene.

## 17. Must-Have / Must-Avoid

**Must-Have:** fingerprint F1–F8 assigned (F9/F10 where applicable) and Distance Rule checked against every registry skill, including the maximum modified form; a named signature frame with its number recorded; the five identity tests passing at greybox; all eight phases dispositioned, with release/impact/expire never `none` on damaging or defensive skills; distinct fail forms per fail type; release frame identical across views, modes and LODs and shared with the audio slots; recovery and cancel windows matching design data; miss, wall hit and resisted hit distinct from a clean hit; lingering effects showing age and ending readably; every shipped camera mode authored; reduced-effects and LOD forms preserving identity; repetition, clutter and light budgets respected; construct lifecycles complete, as applicable; enemy skills under §13.

**Must-Avoid:** recolour/rescale/re-speed presented as a new skill; identity carried by colour, brightness or size alone; generic orb, feet-ring buff, ground-circle zone or fade-in summon for any skill, however minor; same gesture family + hand pattern + timing rhythm as another skill on the same probable bar; an enemy skill confusable with a player skill, or a player effect using reserved danger signals; effect geometry differing from damage geometry in either direction; timing differing by view, mode or LOD, even by a frame; a dead effect reading as live or a live one as dead; homing visuals on a non-homing effect; any ordinary skill covering the screen, flashing full-frame or hiding priority information beyond the stated cap; camera effects used as identity; strobing above the cap at any cast rate; one shared generic cast clip anywhere in the shipped set; a rooted full-body gesture on a design-mobile skill or a weightless gesture on a heavy one; per-cast allocation in the effect path; more dynamic lights per effect than the budget.

## 18. Workflow and acceptance

Workflow, sequential, each phase gated: **1 Audit** (§4; counts reported). **2 Fingerprints** on paper; Distance Rule across the whole matrix; collisions resolved while they cost a spreadsheet edit. **3 Greybox** — primitive shapes, flat colours, rough body clips, real timings; the five identity tests pass in every camera mode. A skill that cannot pass in greybox will not pass with particles. **4 Body pass. 5 VFX pass** (layer stack, shared library). **6 Context pass** — camera modes, reduced forms, LODs, worst-case backgrounds; matrix fully dispositioned. **7 Constructs and enemy pass** — deliberately after player skills, because enemy grammar is defined against the finished player language. **8 Acceptance.** Batch by school or family through phases 3–6, never skill-by-skill through all phases: identity is a property of a set.

Acceptance tests — report per skill, per test, pass/fail with evidence files:

1. **Blind identification, per camera mode:** a non-author tester, muted, max distance, random order, names each skill within 1 s of release. Starting default pass: at least 90% across the registry, 100% within each school + delivery group.
2. **Silhouette (in game):** flat-black signature and release frames identified from stills.
3. **Grayscale run:** a full combat session desaturated; no two skills confused; all ground boundaries still judgeable.
4. **Freeze ladder:** the five stills of §2.3 test 4; every phase distinguishable.
5. **Colourblind simulation:** both common simulations over mixed combat including telegraphs; no danger, expiry or friendly/enemy distinction lost.
6. **Crowd:** the project's crowded-fight case (combatants, constructs at cap, overlapping zones, sustained) — frame time within budget; hierarchy visibly respected; no telegraph hidden at any point.
7. **Repetition:** each repeatable skill at maximum sustainable rate, then a full probable bar in rotation: no strobe breach, no camera-effect stacking, no degrading frame time.
8. **Worst-case backgrounds:** every skill in the project's named worst cases (darkest, brightest, densest, weather-reduced) — identifiable and judgeable in all.
9. **Telegraph fairness:** per enemy skill, a fresh tester told only the response type attempts it on first sight and achieves it by the third.
10. **Fail clarity:** the fail types in random order, muted, per camera mode — the tester names the type every time.
11. **Expire honesty:** lingering effects left to expire during another task; zero dead effects named as live, zero live as dead.
12. **Modifier truth:** tests 1 and 4 re-run at maximum modified form; still itself, still not another skill.
13. **Reduced-effects parity:** tests 1, 3 and 9 in reduced mode; same results within the project's stated tolerance. Quieter, never harder.

A failed skill returns to the earliest phase that can fix the failure — identity failures to phase 2, body failures to phase 4 — not to a local polish pass.

## Appendix — templates and project decisions

Spec sheet per skill: `id | name | school | delivery | fingerprint F1–F10 | signature frame | timings (ms) | phase dispositions | hierarchy rank | particle/light class | camera-mode forms | reduced/LOD rules | test evidence links`. Fingerprint matrix: one row per skill, columns F1–F10, plus same-bar and same-group flags for the Distance Rule.

Decisions the project records in `project.md` (state the proposed default used until then; mark dependent work as assuming it): stepped vs smooth motion if the visual style raises it; which skills, if any, are project-marked ultimates allowed screen-filling forms; any deliberate register-breaking family; clutter and readability numbers, set from measured tests after greybox; hit-stop classes and durations if the game uses hit-stop at all; the reserved danger colour/shape set, chosen once all fingerprints exist and then frozen.
