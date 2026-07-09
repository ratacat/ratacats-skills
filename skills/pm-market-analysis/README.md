# PM Market Analysis

This skill is for market-aware analysis of one prediction-market event.

Use it after the agent has enough world context and needs to connect that context to exact instruments, current market structure, liquidity, resolution risk, platform risk, and possible forecast or proposal outputs. This is disciplined trading context: a good pass identifies the exact market, the exact side, the exact resolution path, and the practical forces around price and execution.

Family role: use `pm-market-analysis` after `pm-situation-framing` and price-blind world research from `pm-deep-analysis`; this skill is the market-aware handoff.

Good fits:

- Analyzing one PM event with many child markets
- Matching Polymarket or Kalshi instrument identity
- Assessing resolution/oracle risk, liquidity, microstructure, and platform risk
- Writing a forecast, brief, proposal, report, or no-publish result
- Separating market mechanics from world facts

## Install

```sh
# skills.sh CLI — Claude Code, Codex, Cursor, OpenCode, and more
npx skills add ratacat/ratacats-skills --skill pm-market-analysis

# or the Claude plugin marketplace
/plugin marketplace add ratacat/ratacats-skills
/plugin install pm-market-analysis@ratacats-skills
```
