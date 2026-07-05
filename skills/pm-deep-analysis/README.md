# PM Deep Analysis

This skill is for deep, price-blind research on prediction-market questions.

Use it when the important work is understanding the world: rules, actors, institutions, dates, proof standards, resolution mechanics, open questions, and evidence quality. It routes each event to a domain playbook (elections, geopolitics, macro, legal, tech, and more), builds a world model, and produces calibrated 0-100 likelihood estimates without looking at prices or letting market odds steer the research. If `pm-research-methodologies` is installed it uses that skill's execution loop for world research; otherwise it falls back to a compact built-in loop.

Market prices are useful in other modes, but they can contaminate the first pass. This skill gives the agent a clean room for broad prediction-market world research before any market-aware analysis happens. Family role: use `pm-situation-framing` to frame the situation first, `pm-deep-analysis` or `polymarket-event-research` for price-blind world research, and `pm-market-analysis` when market facts matter.

Good fits:

- Building or updating a durable research report
- Estimating 0-100 resolution likelihoods from base rates, sources, rules, actors, and deadlines
- Separating world outcomes from market-resolution mechanics
- Routing an event to domain-specific research directions and known resolution gaps
- Feeding PMKNB records with evidence-first sources, claims, reports, and run traces
- Keeping a first-pass analysis clean of odds, prices, order books, or trader positioning

## Install

```sh
# skills.sh CLI — Claude Code, Codex, Cursor, OpenCode, and more
npx skills add ratacat/ratacats-skills --skill pm-deep-analysis

# or the Claude plugin marketplace
/plugin marketplace add ratacat/ratacats-skills
/plugin install pm-deep-analysis@ratacats-skills
```
