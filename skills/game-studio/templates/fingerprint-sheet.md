# Fingerprint sheet template

One sheet per skill or boss, filled on paper before any animation, modelling or retrofit
work. Values come from the controlled vocabularies in `references/skill-animation.md`
section 6 (skills) or `references/boss-encounters.md` sections 3-4 (bosses); inventing a
value means adding it to the vocabulary first, with a definition - never inline in one
sheet. Delete the section that does not apply. Resolve a collision by changing the new
entry, never the shipped one.

```text
<SKILL | BOSS> FINGERPRINT - <id> - <name> - <YYYY-MM-DD>
Registry row: <registry-audit path and row id>; audit date: <YYYY-MM-DD>
Sheet owner: <role>; status: <draft | checked | locked>

SKILL FIELDS (skill-animation.md section 2.1; exactly one value per field)
- F1 Body gesture family: <value>
- F2 Primary shape: <value - the one shape the skill is remembered by>
- F3 Colour pair: <core colour + edge colour; never one colour alone>
- F4 Motion vector: <value>
- F5 Particle behaviour: <birth / life / death, count class>
- F6 Trail type: <value, or "none">
- F7 Ground mark: <value, or "none">
- F8 Timing rhythm: <anticipation / release / linger pattern>
- F9 Light behaviour: <none | steady | pulse | rationed strobe | shadow off>
- F10 Construct silhouette: <summons, placed constructs, traps only; else "n/a">

BOSS FIELDS (boss-encounters.md section 4)
- B1 Archetype pair: <value>
- B2 Signature attack: <the one players name the boss by; unique in the game>
- B3 Movement signature: <the way this boss moves that no other boss does>
- B4 Preferred range band: <band; tool used when the player denies it>
- B5 Vulnerability signature: <how its earned windows are created>
- B6 Add relationship: <value, or "none" - a complete answer>
- B7 Arena relationship: <what it does to its arena>
- B8 Phase change: <the structural change in the final third>
- B9 Silhouette and sound identity: <one readable silhouette; one boss sound set>

DISTANCE CHECK (against the fingerprint matrix, one row per entry)
Nearest neighbours checked: <every existing row; name the closest three explicitly>
| Neighbour | Shared school/archetype or section? | Fields differing | F2/F4 (skills) or signature differs? | Pass? |
|---|---|---|---|---|
| <id> | <yes/no> | <count and field list> | <yes/no> | <yes/no> |
Rules applied (skills): any two differ in at least 3 of F1-F8; sharing school AND
  delivery archetype: at least 4, including F2 or F4; co-equippable in one build: at
  least 4; rank/modifier variants keep the same F2 and F4; an enemy skill differs from
  every player skill in F4 or F7 plus the danger grammar.
Rules applied (bosses): two bosses in the same section differ in at least three fields;
  no two bosses in the game share a signature attack.
Result: <pass | collision - field(s) changed on this sheet: <list>>

IDENTITY TESTS (skill-animation.md section 2.3; on paper, before animating)
1. Silhouette: <pass/fail - tester named it from signature and release frames: yes/no>
2. Grayscale: <pass/fail>
3. Palette-Swap: <pass/fail - if it became an existing sibling, it was a palette swap>
4. Freeze: <pass/fail - each phase distinguishable, per-phase stills listed>
5. Muffled: <pass/fail - reduced size, maximum view distance for <camera_modes>, worst
   visibility context and worst-case background from project.md>
Bosses: tests 1-5 apply to B9/B2 readability as applicable; the encounter-level proof
  is the acceptance list in the boss diagnosis sheet, not this section.
Failed tests: <test, what was changed on this sheet, re-test result - or "none">
```

## Notes

- The sheet is checked against the whole matrix, not only against siblings the author
  remembered; the matrix path is named in the registry audit.
- A locked sheet is an acceptance input: later work that changes a field updates the
  sheet, re-runs the distance check, and records the change in the handoff.
