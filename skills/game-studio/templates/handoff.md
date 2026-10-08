# Handoff template

Write as `handoff.txt` in the evidence folder (or the plan's handoff location). Plain, factual,
numbers exact. Claims must be checkable from the listed paths.

```text
<TASK NAME> - <ROLE> - HANDOFF <YYYY-MM-DD>
Status: COMPLETE | PARTIAL (paused/stopped) | BLOCKED (<blocker, owner>)
Evidence: <evidence folder>; index/README if any.
Constraints honoured: <e.g. headless only, max N runs, not the slot owner, no format change>

CHANGES
- <path>: <what changed and why, one line each>
- Tests changed: <path>: <stale -> current behaviour | de-flaked | bounded>, dated comment, no coverage removed.
- Docs updated: <path>: <section>

DECISIONS
- <decision> - reason: <why>; alternatives rejected: <if material>.

RESULTS
- Tests: <command> -> <N pass / M fail / K timeout>; results file: <path>. Logs grep clean: yes/no.
- Corpus: <area>: <seeds> seeds, <invalid> invalid, <fallback> fallbacks, max <t> s, showcase hash stable: yes/no.
- Visual: <criteria set> before <x/y> -> final <x/y> at <resolutions>; nothing loosened; iterations <paths>.
- Manual review: <what was looked at in the actual images, as a player, and what it shows>.
- Balance/other tables: <before -> after, with the before-data source>.
- Images to open first: <3-6 paths>.

NOT DONE / LIMITS
- <what is not verified or not claimed, honestly>

FOR THE COORDINATOR (outside my scope; not edited)
1. [S0|S1|S2|S3] <area/owner>: <finding> - evidence: <path, seed, command, log line>.

NEXT
- Remaining validation: <exact checks/criteria/evidence; settled design or unresolved root cause>.
- Next model: <runtime-valid model and current chunk complexity reason>.
- Next owner: <role and task>.
- Resume point (if PARTIAL): <exact next step, files mid-edit>.
```
