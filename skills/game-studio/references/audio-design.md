# Audio design

How a game's sound is specified so completeness is provable: what music, ambience and effects must exist, how they combine in the engine, and how a system is accepted. Read when designing, auditing or
generating audio, or briefing an audio worker. How sounds are generated locally (engines, licences, post-processing) is in `audio-generation.md` and `licences.md`; the visual twin of the skill anatomy
below is in `skill-animation.md`. Project specifics — schools, zones, surfaces, `<engine_audio_buses>`, loudness targets, polyphony budget — come from
`project.md`.

## 0. The problem and the three rules

A set counted in files ("we have N sounds") has no finish line: categories can always be called done. One skill is many events; one place is a different sound world by time, weather and state; one footstep
differs by surface. Replace categories with coverage:

**Every asset exists because a real game event, in a real game state, in a real world context, needs it. Every such combination is generated, produced in the engine by layering or parameters, or explicitly
marked out of scope with a reason.**

1. **Audit before generation.** Extract the real lists from the game first (section 3).
Never invent a skill, enemy, zone or object to fill a table.
2. **Generate atoms, combine in the engine.** A projectile is a travel loop plus a school
layer plus an impact plus a target-material layer. Atoms multiply; baked mixes do not.
3. **Frequency decides variant count.** A sound heard hundreds of times an hour needs
several variants and engine randomisation. A sound heard once needs one good variant.

No asset is done because a file exists. It is done when its in-game acceptance test passes.

## 1. Sonic identity

Define, in `project.md` or the audio brief, before any generation:

- **Pillars:** what the world sounds like, what the player's abilities sound like relative
to the world, and the reference works (named for the traits taken, not as decoration).
- **Forbidden:** the registers the project bans (for example modern electronic UI, comedy
sounds, trailer bombast in exploration, vocals outside named moments). A forbidden list with no exceptions process will be broken silently; exceptions are recorded per asset.
- **Leitmotifs:** a small stated cap (starting default: three or fewer). Each motif has
where it must appear, where it must not, and every use is recorded in the manifest. An unplanned motif use is a defect.
- **Stylisation decision:** how literal or stylised sounds are relative to the visuals,
stated once, so hits read at low volume on small speakers.

## 2. The coverage matrix — how completeness is proved

Every sound requirement is one cell on three axes, built before generation for a system:

- **Axis A — Source:** player character, skill, enemy family, NPC, world object, UI, system.
- **Axis B — State:** the game's real states (for example exploration, combat tiers, boss,
safe area, interior/underground, dead, menu, dialogue — replace with the game's states).
- **Axis C — Context:** zone, day phase, weather, surface, interior/exterior, camera mode
(per `<camera_modes>`), intensity tier.

Each cell has exactly one disposition:

- `generate` — a new atom is needed.
- `layer` — an existing atom plus a named context layer produces it (state the layers).
- `parameter` — the engine produces it by pitch, volume, filter or reverb change
(state the parameter and range).
- `none` — deliberately silent (state the reason).

**A system is complete only when every cell in its rows has a disposition.** "I generated the skill sounds" is not a completeness claim. The matrix is.

## 3. Step zero — the audit

Before any generation, read the game (code, data, design notes) and produce six registries. Generation without a registry row is wasted work. Report the counts to the coordinator before generating; a count
that contradicts the game's known scope means the audit failed, not the game.

1. **Skill registry** — every skill: school/element, delivery type, target type, rank
scaling, channel/charge behaviour, whether it can be repeated rapidly.
2. **Passive registry** — every passive that can proc, stack, trigger or expire audibly.
3. **Enemy registry** — every enemy and boss: size, body material, movement type, attacks,
vocal range, zones.
4. **Zone registry** — every zone the game can present: tags for biome, interior/exterior,
water, safe/dangerous, depth, reverb class.
5. **Surface registry** — every walkable surface material.
6. **Interaction registry** — every UI action, inventory action, loot type and rarity,
world object the player can use/open/break/trigger, and every progression trigger.

Registry column templates are in the appendix.

## 4. Music system

Music is a system, not a track list; players hear transitions more often than tracks, so design transitions first.

- **States and stems.** Music plays as horizontal states with vertical stems the engine
adds and removes: bed (always present), figure/melody, pulse (combat), danger (high combat and boss), and a time-variant stem. The night form is a recomposition — fewer instruments, lower register, longer
gaps — never only a filter or a pitch shift.
- **One theme per region**, not per large area grouping, delivered as stems. Never deliver
a flat full mix and call it adaptive.
- **State changes follow game events**, stated per state: for example combat starts on
the first damage event and ends a stated time after the last, with a composed release, never a mid-bar fade. Map/menu states duck or filter music per a stated rule.
- **Stingers and shorts.** Each is a separate asset with a named trigger: discovery
(minor/major), progression (tiers matching how progression actually works in this game), level/skill/passive unlock, boss intro/phase/death, player death, respawn, game start. No trigger, no stinger.
- **Loop length:** exploration themes must loop long enough to survive extended play
(starting default: several minutes before a phrase repeats; project decides).
- Boss music is a hard border: no exploration stem inside the boss state.

## 5. Ambience — the layered model

A procedural or large world cannot have a bespoke track per place. Ambience is built from zone tags, in four layers mixed by the engine:

1. **Base bed** — the place itself (wind, water, insects, room tone for interiors).
2. **Time layer** — day content and night content, with composed dawn/dusk transition
beds (starting default: 30–90 s), not crossfades between day and night files.
3. **Weather layer** — above the bed, below events (section below).
4. **Event scheduler** — timed one-shots from per-zone pools with a no-repeat rule, a
minimum gap per pool, and a stated quiet period after a zone load.

Interiors replace layer 1 with a room tone and muffle layers 2–3 (rain heard through a roof), they do not delete them.

**Per zone**, the matrix needs: base bed, day layer, night layer, interior tone if any, and a depth/underground variant if any. Depth replaces day/night underground: deeper is sparser and lower — day and
night do not exist there.

**Weather is a system, not a rain file.** For each weather state the game has: an ambience layer per surface family it lands on, transition in/out, and its linked effects stated together (wet footsteps,
skill/weather interactions, music ducking if any). Thunder, if present, is a variant pool graded by a distance parameter. If the game has no dynamic weather, deliver weather as zone-tag variants and record
the disposition change in the matrix — never drop it silently.

**Day/night is an audio clock.** Transitions carry a learnable event cue; after extended play the player should hear dusk without looking. Night may raise the audition radius of creature sources as a
stated engine parameter — a design feature, not a mix accident.

## 6. Skills — the nine-slot anatomy

Every skill in the registry gets this row filled. A slot that does not apply is `none` with a reason. A blank slot means the skill is not done.

| Slot | Meaning | Typical failure if skipped |
|---|---|---|
| 1. Fail | Resource, target, range or line-of-sight failure — each fail type distinct | One generic buzz, or silence |
| 2. Cast start | The first moments; identifies the skill before it lands | Every skill in a school starts with the same whoosh |
| 3. Charge / channel loop | Only if the skill charges or channels | A channel that sounds once, then silence |
| 4. Release | The commit moment, distinct from cast start | A miss sounds like a hit |
| 5. Travel | Projectile flight, beam sustain, movement air, falling area | Effects silent between release and impact |
| 6. Impact | On target, on ground and on wall are separate dispositions | One impact for flesh, armour and a door |
| 7. Area tick / ground loop | Ground effects, auras, damage-over-time zones | A long zone that sounds once |
| 8. Summon / apply | Constructs and summons appear, buffs and curses land — as applicable | Arrivals are silent |
| 9. Expire / end | Buff fades, summon dies or despawns, zone ends | Effects end silently; the player cannot play by ear |

Alignment with `skill-animation.md`: its eight animation phases and these nine slots describe the same event. Where they coincide they share the same frame in the spec sheet.

| Audio slot | Animation phase (`skill-animation.md` §5) |
|---|---|
| 1 Fail | 8 Fail |
| 2 Cast start | 1 Anticipation / wind-up (late) and 2 Cast |
| 3 Charge / channel | 1–2 sustained form |
| 4 Release | 3 Release — same frame |
| 5 Travel | 4 Travel |
| 6 Impact | 5 Impact — same frame |
| 7 Area tick / ground | 6 Linger / tick |
| 8 Summon / apply | Within 3–5, per delivery type |
| 9 Expire / end | 7 Expire / end — same frame |

**How the count stays sane:** one skill sound = delivery-archetype atoms (travel, impact shape, timing) + school/element layer + target-material layer on impact. Build the archetype and school atom sets
once; combine per skill. Delete registry rows the game does not have; add the ones it does.

**Per-skill checklist (the commonly missed):** rank scaling adds a layer or a stated parameter, never only volume; multi-target hits play full impacts for the nearest few targets and a reduced shared
impact for the rest (engine rule, section 13); near-miss / pass-by for projectiles, per `<camera_modes>`; constructs and summons, as applicable — materialise, idle, move, attack, hit, death, despawn, and a
"replaced at cap" sound; stationary constructs — placement by surface, idle loop, trigger/fire, damage, destruction, expiry; buffs and shields — apply, subtle loop, absorb hit (shields), break, expiry
warning before long player-applied effects end; curses/debuffs — land, tick, expire, on enemies and on the player separately; heals by target type; traps — place, arm (the player must hear the arm moment),
idle, trigger, expire unused; movement skills — start, air, land by surface, failed form.

**Spam control — applies if `<combat_model>` has no or low cooldowns.** Audio does the pacing work: every repeatable cast has several variants plus a stated engine pitch/volume window; a rapid-repeat
limiter plays a reduced variant inside a stated interval (an engine rule, with a generated reduced asset per archetype); voice barks sit on global and per-type lockouts. Fail sounds for the resource that
gates casting are among the most heard sounds in such a game: give each fail type its own identity so the player knows which decision to change.

**Passives:** one quiet tick per passive family, never per node; stacks sound only at max stacks and at stack loss; progression-unlock sounds form one family pitched or varied by depth, with timbre or
rhythm also differing (no information by pitch alone).

## 7. Combat and creatures

- **Hit feedback is four atoms mixed in the engine:** weapon + school/element + target
material + result. Weapon rows come from the registry (swing light/heavy, hit, miss, blocked). Material rows (flesh, bone, armour, hide, construct, wood, shield, or the game's set) each have normal,
critical and kill forms.
- **Results are information:** hit, critical, miss, dodge, block, parry, break and
immune/no-effect are distinct overlays. Immune, blocked and missed must never sound like a hit — in a fast game the player acts on audio between frames.
- **Player damage taken** is its own set by damage family, plus low-health and
near-death states carried by body sounds and music-stem changes, not warning beeps.
- **Per enemy family:** idle vocal, aggro, attack telegraph, attack, pain, death, corpse
settle, movement by movement type, and special abilities using the section 6 anatomy from the enemy side. Size grades the set; a large creature is not a pitched-down small one (a parameter disposition
needs a stated range in the matrix). Bosses get a unique set per boss, never a family set with a pitch change.
- **Information sounds:** unseen enemies are audible in 3D (exploration information);
every ranged or leaping enemy has a telegraph that works with no visual — list them in the registry and test them blind; death, settle and search/loot are separate sounds.

## 8. The player character — movement, surfaces, states, camera

- **Footsteps:** per material family — walk and run variants, landing, and a wet
disposition or layer if zones can be wet. Build one set per material family plus a surface-detail layer (rustle, crunch, splash) mixed by tag, rather than one baked set per named surface; show the
arithmetic in the audit. Equipment is a layer on top: changing armour or kit must be audible if the game has gear.
- **Other movement:** jump/vault, climb, swim/wade and fall/landing, where the game has
them, each dispositioned.
- **States and voice:** exertion, wounded, afflicted, near-death breath forms (subtle,
player-only); pain by damage family; one composed death sequence; effort barks under the lockouts of section 6.
- **Camera:** per `<camera_modes>`, the mix changes more than the assets: nearer, drier
own-weapon and own-cast sounds and pass-by as a primary channel in a first-person-style mode; fuller distance and reverb in a third-person-style mode. Deliver the small camera-specific set the mode needs;
everything else is a parameter/bus disposition. Test every camera mode the project ships.

## 9. World objects, loot and gear

- **World interaction:** per object type in the registry, in the material of its zone —
doors by material (a secret door needs a learnable tell), containers (locked and trapped are distinct), breakables (a base smash per material plus a zone detail layer, not one smash for the whole game),
levers, shrines/stations, portals/lifts if present. World traps have a pre-trigger tell a careful player can hear.
- **Loot:** drop sounds by item class and material; rarity is a layer on top. The rarest
drop is the most important effect in the game: drop, positional shimmer loop until pickup, pickup and identify are separate assets with no sharing.
- **Inventory and equip:** pick up and place are different sounds and a failed place is
a distinct third sound, so the player hears the item is still held. Equip/unequip per slot material; currency by amount tier; socketing, crafting success and crafting failure (a failure that costs
materials sounds honest, not cheerful); consumable use has a quieter, faster quick-use variant.

## 10. Places, NPCs, dialogue and progression

- **Place life is placed 3D sources, not bed decoration:** work, trade, hearths, animals
and hub systems, each with a day disposition and a night disposition (mostly silent).
- **NPC voices:** one fixed voice per named NPC, never re-picked per line (generation and
licence rules in `audio-generation.md` / `licences.md`). NPCs also need greeting, farewell, trade open/close, cannot-afford, progression-reaction, danger and rare idle barks. Crowd voices are
unintelligible murmur layers — never generate crowd dialogue. Generate only the line sets the game's dialogue model actually has.
- **Named progression chains get named audio.** Per chain, the registry row names: the
object sounds, the before-state and after-state sounds, the progress stinger tier, and the completion asset. A change the player causes must sound different afterwards; a quest that changes the world and
sounds the same is unfinished. Where progression follows player actions rather than dialogue, there is no "quest accepted" sound — there is a "the world changed because you acted" sound, in tiers.
- **Journal/log and dialogue presentation**, where present: open/turn/write sounds in
the world's material register, a quiet new-entry notification distinct from progress, and dialogue open/close/advance/select as UI sounds of the same register.

## 11. UI, HUD and menus

Generate UI early, not last: fail sounds must exist before skill tuning starts. Cover, each dispositioned: general (select, confirm, back, cancel, invalid, tab switch); resource warnings (one pulse at
threshold, then state systems take over — no repeating alarms); skill assignment, learn, rank-up and the cast-fail set of section 6; map open/close and marker actions; inventory (section 9);
character/level-up; merchant (cannot-afford is distinct from generic invalid); menus, settings and save (silent is a valid, stated disposition). No UI information may exist only as pitch: pitched families
also differ in timbre or rhythm.

## 12. Bosses, finales, death and the start loop

- **Per finale/major encounter:** approach (ambience thins, music state changes before
the door), entry, boss set (section 7), phase assets, death, completion asset, and a post-encounter world-state change so a finished place sounds finished on return. Boss encounter structure is in
`boss-encounters.md`.
- **Player death:** death sequence, any death-cost feedback the game charges, death-state
music, respawn state. Anything that cannot be carried honestly by sound is silent by disposition, with the reason recorded.
- **Start/continue loop:** the composed start sequence from menu to the starting place;
measure load time in game and record whether load music is needed as a disposition.

## 13. Engine implementation — delivered with the files

Files without a playback design reproduce a file dump with more files. Deliver, with the assets: a bus layout, a parameter list and a priority table, using
`<engine_audio_buses>` from `project.md` (a typical shape: master over music, ambience, world, combat, creatures, player, voice, UI — replace with the project's).

- Limiters on master and combat; separate volume controls with their bus mapping named.
- **Parameters the engine owns (the designer specifies ranges):** pitch and volume
randomisation on repeatable one-shots (identity sounds — motifs, UI confirm, rarest drops — are never pitched); distance attenuation per source class, including any night change; low-pass filter states
(underground, closed interior, weather, map, pause, death) as named states, never baked muffled copies; reverb as a zone property from zone tags, never baked into files except composed finale/death assets.
- **Priority and voice caps:** state a polyphony budget in `project.md` (a number
proposed by the project against its target hardware) and a steal priority: fail sounds, low-health, rarest drop and boss telegraphs first; player cast/impact and damage taken next; enemy telegraphs and
deaths; enemy hits and world objects; ambience events last. The multi-target and rapid-repeat limiters of section 6 are implemented here.
- **Ducking:** a short stated list only (voice over music/ambience; boss telegraph and
rarest drop over combat; the densest beds under high combat; thunder over music). Ducking that pumps is worse than no ducking.
- **Streaming and loading:** music and beds streamed with loop points set; short
one-shots preloaded per zone with the zone's surface, creature and object atoms; neighbouring-region music preloaded at the stated border trigger.

## 14. Mixing targets and accessibility

- Loudness, trim and loop rules come from `audio-generation.md`. Balance in game, in
stated reference scenes (a safe hub, a mid-size combat, an interior/underground room), not in a waveform editor.
- **Caption-critical list:** deliver, with the assets, the list of information sounds
(fail types, rarest drop, per-boss telegraphs, state-change tones, low-health onset, trap tells, summon death, or the project's set). For each, the game must also carry the information visually.
Captions/subtitles for telegraphs are a project decision in
  `project.md`; flag the need, do not build it silently.
- Every information sound must survive a mono fold-down. Stereo width is never the
carrier of meaning.

## 15. Workflow and phases

1. **Audit** (section 3). Report counts; stop if a registry is clearly incomplete.
2. **Matrix** (section 2), one system at a time, in phase order. Every cell dispositioned
before generation starts for that system.
3. **Generate atoms** per `audio-generation.md`: variants by frequency (high: several,
medium: two, rare/unique: one). Never generate a baked mix the matrix lists as layers.
4. **Name and file** with one scheme, context tokens only from registry values, for
example `<system>_<source>_<action>_<context>_<variant>`.
5. **Manifest:** the generation manifest of `audio-generation.md` plus registry ID,
matrix cell, disposition if not generated, variant count, priority class and caption-critical flag, and motif use if any.
6. **Post** per `audio-generation.md`. No file skips post.
7. **In-game test** per system (section 16), in every camera mode in `<camera_modes>`
where the system is heard in the world.
8. **Fatigue pass:** a full playthrough recording per build archetype the project tests
with, reviewed for repetition, masking and clipping; defects filed against matrix cells, not against vibes.

Phase the work so each phase ends with its tests passing: core loop first (hit feedback, fail set, footsteps, starting-zone ambience and music, basic UI), then skills complete, then world complete, then
later regions/bosses/finales, then voice and fatigue. A phase starts by completing its matrix rows, not by generating.

## 16. Acceptance tests

Report per system: pass/fail and evidence. A completion claim without this evidence is the failure this reference exists to prevent.

1. **Skill audit:** pick several skills at random; for each — fail it, cast it, miss,
hit two material classes, let it expire. All must sound correct and distinct.
2. **Day/night:** stand still in several zone types through a full cycle. Dawn and dusk
are audible events; night differs from day in content, not only volume.
3. **Weather:** the same weather in a street, an interior, a dense exterior and an
underground entrance gives distinct heard results, with linked effects (wet steps).
4. **Spam (if `<combat_model>` allows rapid casting):** fastest repeatable skill at
maximum rate for 30 s in each camera mode. No identical repeat in a row, no clipping, the limiter reads as control, not as a bug.
5. **Blind telegraph:** screen off; survive a ranged and a leaping enemy by telegraph
sound alone, in each camera mode.
6. **Loot:** one item per class and rarity on three surfaces. The rarest drop's shimmer
is locatable in 3D by ear.
7. **Construct/summon (as applicable):** summon at cap, replace one, let a placed
construct be destroyed, let a ranged construct cycle until empty or destroyed. No silent event.
8. **Transition:** safe place → exploration → interior/underground → boss → death →
respawn in one session. No mid-bar music fade, no ambience cut without its transition, no silence gap beyond the stated composed exceptions.
9. **Fatigue:** per-archetype playthrough recordings reviewed; defects filed per cell.
10. **Matrix:** the delivered matrix has no blank cells; every `layer`, `parameter` and
    `none` states its mechanism or reason. Checked by reading. Final gate.

## Appendix — registry templates and project decisions

Registry columns (adapt names to the project):

- Skill: `skill_id | name | school | delivery | target | channel? | rank_scaling | repeat_rate | atoms_needed | matrix_cells`
- Passive: `passive_id | name | family/school | trigger | stack? | proc_disposition`
- Enemy: `enemy_id | name | family | size | body_material | movement | attacks | vocal_range | zones | boss? | telegraph_id`
- Zone: `zone_id | biome | interior/exterior | surface_tags | water | reverb_class | danger | bed_id | day_layer_id | night_layer_id`
- Surface: `surface_id | material_family | detail_layer | wet_disposition | zones_used_in`
- Interaction: `id | type (ui/loot/object/progression) | material | rarity_if_loot | before_sound | after_sound | stinger_tier`

Decisions the project records in `project.md` before the dependent phase (state the proposed default used until then and mark dependent work as assuming it): respawn time/state presentation; captions for
telegraphs; where vocals may appear in music; the polyphony budget against target hardware; scope cuts for systems the game does not have (for example no dynamic weather, no swimming) — recorded as matrix
dispositions the project confirms, never made silently by the generating worker.
