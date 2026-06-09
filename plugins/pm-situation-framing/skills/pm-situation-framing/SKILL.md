---
name: pm-situation-framing
description: Use when the user or router explicitly names PM Situation Framing or pm-situation-framing to create or update a PMKNB situation frame. This skill is direct-invocation-only and must never be automatically loaded for general market, forecasting, research, or news-analysis requests.
---

# PM Situation Framing

Create a durable, isolated reasoning guide for a PMKNB situation. A situation frame is **not evidence, not a forecast, and not a report**. It is a structured model that helps later agents reason, research, and update without mixing facts with interpretation.

## Core Rules

- Keep the frame separate from evidence. Frame judgments are hypotheses until separately sourced.
- Never turn unsourced interpretation into a claim about the world.
- Label every material statement as **Sourced fact**, **Frame judgment**, **Inference**, or **Speculation**.
- State what would change the frame, not merely what would support it.
- Prefer gates, keyholders, actors, incentives, clocks, constraints, and observables over narrative summary.
- Use confidence for the frame's reasoning quality, not for the market outcome.
- Mark uncertainty explicitly. Do not hide cruxes behind smooth prose.
- Keep the frame compact enough for later agents to reuse.

## Build Process

1. Define the **frame boundary**: what the frame covers and excludes.
2. Write a falsifiable **frame thesis**: the current best model of what drives the situation.
3. Identify **resolution pathways**: gates, choices, decisions, or facts that could resolve the market.
4. Map actors:
   - **actor model**: wants, fears, beliefs, constraints, capacities, incentives, action menu.
   - **power map**: who can make, block, delay, force, legitimate, enforce, or route the outcome.
5. Surface structure:
   - gates and keyholders
   - pressure points
   - choice points
   - clocks
   - implementation gaps
   - legibility gaps
6. Identify **cruxes**, **misread risks**, **observables**, and **tripwires**.
7. Set **evidence standards** and **update rules**.

## Evidence Contamination Rules

Use these labels strictly:

- **Sourced fact**: externally supported claim already present in the evidence context.
- **Frame judgment**: analyst view of what matters or how structure fits together.
- **Inference**: reasoning from sourced facts, labeled as reasoning.
- **Speculation**: plausible but weakly supported possibility.

Rules:

- Do not cite the frame as evidence.
- Do not introduce factual claims unless they are sourced in the active evidence context.
- Do not let actor-model language become factual language.
- Do not write naked predictions. Mark them as frame judgments, inferences, or speculation.
- For every important unsourced claim, replace the claim with **Evidence needed**.
- Later agents must separately source any factual claim before using it in research, reports, forecasts, or market-resolution analysis.

Never write:

> Actor X will block the outcome.

Prefer:

> **Frame judgment:** Actor X is a likely blocker if its incentives remain aligned against the outcome.
> **Evidence needed:** public statement, filing, vote behavior, procedural action, or other observable opposition.

## Output Template

```markdown
# Situation Frame: [market/situation name]

## Frame Boundary
Covers:
Excludes:

## Frame Thesis
[1-3 sentences. Falsifiable. Label any judgment, inference, or speculation.]

## Resolution Pathways
1. [Pathway name]: [gates -> keyholders -> possible resolution route]
2. [Pathway name]: [gates -> keyholders -> possible resolution route]

## Actor / Power Map
| Actor | Wants / Fears | Constraints | Power Over Outcome | Likely Action Menu | Basis |
|---|---|---|---|---|---|
|  |  |  |  |  | Sourced fact / Frame judgment / Inference / Speculation |

## Gates, Clocks, and Pressure Points
| Item | Type | Keyholder | Why It Matters | Observable | Basis |
|---|---|---|---|---|---|
|  | gate / clock / pressure point |  |  |  | Sourced fact / Frame judgment / Inference / Speculation |

## Cruxes
1. [Uncertainty that would materially change the frame]
2. [Uncertainty that would materially change the frame]

## Misread Risks
- [Tempting but possibly wrong story, analogy, or causal model]
- [Source interpretation risk]

## Evidence Standard
What should count:
What should not count:
Evidence needed:

## Update Rules
- If [observable], update toward [frame change].
- If [observable], update away from [frame change].
- If [absence by clock/deadline], update by [rule].

## Tripwires
- [High-impact observable requiring immediate reframing or escalation]

## Research Posture
Best source classes:
Noisy / delayed / adversarial source classes:
Next research moves:

## Frame Confidence
[Low / Medium / High] - confidence in the frame structure, not the market outcome.
Reason:
```

## Pressure Modes

Use only when relevant:

- **Fast-moving news:** prioritize tripwires, clocks, and update rules over complete prose.
- **Thin evidence:** make legibility gaps explicit; do not fill gaps with confident narrative.
- **Narrative capture:** separate actor messaging from actor constraints.
- **Formal announcement risk:** check implementation gaps before treating announcements as execution.
- **Procedural market:** identify keyholders, gates, and deadlines before discussing incentives.

## Quality Bar

A good situation frame:

- Has a clear boundary and falsifiable thesis.
- Names who can move, block, delay, force, or legitimate the outcome.
- Identifies gates and keyholders instead of only summarizing events.
- Includes observables that would actually update the frame.
- Contains at least one misread risk.
- Separates sourced facts, inferences, speculation, and frame judgments.
- Avoids forecasting language unless explicitly labeled as a hypothesis.
- Is reusable by a later agent without trust in hidden reasoning.
