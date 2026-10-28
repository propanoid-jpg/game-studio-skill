# Boss diagnosis template

One sheet per boss, completed from the audit before any redesign (boss-encounters.md
section 2). Every answer carries telemetry or a code reference as evidence; an answer
without evidence is unanswered. Banned as primary fixes: more health, more damage per
hit, faster telegraphs - each may appear only as minor tuning after the structural
levers are exhausted.

```text
BOSS DIAGNOSIS - <boss_id> - <name> - <YYYY-MM-DD>
Tier: <tier>; arena: <arena_id>; fingerprint sheet: <path>
Registry rows: <boss / attack / arena / add / build rows in the registry audit: <path>>
Diagnosed by: <role>; classification owner: <coordinator>

BEFORE TELEMETRY (measured, not estimated)
- Duration: <value>   Boss stationary time: <% of fight>
- Forced moves: <count>   Distinct safe spots used: <count>
- Add uptime: <%>; share of player damage spent on adds: <%>
- Deaths and attack credited: <summary>

SYMPTOMS (boss-encounters.md section 0)
- S1 Boss stands still: <present | absent> - evidence: <stationary %, movement code>
- S2 Area effects very easy to avoid: <present | absent> - evidence: <effect families in use>
- S3 Summons are weak adds: <present | absent | no summons> - evidence: <ignore cost measured>

DIAGNOSIS TABLE (D1-D10, boss-encounters.md section 2.1; yes/no with evidence)
| # | Question (short form) | Yes/No | Evidence |
|---|---|---|---|
| D1 | At least three movement behaviours beyond approach? | | |
| D2 | Standing in one spot for the whole fight fails? | | |
| D3 | An attack whose answer is not "step out of the area"? | | |
| D4 | Area effects that overlap, follow up, move, persist or combine? | | |
| D5 | Ignoring a summon costs anything measurable? | | |
| D6 | Killing a summon changes the boss fight? | | |
| D7 | Final third differs structurally from the first third? | | |
| D8 | A vulnerability window the player earns by an action? | | |
| D9 | Behaviour differs against melee and ranged players? | | |
| D10 | Boss can reach an indefinite camper (cover / max range / corner)? | | |
Score: <N of 10> -> classification: <0-3 rebuild | 4-6 retrofit | 7-9 tuning plus one
  missing system | 10 exempt - named reference example for its tier>

FIX PLAN - IN LEVER ORDER (boss-encounters.md section 17; exhaust each lever,
by testing, before the next; a plan that reaches for numbers first is sent back)
1. Movement: <fix named from this boss's B3; portfolio gaps closed>
2. Portfolio coverage: <missing coverage-matrix answers added; counter named per answer>
3. Combination and tempo: <area families and pressure changes>
4. Adds and phases: <per add: keep / rebuild / delete - deletions reported explicitly;
   phase and finale changes>
5. Timing values: <telegraphs within floors, cooldowns, recovery - or "not reached">
6. Stat values: <health within duration budget, damage within fairness budget - or "not reached">
Per-symptom fix: S1 by <B3>; S2 by <B2 and B7>; S3 by <B6, or B6 = none and summons removed>.
Banned-fix check: <no health/damage/telegraph change listed as a primary fix: confirmed>

ACCEPTANCE TESTS TO PROVE THE FIX (boss-encounters.md section 19; per test,
pass/fail with evidence; bots use the build registry, human tests use a tester who
did not design the boss)
- [ ] 1. Stand-Still Test (the direct measurement of S1)
- [ ] 2. Camp Tests (audit camp spots, corner, cover, max range, melee vs caster)
- [ ] 3. Portfolio Test (every player behaviour meets its answer, and no other)
- [ ] 4. Area Coverage Test (caps held; reachable safe position at every sample)
- [ ] 5. Ignore-The-Adds Test and twins (ignore / kill on sight / summons disabled)
- [ ] 6. Build Matrix Test (every build archetype wins by playing its own game)
- [ ] 7. Kiting and Looping Test
- [ ] 8. Rapid-Cast Stress Test (highest cast rate <combat_model> allows)
- [ ] 9. Phase Integrity Test (phases fire in order under burst)
- [ ] 10. Movement and Pathing Test (every movement decision rule fires, logged)
- [ ] 11. Fair-Death Test (every death attributed to a readable cause)
- [ ] 12. All-Cameras Test (tests 1, 2 and 11 in each mode in <camera_modes>)
- [ ] 13. Duration and Stationary Telemetry (before/after table filed)
- [ ] 14. Attempt-Loop Test (reset, runback, attempt three fairer than attempt one)
Tests not applicable: <test, reason recorded - never silently skipped>
After telemetry: <the six BEFORE numbers re-measured, path to the before/after table>
```

## Notes

- One boss end-to-end through the fix plan before the next boss starts its movement
  pass; batching portfolios across bosses repeats the one-template error.
- The diagnosis, classification and deletion list are reported to the coordinator with
  the audit counts, before retrofit work is briefed.
