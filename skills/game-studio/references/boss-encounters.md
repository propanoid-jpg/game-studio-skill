# Boss encounters

How boss fights are diagnosed, designed and accepted so they examine the player instead of outlasting them. Read when designing, implementing, tuning or retrofitting a boss, or briefing a worker to do so. Enemy telegraphs and the danger grammar are in `skill-animation.md` §13; boss sound sets are in `audio-design.md` §§7, 12; the fairness standard and target feelings are in `fun-profile.md`. Project specifics — tiers, builds, `<combat_model>`, `<camera_modes>`, budgets — come from `project.md`.

## 0. The problem: three symptoms, one failure

"Too easy" bosses usually present the same three symptoms. They are one failure: **the boss never contests the player's position, decisions or attention, so the player executes their normal rotation, at their normal range, at their normal pace, until the health runs out.** A fight where the player does what they would do against a training dummy, for longer, is a health bar with a soundtrack.

| # | Symptom | Root cause |
|---|---|---|
| S1 | The boss stands still | No movement *portfolio* and no movement *decisions*: casting is its only verb, casting roots it, and its AI never concludes "my position is now wrong". The player owns positioning for both sides |
| S2 | Its area effects are very easy to avoid | Each effect is single, static, fully telegraphed, placed where the player *was*, with the rest of the arena permanently safe and nothing else happening while the player steps out. Dodging costs nothing |
| S3 | It summons weak adds | Adds are a pause, not a part of the fight: they threaten nothing, protect nothing, cost nothing to ignore or to kill, and interact with the boss not at all |

**Banned obvious fixes** — banned as primary fixes; each may appear only as minor tuning after the structural fixes of sections 6–11 are in:

- **More health.** A stationary boss with double health is the same easy fight at double length — "too easy" converted into "too easy and boring", which is worse.
- **More damage per hit.** Raising area damage does not make effects harder to avoid; it makes the one hit eventually taken feel arbitrary. Difficulty comes from decisions under pressure, not punishment size.
- **Faster telegraphs.** Shortening warning time until dodging is a reflex test converts a design failure into a fairness failure. Telegraph floors (§17) do not move to fix S2.

**Three rules.** 1. **No boss is a bag of attacks.** A boss is a system: archetype, movement portfolio, attack portfolio covering the player's options, arena, phase plan. An attack added without a portfolio reason is decoration. 2. **Every player behaviour has a boss answer, and every boss answer has a player counter.** An answer with no counter is unfair; a behaviour with no answer is a dominant strategy and the fight is already solved (§7.2). 3. **Pressure, not punishment.** The boss wins by forcing movement, spending the player's resources and attention, breaking rhythm and taking preferred positions away — and only then by damaging them. Damage is the receipt for a decision the pressure forced.

## 1. What a boss is

A boss **examines everything its part of the game has taught, in combination, under time pressure**, and is remembered by name and by one mechanic. It must: force movement (a player who stands in one place must fail or be forced to move, by design); force decisions between real alternatives at regular intervals; force attention shifts; teach then test every major mechanic; and end differently from how it began.

A boss is not: a normal enemy with more health and a name; a damage race against a casting statue (S1); a floor-decoration show watched from a safe spot (S2); a summon dispenser whose summons are a separate easier fight nearby (S3); or a cutscene with health bars between phases — phase transitions are gameplay.

**Tiers.** Every boss gets exactly one tier from the project's tier list in `project.md` (a typical shape: mini-boss, dungeon/area boss, major/act boss, optional boss). Tier sets duration and portfolio-depth targets. Invent no tier silently — extend the list first.

## 2. Step zero — the audit and diagnosis

Before redesigning any boss, extract from the game and report counts plus the diagnosis table to the coordinator:

1. **Boss registry** — id, tier, location, archetype if discernible, phases if any, current attacks, current movement behaviour in code terms (any movement decision beyond approach-and-stop?), summon behaviour, arena id, attempt/kill statistics if any.
2. **Boss attack registry** — per attack: owner, range band (§7.1), target logic, telegraph form and duration, damage type, response demanded, internal cooldown, usable while moving or not.
3. **Arena registry** — size, shape, cover, hazards, interactables, entrances/exits and how they close, camera behaviour per `<camera_modes>`, authored for its boss or generic.
4. **Add registry** — per summonable type: attacks, health class, behaviour toward the player, toward the player's constructs/summons (as applicable) and toward its boss; what changes for the boss while it lives and when it dies. "Nothing" is a valid recorded answer — it *is* S3, measured.
5. **Player build registry** — the build archetypes the game actually supports and tests with (at minimum, as applicable: melee, ranged/projectile, channel, DoT/ground-area, and a construct/summon build). Acceptance runs against every one.
6. **Current-fight telemetry**, measured, not estimated: duration; boss stationary time as a percentage; forced moves (the player's position became dangerous or untenable); distinct safe spots used; add uptime and share of player damage spent on adds; deaths and the attack credited. These six numbers are the before-picture.

### 2.1 Diagnosis table — classify every boss before touching it

Answer yes/no per boss, with telemetry or a code reference as evidence.

| # | Question | Yes means |
|---|---|---|
| D1 | At least three movement behaviours beyond approaching the player? | Movement portfolio exists (§6) |
| D2 | Standing in one spot for the whole fight fails? | Position is contested |
| D3 | An attack whose correct answer is not "step out of the area"? | Response variety exists |
| D4 | Any area effect that overlaps, follows up, moves, persists or combines? | S2 partly fixed |
| D5 | Ignoring a summon costs anything measurable? | Adds are a mechanic (§10) |
| D6 | Killing a summon changes the boss fight? | Adds are integrated (§10) |
| D7 | The final third differs structurally from the first third? | Phases exist (§11) |
| D8 | A vulnerability window the player *earns* by an action? | Windows are gameplay (§12) |
| D9 | Behaviour differs against melee and ranged players? | Range bands are real (§7.1) |
| D10 | The boss can reach a player who camps behind cover, at max range or in a corner indefinitely? | Anti-camp exists (§14) |

Scoring (starting default — project decides): 0–3 **rebuild**, 4–6 **retrofit** (sections 6–10 in the workflow order), 7–9 **tuning plus one missing system**, 10 exempt and named as the reference example for its tier.

## 3. Boss archetypes

One implicit template — the stationary caster — is the hidden cause of S1–S3. Each boss gets **one primary and at most one secondary** archetype; its portfolio is built from the pair, not from a global attack pool.

| Archetype | Core verb | Movement character |
|---|---|---|
| Brute | Smash | Advances relentlessly; charges; repositions by leaping to the player |
| Duelist | Duel | Circles, dashes in and out, keeps its preferred band ruthlessly |
| Beast/Predator | Hunt | Stalks at mid-range, pounces, retreats to re-stalk after a burst |
| Artillery Caster | Bombard | **Must still move:** repositions between volleys, retreats from melee pressure, advances when the player hides. A purely stationary artillery boss is forbidden, except where the arena itself is the moving threat and the exception is project-marked |
| Summoner | Command | Keeps distance behind its adds, protects its summoning, turns aggressive when its board is cleared (§10.5) |
| Controller | Deny | Places itself at the centre of the space it denies; advances slowly as its zones grow |
| Guardian/Construct | Hold | Limited range from a post, **by design and visibly tethered** — the one legal near-stationary case; pressure comes from arena and reach, leaving the post is a phase event |
| Trickster/Corruptor | Deceive | Erratic but rule-bound movement on stated triggers; feints only within §8.6 |

Rules: a section of the game whose major bosses share a primary archetype teaches one fight twice; the archetype decides the boss's *weakness of coverage* as well as its strength (compensate with arena and gap-closers, never with a full second portfolio); no attack is borrowed from another boss except basic family attacks — a shared signature is a defect; "caster" never means "stationary": casting is a delivery, stationary is a movement failure.

## 4. Boss identity — the fingerprint

Bosses use the distinctness discipline of `skill-animation.md` §2, at encounter scale. Two bosses in the same section of the game differ in at least three fields; no two bosses in the game share a signature attack.

| Field | Content |
|---|---|
| B1 | Archetype pair (§3) |
| B2 | Signature attack — the one players name the boss by; unique; shown early survivably, examined late combined |
| B3 | Movement signature — the way this boss moves that no other boss does |
| B4 | Preferred range band (§7.1), and the tool used when the player denies it |
| B5 | Vulnerability signature — how its earned windows are created (§12) |
| B6 | Add relationship (§10.4), or "none" — a complete answer |
| B7 | Arena relationship — what it does to its arena |
| B8 | Phase change — the structural change in the final third (§11) |
| B9 | Silhouette and sound identity — one readable silhouette, one boss sound set (`audio-design.md`) |

Never retrofit two bosses with the same fix: fix S1 with *this* boss's B3, S2 with its B2 and B7, S3 with its B6 — or record B6 as none and remove its summons entirely.

## 5. Anatomy of a fight

**Eight beats**, any of which may be short but not absent without a reason in the spec: 1 Approach (arena, soundscape and music change first; the arena is readable) — 2 Introduction (boss seen and identified; B3 and a survivable form of B2 shown) — 3 Establishment (basic portfolio at base tempo, each mechanic alone) — 4 First examination (mechanics combine; first earned window) — 5 Escalation/phase change (structural change, in the open, as gameplay) — 6 Second examination (combinations at full tempo; the player's build is tested) — 7 Finale (aggression and risk peak; the fight visibly *ends* rather than running out) — 8 Death and aftermath (completion, rewards, and a post-fight world-state change where the game records deeds).

**Teach-then-test:** each major mechanic goes shown alone → combined with movement → combined with a second mechanic or adds. Teaching instances are survivable, not harmless: real but reduced damage, reduced *tempo*, never reduced *information*, full telegraphs. Teaching together is at most the first third of target duration — a repeat attempt must be playable at full engagement, not waited through.

**Duration targets** are planning targets judged from telemetry, achieved by portfolio depth, never by health alone: if a portfolio supports two minutes of non-repeating examination, its health budget is a two-minute budget. *Starting defaults — project decides in `project.md`:* mini-boss 45–90 s; area boss 2–4 min; major boss 4–7 min (over ~8 min, split into two examinations with a real intermission rather than stretching one); optional boss up to its section's major-boss ceiling +50%.

## 6. Movement — the fix for S1

Applied first, because movement changes what every other system means.

### 6.1 The movement portfolio (minimum contents)

Every boss (Guardian/Construct excepted, exception recorded) has all five categories; "walks toward the player" fills exactly one.

| # | Category | Purpose |
|---|---|---|
| M1 | Approach/advance | Close to the preferred band when the player is beyond it |
| M2 | Retreat/kite | Restore the band when the player is inside it |
| M3 | Reposition/flank | Change the *angle*: deny a camped spot, leave its own hazard, escape a corner, reclaim the centre |
| M4 | Punish/gap-close | Answer a specific player behaviour (§7.2): camping, casting in the open, hiding behind cover |
| M5 | Phase/arena movement | Movement that is itself a phase or arena event |

### 6.2 Movement decisions

Movement is decided by logged, implementable rules, not a random walk timer. Minimum inputs: **distance band** (player outside/inside the band beyond a stated dwell time — starting default 2 s); **camp detection** (player within a small radius — starting default 3 m — for a stated time while dealing damage → M3/M4 eligible, then prioritised; mandatory — it negates S1's dominant strategy); **line of sight** (player un-targetable behind cover → restore it; the boss never stands casting at a wall); **own position** (cornered, in a player ground effect or its own hazard → M3); **player state** (channelling, healing, rebuilding a construct, back turned to adds → M4 eligible on its own cooldown, so punishment is a learnable rhythm); **phase and add state** (may mandate M5). Log every decision with its triggering rule; a boss whose movement cannot be explained afterwards by its own log has a random walk wearing a portfolio's clothes.

### 6.3 Movement is part of the attack portfolio

At least one movement behaviour is also an attack, fully telegraphed under `skill-animation.md` §13; at least one attack is deliverable while moving or immediately at a movement's end. Casting rootedness is a per-attack property: heavy attacks root, basic attacks of mobile archetypes do not. A boss that can neither move while casting nor attack while moving has a dead zone between states, and the player will live in it.

### 6.4 Movement limits

Movement behaviours have internal cooldowns and maximum frequencies — motion spam is S1 inverted, not fixed. Teleport/blink movement is rationed game-wide: stated trigger, stated cooldown, departure and arrival telegraphs, never the answer to every camp detection. The boss never moves faster than the player can re-acquire it in any mode in `<camera_modes>`; in a first-person-style mode a boss that regularly leaves the frame by its own movement is a camera defect first. Pathing uses the arena's real navigation, tested from every region to every other; stuck on furniture beyond a stated limit (starting default: 2 s) fails the run, and the fix belongs to arena or movement, never to more damage while stuck.

## 7. The attack portfolio — coverage, not a list

### 7.1 Range bands

Fixed vocabulary; radii are set per boss against its arena. **B-Melee** (the boss's own reach; its fastest, most body-telegraphed attacks), **B-Close** (just outside melee: dash/leap/slam landing zone), **B-Mid** (most builds' home; the contested band), **B-Long** (ranged builds' band; answered by movement, honest-travel-time attacks or arena pressure, never by enduring it), **B-Arena** (target is a place or the geometry).

### 7.2 The Coverage Matrix

Built per boss before implementing anything. Rows are player behaviours; each needs at least one answer; for every answer the spec names **the player's counter in one line** (dodge it, bait it, interrupt it, line-of-sight it, kill its source, spend a construct on it, endure it at a cost). An answer with an empty counter field is removed or redesigned.

| Player behaviour | Must be answered by |
|---|---|
| Stands still and deals damage | Camp detection → M3/M4, a growing or predicted hazard, a punish attack |
| Camps one spot/corner | The spot stops being safe: boss takes it, a hazard claims it, or a B-Arena attack targets places |
| Kites at long range | M1 on a rhythm, a B-Long attack with honest travel time, or arena shrinkage |
| Stays in melee permanently | B-Melee arcs, a create-space attack, a punish for greed in recovery |
| Stays behind the boss | A designed turning speed, plus a rear answer for large bosses |
| Fights from behind cover | M3 line-of-sight restoration, a cover-answering attack, or taking the cover position |
| Channels/casts long skills in the open | M4 punish eligibility; an interrupt-capable attack with a fair telegraph |
| Ignores adds | The adds' ignoring cost (§10) — never simply summoning more |
| Kills adds first, always | A boss dangerous alone (§10.5); the add-clear window is the earned reward (§12) |
| Lets constructs do the fighting, as applicable | §13 construct policy, plus pressure on the owner at a stated rhythm |
| Fights from outside the arena | Entry is a commitment (§15): the fight does not run if the player is not in it |

### 7.3 Portfolio minimums and rotation

Every boss: at least one B-Melee/B-Close answer; one movement attack or attack-while-moving; one B-Arena or place-targeted attack; one signature (B2); one attack whose correct response is *not* positional (interrupt, brace, kill-first, use the arena). Archetype emphasis shifts the weights; a Summoner's own portfolio must pass these minimums with its adds removed. Every attack has an internal cooldown. Selection among *eligible* attacks is weighted and rule-based (band, last-used, behaviour flags, phase, add state) and logged — never purely random, which produces impossible and insulting sequences. Combination rules state which attacks may chain and the maximum chain length by tier and phase; combos are rehearsed separately in establishment before they chain. Recovery after a heavy attack or chain is designed: it is where earned damage outside formal windows happens. Two high-pressure attacks are never eligible in the same selection tick during establishment.

## 8. Area effects — the fix for S2

**The seven defects of a trivially avoidable effect:** it targets where the player *was*; it is alone; it covers a small fraction of the arena and the rest is safe before, during and after; it is one moment with nothing left behind; its tempo is uniform and learned in two casts; it does not interact with the boss's position; avoiding it costs nothing — no position, resource decision, uptime or attention. The retrofit removes defects; it does not shorten telegraphs (§0).

### 8.1 The families — use several, never only the first

| # | Family | Pressure | Fairness condition |
|---|---|---|---|
| AE1 | Static targeted (the default) | Basic vocabulary attack | Never a boss's only area family |
| AE2 | Predicted placement | Placed at position + movement vector, capped (§8.2) | A direction change inside the telegraph always escapes |
| AE3 | Staggered set | Sequenced delays: the first drives the player, later ones cover its escape routes | The set as a whole always leaves one real, readable exit |
| AE4 | Moving/travelling area | Wave, rolling hazard, sweeping line, expanding ring: timing and position together | Speed and path fully telegraphed; crossing/circling/outrunning stated, per design |
| AE5 | Persistent hazard | Lands and stays a stated duration, shrinking the usable arena | Readable expiry; obeys §8.2; never outlives its phase without an open rule |
| AE6 | Boss-anchored area | Around/ahead/behind the boss; couples the effect to movement | Anchored geometry follows §6 telegraphs exactly |
| AE7 | Arena-geometry area | Lines, crosses, segmented patterns fitted to *this* arena | Authored per arena (§15) |
| AE8 | Shrinking safe zone | Danger is most of the arena; the *safe* area is the designed element | Safe is telegraphed as clearly as danger (`skill-animation.md` §13) |

### 8.2 Combination, telegraphs, caps, feints

Difficulty comes from **company**: an effect cast while the boss repositions to the escape side, while adds hold the safe zone, or as a movement attack's recovery ends — scheduled by §7.3's rotation, each element shown alone first. The cast costs the boss something (position, recovery, attention), symmetric with what avoiding costs the player; that cost is *positional* (a good spot, a cast in progress, the line to the boss) — never make the dodge action itself expensive. Telegraph duration scales with coverage and company, not only damage; a persistent hazard telegraphs its lifetime and ages visibly; overlapping telegraphs stay separately readable, with family as part of an attack's visual identity. **Fairness caps** — *starting defaults, project decides in `project.md`, then hard limits checked in telemetry:* instantaneous danger covers at most 70% of usable floor, the safe remainder reachable from any position within the telegraph time (finale up to 80% only with a moving safe zone, AE8); prediction capped at position + 1.0 s of current velocity, radius priced knowing this; no effect lands outside the arena or where it cannot be seen telegraphed in any camera mode. **Feints** are allowed only to a project-marked Trickster attack: the change is itself telegraphed before resolution, the resolved area is never larger than the union of the shown forms, and the feint rule is taught alone first. A telegraph that is simply wrong is a lie, forbidden for everyone.

## 9. Pressure and tempo

Count, at every moment, what the player is answering — an active telegraph, a moving boss, a live add with a job, a shrinking zone, a window decision. That count over time is the pressure curve; draw it in the spec against §5's beats (starting default shape: establishment 1, occasionally 2; examinations 2, peaking briefly at 3; finale 3 in bursts with real valleys; pressure 0 only in designed recovery/window beats). A measured flat 1 for minutes is S1/S2 in a graph. Valleys are long enough to act in, follow peaks predictably, and are used by the boss too (repositioning, summoning, taking ground) — a valley is a change of activity, not a shared nap.

**Resource pressure** follows `<combat_model>`: tax what the player actually spends. Where casting is resource-gated rather than cooldown-gated: movement tax (answers that force movement skills spend their cost, on the boss's tempo), interrupt tax (a forced move loses a channel — priced as resource-and-tempo damage even when dodged), re-cast tax (killing constructs, taking ground-effect ground, forcing target switches makes the player buy the same thing twice). Literal resource drain/burn is not a general boss tool — it taxes builds invisibly and unequally; at most one project-marked boss may own it as a signature, fully visible. **Aggression scaling** is per-phase values on selection weights, chain length, movement frequency and recovery length — never a global speed multiplier, which shortens every telegraph's real time and reads as a bug.

## 10. Adds and summons — the fix for S3

**The law: an add is a mechanic the player must answer, with a stated cost for ignoring it and a stated reward for killing it. An add with neither is deleted, and the boss is rebalanced without it.** The law is retroactive to every existing summon in the registry. Expect a substantial share to be deleted or rebuilt; decoration that teaches players to ignore summons is negative content — it makes other bosses' real summons easier too.

### 10.1 One job per add type

| Job | Cost of ignoring it |
|---|---|
| Harasser — pressure on the player, forcing movement while the boss acts | The pressure floor never reaches its valley |
| Shielder/Healer — protects or restores the boss | Damage done is blocked or undone; the fight extends itself |
| Tether/Buffer — channels power to the boss while it lives | The boss is its escalated version for as long as allowed |
| Space-denier — holds or hazards a zone, typically the safe zone or an interactable | The player's best positions are occupied or dangerous |
| Exploder/Chaser — slow, readable, high-consequence approach | It arrives; its detonation is a boss-anchored-class event |
| Construct-hunter — attacks the player's constructs/summons specifically, as applicable | The construct build's investment is dismantled piece by piece (§13) |
| Spawner/Carrier — brings or becomes more adds, or carries a hazard | Target priority itself becomes the decision |

Exactly one primary job per type; a type with two jobs is two types in one model. The job is readable from form and first action — an add whose job its model and behaviour never state has failed before its numbers are read.

**Ignore cost, kill reward, kill cost — stated numbers.** Per type, the spec states: `ignore_cost` (measurably, over its full natural life — if the honest sentence is "very little", the add fails the law); `kill_reward` (what the player gains beyond its absence — a window, posture damage, a resource, a rebound; strong jobs always pay one, felt within seconds); `kill_cost` (the time, resources and position the kill is designed to take, priced against the boss's pressure during it — a kill that takes long while the boss free-casts is a trap option players learn never to take, which returns the design to ignorable at higher cost).

**The boss–add relationship (B6)** — at least one, stated per summoning boss: **Commander** (fights at range behind its adds; mode changes when the board clears), **Protector** (defends its adds; the dive is a designed risk with a designed reward), **Avenger** (an add's death triggers a stated boss attack, movement or brief escalation; kill order becomes a skill), **Symbiont** (boss and adds share a visible resource, both directions), **None** (does not summon — for most bosses, the correct answer).

### 10.2 Summoner rules, spawn discipline, DO/DON'T

A primary Summoner's *own* portfolio passes §7.3 with adds removed; in acceptance it is fought with summoning disabled by a test flag and must remain a real, losing-capable fight, merely a lesser one. Summoning has a cast, a cost and a position (the boss goes somewhere to summon), interruptible or punishable. Wave composition is a designed sequence escalating by job, not a repeated identical pack at health thresholds. Add caps are hard and visible per job; a wave at full cap replaces by a stated rule or waits. Spawns are telegraphed in place a stated moment before adds can act, vary by a stated rule, and never occur in the same tick as a high-pressure combination unless that *is* the designed combination, shown in establishment. Adds path honestly, can be line-of-sighted and stand in hazards; by default the boss's own areas hurt its adds, which the player can weaponise — any immunity is stated in the registry with a reason visible in the add's form. DO: fewer, stronger, jobbed adds (a wave that matters). DON'T: waves of many weak melee adds that die to incidental area damage; a kill whose only effect is one less thing on screen.

## 11. Phases and escalation

Major bosses have at least two structurally distinct phases; the largest tier has at least three beats of change (which may be two phases plus a finale state). Minor tiers may be single-phase if their duration target is met without repetition, stated in the spec. A phase change alters at least **two** of: movement weights, attack portfolio (gained, lost or transformed), arena state, add relationship, vulnerability signature, aggression values. Changing exactly one is a tune, not a phase. Primary triggers are health thresholds the player can see and plan around; secondary behaviour triggers (time, add state, arena state) are visible in the fight when they arm. Phases are clamped to fire in order, each with its introduction, however fast the player's damage is.

A transition has an anticipatable trigger, a form that is itself an event, a stated boss state during it (vulnerable, armoured or absent — one, by design), and an end that deposits both combatants fairly. Full invulnerability is rationed (starting default: at most one transition per fight, short, with something for the player to do during it). The **finale state** (starting default threshold: final 25% of health — project decides) takes more risk: chains lengthen by one, movement frequency rises, recovery shortens by a stated fraction, and defence drops *or* an attack is lost to desperation — a portfolio that narrows as it sharpens. A finale implemented as a speed increase violates §9.

## 12. Vulnerability, stagger and windows

**Working damage** — dealt while also answering the fight — is always available and is never the boss's gift. A design where the boss can only be damaged in windows is a different genre and needs an explicit project decision. **Window damage** is a stated period of substantially higher damageability, the boss stationary by *consequence*.

Every boss has at least one **earned** window type, tied to B5, created by a player action: interrupt its signature or channel; break its posture/shield by the stated damage type or target; bait its movement attack into the arena feature that punishes it; clear its board (§10); use an arena interactable against it; or survive a stated combination sequence unhit. For every window: opening is unmistakable (form, sound and posture together); remaining length is readable on the boss's body, not only a bar; length and frequency are tuned so windows carry a minority of total fight damage for most builds (*starting default: 25–40% — project decides*); and exit is an action (the boss moves or attacks), never a return to an idle cast loop.

Posture/stagger, where used, is diegetic-first (posture, cracks, shield state) with UI as summary only; its rules are uniform across bosses with per-boss values — per-boss *rules* are hidden mechanics and are forbidden. No stagger immunity during exactly the attacks the player is told to interrupt. All boss defences (reduction phases, shields, armour, resistances) are visible in its form while they apply and follow the game's global rules; a hidden boss-specific reduction is a defect. A boss that must resist a build family resists it visibly, in its identity, and gives that family another real job (adds, interactables, posture) for the duration.

## 13. Build fairness

Acceptance runs every boss against the build registry (§2). Design rules that make that passable: **melee** gets honest melee telegraphs, punishable recovery, melee-reachable windows and no permanent close-range hazard a ranged player never sees; **ranged** gets real travel time on long-band answers, cover that works under the same line-of-sight rules as the player's projectiles, and pressure by movement and arena rather than hitscan punishment; **channel** builds get a calculated risk — punish eligibility on a learnable cooldown, never a permanent prohibition; **DoT/ground-area** builds get a boss that moves readably enough that placing an area ahead of it is a practisable skill, and that does not live permanently out of ground effects' reach; **construct/summon builds** get the policy below.

**Target priority:** the boss's default target is the player character. It attacks anything else only under a stated **construct policy** per boss, as applicable: *ignore-then-pressure* (constructs only when they block path or band), *contest* (periodically targets the highest-value construct with a telegraphed attack), or *hunt* (construct destruction is its stated strategy, at a tempo the player can defend — place, protect, rebuild is then the build's real gameplay, priced in §9). Positional built constructs are treated as arena for area patterns. A construct is never a permanent wall the boss paths against forever (§6.4 stuck rule). No attack deletes constructs wholesale at no cost; board clears are telegraphed major events on stated triggers. A boss permanently occupied by a resummonable summon while its owner casts safely has no target logic — fix it here, never by nerfing summons globally.

## 14. Boss AI, adaptation and anti-cheese

Implement the brain as three inspectable, loggable layers: **perception** (what the boss may know, with a stated update interval and reaction delay per tier — it reacts like a creature, not like the simulation reading its own variables), **selection** (§7.3), **execution** (committed behaviours with stated tracking caps; no mid-swing re-deciding beyond them). A monolithic script regresses to standing and casting at the first bug, because that is what a broken boss AI does by default.

The boss may adapt to **patterns over time** (camp dwell, repeated spot, construct or answer) — observations with durations are the legal form of learning. It may **not** react to a single input inside its reaction delay, pre-empt what it could not perceive, or select the perfect frame-level counter; a demonstrated faster-than-perception answer is a fairness failure regardless of how the code produced it. Adaptation has a cap and a decay, and resets on phase change unless a stated grudge is the boss's identity.

Anti-cheese is specific: the audit lists the cheeses testers actually find per boss (corner camping, doorway fighting, pillar looping, out-ranging, construct-walling, geometry safe spots, add-farming) and each gets exactly one designed answer from this reference, tested individually. Never answer cheese with global systems (enrage on fight length, healing when unhit, damage growth over time): those punish slow legitimate play — a learning player's fifth attempt is long *because* they are learning. **Failure default:** if AI or pathing errors, the fallback is basic movement plus a basic attack toward its band, with the failure logged — never standing in place cycling an area cast.

## 15. The arena

The arena registry row must answer: usable floor area relative to the boss's largest effect (§8's coverage is meaningless without it); cover objects and what each blocks; the camp spots players will find, listed in the audit with §7.2's answer verified for each; sightlines per `<camera_modes>` to every spawn and phase location; interactables. **Boss arenas are authored** — placed as fixed units with hand-set cover, hazards and phase geometry. Generation may dress them (materials, minor dressing) and may not move cover, resize the floor or relocate interactables; a variant that changes fight geometry is a new arena and re-enters acceptance. Interactables, where B7 calls for them, cost time, position or a punishable channel; their effect on the boss is visible and stated; they are never mandatory in a way that soft-locks a build that cannot reach or use them; their state resets honestly between attempts. Entry starts the fight's terms, visible before the player commits; death and **runback** follow the game's rules, and the runback is measured in the audit — a long runback through live enemies is a punishment multiplier on every attempt and is priced as such or shortened. Between attempts, boss and arena reset fully and identically.

## 16. Presentation

Every boss attack passes `skill-animation.md` §13 in full. Movement is telegraphed as attack (preparation in form and sound), because charges the player could not read are ambushes. The boss's body is its health and posture language: damage states by phase, the stagger read of §12, the window read of §12 — a boss identical at high and low health withholds information the fight is priced on. Sound covers movement per behaviour (a boss heard repositioning is fair in a first-person-style mode; a silent teleporting boss is not), add jobs, phase and window stingers (`audio-design.md`). Boss scale is a camera problem before an art triumph: test telegraph readability and re-acquisition after boss movement in every mode in `<camera_modes>`, at real camera settings.

## 17. Numbers — lever order and budgets

When a boss is too easy or too hard, adjust in this order, exhausting (testing, not merely touching) each lever before the next: **1 Movement** (portfolio, decisions, frequency) → **2 Portfolio coverage** (add the missing §7.2 answer) → **3 Combination and tempo** (§§8–9) → **4 Adds and phases** (§§10–11) → **5 Timing values** (telegraphs within their floors, cooldowns, recovery) → **6 Stat values** (health within its duration budget, damage within its fairness budget). Levers 1–4 are design, and they are where an easy boss's problem lives; an agent that reaches for numbers first is sent back.

*Starting defaults — project decides in `project.md`, then treated as hard budgets:* damage — no single attack outside a project-marked signature examination removes more than ~35% of an appropriately-geared player's health; a full designed combination, fully failed, may threaten ~60–70%; one-shot kills only as project-marked, fully telegraphed, slow examination attacks with a positional counter taught alone first (default per boss: 0–1). Telegraph floors at reference player speed — dodge a local area/slam 600 ms; dodge a movement attack 500 ms plus honest travel time; interrupt window at least 800 ms of readable cast; reposition out of a large pattern 1000 ms, scaled by distance to the nearest safe ground; kill-first priced by §10, never a sub-second demand. **No hard enrage timers** by default; soft escalation only as a visible, telegraphed portfolio event, late enough that honest learning attempts never meet it (starting default: not before 150% of tier target duration). Boss self-healing as a timer substitute is forbidden except as a Shielder-add mechanic under §10, where killing the source is the counter. Difficulty is calibrated against the builds and gear the game actually gives by that point (the build registry is the standing evidence), and each section's bosses examine that section's new mechanics disproportionately.

## 18. Must-Avoid / Must-Have

**Must-Avoid** (a boss matching a line does not ship, or enters the retrofit queue): stationary caster; floor-decoration offence (AE1 alone, avoidable at walk speed at no cost); decoration summons (any add failing §10); difficulty claimed from health or damage while levers 1–4 are untouched; one-template cloning (same-section bosses sharing primary archetype, signature *and* retrofit fix); phase fraud (a "phase" changing only speed or one value; a transition that is a cutscene or empty invulnerability); window fraud (damage only in windows, or timer-granted windows called earned); any §7.2 row without an answer, or any answer without a named counter; telegraph lies (area shown ≠ area damaged, feints outside §8.2, prediction beyond cap, unseeable landings); input reading inside the perception delay; hidden boss rules; global anti-cheese or stealth enrage; coverage over §8's caps or an unreachable safe remainder; build deletion (a whole family unable to answer with its own tools, or a wholesale board-clear construct policy); add overflow, untelegraphed spawns, or adds acting the tick they appear; hazards, areas or adds persisting past their owner's death or phase without a stated rule; any error state that leaves the boss standing and casting.

**Must-Have:** fingerprint B1–B9 complete with no same-section collision; diagnosis answered with evidence and tier assigned; eight beats present; duration inside its tier target by portfolio depth; movement portfolio M1–M5 with logged decision rules; at least one movement attack and one attack usable while moving or at a movement's end; coverage matrix complete in both directions; portfolio minimums and rotation rules in the attack registry; area effects from at least three §8.1 families with caps verified in telemetry; a pressure curve drawn in the spec and matched by measured runs; every add passing §10, Summoners passing the no-summon test; phases and finale passing §11; at least one earned window with visible defences; telegraph floors and damage budget verified; build matrix run with no family deleted and none trivial; arena authored, camp spots listed with answers, attempt loop and runback measured; presentation pass in every camera mode.

## 19. Workflow and acceptance

Workflow, in lever order: **1 Audit** (§2; counts and diagnosis reported). **2 Classify** (rebuild/retrofit/tune; queue ordered major bosses of each section first — finales define the standard the rest are held to). **3 Fingerprints** on paper; collisions resolved while cheap. **4 Movement pass** — one boss at a time, then immediately fought in greybox before any new attack is built. **5 Portfolio pass. 6 Area pass** (existing areas re-familied; at most one AE1 remains as a basic). **7 Adds pass** (§10's law applied as keep/rebuild/delete; the deletion list is reported explicitly — removed adds are design decisions, not silent savings). **8 Phases and windows. 9 Arena and presentation. 10 Numbers — last**; any number that must leave its budget to make a boss work sends the boss back to the step whose system is actually missing. **11 Acceptance.** One boss end-to-end through steps 4–10 before the next starts step 4 — batching portfolios across bosses before fighting any of them repeats the one-template error at the process level.

Acceptance tests — per boss, per test, pass/fail with evidence; bots use the build registry, human tests use a tester who did not design the boss:

1. **Stand-Still Test.** A bot/tester stands in one spot and executes its damage rotation, moving for nothing. Pass: it dies, or is forced off the spot by telegraphed pressure, within the project's stated time (starting default: 20 s) — in every phase. *This is the direct measurement of S1. A boss that fails it is not done.*
2. **Camp Tests.** Test 1's intent from the audit's camp spots, a corner, behind main cover, at maximum range, and in melee against a caster. Every camp answered by a logged §6.2 rule inside its dwell time; every answer avoidable by its named counter.
3. **Portfolio Test.** Scripted behaviours from §7.2, one per run, repeated runs. Every behaviour meets its answer; no answer fires against a behaviour it was not designed for.
4. **Area Coverage Test.** Telemetry over full fights: coverage against §8's caps; escape-reachability sampled at every telegraph start. No breach; a reachable safe position existed at every sample.
5. **Ignore-The-Adds Test, and its twins.** (a) Adds ignored completely: the stated ignore costs measurably occur; ignoring is a losing or clearly costly line. (b) Adds killed on sight: kill rewards occur and the boss alone remains a real fight. (c) Summoner only: summons disabled by test flag — the fight is lesser but real.
6. **Build Matrix Test.** Every build archetype fights the boss. Every build can win by playing its own game; no build's winning time falls outside the project's band around the cross-build median (starting default: 40%–250%) without a spec reason tied to the archetype's declared, bounded weakness.
7. **Kiting and Looping Test.** Deliberate max-range kiting and pillar looping for the full fight: pressure lands, the loop costs uptime, the boss is never pathing-stuck beyond the stated limit, no teleport spam beyond budget.
8. **Rapid-Cast Stress Test.** The highest-cast-rate build `<combat_model>` allows: the punish rhythm taxes repetition without hard-prohibiting casting; frame time and readability hold.
9. **Phase Integrity Test.** An over-geared build tries to burst through phases: every phase fires in order with its introduction; every mechanic is met once survivably before its combined form.
10. **Movement and Pathing Test.** Scripted runs forcing every §6.2 rule from every arena region: every rule fires, logged; no stuck event beyond the limit; no movement decision unexplained by the log.
11. **Fair-Death Test.** Every death in human runs is reviewed with the player: event, telegraph, counter. Every death is attributed by the player to a readable cause. Any "never saw it" or "that is not what the telegraph said" death is a fairness defect filed against its system, not the player's attention.
12. **All-Cameras Test.** Tests 1, 2 and 11 repeated in each other mode in `<camera_modes>`: same outcomes; nothing unreadable in any.
13. **Duration and Stationary Telemetry.** §2's six numbers re-measured: duration inside tier target; boss stationary time under the project's ceiling outside designed states (starting default: 25% of fight time); forced moves per minute at or above the spec's pressure curve; before/after table filed.
14. **Attempt-Loop Test.** Three consecutive deaths and retries: identical reset, runback within budget, and the tester's report that attempt three felt fairer than attempt one because of what they learned.

## Appendix — templates and project decisions

Boss spec sheet: `id | tier | fingerprint B1–B9 | preferred band | movement portfolio M1–M5 with decision rules | attack registry rows | coverage matrix + counters | area families + caps | add rows (job, ignore_cost, kill_reward, kill_cost, B6) | phases + triggers + finale | windows (B5) | construct policy | arena id | pressure curve | duration/damage/telegraph budgets | acceptance evidence`. Retrofit one-pager per existing boss: diagnosis answers with evidence, classification, fingerprint, and the per-symptom fix named from that fingerprint.

Decisions the project records in `project.md` (state the proposed default used until then; mark dependent work as assuming it): tier list and duration targets; working damage vs window share; stationary ceiling and stand-still clock; enrage position; stationary exceptions beyond the Guardian case, named individually with the arena threat that replaces movement; which bosses, if any, own a one-shot examination attack; which boss, if any, owns a resource-drain signature; build-matrix time band; the coverage and prediction caps of §8.
