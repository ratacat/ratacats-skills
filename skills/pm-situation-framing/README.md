# PM Situation Framing

This skill creates a compact reasoning frame for a prediction-market situation.

Use it when the user explicitly asks for situation framing. The skill does not gather evidence, make a forecast, or write a market report. It builds the mental scaffolding that later research can use: actors, incentives, gates, clocks, constraints, observables, and cruxes.

A frame is useful because it does not pretend to be fact. It says, "Here is how to think about this situation, and here is what would change the frame." Note: this skill is direct-invocation-only, not a general market-analysis or news-research trigger. Family role: start with `pm-situation-framing`, move to price-blind research with `pm-deep-analysis`, then use `pm-market-analysis` when market facts matter.

Good fits:

- Starting a new PMKNB situation
- Clarifying keyholders and veto points
- Naming actors, gates, clocks, cruxes, and observable signals before research
- Capturing hypotheses without laundering them into evidence

## Install

```sh
# skills.sh CLI — Claude Code, Codex, Cursor, OpenCode, and more
npx skills add ratacat/ratacats-skills --skill pm-situation-framing

# or the Claude plugin marketplace
/plugin marketplace add ratacat/ratacats-skills
/plugin install pm-situation-framing@ratacats-skills
```
