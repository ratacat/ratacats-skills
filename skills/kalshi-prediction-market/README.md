# Kalshi Prediction Market

This skill gives the agent a working mental model of **Kalshi**, the regulated prediction-market exchange.

Use it when a user asks about Kalshi prediction markets or mechanics. It keeps "series," "event," "market," "contract," and "ticker" straight, since those terms point to different levels of the Kalshi hierarchy.

Prediction-market systems get confusing fast when pricing, settlement, order books, and API objects blur together. This skill keeps the agent anchored in the right level before it explains, queries, or designs anything.

Good fits:

- Explaining Yes/No pricing
- Distinguishing series, events, and markets
- Reading market metadata and order books
- Reasoning about settlement sources
- Planning API or WebSocket usage

It is a domain primer, not a trading strategy. Use it to understand the machinery before making decisions on top of it.

## Install

```sh
# skills.sh CLI — Claude Code, Codex, Cursor, OpenCode, and more
npx skills add ratacat/ratacats-skills --skill kalshi-prediction-market

# or the Claude plugin marketplace
/plugin marketplace add ratacat/ratacats-skills
/plugin install kalshi-prediction-market@ratacats-skills
```
