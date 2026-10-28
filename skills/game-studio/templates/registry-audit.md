# Registry audit template

The step-zero audit shared by `references/audio-design.md`, `references/skill-animation.md`,
`references/boss-encounters.md` and `references/fun-profile.md`. Extract the real lists
from the game (code, data, design notes); never invent an entry to fill a table. A blank
cell means "not done"; a filled cell with no source is a defect in the audit. Report the
counts to the coordinator before any design or generation work starts.

```text
<PROJECT> - REGISTRY AUDIT - <YYYY-MM-DD>
Reference used: <audio-design | skill-animation | boss-encounters | fun-profile>
Auditor: <role>; evidence folder: <evidence_dir>/<stream>/<task>/
Sources read: <code paths, data paths, design notes - the extraction is checkable from these>
Counts reported: <per registry below; a count that contradicts the game's known scope
  means the audit failed, not the game>

REGISTRY: <name, from the reference's step-zero list>
| <columns exactly as the reference's appendix states for this registry> | source |
|---|---|
| <one row per real entry> | <file / data id the row was extracted from> |
Rows: <N>; with no data: <N, named below>

<repeat the REGISTRY block once per registry the reference requires>

COVERAGE MATRIX
Rows: <first dimension, from the reference>   Columns: <second dimension>
Cell values are dispositions, one per cell:
  covered   - a registry row proves this cell exists and is accounted for
  missing   - the cell should exist and does not; it is a finding, with an owner
  n/a       - the game does not have this cell; the reason is recorded here and
              confirmed by the project, never decided silently by the auditor
| <row> | <column> | <column> | ... |
|---|---|---|---|
| <row> | <covered | missing | n/a - reason> | | |
Completeness: <covered> of <total applicable> cells; missing cells listed as findings.

GAPS AND FINDINGS
1. [S0|S1|S2|S3] <gap> - evidence: <registry row, path or count>.
- Moments / entries with no data: <count and list; a large no-data count is itself the
  first finding, not a footnote>

DECISIONS
- Project decisions this audit depends on: <appendix pointer - the "Decisions" appendix
  of the reference used, as recorded in project.md: <path/section>; state the proposed
  default used until each is recorded, and mark dependent work as assuming it>
- Scope cuts confirmed by the project: <systems the game does not have, recorded as
  matrix dispositions above>
```

## Notes

- One audit file per reference per audit run; a re-audit after major content changes is
  a new file with a new date, not an edit of the old counts.
- Registries feed the design references' own deliverables (coverage proof, fingerprint
  matrix, diagnosis table, moment target table). Work that has no registry row behind
  it is out of scope until the registry is corrected.
