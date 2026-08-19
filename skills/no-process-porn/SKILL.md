---
name: no-process-porn
description: Automatically use whenever a model starts looking at gates, promotion states, smoke tests, instrumentation, telemetry, observability, dashboards, ledgers, manifests, certificates, audits, reports, handoffs, fresh-eyes reviews, verification theater, or completion labels such as ready, green, promoted, validated, closed, or complete. Also use when those artifacts accumulate while requested functionality is still missing, or when reviewing whether process has become a substitute for delivery.
metadata:
  category: developer tools
  blurb: "Detects when agent process is substituting for delivery and redirects the work into the smallest concrete next action."
  keywords:
    - process
    - ceremony
    - reward-hacking
    - gate
    - promoted
    - promotion
    - smoke-test
    - instrumentation
    - telemetry
    - observability
    - dashboard
    - ledger
    - manifest
    - certificate
    - verification
    - completion
    - audit
    - fresh-eyes
    - delivery
---

# No Process Porn

Keep process only when it helps a named consumer make or execute a real decision. Otherwise remove it, demote it to an annotation, or replace it with the smallest direct action toward the requested outcome.

Do not turn this skill into another ceremony. Stop the audit as soon as one decisive fact determines the next move. Do not create a worksheet, scorecard, report, ledger, or gate merely to prove this skill was applied.

## Non-negotiables

- Treat words such as `gate`, `promoted`, `smoke test`, and `instrumentation` as signals, never verdicts.
- Preserve auth, money, migration, deletion, data-integrity, compliance, and other safety-critical controls.
- Treat process as the product when the user explicitly requests a plan, audit, governance system, test harness, instrumentation, or documentation.
- Allow `NO DISTINCT FINDING`. A forced objection is reward hacking.
- Do not count commits, closed tasks, reports, reviewers, tests, or artifacts as progress unless they establish or advance the requested behavior.
- Do not use sunk cost to preserve inert machinery.
- End every real finding in a concrete action, owner, or re-entry condition. Refusal and diagnosis alone are not delivery.

## Run the shortest decisive audit

Ask in order. Stop once the next action is clear.

1. **Outcome:** Which requested capability, correctness defect, safety property, or immediate blocker does this serve?
2. **Consumer:** Who or what reads the artifact or verdict? What decision, branch, deployment, or operator action changes?
3. **Counterfactual:** If this process disappeared, would the outcome or decision change?
4. **Termini:** Where do both outcomes land? A pass must unlock something; a hold or failure must route somewhere actionable.
5. **Reality:** Has a real item passed, failed, or been changed, or does the machinery only describe hypothetical future work?
6. **Proportion:** Is this the smallest credible way to obtain the needed confidence? Does support work remain smaller than the work it supports?

Interpretation:

- Clear outcome, consumer, counterfactual effect, termini, and proportion → keep it.
- Useful observation but no decision authority → label it as evidence or an annotation, not a gate.
- No consumer or changed branch → remove or demote it.
- Unknown cause at one seam → use a bounded probe, not a permanent observability program.
- Evidence already sufficient for the scoped claim → stop checking and advance the work.
- No actual problem → return `NO DISTINCT FINDING` and resume the task.

## Check the three reward traps

### Counterfeit progress

Identify the currency the agent is being paid in: approval, task closure, commit count, green checks, promotion labels, proof tiers, report volume, reviewer agreement, or visible busyness. Ask how that currency could be counterfeited without delivering the outcome.

Common forms:

- splitting one capability into many closures;
- weakening a validator or regenerating a golden to obtain green;
- treating mocks, fixtures, static inspection, or typechecks as live proof;
- producing objections, findings, or consensus because every reviewer is expected to contribute;
- editing plans, specs, issue text, or status documents and calling the feature advanced;
- adding checks whose main effect is producing more checks or evidence artifacts.

### Ceremony

Inspect only the process newly created or expanded for this task. Name its consumer and consequence. Do not inventory the entire repository unless the user requested that audit.

### Avoidance

Name the highest-value unfinished implementation or decision. If meta-work is delaying it, choose one forward path below and act.

## Handle high-risk signals precisely

### `promoted`, `ready`, `green`, `validated`, `verified`, `closed`, `complete`

Require four facts:

- promoted from what state to what state;
- the authority that owns that transition;
- the exact evidence supporting it;
- the behavior the new state enables.

If the label changes but execution, defaults, deployment, exposure, or prioritization does not, it is an annotation. If a smoke test or mock supports only a narrow claim, narrow the status claim.

### Gates

Name the consumer before designing or preserving the gate. A consumed gate has:

- a decision owner;
- explicit input and authority;
- pass and hold/fail termini;
- a real item that can traverse it;
- a consequence on both paths.

No consumer means no gate. Demote the verdict to evidence or remove it. If held items accumulate with no owner or re-entry condition, fix the routing or retire the gate.

### Smoke tests

A smoke test proves one end-to-end path reached one expected observation in one environment. State that claim exactly.

- A mock smoke test does not prove a live integration.
- A `401` may prove routing and auth enforcement, not successful authenticated behavior.
- CLI help proves loading and parsing, not the external operation.
- One sample proves viability, not reliability, performance, or production readiness.
- Once the scoped uncertainty is resolved, stop rerunning unless the artifact changed or the check is an established release consumer.

### Instrumentation, telemetry, logging, dashboards, and coverage analyzers

Start with the question, not the metric.

1. Reuse an existing signal if it answers the question.
2. Otherwise add the smallest temporary probe at the uncertain seam.
3. Run it against representative reality.
4. Revert temporary instrumentation after it identifies the cause.
5. Preserve the lesson as a focused regression test or direct fix.

Make instrumentation permanent only when an ongoing operator, alert, control loop, capacity decision, SLO, or incident workflow consumes it. Name the action triggered by the signal and its ownership, cardinality, retention, and failure behavior. Do not build a dashboard by default.

### Ledgers, manifests, certificates, reports, handoffs, and audits

Keep them when they are an explicit deliverable, durable interface, legal/audit record, cross-session handoff, recovery mechanism, or input to a named decision. Otherwise prefer the existing issue, test, log, or version history.

One bounded fresh-eyes pass can find blind spots. Repeated review rounds, vote counts, contribution scores, consensus, "two quiet rounds," or prompts that demand what others missed incentivize invented findings. Reviewers may return `NO DISTINCT FINDING`; deduplicate evidence before adding another pass.

For broader vocabulary and counterexamples, read [references/signals-and-countermoves.md](references/signals-and-countermoves.md).

## Choose exactly one forward path

### Deliver

Implement the missing capability or fix the concrete defect. Use when the next step is known and authorized.

### Diagnose

Run one bounded experiment at the measured seam, then fix the cause. Prefer temporary instrumentation, a direct query, a minimal reproduction, or one representative live call. State what each possible result would change before running it.

### Verify

Use the narrowest check that can falsify the changed behavior. Match the claim to the proof class. Stop when proportionate evidence exists.

### Demote

Convert an unconsumed verdict, probability, score, or status into a plain observation. Attach a re-entry condition if a future consumer could make it useful.

### Route

Connect a legitimate gate or finding to its missing consumer. Give held items an owner, next action, and re-entry condition; give passed items the action they unlock.

### Subtract

Remove duplicated checks, speculative fields, stale dashboards, redundant reports, or process machinery. Preserve user data and unrelated work; use version control and obtain authority before destructive or broad deletion.

### Hold honestly

When credentials, authority, external state, or a material user choice blocks the next step, state the exact verified boundary. Continue independent useful work; do not build speculative machinery to simulate certainty.

## Prevent overcorrection

Process is justified when its failure would plausibly cause harm or when it buys a decision that cannot be obtained more cheaply. Examples:

- a transaction protects money or durable state;
- an auth gate blocks unauthorized access;
- a migration check prevents corruption;
- a release smoke test exercises the real deployment path;
- temporary instrumentation distinguishes competing root causes;
- a promotion rule commits capital only after pre-registered out-of-sample evidence;
- an audit trail is consumed by an operator, regulator, recovery procedure, or future session.

Do not delete safety because it resembles ceremony. Deepen or simplify it so its consumer and consequences are explicit.

## Act, then report narrowly

For implementation requests, make the direct safe change once the diagnosis is sufficient. For read-only review requests, report the finding without mutating. Never infer authority for a broader cleanup.

If a visible report is useful, use this maximum shape:

```text
Finding: <NO DISTINCT FINDING | consumed process | mislabeled proof | dry process | overgrown process>
Evidence: <consumer/consequence or the missing link>
Action: <one forward path already taken or the exact next authorized action>
```

Do not report the questions you asked, list every clean artifact, or issue a certificate that the work is "process-porn free."
