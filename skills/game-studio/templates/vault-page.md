# Vault page templates

Copy one template per page. Fill every field. Filenames are lowercase-kebab-case.
Internal links are always [[wikilinks]].

## Concept / system / mechanic / constraint

```markdown
---
date: YYYY-MM-DD
tags: [domain]
type: concept
status: active
source-path: <repo-relative path, only when derived from a repo doc>
source-hash: <SHA-256 of that file at compile time, only with source-path>
---

# Page Name

<one-paragraph summary>

## Details

...

## See Also

- [[related-page]]

## Counter-Arguments and Gaps

...
```

Use `type: system` for a game system and its contract, `type: mechanic` for a mechanic,
skill or encounter rule, and `type: constraint` for a hard limit or protected decision.
For a constraint, state the limit and its source in the first paragraph.

## Decision

```markdown
---
date: YYYY-MM-DD
tags: [domain, decision]
type: decision
status: active
source-path: <repo-relative path, only when derived from a repo doc>
source-hash: <SHA-256 of that file at compile time, only with source-path>
---

# Decision Name

<one-paragraph summary: what was decided, when, and why>

## Details

...

## Superseded by

<!-- Only when status is superseded: [[newer-decision-page]] -->

## See Also

- [[related-page]]

## Counter-Arguments and Gaps

...
```

A decision is never rewritten to a different outcome. A changed decision gets a new page
and the old page becomes `status: superseded` with a link to it.

## Person

```markdown
---
date: YYYY-MM-DD
tags: [domain, person]
type: person
status: active
---

# Person Name

Role / affiliation.

## Key Contributions

...

## See Also

- [[related-page]]
```

## Source summary

```markdown
---
date: YYYY-MM-DD
tags: [domain]
type: source-summary
source-url: <original URL, for external sources>
source-path: <repo-relative path, for repo docs>
source-hash: <SHA-256, for repo docs>
---

# Source Title

One-paragraph summary.

## Key Points

...

## Entities Mentioned

- [[person-or-concept]]
```

## Filed query answer

```markdown
---
date: YYYY-MM-DD
tags: [domain]
type: query-output
question: "<original question>"
status: filed
---

# <Question as title>

<synthesised answer>

## Sources

- [[page-1]]
- [[page-2]]
```

Promotion moves the file from `wiki/queries/` to `wiki/` and changes `status` from
`filed` to `promoted`. Routine worker lookups are never filed.
