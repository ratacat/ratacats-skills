# Lens Pack: Software Audit

Mode: falsify. Targets: repos, features, modules, diffs, runtime paths, data pipelines, UI surfaces, API routes, background jobs, integrations, or any bounded slice of a software system.

Probe grammar: conjectures — specific, testable failure claims ("the retry path drops the last page when the cursor expires"). In this pack, `confirmed` means an open defect or reliability risk.

## Tooling

Check available tools once near the start:

```sh
command -v codedb rg colgrep
```

Use `codedb` when installed:
- `codedb tree` maps files and symbol density.
- `codedb search <query>` finds broad text matches.
- `codedb word <identifier>` finds exact identifiers.
- `codedb find <name>` locates definitions.
- `codedb outline <path>` summarizes symbols in a file.
- `codedb read <path> -L FROM-TO --compact` reads focused file ranges.

Use `rg` for exact text, file enumeration, and project-wide confirmation.

Use `colgrep` for semantic searches such as "retry logic", "cache invalidation", "permission scope", or "feed filtering" when exact words are unknown.

When `codedb` is unavailable, combine `rg` for exact coverage with `colgrep` for conceptual coverage.

## Lenses

Generate 1-5 conjectures per applicable lens unless the user requests a different distribution.

1. Core execution flow
2. Core data flow
3. Data loss / dropped records
4. Freshness / cache / invalidation
5. Filter / query / predicate mismatch
6. Pagination / cursor / ordering
7. Race / retry / backoff / queueing
8. Permission / ownership / visibility scope
9. Serialization / schema / contract drift
10. Source-of-truth confusion
11. UI state hiding backend truth
12. Background job / async worker failure
13. Partial failure treated as success
14. Metrics / telemetry / observability blind spots
15. Compatibility cruft / stale branches
16. Naming drift / concept drift
17. Boundary leakage / caller burden
18. Test blind spots

## Operator Hints

Operators that pay off most on code targets:
- **Negation** — the handler that doesn't exist, the error path with no logging, the state no test asserts.
- **Extremization** — empty input, one item, max page size, clock skew, zero-length batch.
- **Time shift** — what happens on the second run, after a deploy mid-job, when cached state outlives its schema.
- **Stakeholder rotation** — the caller who retries, the operator reading logs at 3am, the migration author six months out.
