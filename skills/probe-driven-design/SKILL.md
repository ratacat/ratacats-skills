---
name: probe-driven-design
description: "Use when a consequential design, architecture, process, or policy choice depends on unknowns that reasoning alone cannot settle, or when an investigation plan may be over-scoped, prematurely branched, or full of experiments whose results may not change a decision. Not for questions answerable by a straightforward lookup alone."
metadata:
  category: tools
  blurb: "Use the smallest useful probe to ground consequential decisions before uncertain detail hardens into design."
  keywords:
    - probe
    - prototype
    - uncertainty
    - design
    - discovery
    - fog of war
    - decision making
    - graph workflow
---

# Probe-Driven Design

Navigate the fog of war by making consequential uncertainty concrete before designing around it.

**Core principle:** Make uncertainty observable before filling it with plausible detail.

Use the smallest useful probe: the least costly action that can ground the next design decision without simplifying away the thing being decided. Stop when that decision is grounded enough for its stakes and reversibility, or when another probe would cost more than it could change.

## Vocabulary

| Term | Meaning |
| --- | --- |
| **Design decision** | A consequential choice about what or how to build, organize, or operate. |
| **Probe** | A bounded action taken to obtain decision-relevant information. It may be a targeted inspection, query, interview, walkthrough, trial, simulation, enactment, or prototype. |
| **Learning prototype** | A temporary version or enactment of a candidate design used inside a probe. Not every probe uses one, and not every temporary probe artifact is a prototype. |
| **Result** | What the probe actually observed or gathered, with enough provenance and material limits to judge it. |
| **Learning** | A change in understanding supported by the result. Record it separately when the interpretation is non-obvious, consequential, or disputed. |

`Result` names what came back. `Learning` names what that result changes in the understanding of the problem. Never present an interpretation as though it were the result itself.

## Boundary

This skill selects and sequences probes around a design decision. It applies to code and non-code work.

Prefer existing evidence when it is adequate. Documentation, direct inspection, a targeted query, or reconstructing an existing trace may settle the question without constructing anything. Do not build an artifact merely to make the work feel experimental.

This skill decides whether a prototype is needed and what its question requires. When a `prototype` skill is available, use it for the mechanics of building throwaway code while preserving the fidelity rules here. Use `conjecture-cascade` when broad coverage across many lenses is the primary objective; use probe-driven design when probes are selected and sequenced because their possible results could change a decision or activate a branch.

## Judgment Gates

Before creating probes or a probe program, classify each proposed item:

| Class | Treatment |
| --- | --- |
| Known correction | Implement with deterministic acceptance; no learning question or result state. |
| Observation needed now | Measure only what the current decision needs. |
| Probe needed now | Put on the active decision path. |
| Conditional question | Keep as a question and dependency only; design it if activated. |
| Independent opportunity | Track outside the current decision path. |
| No decision leverage | Drop it. |

Only work needed to ground or safely execute the current decision belongs on its active path. A known correction is a prerequisite only when leaving the defect in place would make the probe unsafe or contaminate its interpretation.

A probe is warranted only when all are true:

1. A concrete decision is current, not merely imaginable.
2. At least two plausible results lead to materially different next actions.
3. Existing evidence cannot ground the decision at its stakes and reversibility.
4. The probe's expected decision value justifies its cost, delay, and operational exposure.

If a condition fails, do direct work, use existing evidence, retain a conditional question, separate the opportunity, or stop. Do not create a probe whose main output is permission to ask another already-known question.

Evidence is also budgeted. Every required field, artifact, manifest, threshold, safety study, or prerequisite must name the interpretation or safety decision it can change. If removing it would not make the result unsafe or materially less interpretable, remove it. A reusable evidence platform requires demonstrated recurring consumers; one probe defaults to the light closeout below.

## Core Loop

### 1. Choose the next decision and question

Identify the next consequential design decision rather than attempting to settle the entire system.

Separate what actual constraints already support from what remains provisional. Continue designing only where known constraints support the structure or where reversal is cheap. A conventional-looking boundary is not evidence that it is stable, and a detail shared by every imagined candidate may still be a shared guess. If implementation must begin, label the cheapest reversible choice provisional rather than promoting it to architecture.

Ask:
- What are we pretending to know?
- Which unknown could reverse, split, or substantially reshape this decision?
- What would become expensive to undo?
- What could be learned only through contact with the concrete problem?

### 2. Select the smallest useful probe

Choose the least costly probe whose limitations will not invalidate the decision.

Prefer probes that:
- test an assumption with a high cost of being wrong
- distinguish between competing explanations or approaches
- unblock several downstream decisions
- expose a real boundary, handoff, failure mode, or operating constraint
- can be run quickly and reversed cleanly

Before running it, ask: **What plausible result would change the decision or next branch?** If none would, the probe is theater.

Design the next probe. Give later branches only a question and dependency until they become ready; do not yet specify their method, inputs, schedule, or acceptance criteria. Their design depends on results not yet available. A multi-stage probe program planned through unresolved dependencies repeats the same mistake as a detailed architecture through fog.

For a nontrivial probe, make these four things recoverable from the work:
- the decision and primary question
- the probe
- what must be real and what may be simplified
- which plausible results would change the decision or next branch

These need not be headings or a separate document. Add a result form or stop condition only when it prevents ambiguity, cherry-picking, or wasted work.

Do not invent sample sizes, thresholds, schedules, confidence levels, or acceptance criteria to make a probe look rigorous. Use supplied constraints, or identify such values as calibration choices that the first pass must inform. An invented number is a design decision smuggled in as a parameter.

Do not combine the stages merely to save a planning round. Characterization ends with facts and a next question. A design comparison begins only if those facts make the choice consequential. An intervention begins only after one candidate and its bounds are grounded.

### 3. Run the probe

Match fidelity to the question. A performance question needs a representative workload; an interaction question needs a convincing interaction; an organizational question may need a real handoff between people. Everything the question does not touch may be simplified or omitted.

When the probe uses a learning prototype, make the dimensions under investigation credible enough that the result can be trusted. Temporary describes lifecycle, not acceptable sloppiness. If maintainability, interface depth, recovery, or failure behavior is under investigation, design those parts well enough to learn about them.

When comparing alternatives:
- make each credible on the dimensions being compared rather than building straw men
- hold irrelevant conditions steady
- allow the eventual design to combine or surpass the prototypes rather than selecting one wholesale

A prototype may be discarded, retained for another probe, or deliberately rebuilt into production form. Never promote it by inertia; review retained code against production requirements as a new decision.

### 4. Capture the result and update the design

Use the lightest closeout that preserves what matters:

```md
Result: <what was observed or gathered, including material limits>
Learning: <when non-obvious or disputed: what is now understood differently>
Next: <design update, new question or probe, or stop>
```

An inconclusive result is still a result. It may show that the question was too broad, the probe lacked fidelity, the expected distinction does not matter, or another unknown dominates. Do not manufacture learning to make a probe appear successful.

Update the design rather than defending the starting plan. Close branches the result no longer supports, open newly exposed questions, or stop when the decision is grounded enough.

## Graph-Shaped Work

Use a graph only when probes have real dependencies, branch conditions, parallel paths, or convergence. Keep a simple question as a simple note.

For each graph node, retain only what the coordinator needs:

```text
id
decision/question
depends_on
dependency_mode: blocking | non_blocking
starting_assumptions
status
probe                 # ready or running nodes only
result
limits
branch_effect
```

Before publishing the graph, audit every hard dependency against the immediate decision:

- Would its absence make the next probe unsafe?
- Would its absence make the result materially uninterpretable?
- Does it resolve a confounder that cannot simply remain represented and observed?

If none apply, it is not a hard dependency. Make it informing, independent, conditional, or remove it. Scope safety evidence to the proposed intervention: an operational change may need matched session and write observations, but not a universal pool-sizing or DDL program unless it actually touches those decisions.

Only the active frontier gets methods, inputs, schedules, acceptance criteria, or artifact schemas. An unresolved descendant retains its question, dependency, and the result that would activate it—nothing more.

Use the host tracker’s status vocabulary; statuses such as `ready`, `running`, `closed`, and `inconclusive` are implementation details, not concepts this skill imposes.

Apply these execution rules:
- A probe is ready when its blocking dependencies are resolved.
- A non-blocking branch may proceed only when it records the assumption that permits work to continue before the dependency resolves.
- Independent ready probes may run in parallel.
- A result may open, close, split, or deprioritize later branches.
- When a late result overturns a starting assumption, revisit work already completed under that assumption; reopen or invalidate it where necessary.
- At convergence, merge results and limits—not branch conclusions or agent votes—before updating the shared decision.
- Preserve contradictory results as unresolved information. Do not average them into false agreement.
- Create another probe only for uncertainty exposed by the merge.

## Independent Checks

Use an independent context or agent only when anchoring, a favored explanation, or hidden author context could materially distort the result.

Give it the raw target, question, necessary facts and constraints, and required output. Omit the favored conclusion or prior rationale only when they would leak the answer; never omit domain facts needed to do the work.

Treat the returned result and limits as information, not as an independent vote. If it disagrees with another result, the disagreement is itself a result to resolve or preserve—not a reason to average the answers or rerun until they agree. Multiple agents sharing the same hidden assumption are replication, not independence.

## Guards

- Do not elaborate contingent detail merely because it sounds implementable.
- Do not turn every plausible later question into a designed probe before its branch is ready.
- Do not invent precision the situation does not supply.
- Do not construct a prototype when existing evidence can answer the question.
- Do not put known corrections, characterization, design comparison, and intervention under one generic experimental contract.
- Do not make independent improvements or possible later ceilings prerequisites merely because they share a resource.
- Do not build a universal evidence schema, artifact graph, or safety program for one bounded decision without demonstrated reuse.
- Do not exhaustively compare candidates when the cheapest credible candidate can be tested first and later branches depend on that result.
- Do not promote temporary work by inertia.
- Do not graph work that has no meaningful branching or dependency structure.
- Do not continue probing when no plausible result would change the decision.
