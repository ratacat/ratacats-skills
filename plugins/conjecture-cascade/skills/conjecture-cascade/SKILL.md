---
name: conjecture-cascade
description: Use when inspecting a software target for hidden bugs, dropped behavior, missing records, stale state, unclear failures, broad reliability risks, or likely issue classes across a bounded scope.
---

# Conjecture Cascade

Goal: Find and surface issues in a bounded software target by testing many plausible failure claims against evidence.

Success means:
- The target scope is explicit.
- Every selected lens receives a real pass.
- Every conjecture closes with evidence and a status.
- Confirmed and unexpected issues appear before lower-value notes.

Stop when: Each selected lens and conjecture has a status, every confirmed issue has evidence, and the final report identifies fixes, residual risks, and incomplete checks.

## Core Idea

A Conjecture Cascade sends many small, falsifiable probes through a software target. Each probe becomes evidence: disproved, fixed, confirmed, intentional, or incomplete.

Use the conjecture list as a search map. Surface unrelated or unanticipated issues when evidence reveals them.

## Targets

A software target can be a repo, feature, module, diff, runtime path, data pipeline, UI surface, API route, background job, integration, plan, or any bounded slice of a system.

Infer the target from the user request. Ask one blocking question when the context lacks a bounded target.

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

## Cascade Discipline

Treat the lens list as the coverage contract. Walk the lenses top to bottom and give each lens a real pass.

For each lens:
1. Name the lens.
2. Generate its conjecture batch, or mark the lens `not-applicable` with a concrete reason.
3. Investigate every conjecture in that batch.
4. Close each conjecture with one status: `disproved`, `fixed`, `confirmed-issue`, `intentional`, or `incomplete`.
5. Record the evidence that supports the status.

Move to the next lens after every conjecture in the current lens has a status and evidence note.

If the scope exceeds one pass, split the cascade into numbered rounds and preserve the unfinished lens/conjecture position in a ledger or handoff note. Resume from that exact position.

## Conjecture Count

Generate 10-100 conjectures depending on scope:

| Scope | Count |
|---|---:|
| Narrow function, diff, or bug report | 10-20 |
| Feature, module, or runtime path | 20-40 |
| Broad subsystem or repo sweep | 50-100 |

Honor a user-requested count when provided. Distribute conjectures across lenses so coverage is visible.

## Lenses

Generate conjectures in batches by lens. Use 1-5 conjectures per applicable lens unless the user requests a different distribution.

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

## Falsification Standard

Close a conjecture with direct evidence from code, tests, logs, runtime output, data, docs, or controlled execution.

Accept absence evidence only when the search method is named and the searched scope covers the mechanism. Mark the conjecture `incomplete` when evidence access is missing, the search scope is weak, or runtime behavior remains untested.

## Status Meanings

| Status | Meaning |
|---|---|
| `disproved` | Evidence excludes the failure mechanism in the scoped conditions. |
| `fixed` | Evidence confirmed the issue and the current session corrected it. |
| `confirmed-issue` | Evidence confirmed the issue and it remains open or needs user decision. |
| `intentional` | Evidence shows the behavior is a deliberate product or architecture rule. |
| `incomplete` | Evidence is insufficient to close the conjecture. |

## Output Matrix

Use a visible matrix so coverage stays inspectable:

| Lens | ID | Conjecture | Evidence Checked | Status | Issue/Fix |
|---|---|---|---|---|---|

Lead the final answer with confirmed issues and fixes. Then include the matrix summary, incomplete checks, and residual risks.

## Quality Bar

Give every lens and conjecture enough attention to produce evidence. Prefer fewer well-investigated conjectures over a larger list with shallow closure.

Treat unexpected findings as first-class issues. The cascade exists to find problems, not to defend the original conjecture list.
