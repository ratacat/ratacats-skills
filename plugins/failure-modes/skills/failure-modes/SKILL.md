---
name: failure-modes
description: Use when reviewing a codebase, uncommitted changes, recent agent work, or one subsystem for hidden bugs, flawed assumptions, drift, duplication, weak tests, broken contracts, or other failure modes.
---

# Failure Modes

Use this skill to conduct a slow, systematic, first-principles review of a codebase. The goal is not to skim for obvious bugs. The goal is to stretch attention across the system from many angles, find failure modes that ordinary review misses, fix small issues immediately when safe, and leave a terminal-readable report with evidence.

## Core Loop

1. Reread the nearest `AGENTS.md`, `CLAUDE.md`, or equivalent repo instructions before judging code.
2. Refresh the whole-codebase map: entrypoints, core modules, generated artifacts, tests, data stores, queues, clients, worker processes, and ownership boundaries.
3. Check `git status`, uncommitted changes, and recent commits first. Treat recent agent-written code as the highest-priority review surface.
4. Pick a pathway from the exploration pathways below. Move slowly through concrete files and call sites.
5. On every pathway, search for all failure-mode families in the schema. Do not limit the pass to one smell.
6. Diagnose each suspect issue from first principles: invariant, inputs, state transition, output, evidence source, user-visible risk, and root cause.
7. Fix safe issues in small edits. Avoid one broad refactor unless the evidence demands it.
8. Verify after each meaningful fix with the narrowest relevant test, typecheck, lint, smoke command, or direct inspection.
9. Continue with a different pathway until time or scope is exhausted.
10. End with the terminal report format in this skill.

## Review Stance

Review as if the code was written by another capable agent that may have made subtle mistakes:

- Ask what would make the code wrong, stale, racey, leaky, misleading, probabilistically invalid, or hard to maintain.
- Look for conceptual errors, logical contradictions, bad implicit assumptions, inaccurate data, hidden state, and terminology drift.
- Prefer concrete evidence over taste. Cite file paths and line-level examples.
- Treat repeated behavior as more important than repeated strings.
- Distinguish accidental duplication from intentionally separate semantics.
- Respect the worktree. Do not revert unrelated changes. Work with concurrent edits.

## Failure Mode Schema

Use this schema for findings. Add repo-specific notes only in the report, not in the skill.

| ID | Family | Look For | Evidence Required | Typical Remediation |
| --- | --- | --- | --- | --- |
| FM-01 | Boundary field loss | Fields accepted, transformed, serialized, or persisted at one boundary but silently dropped at another. | Source field, transformation path, missing consumer or output field. | Share a typed contract, mapper, or projection test across the boundary. |
| FM-02 | Stale generated artifacts | Generated files, manifests, clients, lockfiles, schemas, docs, or bundles that do not match sources. | Source change plus stale generated output or missing generation step. | Regenerate artifacts, add freshness checks, or remove generated file from manual flow. |
| FM-03 | Route or transport ambiguity | Similar URLs, params, headers, encodings, methods, or route builders with divergent behavior. | Two or more route construction sites or transport paths with inconsistent rules. | Centralize route construction or define one transport contract. |
| FM-04 | Partial numeric parsing | `parseInt`, `parseFloat`, unary coercion, defaulting, or range checks that accept junk or reject valid values. | Input examples, parser behavior, validation gap, affected downstream logic. | Use strict parsing and explicit bounds; test malformed and boundary inputs. |
| FM-05 | Boolean and string normalization | Boolean-ish strings, case, whitespace, empty string, null, undefined, or enum aliases normalized inconsistently. | Multiple normalization sites or missing edge-case tests. | Create one parser/normalizer at the boundary and reuse it. |
| FM-06 | Schema strictness mismatch | Runtime schema, API contract, type definitions, database shape, and docs disagree on optionality or extra keys. | Contract pair that disagrees plus a real path between them. | Align schemas and types; add contract tests for strict and permissive cases. |
| FM-07 | Weak tests around risky changes | Tests assert happy paths, static types, mocks, or snapshots while missing the behavior that can fail. | Risky code path plus missing negative, boundary, concurrency, or integration test. | Add behavior-focused regression tests before or with the fix. |
| FM-08 | Async cancellation and timer bugs | Timers, abort signals, intervals, promises, event listeners, streams, or cleanup paths that can leak, fire late, replay unexpectedly, or miss terminal event shapes. | Lifecycle path where cleanup, abort, event handling, or error propagation is incomplete. | Use explicit cleanup, cancellation propagation, `finally`, and lifecycle tests. |
| FM-09 | Queue claim races | Workers, leases, retries, idempotency, job state, backoff, or concurrency controls that can double-run or lose work. | State transition diagram or interleaving that shows race or lost update. | Make claims atomic, idempotent, and observable; test concurrent workers. |
| FM-10 | Cache mutation and recovery | Cached objects mutated by consumers, stale fallback data, degraded-mode recovery, cache invalidation gaps, or deferred/backing state missing from snapshots. | Mutability path, stale state path, missing backing state, or recovery condition. | Clone or freeze data, define freshness policy, and test recovery from stale/degraded states. |
| FM-11 | Composite key collisions | Keys built by concatenation, lossy normalization, ordering assumptions, or partial identifiers. | Two distinct logical entities producing same key or ambiguous key parsing. | Use structured keys, delimiters with escaping, tuples, or typed key builders. |
| FM-12 | Sentinel value bugs | Magic strings, empty arrays, `-1`, `0`, `null`, `undefined`, empty cursors, or status sentinels overloaded across meanings. | Sentinel meaning differs across layers or branches, such as zero meaning both "none" and "replay all". | Replace with explicit tagged state, enum, or separate fields. |
| FM-13 | Errors hide evidence | Errors catch and replace useful context, swallow causes, log too little, or report misleading summaries. | Failure path where original evidence is lost or misclassified. | Preserve cause, context, and actionable metadata while keeping secrets redacted. |
| FM-14 | Redaction gaps | Secrets, tokens, cookies, keys, credentials, or private data emitted through logs, errors, reports, URLs, caches, or telemetry. | Unredacted sensitive value path or inconsistent redaction helper. | Centralize redaction and test representative sensitive shapes. |
| FM-15 | Generated contract drift | Generated clients, schemas, API bindings, migrations, or codegen outputs drift from runtime contracts. | Contract source and generated consumer disagree. | Regenerate, add drift checks, and make generated artifacts part of the build gate. |
| FM-16 | Shallow health checks | Health/readiness/status endpoints verify process liveness but not real dependencies or degraded states. | Health path that stays green while a required dependency is unusable. | Add dependency-specific checks or separate liveness/readiness/degraded signals. |
| FM-17 | Fallback misdiagnosis | Fallback paths hide root failures, make bad data look valid, or recover silently when user action is needed. | Fallback branch and missing distinction between degraded, empty, stale, and failed. | Make fallback state explicit and observable; fail closed when correctness matters. |
| FM-18 | Runtime artifact freshness | Runtime reads files, snapshots, caches, generated data, or persisted state without checking freshness or compatibility. | Artifact producer, consumer, version, timestamp, or invalidation gap. | Add versioning, mtime/hash checks, migrations, or rebuild triggers. |
| FM-19 | External API shape drift | Assumptions about third-party responses, SDK behavior, pagination, streaming event shapes, errors, limits, or auth shape not validated. | External boundary lacking validation or test fixture for changed shape, partial responses, or alternate terminal events. | Validate at boundary, add fixtures, and handle unknown or partial responses explicitly. |
| FM-20 | Terminology drift | Same concept named differently across modules, or same term used for different concepts. | Name variants and paths where they map to one concept or diverge silently. | Choose one owner and vocabulary; rename or add adapter only at true boundaries. |
| FM-21 | Type-trust blind spots | Static types, mocks, or casts used as proof while runtime data can violate the assumed shape. | Cast, mock, or type-only test near untrusted input. | Add runtime validation and tests with malformed real inputs. |
| FM-22 | Retry and throttling blind spots | Retry loops, rate limits, backoff, jitter, idempotency, stale retry metadata, and permanent failures treated inconsistently. | Failure/retry path that can spam, duplicate work, give up too early, or keep stale error state after success. | Use bounded retry policy with idempotency, classification, metadata cleanup, and observability. |
| FM-23 | Projection cleanup gaps | Derived data, indexes, search documents, denormalized tables, or UI projections not updated or removed with source changes. | Source lifecycle path without matching projection lifecycle. | Centralize projection updates or add reconciliation/cleanup tests. |
| FM-24 | Query tests inspect strings only | Database, search, or filter tests assert generated query text or builder shape but not execution semantics or edge cases. | Test proves text/build shape while runtime semantics remain untested or filters remain advisory-only. | Add execution tests against representative data, including boundary cases. |
| FM-25 | Overloaded state fields | One field represents status, phase, error, retry state, lifecycle, or user-visible state at once. | Branches assign incompatible meanings to the same state field. | Split fields or introduce explicit state machine with transition tests. |
| FM-26 | Output/status propagation loss | CLIs, subprocesses, tests, or workers emit large or final output or success/failure status through stdout, stderr, pipes, streaming responses, shell wrappers, or child-process capture. | A pipe/capture/wrapper path can miss bytes, truncate structured output, lose final lines, mask non-zero exit status, or differ from direct-command or redirected-file output. | Await drain/close, propagate child exit status, use explicit status capture or pipefail, write large artifacts to explicit files/transports, and add pipe-vs-file regression tests. |
| FM-27 | Implicit execution-scope binding | Code infers project, profile, account, credential, daemon, cache, or config from cwd, global symlinks, env defaults, process registries, install paths, or hidden defaults. | Two plausible scopes exist and an action, status, load, or mutation uses the wrong one or hides which one was used. | Resolve scope explicitly, show it in status/diagnostics, require disambiguation for mutations, and test multi-scope cases. |
| FM-28 | Predicate/filter semantics drift | Filters or selectors implemented across API, CLI, UI, database, cache, worker, or search layers have different invalid-input handling, boolean algebra, missingness rules, or execution semantics. | Same logical filter behaves differently across two boundaries, or malformed filters silently become no-op, empty, widened, or advisory-only filters. | Centralize predicate parsing and execution, reject invalid filters, and test execution semantics with representative data. |
| FM-29 | Durable append corruption and skip-on-parse recovery gaps | Append-only JSONL/log/event stores where writers do not guarantee record boundaries and readers skip malformed records while dedupe, status, or resume state depends on parsed records only. | Corrupt physical rows plus a reader skip/fallback path that hides existing logical records or creates duplicates/missing state. | Use atomic append helpers, newline/record-boundary checks, repair tooling, parse-error visibility, and recovery tests with malformed rows. |
| FM-30 | Clock/time authority drift | Caller-supplied `now`, as-of, deadline, expiry, retry, historical render, or date-window logic mixes with runtime wall clock or invalid-time fallback. | Two time authorities can affect one output, or invalid/missing time silently falls back and changes IDs, windows, persistence, expiry, or audit state. | Choose one clock owner per boundary, reject invalid time inputs, pass clocks explicitly, isolate historical outputs, and use deterministic clock tests. |
| FM-31 | Speculative state writes | Durable state, topology, cache, projection, or workflow transitions are written from intended action, heuristic inference, or optimistic assumption before observed confirmation. | A prediction or intended state becomes durable without a confirming observation, reconciliation path, or ambiguity marker. | Split intended vs observed state, require confirmation before durable facts, mark speculative state explicitly, and add reconciliation tests. |
| FM-32 | Validate-then-write stale snapshot | Validation, uniqueness, dependency checks, or safety checks run before acquiring the lock/transaction or before the final write snapshot. | Mutable state can change between check and write, allowing stale validation, duplicate writes, dangling references, or sidecar drift. | Move validation inside the write transaction, compare fingerprints, make side effects atomic, and test concurrent/stale-snapshot writes. |
| FM-33 | Cache validator dependency omissions | ETags, cache keys, fingerprints, or freshness metadata depend only on primary route params or primary rows while responses embed joined, projected, permissioned, or configured data. | A dependency change can alter the response body without changing the validator or cache key. | Include all response-affecting dependencies in validators, version projections, and test cache behavior after dependency updates. |
| FM-34 | Bootstrap readiness order gaps | Read/status paths are callable before migrations, seeds, worker warmup, lease recovery, cache hydration, or config loading complete. | Startup or first-read returns a valid-looking empty/offline/healthy result before required initialization has run. | Separate liveness, readiness, warming, empty, failed, and degraded states; gate reads or mark warming; add cold-start and recovery tests. |
| FM-35 | Untrusted lifecycle control | External, model, client, or job input directly controls IDs, TTLs, expiry, priority, retry windows, next actions, lease duration, or state transitions. | The consumer trusts lifecycle metadata from an untrusted producer and can repeat, stale, skip, reorder, or over-extend work/actions. | Stamp lifecycle metadata at the runtime boundary, bound values, consume one-shot actions, and test stale/replayed producer output. |
| FM-36 | Pooled resource state contamination | Resource pools for sessions, connections, credentials, profiles, clients, workers, or tenants reuse identity, auth, health, cooldown, or readiness state across logical owners. | A pool member selected for one owner can carry another owner's state, or verification checks the wrong authority. | Bind resource identity explicitly, verify with owner-bound readback, quarantine mismatches, and test pool reuse/cross-owner cases. |
| FM-37 | Declared capability wiring drift | A feature, mode, enum value, command, route, flag, error code, or documented capability is declared but not reachable, not implemented in all dispatch paths, or silently falls through. | Declaration or contract surface plus missing handler, client method, route branch, exhaustive check, or execution test. | Make declarations executable through exhaustive dispatch, contract-to-runtime tests, and fail-closed unknown capability handling. |
| FM-38 | Observation probe trust gaps | Probes, readbacks, status checks, snapshots, logs, screenshots, or API/browser observations are partial, stale, hanging, or wrapper-truthy but treated as conclusive facts. | Low-confidence observation marks success, failure, readiness, or identity without confidence, timeout, or semantic assertion. | Define probe authority and confidence, preserve raw evidence, require semantic success checks, and test false-positive/partial/hanging probes. |
| FM-39 | Shared resource isolation gaps | Process-global singletons, handles, caches, temp paths, ports, schemas, fixtures, locks, or coalescing helpers bleed state across calls, tests, tenants, or lifecycle phases. | Shared resource reuse lacks reset/ownership boundaries, or tests pass only because order or ambient state hides the bug. | Scope resources per owner/test, close/reset shared handles, make coalescing semantics explicit, and add cross-call/order/concurrency tests. |
| FM-40 | Operator mutation proof gaps | Admin, CLI, review, repair, migration, or manual tooling mutates live/durable state without explicit scope, guarded transition, durable proof, preview, or auditable outcome. | Operator path can report success while a side effect failed, race with another operator, or mutate more than the intended target. | Require explicit scope and confirmation, use atomic guarded transitions, record before/after proof, and test stale/racing/failed side effects. |
| FM-41 | Reference data provenance gaps | Hardcoded constants, curated datasets, seed files, scraped facts, generated summaries, fixture values, thresholds, or docs are used as truth without source, timestamp, unit, confidence, or refresh path. | Data affects behavior, tests, docs, or decisions and lacks provenance/freshness evidence or contradicts an authoritative source. | Store source, timestamp, unit, and confidence; validate against authoritative sources; mark unverified data; and add refresh/reconciliation checks. |

Overlap notes:

- Use FM-27 when the action chooses the wrong scope; use FM-36 when the chosen pooled resource carries wrong owner state.
- Use FM-15 for generated artifacts drifting from runtime contracts; use FM-37 for declared capabilities not wired through dispatch.
- Use FM-16 for readiness/status that ignores dependencies; use FM-38 when any observation is overtrusted as proof.
- Use FM-08 for lifecycle cleanup/cancellation; use FM-39 when shared resources bleed across owners, calls, tests, or phases.
- Use FM-32 for stale validate-then-write flows; use FM-40 when the risky path is operator/admin/manual mutation proof.
- Use FM-18 for stale runtime artifacts; use FM-41 when reference data lacks source authority, units, confidence, or verification.

## Patterns And Code Smells

Apply these across every pathway:

- Bad implicit assumptions: hidden assumptions about ordering, uniqueness, idempotency, freshness, user intent, clocks, environment, filesystem, time zones, locale, network reliability, or third-party stability.
- Scope ambiguity: hidden assumptions about which project, profile, account, credential, daemon, cache, config, or install path a command or runtime action targets.
- Conceptual errors: the code models the wrong domain concept, conflates two concepts, or encodes a policy at the wrong layer.
- Logical violations: branches that cannot be reached, branches that must be reached but are missing, contradictory conditions, broken invariants, or impossible states made possible.
- Probability errors: treating uncertain data as certain, ignoring base rates, overfitting to one example, using stale measurements as current truth, or presenting estimates without uncertainty.
- Data accuracy risks: stale fixtures, inaccurate constants, unverified scraped data, missing units, rounding errors, lossy conversions, or undocumented thresholds.
- Boundary drift: API, CLI, database, worker, cache, client, config, schema, and docs disagree.
- Predicate drift: filters, selectors, query builders, and post-filters do not share one parser, one validity model, and one execution semantics.
- Ownership ambiguity: no single module owns a shared concept, contract, transport, concurrency primitive, schema primitive, or data lifecycle.
- Clock ownership ambiguity: caller-supplied time, runtime wall clock, historical/as-of views, deadlines, expiry, and retry windows mix without an explicit owner.
- Speculative persistence: intended, inferred, optimistic, or model-proposed state is written as durable observed fact before confirmation.
- Append-log fragility: append-only stores lack atomic record boundaries, visible parse failures, or recovery paths for malformed records.
- Cache validator gaps: cache keys, ETags, freshness markers, or fingerprints omit joined, projected, permissioned, or configured dependencies.
- Dead compatibility code: old aliases, legacy branches, deprecated adapters, stale feature flags, dual config formats, or unused migration paths.
- Copied helpers: similar helpers with small edits that should have one owner plus parameters.
- Rebuilt envelopes: repeated JSON response shapes, headers, method guards, logging context, auth checks, or error wrappers.
- Duplicated validation: the same CLI/API/schema/runtime rule enforced in multiple places with drift risk.
- Lifecycle trust gaps: untrusted producers supply IDs, TTLs, priorities, retries, leases, next actions, or expiry values that the runtime should own.
- Pooled state bleed: shared sessions, handles, credentials, profiles, clients, or workers carry identity, health, readiness, or cooldown across owners.
- Declared-but-unwired capability: enums, flags, routes, modes, commands, or docs advertise behavior without exhaustive runtime dispatch.
- Probe overtrust: snapshots, logs, readbacks, screenshots, health checks, or wrappers are treated as proof without semantic success checks.
- Shared-resource bleed: globals, fixtures, temp paths, ports, schemas, caches, or coalescers survive across tests, calls, tenants, or stop/start cycles.
- Operator proof gaps: admin/CLI/manual paths can mutate state or report success without scope, atomicity, durable evidence, or audit trail.
- Reference provenance gaps: constants, fixtures, seed data, generated summaries, thresholds, or docs lack sources, units, timestamps, or confidence.
- New abstraction not adopted: old code remains after a better shared abstraction was introduced.
- Cosmetic abstraction risk: abstraction proposed only because strings repeat, while behavior or semantics differ.

## DRY And Cruft Audit

Use this when the review turns toward extraction, consolidation, and dead-code removal:

1. Map entrypoints, core modules, and ownership boundaries before judging duplication.
2. Trace real execution flows. Repeated behavior matters more than repeated strings.
3. Ignore test boilerplate and generated files unless they leak into production design.
4. Look for the same validation, parsing, mapping, retry, or error logic in multiple places.
5. Look for the same domain concept modeled by hand in multiple layers with different names.
6. Treat drift as a smell: `q` versus `query`, `count` versus `pageSize`, `dto` versus `model`, route variants, and client variants.
7. Flag helpers copied with minor edits. They usually want one owner plus parameters.
8. Flag modules that rebuild the same JSON envelopes, headers, logging, or method guards.
9. Flag duplicate CLI/API/schema rules enforced in both parser and runtime layers.
10. Flag dead compatibility code: old aliases, legacy branches, unused adapters, stale feature flags.
11. Check whether old code remains after a newer abstraction was introduced but not adopted.
12. Prefer removing duplication at the highest stable boundary, not with the smallest helper.
13. Do not abstract endpoint-specific logic that is truly different. Abstract shared control flow.
14. Demand one clear owner for shared concepts: contract, schema primitives, concurrency, transport.
15. For each finding, record the files, repeated behavior, and user-visible risk of drift.
16. Suggest the smallest safe remediation: shared helper, factory, registry, typed adapter, or deletion.
17. Note when duplication is intentional and should stay separate because semantics differ.
18. Rank findings by blast radius: concept drift first, route/CLI plumbing second, cosmetic repeats last.
19. Prefer concrete evidence over taste. Cite line-level examples from each duplicate site.
20. End with actionable issues: title, problem, suggested remediation, and acceptance criteria.

## Exploration Pathways

Run multiple pathways. Each pathway is a complete review method, not a single query. During each pathway, actively check every failure-mode family in the schema.

### Pathway 1: Execution Flow Down And Up

Pick one user-facing or machine-facing entrypoint. Trace downward through parsing, validation, state changes, side effects, external calls, persistence, projection, response, logging, and cleanup. Then trace upward from a deep function back to its callers.

Look for:

- Boundary field loss, schema drift, overloaded state, and external API shape assumptions.
- Error paths that lose evidence or turn failures into misleading success.
- Cleanup, cancellation, retry, and cache recovery behavior.
- Pooled resources, observations, and operator actions that need owner-bound proof.
- Tests that do not match the traced behavior.

Output: a flow map, findings, small fixes, and tests or verification.

### Pathway 2: Term And Concept Search

Pick a domain term, config key, status value, route segment, field name, or error phrase. Search for all variants and inspect surrounding code, not only exact matches.

Use this to find:

- Terminology drift.
- Same concept modeled under different names.
- Sentinel values and overloaded states.
- Duplicate validation, parsing, mapping, and projection logic.
- Generated contract drift.

Output: canonical meaning, variants found, true differences, accidental drift, and remediation.

### Pathway 3: Folder Sweep

Pick one folder and read every source file in it at human speed. Build a local map of responsibilities before editing. Include neighboring tests, fixtures, generated artifacts, and index files.

Look for:

- Files that share ownership of the same concept without a clear boundary.
- Copied helpers, stale branches, and dead compatibility code.
- Boundary assumptions repeated across sibling modules.
- Missing tests for the highest-risk branches.

Output: folder responsibility map, findings, intentional duplication notes, and small cleanup patches.

### Pathway 4: File Plus Related Code

Pick one file. Read it fully. Then inspect imports, exports, callers, callees, tests, fixtures, runtime config, generated consumers, and documentation references.

Look for:

- Invariants that callers violate.
- Public functions with private assumptions.
- Mismatched type/runtime/schema behavior.
- Stale references after recent changes.

Output: file-centered dependency map, violated assumptions, fixes, and verification.

### Pathway 5: Uncommitted And Recent Change Audit

Start with `git status`, uncommitted diffs, and recent commits. Review the changed code as if it was produced by several agents with partial context.

Look for:

- Edits that solve one branch but miss adjacent paths.
- Refactors that changed names without changing all consumers.
- New helpers not adopted everywhere.
- Tests that assert the new implementation rather than the intended behavior.
- Build artifacts, generated files, or docs left stale.
- Declared capabilities, operator paths, or shared resources not wired through every runtime path.

Output: reviewed files, root causes for defects, small revisions, and remaining risk.

### Pathway 6: Contract Boundary Walk

Pick one boundary: CLI to runtime, UI to API, API to database, worker to queue, service to external provider, config to runtime, or generated client to server. Walk both sides.

Look for:

- Field loss, strictness mismatch, transport ambiguity, and runtime artifact freshness.
- Duplicate validation in parser and runtime layers.
- Missing runtime validation for untrusted inputs.
- Fallbacks that hide contract failures.
- Declarations that do not have exhaustive runtime dispatch or execution tests.

Output: contract table, mismatches, chosen owner, and contract tests.

### Pathway 7: Data Lifecycle Walk

Pick one entity or data object. Follow create, validate, normalize, persist, cache, read, update, project, search, retry, archive, and delete flows.

Look for:

- Projection cleanup gaps.
- Cache mutation and stale recovery defects.
- Composite key collisions.
- Status overload and sentinel values.
- Data accuracy and provenance risks from rounding, units, timestamps, stale fixtures, unverified sources, or missing refresh paths.

Output: lifecycle diagram or bullets, missing transitions, fixes, and reconciliation tests.

### Pathway 8: Test-To-Production Inversion

Start from tests. Pick tests that are brittle, shallow, mocked heavily, snapshot-heavy, or string-only. Walk from the test to production code and ask what the test does not prove.

Look for:

- Static types trusted without runtime validation.
- Database/search query tests that inspect strings but not execution semantics.
- Missing negative, malformed, concurrent, timeout, retry, or stale-data cases.
- Tests that pass while the user-visible behavior can be wrong.
- Shared fixtures or probes that prove wrappers, not semantic behavior or isolation.

Output: test gap list, new or revised regression tests, and bugs found by strengthening tests.

### Pathway 9: Error And Observability Walk

Pick errors, logs, metrics, reports, status endpoints, health checks, and diagnostics. Trace how failures are classified and exposed.

Look for:

- Redaction gaps.
- Errors that hide root evidence.
- Shallow health checks.
- Fallbacks that report success or emptiness instead of degraded/failure states.
- Missing context needed to debug production failures.
- Probes, snapshots, readbacks, or operator proofs that do not establish the claimed fact.

Output: failure taxonomy, evidence-preserving fixes, redaction checks, and health/readiness improvements.

### Pathway 10: DRY And Ownership Walk

Search for repeated behavior, not repeated text. Trace whether two modules are enforcing the same concept, rebuilding the same control flow, or drifting on vocabulary.

Look for:

- Duplicate validation, parsing, mapping, retry, throttling, logging, route, and error logic.
- Helpers copied with minor edits.
- Shared concepts with no clear owner.
- Shared resources or pools with no clear owner, reset boundary, or identity binding.
- Old compatibility branches after new abstractions landed.
- Places where semantics differ and duplication should remain.

Output: ranked DRY/cruft findings, evidence from each duplicate site, smallest safe remediation, and issue stubs.

## Search Rule Seeds

Use these as starting points. Adapt directories and languages to the repo.

```sh
rg "payload|params|filters?|options|metadata|serialize|normalize|mapper|to[A-Z]|from[A-Z]" .
rg "generated|do not edit|manifest|version|contract|schema|client|dist|build|bundle|compiled" .
rg "URLSearchParams|headers|query|params|route|router|endpoint|method" .
rg "parseInt|parseFloat|Number\\.parse|Number\\(|Boolean\\(|\\+[^+]" .
rg "true|false|yes|no|enabled|disabled|trim\\(|toLowerCase\\(|toUpperCase\\(" .
rg "z\\.object|schema|validate|type |interface |as const|unknown|any|cast" .
rg "setTimeout|setInterval|AbortController|addEventListener|removeEventListener|finally|timeout|cleanup" .
rg "claim|lease|retry|backoff|jitter|worker|concurrency|inFlight|lock|idempot" .
rg "cache|stale|degraded|fallback|clone|structuredClone|invalidate|ttl|fresh" .
rg "join\\(|split\\(|key|id|hash|dedupe|composite|delimiter" .
rg "sentinel|-1|null|undefined|empty|unknown|pending|status|state|phase" .
rg "catch|throw new|cause|error|warn|debug|silent|swallow" .
rg "redact|secret|token|password|cookie|authorization|bearer|csrf|private" .
rg "health|ready|live|status|diagnostic|probe|degraded" .
rg "provider|external|api|sdk|pagination|rate limit|429|shape|response" .
rg "TODO|deprecated|legacy|compat|alias|adapter|feature flag|unused" .
rg "stdout|stderr|pipe|pipefail|tee|spawn|exec|exitCode|process\\.exit|drain|flush|console\\.log" .
rg "cwd|process\\.cwd|HOME|PROFILE|ACCOUNT|credential|env|global|daemon|default" .
rg "filter|where|selector|include|exclude|postFilter|kind|type|tag|limit" .
rg "append|jsonl|ledger|event log|JSON\\.parse|malformed|truncated|dedupe|resume" .
rg "Date\\.now|new Date|now|asOf|deadline|expiry|ttl|window|yesterday|tomorrow" .
rg "optimistic|infer|predicted|assume|intended|observed|confirmed|reconcile" .
rg "validate|exists|unique|lock|transaction|atomic|write|apply|sidecar" .
rg "etag|cacheKey|fingerprint|lastModified|304|projection|joined|summary" .
rg "ready|readiness|startup|init|seed|migration|warm|hydrate|worker|lease" .
rg "ttl|expires|priority|lease|retry|next action|sequence|model|client" .
rg "pool|session|connection|credential|profile|tenant|owner|quarantine|mismatch" .
rg "enum|mode|flag|command|route|capability|handler|dispatch|fallthrough|unreachable" .
rg "probe|snapshot|screenshot|readback|status|observed|verified|confidence|timeout" .
rg "singleton|global|fixture|tmp|temp|port|schema|handle|coalesce|shared" .
rg "admin|operator|manual|repair|migration|preview|dry-run|confirm|audit|proof" .
rg "source|provenance|confidence|verified|unverified|updated_at|generated summary|fixture|seed|constant|threshold|unit" .
```

Pair text search with structural inspection:

- Inspect all nearby code around each match.
- Search for synonyms and alternate spellings.
- Search tests and generated artifacts as well as production code.
- Use `git diff` and `git log` to understand why code changed.
- Follow imports, exports, callers, and callees before deciding.

## First-Principles Diagnosis

For every serious finding, write down:

- What invariant should always hold?
- What inputs can violate it?
- Where is the boundary that should enforce it?
- What state transition happens?
- What output, side effect, or user-visible behavior becomes wrong?
- What evidence proves the issue is real?
- What root cause allowed it: missing owner, wrong abstraction, stale artifact, weak test, invalid assumption, or drift?
- What is the smallest fix that removes the cause without broad churn?
- What test or verification would fail before the fix and pass after?

## Fixing Rules

- Prefer a small edit plus focused verification over a sweeping rewrite.
- Keep behavior-preserving cleanup separate from behavior-changing fixes when practical.
- Delete dead code when a newer implementation fully replaces it.
- Do not add fallback paths to hide uncertainty. Make degraded, empty, stale, and failed states explicit.
- When consolidating duplication, choose the highest stable owner for the shared behavior.
- When two paths only look similar but mean different things, document that they intentionally stay separate.
- Do not rely on static types alone at untrusted boundaries.
- Do not weaken tests to make the code pass.

## Severity Rubric

- P0: Data loss, security exposure, runaway side effects, hard crash, infinite loop, or core workflow failure with no workaround.
- P1: Major feature or subsystem broken, silent logic error, persistent stale state, serious contract drift, or high-risk security/availability issue.
- P2: Isolated edge case, confusing behavior, missing retry/cleanup, weak test around real risk, or degraded workflow with workaround.
- P3: Cosmetic issue, minor naming drift, low-risk cruft, or missing documentation/test around currently working behavior.

## Terminal Report Format

End with a report in the terminal. Keep it concrete and evidence-backed.

```md
# Failure Modes Report

Scope:
- Repo:
- Review target:
- Time budget or stopping point:
- Repo instructions read:
- Commands run:

Context Map:
- Entrypoints:
- Core modules:
- Boundaries:
- Generated/runtime artifacts:
- Tests and fixtures:

Pathways Run:
- Pathway:
- Files inspected:
- Failure-mode families checked:
- Notes:

Findings:
| ID | Severity | Files | Failure Mode | Evidence | Root Cause | Fix | Verification |
| --- | --- | --- | --- | --- | --- | --- | --- |

DRY/Cruft Findings:
| Severity | Files | Repeated Behavior | Drift Risk | Suggested Remediation | Acceptance Criteria |
| --- | --- | --- | --- | --- | --- |

Actions Taken:
- Small edits:
- Deleted code:
- Tests or checks added:

Verification:
- Passing:
- Not run:
- Blocked:

Residual Risks:
-

Proposed Issues:
- Title:
  Problem:
  Suggested remediation:
  Acceptance criteria:
```

If no issues are found, say that explicitly and include the strongest remaining test gaps or residual risks.

## Common Failure Modes In The Reviewer

Avoid these reviewer mistakes:

- Skimming because the code looks familiar.
- Searching exact strings only and missing synonyms.
- Treating types as proof of runtime correctness.
- Trusting mocks more than production behavior.
- Calling duplication harmless without tracing drift risk.
- Abstracting too early because text repeats.
- Ignoring generated artifacts, fixtures, and runtime files.
- Letting fallbacks hide failed, stale, or degraded states.
- Fixing symptoms before naming the root cause.
- Making one large edit that mixes unrelated concerns.
