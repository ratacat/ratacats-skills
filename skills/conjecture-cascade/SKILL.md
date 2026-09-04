---
name: conjecture-cascade
description: "Probe a bounded target from many angles at once — audit for hidden bugs/stale state, stress-test a claim or plan, or brainstorm wide. Falsifiable or generative probes through explicit lenses, each closed with evidence."
metadata:
  category: tools
  blurb: "Directional thinking engine: fires batches of probes through any bounded target — code, claims, plans, or ideas — and closes each probe with evidence or yield."
  keywords:
    - bugs
    - review
    - reliability
    - audit
    - brainstorming
    - thinking
    - lenses
    - probes
---

# Conjecture Cascade

Goal: Cover a bounded target with many small directed probes so that what is broken, false, missing, or unexplored becomes visible — with proof or yield, not vibes.

Success means:
- The target scope is explicit.
- Every selected lens receives a real pass.
- Every probe closes with a status and its supporting evidence or yield.
- Confirmed findings and surprises appear before lower-value notes.

Stop when: every lens and probe has a status, every confirmed finding has evidence, every fertile direction has captured yield, and the final report identifies findings, residual risks, and incomplete checks.

## Core Idea

A cascade sends many small probes through a target from deliberately different directions. A **probe** is one shot along one **lens** (an aimed direction of attention). Lenses come from prebuilt **packs** or are derived fresh with **direction operators**. Every probe closes with a status.

Two closure regimes exist:
- **Falsify mode** — probes are conjectures: testable claims closed against evidence.
- **Explore mode** — probes are directional questions closed on yield: the distinct material they produce.

Never blur the regimes. Explore-mode output is raw material, not verified findings. Falsify-mode output is verified or it is `incomplete`.

The probe list is a search map, not a cage. Surface unrelated or unanticipated findings as first-class results whenever a probe turns them up.

## Targets

A target is any bounded subject: a repo, feature, module, diff, runtime path, data pipeline, API surface, plan, spec, essay, argument, business idea, product concept, decision, research question, or topic.

Infer the target from the user request. Ask one blocking question only when no bounded target can be inferred.

## Modes

| | Falsify mode | Explore mode |
|---|---|---|
| Probe grammar | Conjecture: a specific, testable claim ("X drops records when Y") | Directional question ("what lives in this direction?") |
| Closes on | Evidence | Yield — concrete distinct ideas, framings, options, risks |
| Statuses | `confirmed`, `disproved`, `fixed`, `intentional`, `incomplete` | `fertile`, `barren`, `merged`, `parked` |
| Good for | Bug hunts, claim audits, plan stress-tests, argument checks | Brainstorming, option generation, reframing, angle-finding |

Pick the mode from intent: "find what's wrong / is this true" → falsify; "find what's possible / what am I missing" → explore. Mixed requests may run one round in each mode over the same target; keep the matrices separate.

## Lenses and Packs

A lens is one aimed direction. Get lenses two ways, and use both:

1. **Prebuilt packs** — curated lens sets for a domain. Read the pack file before the first pass:
   - `packs/software-audit.md` — falsify mode, code targets: bugs, dropped data, stale state, races, contract drift. Includes code-search tooling guidance.
   - `packs/inquiry.md` — falsify mode, non-code targets: claims, plans, arguments, decisions.
   - `packs/ideation.md` — explore mode: brainstorming and option generation.
2. **Operator-derived lenses** — when no pack fits, or to widen a pack's coverage, derive lenses by applying direction operators to the target's main facets.

Every cascade MUST include at least a few operator-derived lenses beyond the pack. Packs are the floor; operators are the ceiling.

## Direction Operators

Composable transforms that generate lenses from any target. Apply an operator to the target (or to an earlier probe's result) to mint a new direction:

| Operator | Move |
|---|---|
| Inversion | Assume the opposite; argue the anti-thesis; run the flow backward |
| Negation | Hunt what is absent: the missing case, unsaid assumption, unrepresented actor |
| Scale shift | Zoom to one concrete instance; zoom out to the systemic pattern |
| Time shift | Trace origins; project decay; chase second-order future consequences |
| Stakeholder rotation | Re-see the target through each actor's incentives and failure costs |
| Analogy transfer | Map structure from a distant domain onto the target |
| Constraint mutation | Remove, tighten, or swap a load-bearing constraint; see what breaks or opens |
| Extremization | Push a variable to its limit — zero, one, infinity, worst case |
| Recombination | Cross two earlier probes or findings into a hybrid direction |
| Modality shift | Re-express the target as a diagram, number, narrative, or counterexample; probe the gap between representations |

Operators compose: invert a stakeholder's view, extremize a time-shifted projection. Name the operator(s) behind each derived lens so spread stays auditable.

## Cascade Discipline

**No subagents unless commanded.** Run every lens and probe in this session. Do not spawn other agents, delegate lens groups, or fan probes out unless the user explicitly commands it. Volume is more in-session rounds, not more agents. When commanded: split by lens group; each returns a closed matrix segment; merge and dedupe here.

Treat the lens list as the coverage contract. Walk it top to bottom; give each lens a real pass.

For each lens:
1. Name the lens (and its source: pack or operator).
2. Generate its probe batch, or mark the lens `not-applicable` with a concrete reason.
3. Investigate every probe in the batch.
4. Close each probe with one status.
5. Record the evidence or yield behind the status.

**Branch on surprise.** This is what makes it a cascade: when a probe closes with an unexpected result — a surprising confirmation, a weird disproof, an unusually fertile direction — open a child batch in this session aimed at that surprise. Apply a fresh operator to the surprise to pick the child direction. Bound branching to 2 levels of depth unless the volume tier allows more.

If the scope exceeds one pass, split the cascade into numbered rounds and preserve the unfinished lens/probe position in a ledger or handoff note. Resume from that exact position.

## Spread Discipline

Volume without spread is just one direction repeated. Enforce spread, not count:

- Each round must span multiple distinct lens sources — pack lenses plus at least two distinct operators.
- No two probes closable by the same evidence, or likely to produce the same yield. When two probes collapse into one, `merge` them and mint a replacement in an unused direction.
- Spread check before investigating a batch: if the batch clusters (all inversions, all near-synonyms, all one subsystem), regenerate the redundant probes with unused operators.
- In explore mode, judge each probe's yield against the yield of *other* probes: material that repeats an earlier direction's output marks the probe `merged`, not `fertile`.

## Volume

The unit is the probe. Scale by tier — a requested probe count selects the tier and the tier sets the behavior:

| Tier | Probes | Behavior |
|---|---:|---|
| Spot-check | 10–20 | One round, 3–6 lenses, deep closure on every probe, branch depth 1 |
| Sweep | 20–50 | One round, full pack + a few operator lenses, branch depth 2 |
| Dragnet | 50–150 | Numbered rounds with a ledger; full pack + broad operator derivation; branch depth 2 |
| Saturation | 150+ | Multiple rounds with a ledger; full pack + broad operator derivation; branch depth 3 |

Default tier by scope: narrow function, diff, or single question → spot-check; feature, module, or one topic → sweep; subsystem, repo, or multi-facet topic → dragnet. Honor a user-requested count exactly; distribute probes across lenses so coverage stays visible.

Evidence depth never scales down: at every tier, prefer fewer well-closed probes over a larger list with shallow closure. Higher tiers get more probes by adding rounds, not by cheapening closure.

## Closure Standards

**Falsify mode.** Close a conjecture with direct evidence: code, tests, logs, runtime output, data, documents, sources, or controlled execution. Accept absence evidence only when the search method is named and the searched scope covers the mechanism. Mark the probe `incomplete` when evidence access is missing, the search scope is weak, or the behavior remains untested.

**Explore mode.** Close a probe on yield. `fertile` requires captured, concrete material — ideas, framings, options, named risks — distinct from every other probe's yield. `barren` requires an honest pass, not a skipped one: state what was tried in that direction. Yield is judged on distinctness and usefulness, never on truth; explore mode makes no truth claims.

## Statuses

Falsify mode:

| Status | Meaning |
|---|---|
| `confirmed` | Evidence confirms the conjecture; the finding stands open or needs a decision. |
| `disproved` | Evidence excludes the mechanism in the scoped conditions. |
| `fixed` | Evidence confirmed the finding and the current session corrected it. |
| `intentional` | Evidence shows the behavior or state is a deliberate choice. |
| `incomplete` | Evidence is insufficient to close the probe. |

Explore mode:

| Status | Meaning |
|---|---|
| `fertile` | The direction produced distinct, captured yield. |
| `barren` | An honest pass produced nothing distinct; the attempt is recorded. |
| `merged` | The probe collapsed into another probe's direction or yield. |
| `parked` | Promising but out of scope now; noted for a future round. |

## Output Matrix

Keep coverage inspectable with a visible matrix:

| Lens (source) | ID | Probe | Evidence / Yield | Status | Finding |
|---|---|---|---|---|---|

Lead the final answer with confirmed findings and fixes (falsify) or the strongest yield, clustered by theme (explore). Then the matrix summary, incomplete or parked items, and residual risks.

## Quality Bar

Give every lens and probe enough attention to produce real evidence or real yield. Treat unexpected findings as first-class results. The cascade exists to find what you were not looking for — never to defend the original probe list.
