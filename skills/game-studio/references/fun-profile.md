# Fun profile — emotional intentionality and the kinds of fun

How a project decides which feelings it is designing for, proves the decision moment by moment, and tests it with players without averaging them away. Read when adopting or revising a design direction,
auditing systems for feeling, planning playtests, or briefing design work. The profile constrains the other references: audio carriers are in
`audio-design.md`, skill presentation in `skill-animation.md`, encounter fairness in
`boss-encounters.md`. The project's adopted profile, fences and segment priorities live
in `project.md` (or a profile doc it points to).

## 0. Honest source note — read first

This method operationalises two sources. Credit them exactly, and nothing beyond them:

- **Emotional intentionality:** designing for a *specific* intended emotion produces a
more cohesive experience than designing mechanics and hoping. The formulation used here follows Marc LeBlanc's and Mark Rosewater's teaching as summarised in Riot Games' URF Academy Module 1, "Game Feeling
& 8 Kinds of Fun" — a school lesson plan (2 lessons, CC BY-NC-SA 4.0), not a design treatise or a studio-internal method. Do not cite it for anything section 1 does not list.
- **The 8 kinds of fun** are the **Aesthetics component of the MDA framework**
(Hunicke, LeBlanc, Zubek, 2004), not any one studio's invention.

Two naming traps, mandatory to avoid:

1. **"Game feeling" in that module is NOT "game feel" in Steve Swink's sense.** The module
means *the emotions a game intends to evoke*. It contains nothing about input latency, simulated space, polish, hit-stop, screenshake or juice. If a project wants that material, it commissions it as a
separate, supplementary pass, labelled as its own source — never attributed to the module or to MDA. Do not use the words "game feel" in deliverables without that label.
2. **Everything after section 1 is this plugin's operationalisation** — registries,
tables, protocols and tests written to execute the framework against a real game. It is not source content and must not be presented as such.

Anti-bias rules for anyone applying this reference:

- **More kinds is not better.** Targeting a specific feeling is the claim. A game weakly
serving all eight kinds is worse, under this framework, than one strongly serving three.
- **Do not add a system to serve a kind.** No multiplayer for Fellowship, no crafting for
Expression, no cutscenes for Narrative, unless the project approves it as a scope decision. First exhaust what existing systems can be *tuned and framed* to deliver.
- **Negative feelings are not defects by default.** Frustration is a normal product of
Challenge; the defect category is *unfair* frustration only (section 5).
- **Do not average players.** The same experience produces different feelings in different
players. Every playtest result is reported per segment, never as one mean score.
- **State assumptions.** Until the project answers a decision in the appendix, proceed
with the marked proposal, label dependent work as assuming it, and do not silently harden an assumption into a design fact.

## 1. The source, distilled

Six claims. This is the complete usable content.

- **C1. Games evoke feelings; design the feeling, not just the game.** A designer who
cannot name a system's intended feeling, in plain words, has not finished designing it.
- **C2. The same experience produces different feelings in different players.** One
intended feeling per system is a *target*, not a guaranteed result; a segment will legitimately feel something else.
- **C3. "Fun" unqualified is useless; fun must be typed.** The eight kinds:

| # | Kind | Gloss |
|---|---|---|
| 1 | Sensation | Fun from the senses: audio and visual feedback, effects, reward presentation |
| 2 | Fellowship | Working together, shared experience |
| 3 | Challenge | Meaningful decisions, mastery growing against rising obstacles |
| 4 | Fantasy | Living the experience as a character in that world |
| 5 | Narrative | Experiencing a story as it develops |
| 6 | Discovery | Exploring, finding hidden things, being rewarded for it |
| 7 | Expression | Choices that showcase creativity or individuality — including item builds and combinations |
| 8 | Submission | Relaxing, completing tasks with minimal effort or mental burden |

- **C4. Kinds combine — some well, some badly.** They are not exclusive. A commonly
cohesive package is Sensation + Fantasy + Narrative. Challenge and Narrative are a pair that does not blend well (section 5). Every combination in a profile is argued, not assumed.
- **C5. Frustration is data, not failure — the standard is "hard, but not unfair".**
Frustration frequently emerges from Challenge, and a challenge overcome after frustration can be more rewarding. Designers keep challenges hard but not unfair.
- **C6. The least-recognised kinds are where unexamined games leak players.** Submission,
Sensation, Expression and Discovery are the kinds players least often identify — so they are the ones a team most likely serves by accident or not at all. Audit weights them first.

## 2. Step zero — the audit

Audit before design, as everywhere in this plugin. Extract the real lists; never invent a system or moment to fill a table. A blank cell means "not done"; a cell filled by invention is worse than a blank —
a blank is a finding, an invention is a lie in the audit.

1. **System inventory** — every player-facing system, one row each: `system_id | name |
where in game | player verbs | cost to player (resource / attention / time / risk) | existing spec (audio / animation / none)`.
2. **Moment inventory** — the named moments a player actually lives through (first
minutes, first combat, first unlock, first rare reward, discoveries minor and major, time/weather transitions, entering dangerous places, boss intro/phase/death, player death and respawn, entering a new
area, housekeeping, reading the game's log/journal if any, each distinct failure type). Verify each exists against the real game; add the ones it has, delete the ones it does not, with a note. Columns:
`moment_id | name | scope | frequency per hour (from play or telemetry, else "unknown") | systems involved`.
3. **Current-state fun mapping** — per moment, what it *currently* delivers, with
evidence (a build, a recording, a playtest note), not intention: `moment_id | kinds currently served (observed) | feelings players actually report (else "no data") | evidence`.

Report the counts to the coordinator before designing anything: systems, moments, and moments with *no data* on player feeling. A large "no data" count is a normal early result and is itself the first
finding: without feeling data, section 7 exists.

## 3. The Target Fun Profile — method

The profile is a ranked commitment, adopted by the project and recorded (appendix). Order matters: when two systems conflict, the higher kind wins.

- **Primary (one to three kinds):** what the game is *for*. Each primary names its target
feelings (plain words) and the existing systems that already spend the most on it.
- **Supporting:** kinds that serve the primaries. Each states which primary it serves
and in what way — a supporting kind with no stated primary is an unranked ambition.
- **Bounded:** kinds allowed only inside named fences (section 6 gives the Submission
pattern). A bounded kind outside its fence is a defect, not a bonus.
- **Not targeted:** kinds the game deliberately does not serve, said out loud. Where
players will still feel something adjacent, name it honestly as a **proxy** and label it as a proxy in every deliverable (for example company or belonging in a single-player game are Fellowship-*proxies*,
never Fellowship). Claiming a kind the game does not deliver is a profile defect.
- **The profile line:** one sentence, at the top of the adopted profile, of the form
"This is a \<Primary\> game about \<core experience\> (\<next primary\>), examined / delivered / personalised by \<kinds\>, with \<bounded kind\> fenced to \<fences\> and no \<not-targeted kind\>." If a
proposed change cannot say which word in that sentence it serves, it does not ship under the profile.

Template — the project fills this from its audit; there is no default profile:

| Slot | Kind(s) | Target feelings | Carrier systems (from Registry 1) | Conflict rule |
|---|---|---|---|---|
| Primary | | | | Wins against supporting and bounded |
| Supporting | | | | Serves the named primary; loses to it |
| Bounded | | | | Only inside the fences of section 6 |
| Not targeted | | — | Proxies, labelled, if any | Any system proposing it is a scope decision |

## 4. The Moment Target Table — the core deliverable

For every moment in Registry 2, one row. This table *is* the application of the framework to the game.

| Column | Rule |
|---|---|
| Moment | From Registry 2 |
| Target feeling | Maximum two words, in the source module's exercise format |
| Primary fun | Exactly **one** kind. Two primaries means no primary |
| Supporting fun | Zero or more kinds |
| Anti-fun | The feeling that, if reported for this moment, **fails the row**. A target without an anti-fun is a wish |
| Carrier systems | The real systems that deliver the feeling. If none can be named, the moment is currently *undesigned for feeling*: enter it in the gap report, do not invent carriers |

Worked shape (illustrative rows only — replace every row with the project's real moments):

| Moment | Feeling | Primary | Supporting | Anti-fun | Carriers |
|---|---|---|---|---|---|
| First combat | capable, endangered | Challenge | Sensation | safe repetition | Combat system, hit feedback, telegraphs |
| A major discovery | I found it | Discovery | Fantasy | signposted chore | Discovery stinger (`audio-design.md`), world-state change, log entry |
| Boss death | earned triumph | Challenge | Sensation, Narrative | relief it is over | Victory assets, world change, log/journal |
| Player death | cost, understood | Challenge | — | rage, unfair | Death sequence, cost feedback, cause legibility |
| Housekeeping in a safe place | at home | Submission (bounded) | Fantasy | busywork | Trade, inventory, log — low-effort by design |

Frequency weights priority: a moment felt hundreds of times an hour (a failure type, hit feedback) outranks a moment felt once per area, exactly as high-frequency sounds outrank rare ones in
`audio-design.md`.

## 5. Combination and conflict rules

Argue each combination the profile relies on. The recurring ones, as binding patterns the project adapts to its own systems:

- **Challenge × Narrative (the conflict the source names).** Story comprehension and
combat tension compete for the same attention in the same seconds. Default resolution: narrative is delivered in *safe states only* (safe places, retrospective records, post-action reactions); combat may
*create* narrative facts but may not *explain* them — explanation happens afterwards, in the game's retrospective carrier if it has one. Adjust only as a recorded project decision.
- **Sensation + Fantasy + Narrative (the endorsed package).** They reinforce only if
they agree: every narrative beat needs a Sensation carrier in the world, not only in text (a changed place must look and sound changed — verify the audio side against
  `audio-design.md`); every Fantasy beat must survive Sensation restraint (an
out-of-identity generic sting damages Fantasy more than silence). A beat with text but no world change is flagged `narrative-unbacked`; more than a handful is a profile defect.
- **Expression × Challenge.** A build or choice that removes the game's core decision
(its resource, positioning or reading decisions, per `<combat_model>`) is not Expression succeeding — it is Challenge being deleted by another system. Flag
  `expression-eats-challenge`; resolve by design rules, not number-tuning alone.
- **Expression × Fantasy.** Expression may change *how* the character acts; where the
game has a defined character identity or voice, it may not change *who* the character is. Presentation contradicting that identity is an Expression defect.
- **Discovery × procedural generation (where applicable).** Generated variety is a
Discovery engine and its biggest risk: once a player recognises the repeated unit, they are pattern-matching, not discovering. Discovery value is measured per *unit recognition*: content counts as
discovery only while its payload is not predictable from a previous visit. Every generated unit declares its discovery payload in the audit (secrets, optional areas, unique events, what varies); an empty
payload is a corridor — allowed, but labelled. Guarantee at least one generation-independent discovery beat on first entry to an area.
- **Challenge × Submission, and the frustration budget.** The same player needs both at
different times (C2), so the game signals which mode a space is in *before* the player commits (map, ambience, music state, framing). A space presenting as rest that then punishes is *unfair* in the C5
sense, whatever its numbers say. Frustration budget, stated per project: failures are acceptable; *unexplained* failures are not. Every failure in playtest is classified by the player, unaided, as a
resource cause, a position cause, or "I didn't know that rule" — the third class is a fairness defect with a named owner system, never a player defect.
- **Discovery × Expression.** An optimised build that crosses an area at speed converts
Discovery into a commute. Mitigate by gating discovery payloads behind *interaction* (searching, opening, reading the world), not only traversal — not by nerfing builds.

## 6. Per-kind playbooks

For each kind: adapt these hunts and questions to the project's systems. A kind the profile does not target gets no playbook — only honest proxy labelling (section 3).

- **Discovery.** Hunt: units with empty payloads; secrets findable by only one repetitive
verb; rewards that are only currency (a discovery that changes the world or the record is worth more); content hidden entirely behind unchosen difficulty. Do: make discovery legible after the fact so
players learn searching pays; vary the discovery verb. Don't: mark unfound secrets on the map; let generation hide progression. Playtest question: *"Tell me about something you found that you weren't sent
to find."* No answer means Discovery failed that session, whatever the content count says.
- **Fantasy.** Hunt: text addressing the character as an errand-runner where the game's
fiction says otherwise; UI language in the wrong register; presentation belonging to a different character than the game's defined one; places that do not react to major change. Do: keep the competence
fantasy specific — what this character *does* that the world answers. Don't: import generic bombast (section 5). Question: *"Who were you, in that session?"* First-person answers about deeds mean Fantasy
is working; answers about stats only mean it is absent.
- **Challenge.** Hunt: failures the player cannot attribute; difficulty from missing
information rather than decision pressure; encounters whose honest solution is to leave and over-prepare (once is a tactic, a pattern is a defect); fights in any mode in `<camera_modes>` where fairness
information is visual-only (the blind-telegraph requirement of `audio-design.md` is a Challenge requirement, not only accessibility). Do: apply the C5 checklist per new enemy family and boss — readable
telegraph, attributable failure, fast retry, legible cost before commitment (see
  `boss-encounters.md`). Don't: tune difficulty by raising numbers before auditing
information, or automate away the core decision without pricing the deleted Challenge. Question, after any failure: *"Why did you fail?"* The distribution *is* the report.
- **Sensation.** Most of Sensation is contracted elsewhere: verify each Moment Table row
has a carrier and cross-reference its `audio-design.md` matrix cell where the carrier is audio; audit the visual carriers with the same discipline (reward presentation, discovery presentation, encounter
presentation, time/weather readability, camera behaviour per `<camera_modes>`). A separate Swink-sense feel-execution pass is a project decision (section 0), never smuggled in here. Question: *"What was
the best-feeling moment, physically — a hit, a drop, a place, a sound?"* Sensation nobody can point to did not happen.
- **Expression.** Hunt: options that play identically despite different paper (the
identity tests of `skill-animation.md` define this for skills); one dominant option per class in playtest (the metric is *distinct viable play patterns observed*, never option counts); identity expression
contradicting Fantasy (section 5). Do: protect a deliberately unusual viable build where the audit finds one — it is Expression's proof. Don't: add or remove build-change friction as a tuning default; its
cost is a project decision. Question, to two players of the same class: *"How is your character different from a standard one?"* The same answer twice means Expression is thinner than claimed.
- **Narrative.** Hunt: `narrative-unbacked` beats; records that summarise numbers instead
of deeds; completions that change nothing perceivable on return; story information existing only in missable dialogue (in an action-driven game the *world* keeps the receipt). Do: audit the game's
retrospective record, where it has one, as a story — a reader of only that record should get a coherent account; that audit is cheap and decisive. Don't: write foreshadowing the action systems cannot pay
off, or add a lore database to compensate for thin world-backing. Question: *"What happened in the story so far?"* Deeds retold means Narrative is working.
- **Submission (bounded).** Fences are named places and loops (typical candidates: safe-hub
housekeeping, return travel through cleared areas, one repeatable low-intensity loop per area, which must stay low-*reward* as well as low-effort so it can never become the optimal way to play). Submission
never colonises dangerous first entries, encounters or their approaches. Hunt both directions: accidental Submission inside fences-out (a defect), and accidental *absence* of rest — long stretches with no
low-effort beat (exhaustion leaks the segment C2 guarantees exists). Don't: add retention mechanics (daily loops, login-style rewards) under the Submission banner; fenced rest serves the session. Question:
*"Where did you relax?"* A named place means the fence exists; "nowhere, I just stopped playing" means the session ended early for want of one.
- **Fellowship.** No playbook unless targeted. Proxies are audited only for honesty of
labelling. Any work proposing Fellowship systems stops at a scope decision.

## 7. The playtest protocol — feelings first, categories later

The source module's classroom exercise, unchanged in structure, is a valid playtest instrument: players write feelings on cards, then sort them, then map them to kinds.

1. The player plays a defined slice (name it: area, duration, starting state).
The facilitator does not coach, prompt or explain intentions.
2. **Immediately** after play, before any discussion, the player writes **three feelings,
maximum two words each**, positive and negative both explicitly allowed, on separate cards/fields. This order is the method: feelings first, categories later, the facilitator's hopes never.
3. The player talks through each card: which game moment caused it. Record `feeling →
moment_id` (Registry 2).
4. Only now introduce the eight kinds. The **player** (not the facilitator) assigns each
card a kind. Disagreements with the Moment Table's target are *findings*, recorded as-is.
5. Failure debrief, if failures occurred: the section 5 classification, per failure.
6. The per-kind questions of section 6, in profile order, skipping untargeted kinds.

**Segments (applying C2).** Recruit and report by the segments the project defines (starting default: **Explorer** — came for Discovery; **Mastery** — came for Challenge; **Builder** — came for Expression;
rename or replace per the adopted profile). Rules: never merge segments into an average; a moment hitting its target for its intended segment and missing for others is *working as profiled* — record, do
not "fix"; a moment missing for its intended segment is a defect at the priority of its table frequency. Minimum useful run: two players per segment per slice before any design change is justified by
playtest evidence; below that, label the results anecdotes.

**Scoring sheet:** `session_id | date | build | slice | segment | cards (feeling, player-assigned kind, moment_id) | target kind for moment | match? | failure cause classes | per-kind answers | facilitator
notes`. **Evidence** is cards written before discussion, failure-cause classes, and per-kind answers tied to named moments. **Not evidence:** facilitator impressions, completion rates, performance metrics,
session length alone, or a player's untyped "it was fun" (exactly what C3 rejects).

## 8. Acceptance tests

Run per slice, report per segment. A test passes or fails; "mostly" is a fail with notes. Thresholds marked as defaults are starting defaults — project decides in
`project.md`.

1. **Target-match.** At least two-thirds (starting default) of feeling cards, per intended
segment, map to the Moment Table's primary or supporting kind for the moment that caused them. Below that, the table or the game is wrong — decide which, in writing, per moment.
2. **Anti-fun.** No moment's anti-fun feeling appears on cards of its *intended* segment.
One appearance means investigate; two segments means defect.
3. **Unprompted discovery** (if Discovery is targeted or supporting). Every
Discovery-segment player answers section 6's question with a specific find. Zero answers across a slice means Discovery is content-claimed, not experienced.
4. **Safe-state narrative** (if Narrative is targeted or supporting). No player reports
story information arriving during combat or as an instruction; players can retell the slice's deeds as a story.
5. **Two-characters test** (if Expression is targeted or supporting). Two players, same
class, different builds, same area: an observer can describe how their minute-to-minute play differed. If not, Expression fails for that class regardless of option count.
6. **Fence test.** "Relaxing / switched off" cards map only to bounded-fence moments;
"tense / tested" cards never map to fenced housekeeping. Any cross-mapping is a section 5 legibility defect.
7. **Fair-failure test.** All failures classified by players as resource or position
causes; every "didn't know that rule" failure files a fairness defect with a named owner system before the next run.
8. **Record-as-story test** (where a retrospective record exists). A reader given only
the slice's record retells an account matching what the player actually did. Mismatch means the record is logging, not narrating.
9. **Rest test.** Every player names where they relaxed, or the slice is certified as
intentionally rest-free (an encounter slice). An unnamed, uncertified rest-free slice fails.
10. **Matrix test.** The delivered Moment Table has no blank cells: every moment has a
target feeling, one primary kind, an anti-fun and named carriers — or an explicit
    `undesigned` entry in the gap report with a proposed owner. Checked by reading.
Final gate.

## 9. Workflow, deliverables and standing bans

- **Phase 0 — Audit.** Registries 1–3 (section 2). Counts reported. *No design changes
in this phase.*
- **Phase 1 — Profile adoption.** The project answers the appendix decisions (or accepts
the proposals). Produce the adopted profile (section 3, final wording) and the complete Moment Target Table. Gate: the profile line is signed off or amended by the project.
- **Phase 2 — Gap report and cheap fixes.** Every `undesigned`, `narrative-unbacked`,
  `expression-eats-challenge` and empty-payload entry, prioritised by moment frequency.
Fix first only what is tuning or framing of existing systems. The record-as-story audit happens here.
- **Phase 3 — Playtest.** Section 7 on two slices (one early-game, one encounter/dangerous).
Score per section 8. File defects against Moment Table rows and owner systems, never against "feel" in general.
- **Phase 4 — Iterate.** Changes justified by Phase 3 evidence only, smallest change that
moves the failing test; re-run the failing tests plus Test 10, not the whole suite.
- Out of scope in all phases: new systems (appendix decisions), re-opening the audio or
animation references (cross-reference them; contradictions go to the coordinator).

Deliverables: the audit (registries with counts and evidence links); the adopted profile with its profile line, fences and proxies; the Moment Target Table with no blanks; the prioritised gap report with
owner systems; the playtest kit (facilitator script, cards, scoring sheet); playtest reports per slice per segment with section 8 verdicts; and a short dated decisions log, so the next worker never
re-litigates a settled choice.

Standing bans: do not present any operationalisation here as source content; do not report a kind as "covered" because content exists — covered means a Moment Table row, a carrier, and a matching playtest
card, anything less is `claimed` and the gap report uses that word; do not invent a system, moment or feature to fill a matrix cell.

## Appendix — decisions for the project

Record each answer, dated, in `project.md` or the profile doc. Until answered, proceed with the proposal and mark dependent work as assuming it.

- **D1. Not-targeted kinds.** Proposal: any kind the game cannot honestly deliver is
declared not targeted, with proxies labelled (section 3) — never claimed.
- **D2. Submission fences.** Proposal: the section 6 fence pattern. Confirm which loops
are fenced — in particular whether deliberate low-intensity repetition is a supported rest loop or an accident to be priced out. Blocks: Fence test criteria.
- **D3. Profile order.** Proposal: the audit decides — the primaries are the kinds the
game's architecture already spends the most on, in that order. Reordering changes real budgets (Challenge first raises encounter and failure stakes; Fantasy first raises character/record budget over
breadth). Blocks: Phase 1 gate.
- **D4. Supplementary feel-execution pass.** Proposal: out of scope here; commission a
Swink-sense pass (latency, response, polish) as its own document only if wanted. Blocks: nothing; prevents scope creep.
- **D5. Build-change cost** (where builds exist). Proposal: decide once, record it, and
let all Expression recommendations cite it instead of re-deciding per case.
- **D6. Primary player segment.** Proposal: the segment matching the first primary kind
is primary; slice selection in Phase 3 follows it. Blocks: Phase 3 slice selection.

Source note for the audit trail: MDA — Hunicke, LeBlanc & Zubek, "MDA: A Formal Approach to Game Design and Game Research" (2004). Riot Games, URF Academy Module 1, "Game Feeling & 8 Kinds of Fun" (lesson
plan, CC BY-NC-SA 4.0), whose first lesson draws on Mark Rosewater, "Twenty Years, Twenty Lessons Learned". Where an adopted profile disagrees with a source claim, the source is the source and the profile
is the application — note the disagreement in the decisions log rather than editing the claim.
