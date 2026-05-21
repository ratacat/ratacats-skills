---
name: name-review
description: Use when reviewing or designing names for plans, beads, work items, architecture docs, codebases, APIs, schemas, modules, states, or domain vocabulary where terminology drift, overloaded concepts, boundary ambiguity, or AI-confusing naming may exist.
---

# Name Review

Boundary-aware naming review improves the system's conceptual vocabulary. Do not begin by renaming. First understand the target, its boundaries, and the concepts that names are supposed to carry.

## Core Principle

A rename is only an improvement when it makes the system easier to reason about across time, contributors, tools, and boundaries.

Optimize for:
- one concept with one primary name
- one primary name that points to one concept
- related concepts forming coherent name families
- contrasting concepts contrasting clearly
- names that remain clear out of context

## When To Use

Use this skill when the user asks to review, improve, audit, defuzz, or design names in:
- a plan, PRD, spec, architecture note, or implementation proposal
- beads, issues, tickets, tasks, or work items
- an existing codebase, package, module, API, schema, CLI, event set, or data model
- a mixed target where plans and code need vocabulary alignment
- any artifact where terms feel overloaded, vague, misleading, inconsistent, or likely to confuse coding agents

Do not use this skill for pure prose copyediting, brand naming, or stylistic polish unless those names also affect system boundaries or implementation concepts.

## Required First Move: Determine The Target

Identify the target before reviewing names. The target is usually one or more of:
- plan
- beads or work items
- architecture docs
- existing codebase
- mixed plan plus codebase

If the user has not clearly specified the target and no artifact can be inferred from context, ask which of these you are analyzing before continuing. If there is an obvious artifact in context, state the target assumption and proceed with a bounded review.

Record:
- artifact type and scope
- evidence inspected
- evidence missing
- whether recommendations are review-only or implementation-ready
- whether public contracts or persisted names are in scope

Default to review-only. Do not edit files, rename symbols, rewrite plans, or modify work items unless the user explicitly asks for implementation.

## Operating Rules

- Be boundary-first, not word-first.
- Familiarize yourself with the system before judging names.
- Preserve names that are already good.
- Prefer convergence over churn.
- Do not recommend style-only renames.
- Do not invent a cleaner vocabulary that is incompatible with the system's actual meaning.
- Do not flatten real distinctions just because two names look similar.
- Treat public APIs, persisted schemas, event names, CLI commands, URLs, package names, and user-facing names as migration-sensitive.
- Ignore incidental local names unless they create real ambiguity or expose a larger conceptual problem.
- Prefer the smallest set of high-leverage renames.
- Accept "no findings" as a valid outcome when the vocabulary is already clear or the available evidence does not justify churn.

## Boundary And System Map

Before evaluating names, build a rough model of the target. Scale depth to evidence and requested scope; do not exhaustively inspect every surface unless the user requested a broad audit, but do not skip this step.

Map:
- major domain concepts
- actors, users, systems, and external integrations
- modules, packages, folders, subsystems, or work streams
- layer boundaries: UI, domain, application, infrastructure, persistence, transport, operations
- ownership boundaries: which module, team, work item, or artifact owns each concept
- lifecycle and state boundaries
- dependency and call relationships
- public interfaces and external contracts
- data model, API, event, job, command, workflow, and storage boundaries
- source and target boundaries for data flow

Distinguish domain concepts from implementation details. Domain names should not be replaced with generic software names unless the domain name is misleading.

## Concept And Vocabulary Map

Create a vocabulary map before proposing changes.

For each concept, track:
- concept
- current names used
- locations or surfaces
- owning boundary or module
- adjacent or easily confused concepts
- status: canonical, inconsistent, overloaded, ambiguous, misleading, or acceptable
- whether the name is public, shared internal, or local

Look across all available naming surfaces:
- directories, files, packages, modules
- classes, types, interfaces, schemas, DTOs, records
- functions, methods, commands, jobs, events
- routes, endpoints, database tables and fields, configs
- tests, fixtures, comments, logs, metrics, docs
- plan headings, milestones, beads, issue titles, acceptance criteria
- diagrams, glossary terms, ADRs, operational runbooks

Always check both directions:
- same concept, different names
- same name, different concepts

Same-name/different-concept conflicts are usually higher priority than simple synonym drift because they cause readers and coding agents to merge concepts incorrectly.

## Review Lenses

Run the naming review through these lenses and cross-link findings back to the concept map.

| Lens | Focus |
| --- | --- |
| Boundary | Does the name expose, hide, or blur the correct boundary? |
| Concept | Does the name point to one real concept? |
| Responsibility | Does the name match what the module or artifact owns? |
| State | Does the name preserve lifecycle distinctions? |
| Layer | Does the name mix domain, UI, persistence, infrastructure, or protocol language? |
| Publicness | Is the rename cost different because the name is external, persisted, or user-facing? |
| Searchability | Can humans and agents grep, discuss, and trace the concept reliably? |
| Family | Do related names form a coherent family without weak suffixes? |

## Naming Rubric

A strong name is:
- specific, not generic
- bounded to the actual responsibility
- distinguishable from nearby concepts
- consistent with the project's vocabulary
- stable across likely implementation changes
- readable in code, docs, logs, diagrams, tickets, and discussion
- searchable and easy to grep
- role-revealing when the role matters

Useful role words include:
- model
- service
- adapter
- policy
- event
- command
- query
- store
- repository
- schema
- record
- request
- response
- job
- projection
- snapshot
- definition
- execution

Use role words only when they add real boundary information. Do not add suffixes as decoration.

## Failure Modes To Check

Look specifically for:
- one word used for multiple concepts
- multiple words used for the same concept
- folder or module names that do not match the responsibility inside
- names that blur ownership, modules, or layers
- names that leak implementation detail into domain language
- domain names replaced by generic software terms
- vague generic names such as `Manager`, `Helper`, `Utils`, `Processor`, `Handler`, `Engine`, `Core`, `Common`, `Misc`, `Data`, or `Info` unless narrowly justified
- weak suffix or prefix distinctions such as `XData`, `XInfo`, `XPayload`, `NewX`, `X2`, `BaseX`, or `CommonX`
- unclear state distinctions: draft versus submitted, requested versus actual, template versus instance, definition versus execution, planned versus observed, source versus target, input versus output, internal versus external
- singular/plural inconsistency
- verb/noun inconsistency
- entity/model/schema/DTO/record confusion
- names whose scope is broader or narrower than the thing they name
- clever names that are not explicit
- abbreviations that hide important concepts
- overloaded roots that force readers to rely on surrounding context
- work item titles that sound elegant but no longer identify a concrete deliverable
- architecture component names that say category but not responsibility
- code names that are semantically right but too expensive to change now

## Target-Specific Guidance

### Plans, PRDs, And Specs

Optimize for implementation-ready concept formation.

Check:
- whether feature names hide multiple concepts
- whether future modules, APIs, schemas, jobs, or events have stable names
- whether product, domain, and implementation terms are mixed
- whether vague terms such as "system", "workflow", "pipeline", "engine", "sync", or "manager" stand in for unresolved design
- whether planned state names distinguish definition, request, execution, observation, and result

Treat plan vocabulary as provisional unless supported by implementation or domain evidence. Prefer vocabulary proposals over hard rename mandates when the design is not yet settled.

### Beads, Issues, Tickets, And Work Items

Optimize for executable work boundaries.

Check:
- whether each title names a concrete deliverable
- whether dependencies and sequencing are visible
- whether the name identifies the right layer: product, domain, infra, migration, test, docs, operations
- whether nearby work items use competing names for the same concept
- whether similar titles actually describe different lifecycle phases
- whether acceptance criteria use the same vocabulary as the title

Do not abstract work item names past the point where a contributor can tell what to build.

### Architecture Docs

Optimize for responsibility and boundary clarity.

Check:
- whether a named component is a domain concept, module, adapter, storage mechanism, protocol, external system, or UI concept
- whether the name describes what the component owns rather than how it happens to be implemented
- whether external systems are clearly distinguished from internal abstractions
- whether diagram labels, prose, APIs, and schemas use compatible vocabulary
- whether broad names like `Orchestrator`, `Coordinator`, `Engine`, or `Service` hide multiple responsibilities

Architecture names should make the next boundary obvious.

### Existing Codebases

Optimize for observed usage and safe convergence.

Start with repo instructions, folder structure, entrypoints, tests, schemas, public interfaces, and recent or relevant code paths. Inspect call sites and adjacent names before judging an identifier.

Classify each name as:
- public or external contract
- persisted or serialized contract
- shared internal concept
- module-private concept
- local incidental symbol

For public, persisted, generated, or serialized names, weigh compatibility and migration cost before recommending a rename. When the rename is correct but expensive, mark it "rename later" or "rename when next touched" unless the current name is actively dangerous. Include a concrete migration note: coordinated replacement, version boundary, schema migration, generated artifact update, release note, or "do not rename now."

### Mixed Plan Plus Codebase

Compare intended vocabulary with implemented vocabulary without assuming either is canonical.

Classify drift:
- plan term absent from code
- code term absent from plan
- same term, different meaning
- different terms, same meaning
- plan abstraction too broad
- code abstraction too broad
- plan stale after implementation learning
- implementation leaked infrastructure terms into domain language

Align future planned names with the existing canonical vocabulary unless the existing vocabulary is itself the source of confusion.

## Recommendation Priority

Prioritize recommendations in this order:
1. core domain vocabulary
2. subsystem, module, package, or architecture boundary names
3. public APIs, schemas, routes, events, commands, and persisted fields
4. shared internal types, classes, services, functions, and jobs
5. lower-level internals and local names

Use this severity scale:

| Priority | Meaning | Typical action |
| --- | --- | --- |
| P1 | Same name for different concepts, misleading boundary, or high-risk public confusion | Rename now or create a concrete migration plan |
| P2 | Same concept has multiple shared names, or responsibility has drifted | Rename now if scoped, otherwise rename when next touched |
| P3 | Scope, state, role, or family naming is weak but contained | Monitor or rename later |
| P4 | Style preference or local polish | Keep |

Do not rename a local symbol if the real problem is the parent concept or boundary.

Usually omit P4 observations unless the user asks for exhaustive notes.

## Output Format

For broad or thorough reviews, produce output in this structure:

1. Target analyzed
2. Boundary and system map
3. Observed canonical vocabulary, or proposed canonical vocabulary when supported by evidence
4. Naming issues found
5. Recommended renames, prioritized
6. Risks to prevent going forward
7. Open questions or assumptions

For narrow or quick reviews, preserve the same logic but compress the output to target analyzed, high-value naming issues, prioritized recommendations, and assumptions.

For each naming issue, include:
- current name
- location or scope
- intended concept
- why it is confusing
- problem type: semantic, boundary-related, state-related, role-related, public-contract, or stylistic
- evidence inspected
- recommended action: keep, rename now, rename later, or monitor

For each rename recommendation, include:
- proposed new name
- rationale
- confidence
- blast radius
- timing: change immediately, change when next touched, or defer
- migration note when public, persisted, generated, or serialized names are involved

If there are no worthwhile renames, say so. A good name review may preserve the vocabulary and only document why it works.

## Common Mistakes

| Mistake | Correction |
| --- | --- |
| Starting with a rename list | Build the boundary and concept map first. |
| Renaming because a word feels generic | Prove it hides a concept, boundary, state, or responsibility. |
| Normalizing all synonyms | First decide whether they are truly the same concept. |
| Treating code as the only evidence | Include docs, tests, schemas, APIs, diagrams, issues, logs, and plans when available. |
| Treating the plan as automatically canonical | Compare plan and code; decide whether the plan is stale, the code is leaky, or both are valid layers. |
| Ignoring public contracts | Mark migration-sensitive names and avoid casual churn. |
| Inventing clever families | Prefer explicit, searchable, boring names that encode real distinctions. |
| Fixating on locals | Find the highest stable boundary that owns the concept. |

## Red Flags

Stop and reframe if you catch yourself saying:
- "This just sounds better."
- "Everything should use one term" before proving concept equivalence.
- "This is only internal" without checking serialization, docs, tests, logs, or generated outputs.
- "The code already knows what this means."
- "The plan name must be right because it came first."
- "The implementation name must be right because it exists."
- "Manager/Helper/Engine is fine because it is common."

## Compact Example

Issue:
- current name: `Job`
- location or scope: plan headings, `jobs` table, worker module, UI task list
- intended concept: three concepts are using one root: durable background execution, user-visible task, and scheduled template
- why confusing: future implementers may merge lifecycle state for template, queued execution, and displayed task
- problem type: semantic and state-related
- evidence inspected: plan milestones, schema draft, worker folder names, UI labels
- recommended action: rename now

Recommendation:
- proposed names: `JobDefinition`, `JobRun`, `TaskCard`
- rationale: separates definition versus execution versus UI presentation
- confidence: high
- blast radius: medium if schema already exists, low if still in plan
- timing: change immediately before APIs and persistence solidify

Naming rule:
- Use `Definition` for reusable configuration, `Run` for one execution, and UI-specific names only at the presentation boundary. These suffixes are justified because they encode lifecycle and boundary distinctions, not decoration.
