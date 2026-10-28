# Asset manifest entry template

One `manifest.json` per generated asset folder (asset-pipeline.md section 6). Copy one
entry per generated file - variants and failures included - and fill every field; a
manifest entry without a licence field is incomplete and the asset is not final
(licences.md section 5). Keep the prepared input that produced the asset beside it.

```text
file: <slug>_<variant>_<seed>.<ext>
asset_folder: <generated_dir>/<type>/<slug>/
asset_type: <image | texture | pbr-set | model | music | sfx | ambience | voice | other>
status: <draft | verified | approved | promoted | failed | prototype_only>
date: <YYYY-MM-DD>

GENERATION
- Prompt: <exact prompt used>
- Negative prompt: <exact text, or "none - architecture uses none">
- Style anchor applied: <yes - <style_anchor> recorded verbatim in the folder | no>
- Seed: <seed, as a number>
- Engine: <engine name and version>
- Model: <exact model file(s) and version/checkpoint, not the family name>
- Workflow: <workflows_dir file name; locked: yes/no>
- Settings: <sampler/settings or generation parameters, size/duration as applicable>
- Input: <prepared input file saved beside the output, or "text only">
- Route used: <Route A - MCP (<comfyui_mcp_server>) | Route B - REST batch script
  (<runner path>, job file <path>, prompt id <id>)>

LICENCE
- Licence status: <cleared | cleared-conditional | gated | prototype-only | banned>
- Licence: <licence name; source checked <licence text / official model card>; date <YYYY-MM-DD>>
- Conditions: <condition written out, or "none"> (travels with the asset)
- Input rights: <project-owned | generated | licensed - source; voice: rights basis>

POST
- Post steps applied: <per the pipeline's post contract, in order, or "none yet">
- Measurements: <tile/seam check, multi-view render, loudness/loop check, mesh budgets -
  as the pipeline requires, with values>

APPROVAL
- Verified by: <role; viewed/rendered/listened personally: yes>
- Approval state: <unreviewed | approved <by, date> | rejected <reason>>
- Promoted to: <runtime asset path and import metadata, or "not promoted">
- Flags: <prototype_only: true/false; known weaknesses: <notes or "none">>
```

## Notes

- Variants change one variable at a time; an approved asset has its seed recorded here
  before variants are made.
- A failed generation still gets an entry: `status: failed`, the server error verbatim
  under Post, and no approval fields filled.
- If the engine is later re-classified, every entry from that engine inherits the new
  status until re-checked; update the entry, do not leave it labelled cleared.
