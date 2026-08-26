---
name: prediction-drill
description: Use when a bug, regression, or misbehavior has an unknown cause and the user wants iterative hypothesis-driven investigation — invoked by name ("prediction drill", "drill into this bug"), or when asked to falsify hypotheses and converge on a root cause and fix through repeated prediction rounds.
metadata:
  category: tools
  blurb: "Vertical two-phase falsification loop for a single bug: rounds of five cheap-to-check predictions drill down to the root cause, then drill back up to a validated fix."
  keywords:
    - bug
    - root-cause
    - falsify
    - hypothesis
    - prediction
    - convergence
    - investigation
    - debugging
---

# Prediction Drill

One bug. One agent. Two drills. Descend the problem space to the root cause, then ascend the solution space to a validated fix. Every step is a falsifiable prediction, checked cheaply.

Guiding principle: **reduce the problem before trying to fix it.** Every lookup and every round shrinks scope until the cause jumps out — the drill is reduction made rigorous.

Single-stranded: run every round in this session. No subagents unless the user explicitly commands it. If commanded for multiple issues, each issue runs this loop independently; the orchestrator verifies each drill log on return.

## Not This Skill

- Wide one-pass coverage of a bounded target (audits, brainstorming, claim stress-tests) → conjecture-cascade
- No cheap repro exists and the bug needs standing instrumentation first → debugging / diagnose
- One bug, unknown cause, iterative descent → you are here

## The Round

A round is **5 predictions**. Each must be:

1. **Falsifiable** — name the check that could prove it wrong, before running it.
2. **Cheap** — verifiable in ≤ ~5 minutes: read, grep, one-shot command, small repro, log check. If a prediction needs more, narrow or split it until it doesn't. Never silently upgrade the budget.
3. **Load-bearing** — state what you'd do differently if it's false. If nothing changes, replace it: a prediction that can't surprise you can't narrow the search.
4. **Narrower than the last round's survivors.**

Check all five. Mark each TRUE (survived) or FALSIFIED (with the lesson the failure taught — what it excluded).

- Any falsified → next round: 5 new predictions recentered on the survivors and lessons. Never re-test a falsified claim unchanged.
- All 5 TRUE at terminal granularity (below) → phase converged.

**Convergence is rung-gated.** All-5-true at a coarse rung does not end the phase — it earns one rung deeper. Only terminal-rung survivors converge. This blocks timid rounds from finishing early.

**Stall valve.** Typically 2–4 rounds per phase. If ~5 rounds die at the same granularity, stop honestly: report the verified boundary (confirmed facts, excluded causes), name the check that is too expensive to run, and ask the user before scaling any check past the minutes budget. Never soften predictions to force convergence — that counterfeits a green and delivers nothing.

## Phase 0 — Triage (before reading code)

Answer five questions with lookups first — git history, logs, and input inspection are cheaper than code comprehension:

1. **What changed?** — code, config, deps, environment (`git log`, `git diff`, recent deploys)
2. **When did it start failing?** — tie it to a commit, deploy, or data shift
3. **Can I reproduce it?** — cheap repro now, or not yet
4. **What do the logs say?** — first divergence, error, warning
5. **Are the inputs different?** — data shape, volume, env, flags

Answers seed round 1; unanswered questions become round 1 predictions. Read only the code the answers implicate — never start by reading the code at large.

## Phase A — Drill Down (problem)

Goal: root cause at mechanism granularity — where it lives, what state/input triggers it, why behavior diverges.

Granularity ladder — one rung per round, recentered on survivors:

1. Layer / subsystem
2. Component / path
3. Function / interaction
4. Line / state / invariant + trigger ← terminal rung

## Phase B — Drill Back Up (solution)

Goal: a minimal fix, validated element by element.

Predict about **elements of one solution, not competing whole solutions**: the guard that prevents the state, the invariant the fix restores, what callers do after the change, which test flips, what breaks elsewhere.

Ladder outward: fix shape → element → exact change → integration (callers, side effects) → verification (repro flips, suite green) ← terminal rung = fully specified fix + blast radius.

Recenter on the closest approach from falsified rounds.

## Close-Out

1. Implement the smallest change embodying the surviving solution elements.
2. Re-run the converged checks against the real change — every solution prediction must still hold on actual code. This is the work-verification step.
3. Verify end-to-end: repro flips, existing suite green.
4. If the bug is bead-tracked, record the root cause, the falsified dead ends (so they're never retried), and the validated solution in the bead; close with `bd close <id> --reason "root cause + fix"`, then `bd sync`.

## Drill Log

Keep in-session; it is the evidence the close-out files.

```
Triage: broke after 08-20 deploy; git log → ts parser touched 08-19; repro = midnight fixture
A1 P1 cause is in ingest path, not query — grep router; both pass through normalize() — TRUE
A1 P2 rows drop before validation — counter at validation entry — FALSIFIED (rows arrive intact; drop is later)
A2 P1 (recentered: post-validation) midnight ts sorts before epoch floor — fixture repro — TRUE
B1 P1 clamping ts at parse prevents the drop — patched repro no longer drops — TRUE
```

## Red Flags — restart the round

- Check would take > 5 minutes → narrow the prediction
- "Probably something complicated" → unfalsifiable, replace
- Its truth wouldn't change your next action → inert, replace
- Re-testing a falsified prediction unchanged
- Five round-1 survivors at a coarse rung declared converged → descend instead
- Softening predictions so all five survive → counterfeit green; report the boundary instead
- Reading code before answering the triage questions → answer them first
