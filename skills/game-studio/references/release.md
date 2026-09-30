# Release process

A release is a versioned, packaged export of the current game with its notes and notices. It happens
**only after explicit user approval** of that release. Completed streams or a green build never imply
approval. Commands, presets and output paths come from `project.md`.

## Roles

- Coordinator: obtains approval, confirms readiness, briefs one fresh release manager, reviews.
- Release manager: executes the checklist; no gameplay changes beyond version and release gating;
  stops BLOCKED with named owners if a prerequisite is missing.

## 1. Readiness

- [ ] Explicit user approval recorded in `<queue_doc>` with date and scope.
- [ ] Every planned stream is COMPLETE or explicitly deferred by the user; open S0/S1 items are
      resolved or listed as known issues with the user's agreement.
- [ ] Tree builds; import/parse is clean apart from known harmless diagnostics.
- [ ] Targeted suites of every accepted change are green, plus the exported smoke test. Run a full
      sweep only if the user explicitly asked.
- [ ] Playthrough bots run on several seeds; results recorded honestly (not a human playthrough).
- [ ] Save/data format stated: current version, whether a fresh profile is required.
- [ ] Debug grants and debug-only UI are gated out of the export.

## 2. Versioning

- [ ] Version string set everywhere it shows (build settings, title screen).
- [ ] Export preset for the new version; new output folder `<release_dir>/<version>/`; previous
      releases' files untouched.

## 3. Packaging

- [ ] Packaging script takes version/preset/output as parameters rather than overwriting earlier
      releases.
- [ ] Export templates/tools verified against their published checksums.
- [ ] Import and release export with isolated user data; logs free of script/resource errors.
- [ ] Pack audit: every runtime resource loads from the package; tests, tools, editors, raw packs,
      editable sources, caches and player saves are excluded.
- [ ] Contents: executable(s), README (run, controls, save location), release notes, license,
      credit and third-party notices, per-file checksum manifest; archive plus its checksums.
- [ ] Archive verified: every entry extracted and compared with the manifest; no unexpected entries.

## 4. Exported smoke (isolated user data, off-screen window)

- [ ] Launch; title and caption show the version.
- [ ] New profile; open main UI panels and a service; one attack and one skill.
- [ ] Death/retry flow keeps state as designed; save, quit, continue.
- [ ] Debug grants absent.
- Stop at a meaningful smoke; no automated full campaign in the export.

## 5. Release notes

- Features since the previous release (from accepted handoffs).
- **Known issues and limitations**: open S1/S2 items, what is not certified (full human completion,
  balance and feel, audio listening, hardware coverage), save/restart requirement, unsigned build.

## 6. Hand-off and records

- [ ] A release status doc: deliverables with sizes and hashes, validation actually performed, what
      is NOT claimed, save behaviour, rebuild command, log paths.
- [ ] Coordinator reviews, records acceptance in `<queue_doc>` and updates the knowledge base.
- No publishing, uploading or signing unless the user asks.
