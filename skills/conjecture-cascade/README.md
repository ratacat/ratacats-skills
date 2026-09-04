# Conjecture Cascade

A directional thinking engine. It covers a bounded target — a codebase, a claim, a plan, a topic, an idea — with batches of small probes fired through explicit lenses, and closes every probe with a status backed by evidence or yield.

Two closure regimes:

- **Falsify mode** — probes are conjectures: testable claims closed against evidence (`confirmed`, `disproved`, `fixed`, `intentional`, `incomplete`). For bug hunts, claim audits, and plan stress-tests.
- **Explore mode** — probes are directional questions closed on what they produce (`fertile`, `barren`, `merged`, `parked`). For brainstorming and angle-finding.

Lenses come from prebuilt packs — `software-audit` (the original bug-hunt lens set), `inquiry` (claims, arguments, plans), `ideation` (brainstorming) — plus a table of composable direction operators (inversion, negation, scale shift, time shift, stakeholder rotation, analogy transfer, constraint mutation, extremization, recombination, modality shift) that derive fresh lenses for any target. Spread discipline keeps probes genuinely different directions, volume tiers (spot-check, sweep, dragnet, saturation) scale the run from 10 to 1000+ probes, and surprising closures branch into child probes — the cascade. The operator runs the cascade in this session; it does not use subagents unless you command it to.

Good fits:

- Auditing a subsystem or recent changes for hidden defects
- Stress-testing an argument, spec, or plan before committing to it
- Brainstorming a topic or product idea from dozens of deliberate directions
- Producing an evidence-backed report with findings, proof, and residual risks

## Install

```sh
# skills.sh CLI — Claude Code, Codex, Cursor, OpenCode, and more
npx skills add ratacat/ratacats-skills --skill conjecture-cascade

# or the Claude plugin marketplace
/plugin marketplace add ratacat/ratacats-skills
/plugin install conjecture-cascade@ratacats-skills
```
