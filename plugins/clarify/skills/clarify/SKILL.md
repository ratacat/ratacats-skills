---
name: clarify
description: Run a chained clarity review across a target repo, plan, or work items. Use when the user asks to clarify, defuzz, audit, review, harden, distill, de-duplicate, inspect naming, apply fresh eyes to recent code, or combine code review, plan refinement, deep-module architecture, DRY/cruft, and naming analysis into one reusable workflow.
---

# Clarify

Use this skill to move a target from fuzzy or error-prone toward implementation-ready clarity. The target may be a repository, uncommitted diff, plan, beads/work items, or a mix of plan plus code.

The workflow is intentionally chained. Each pass should feed the next pass with concrete findings, not restart from taste or vague preference.

## Operating Rules

- Start by identifying the target: codebase, uncommitted diff, recent changes, plan, beads/work items, or mixed target. Ask one blocking question only if the target is genuinely unclear.
- Prefer evidence from files, diffs, tests, docs, work items, and execution traces over style opinions.
- Preserve already-firm specifications. Change only the parts that are wrong, ambiguous, duplicated, shallow, or misleading.
- Make small granular edits when editing shared artifacts. Assume other agents may be working in the same tree.
- Do not create churn. Repeated runs should converge: update existing findings, ledgers, issues, or plan text instead of duplicating them.
- If changing code, preserve behavior unless the review finds a real bug. Add or update focused tests when the risk justifies it.
- When producing issues, include title, problem, suggested remediation, and acceptance criteria.

## Chain Overview

Run the passes in this order unless the user asks for a narrower mode:

1. **Frame** the target and evidence.
2. **Fresh-eyes code review** for correctness blunders and root causes.
3. **Defuzz** plans or work items by resolving missing mechanics.
4. **Deep Modules** pass for caller burden, Interface shape, Depth, Leverage, and Locality.
5. **DRY/cruft** pass for duplicated behavior, drift, dead compatibility code, and scattered ownership.
6. **Naming** pass for boundary-aware vocabulary convergence.
7. **Consolidate** into edits, tests, ledger updates, or issues.

Skip a pass only when it clearly does not apply, and say so briefly in the final result.

## Pass 1: Frame

Build a concise target map before judging anything.

For code:
- Inspect git status, recent commits, uncommitted diffs, entrypoints, tests, docs, and core modules.
- Focus uncommitted code and recent changes first.
- Map execution flows and ownership boundaries before extracting or renaming anything.

For plans or work items:
- Identify the goal, actors, data, state changes, external systems, acceptance criteria, and unresolved assumptions.
- Separate firm specifications from low-resolution areas.

For mixed targets:
- Align planned names and concepts with the existing code vocabulary unless the existing vocabulary is the source of confusion.

## Pass 2: Fresh-Eyes Code Review

Review the target as if checking another agent's work for blunders, mistakes, omissions, misconceptions, logic errors, and bugs.

Prioritize:
- correctness and behavior regressions
- uncommitted and recent changes
- unsafe assumptions
- missing error handling or state transitions
- tests that would not catch the suspected failure
- root causes, not symptoms

For each significant finding, include:
- severity or issue level if the repo uses levels
- file and line evidence
- observed or likely failure mode
- first-principles root cause
- smallest safe fix or revision

If implementation is requested or clearly implied, fix the issue after diagnosing it.

## Pass 3: Defuzz Plans And Work Items

Use this pass when the target includes a plan, beads, tickets, PRD, architecture note, or task list.

Look for:
- ambiguity pockets where the "what" exists but the "how" is missing
- implied mechanisms such as "sync," "authenticate," "hydrate," "validate," "route," or "persist" without execution details
- under-specified Interfaces, data handoffs, state boundaries, or ownership boundaries
- logic gaps where intermediate steps are assumed rather than specified

Edit the plan in place only where needed:
- replace broad directives with deterministic mechanics
- add concrete state changes, data structures, API calls, control flow, contracts, or acceptance criteria
- leave resolved sections untouched
- preserve the core architecture unless a real contradiction is found

## Pass 4: Deep Modules

Use the Deep Module principle: a good Module gives callers a small simple Interface while hiding substantial useful Implementation.

Vocabulary:
- **Module**: anything with an Interface and Implementation.
- **Interface**: everything a caller must understand to use the Module correctly: names, types, invariants, ordering, errors, configuration, lifecycle, and hidden assumptions.
- **Implementation**: behavior hidden behind the Interface.
- **Depth**: leverage provided by a small Interface.
- **Seam**: where behavior can change without editing callers in place.
- **Adapter**: concrete Implementation satisfying an Interface at a Seam.
- **Leverage**: what callers gain.
- **Locality**: what maintainers gain when behavior, bugs, tests, and decisions are concentrated.

Find places where callers know too much:
- repeated validation, ordering, error interpretation, retries, or configuration
- callers coordinating the same multi-step sequence
- tests mocking internals instead of proving behavior through an Interface
- pass-through Modules whose Interface is as complex as their Implementation
- fake Seams with only one Adapter and no real variation

Apply the deletion test:
- If deleting a Module removes noise, it may be shallow.
- If deleting it leaks knowledge into many callers, it may be earning its keep.

If the repo has architecture docs, maintain or create `docs/deep-modules.md` only when permitted by the repo's scaffolding rules. Use stable entries:

```md
## DM-001: <short name>

Status: proposed | accepted | implemented | rejected | obsolete
Area:
Domain concept:
Problem:
Deletion test:
Proposed deepening:
Interface shape:
Expected leverage:
Expected locality:
Testing impact:
Decision notes:
Last checked:
```

Prefer one high-confidence deepening over many speculative abstractions.

## Pass 5: DRY And Cruft

Audit duplication as repeated behavior, not repeated text.

Look for:
- duplicate validation, parsing, mapping, retry, logging, headers, JSON envelopes, method guards, or error logic
- one domain concept modeled by hand in multiple layers with different names
- drift such as `q/query`, `count/pageSize`, `dto/model`, route/client variants
- copied helpers with minor edits
- duplicate CLI/API/schema rules enforced in both parser and runtime layers
- old aliases, legacy branches, unused Adapters, stale flags, and compatibility code left behind after replacement

Do not abstract endpoint-specific logic that is semantically different. Abstract shared control flow or assign one clear owner for the shared concept.

For each finding, record:
- files and line evidence
- repeated behavior
- user-visible or maintainer-visible risk of drift
- smallest safe remediation: helper, factory, registry, typed Adapter, stronger owner, or deletion
- whether duplication is intentional and should stay separate

Rank concept drift first, route or CLI plumbing second, cosmetic repeats last.

## Pass 6: Boundary-Aware Naming

Do not begin by renaming. First understand boundaries and vocabulary.

Build a concept map:
- concept
- current names
- locations
- owning Module or boundary
- adjacent concepts that are easy to confuse
- status: canonical, inconsistent, overloaded, ambiguous, or misleading

Check failure modes:
- one word used for multiple concepts
- multiple words used for one concept
- module or folder names that do not match responsibility
- names that blur layer, state, ownership, source/target, internal/external, template/instance, definition/execution, or input/output distinctions
- vague names such as `Manager`, `Helper`, `Utils`, `Processor`, `Handler`, `Engine`, `Core`, `Common`, `Misc`, `Data`, or `Info` unless narrowly justified
- weak suffixes such as `Data`, `Info`, `Payload`, `New`, or `2`
- singular/plural, verb/noun, entity/model/schema/DTO/record drift

Recommend the smallest set of renames that gives the largest clarity gain. Distinguish public/API names, shared internal names, and local names. For each issue, include current name, scope, intended concept, confusion type, recommended action, confidence, blast radius, and timing.

## Pass 7: Consolidate

Merge findings across passes so the output is actionable rather than repetitive.

If reviewing only, return:
- target analyzed
- passes run and skipped
- highest-severity findings first
- root causes
- recommended fixes or issues
- assumptions and residual risks

If editing, make the smallest safe changes, then report:
- files changed
- why the changes improve correctness, specificity, Depth, DRYness, or naming clarity
- tests run and results
- any ledger, plan, or issue updates

If producing issues, use:

```md
Title:
Problem:
Suggested remediation:
Acceptance criteria:
Evidence:
Priority:
```

## Output Templates

Use these shapes when they fit.

### Clarify Review

```md
# Clarify Review

## Target
<codebase | diff | plan | beads | mixed>

## Findings
1. <severity>: <finding>
   Evidence:
   Root cause:
   Fix:

## Plan/Spec Gaps
- ...

## Deep Module Opportunity
- Module:
- Caller burden:
- Interface shape:
- Locality gain:

## DRY/Cruft
- ...

## Naming
- ...

## Issues
- ...

## Assumptions
- ...
```

### Clarify Change

```md
# Clarify Change

## Changed
- ...

## Why
- Correctness:
- Specificity:
- Depth:
- DRY:
- Naming:

## Tests
- ...

## Follow-Up Issues
- ...

## Assumptions
- ...
```
