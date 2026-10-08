# Worker brief template

Before launching, choose the worker's model tier and runtime ID per SKILL.md "Runtime model mapping" and "Model choice". Copy, fill every `<...>`,
delete lines that do not apply. The brief must be self-contained: the worker cannot see the
coordinator's conversation or memory.

```text
You are a fresh worker on <project> (workspace root <workspace_root>; engine project <engine_root>).
CHUNK MODEL: <runtime-valid model>; complexity: <light | medium | complex>; reason: <current work or concrete failure>
VALIDATION HANDOFF: <focused checks retained; exact routine checks and next fresh Sol/Luna owner after design settles>
ROLE: <Feature/system worker | Art owner | Prep worker | Integration/validation worker |
       QA/test-health worker | Balance worker | Visual polish/review worker | Knowledge keeper |
       Release manager>  (definitions: <skill_dir>/references/roles.md)
Work autonomously. Do not ask questions, do not talk to the user, do not launch sub-workers.

GOAL
<one sentence: the outcome, not the steps>

CONTEXT
- User direction / queue lines: <quote or cite <queue_doc> section and date>
- Knowledge-base pages to read first (if configured): <pages>
- Docs and prior handoffs: <paths>
- Recorded before-data to reuse (never rerun old builds): <paths>
- Decisions already made by the coordinator: <list, with dates>

SCOPE
- Do: <bullets>
- Do not: <non-goals; other owners' areas; performance work; packaging>

FILES
- Owned (you may edit): <paths/globs>
- Shared (targeted edits only, re-read first): <paths>
- Everything else: read-only. Report needed changes as findings.

ACCEPTANCE
- <targeted tests to pass, exact commands>
- <corpus: areas, seeds (fixed + random batch), invalid/fallback counts, hash stability>
- <visual: sketch + locked criteria at <resolutions> (path), all pass, manual review as a player>
- <balance: before/after table from recorded data>
- <docs to update>

RESOURCES
- Evidence folder: <evidence_dir>/<stream>/<task>/ (logs, user data, captures, scratch)
- Engine runs: max <per_worker_runs> concurrent, each under <timeout>, isolated user-data dirs
  (absolute paths), windowed only off-screen and one at a time.
- Exclusive tools: <"You are the owner of slot <X> (<address>); check the connection and scene first;
  never close a session you did not launch." | "You do not own any exclusive-tool slot.">
- Image generation: <budget N, log prompts | none>

WORKER RULES (canonical: <skill_dir>/references/worker-rules.md; read it)
<paste the "Hard limits" block from worker-rules.md>

HANDOFF
- Write <evidence folder>/handoff.txt using <skill_dir>/templates/handoff.md.
- Next owner after you: <e.g. integration worker runs sweeps X, Y>.
- Update knowledge-base pages: <pages | "none; the coordinator will">.
- Return a concise report: status, files, decisions, numbers, test counts, image paths, findings.
```

## Role-specific additions

- **Art owner:** asset list in queue order, prep packet paths (concepts, sketches, locked criteria,
  spec, capture cases), export manifests, wiring target; "one quick in-game capture only; name the
  integration worker's outstanding sweeps in your handoff".
- **Prep worker:** assets, capture environment, resolutions, stability probes, proof the current
  state fails, spec discrepancies to report.
- **Integration worker:** the drop's handoff path, areas, seeds, forced fallback, campaigns,
  comparison iterations and the near-miss list.
- **QA/test-health worker:** only if the user asked; suite scope, windowed/serial list, "stale test
  vs real bug" rule, routing format.
- **Balance worker:** the probe to reuse or build, scenarios, before-data source, levels/areas.
- **Resume after pause:** "Your predecessor was stopped mid-task; edits may be partial. Checkpoint:
  <path>. Verify the tree builds and your files are consistent before continuing."
