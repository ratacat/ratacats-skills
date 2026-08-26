# prediction-drill

A vertical falsification loop for a single bug. Rounds of five cheap-to-check predictions drill down the problem space to the root cause, then drill back up the solution space to a validated fix. Inspired by the debugging habit of predicting what you'll find before you look — so that being wrong is informative.

## What it does

- **Phase 0 — Triage.** Before reading code: what changed, when did it start failing, can it be reproduced, what do the logs say, are the inputs different. Answers seed the first round; unanswered questions become its predictions.
- **Phase A — Drill down.** Five falsifiable predictions per round, each checkable in minutes. Falsified predictions recenter the next round; the ladder descends layer → component → function → line/invariant. Convergence is rung-gated: all five surviving at a coarse grain only earns a deeper round.
- **Phase B — Drill back up.** Same loop over *elements of one fix* — not competing whole solutions — until the change is fully specified with its blast radius.
- **Close-out.** Implement, re-run the converged checks against real code, flip the repro, and if the bug is bead-tracked, file the root cause and the falsified dead ends with `bd close` so they're never retried.

Guard rails: every prediction must be falsifiable, cheap (≤ ~5 min), load-bearing (its falsity would change your next action), and narrower than last round's survivors. A stall valve stops the drill honestly instead of softening predictions to force a green.

## Good fits

- A reproducible bug with an unknown cause and a suspicion that the first plausible fix is wrong.
- Regressions where git history, logs, and input diffs can shrink the search before code comprehension.
- Bugs where you want the dead ends recorded, not just the answer.

Not this skill: wide one-shot audits or brainstorming (use `conjecture-cascade`), bugs needing standing instrumentation before any cheap check exists (use your debugging skill).

## Install

```sh
# Claude Code
/plugin install prediction-drill@ratacats-skills

# Any agent
npx skills add ratacat/ratacats-skills --skill prediction-drill
```

No setup requirements. `bd` (beads) is optional — only used at close-out when the bug is already bead-tracked.
