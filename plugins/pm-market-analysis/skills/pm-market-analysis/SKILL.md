---
name: pm-market-analysis
description: "Use when Codex must analyze one prediction-market PM event for PMKNB: ingest subject/world research and market data, identify exact Polymarket or Kalshi instruments, assess market forces, resolution/oracle risk, liquidity, and platform/counterparty risk, then output a forecast, report, brief, proposal, or no-publish result. Triggers include prediction market, Polymarket, Kalshi, PM event, instrument identity, conditionId, token IDs, event_ticker, market ticker, YES/NO, PMKNB market_analysis, resolution risk, negative risk, or multi-market event analysis."
---

# PM Market Analysis

## Purpose

Analyze one PM event for PMKNB and produce a concise, evidence-first package. A PM event may contain multiple child markets, but the analysis must center on one event identity and output exact PMKNB instruments.

Use PMKNB terms: situation, source, claim, instrument, forecast, position, report, brief, proposal, run_trace, and PM event.

Use instrument, not contract. Use PM event, not venue event. Do not use memo as a product term for this skill.

## Practical Trading Heuristics

Use these as the core trader-facing lens. Keep them practical and human-readable; do not turn them into wallet, API, or execution-system details unless the user is explicitly building execution infrastructure.

- Watch for crowded obviousness. If the reason is easy to see, assume fast traders or market makers have probably seen it too.
- Have an exit reason before entering. Is this a hold-to-resolution trade, a catalyst trade, a mispriced-spread trade, or just a research watch? Those are different.
- The best trades often start with source advantage. Know where the resolving fact will appear: docket, official site, clerk, agency feed, certification board, box score, or another concrete proof channel.
- Read the rules, not the title. A market can be right in the world and still resolve differently because of source, deadline, wording, or proof standard.
- Know what price you can actually get. Displayed price is not executable price. Spread and depth matter more than headline probability.
- Size matters. A good-looking price may only exist for tiny size. Before treating a market as attractive, ask what the effective price is for the amount that would actually be traded.
- Timing is part of the trade. News, official releases, games starting, deadlines, dispute windows, and close times change whether a position is worth entering or exiting.

## Load The Reference

Load [references/pm-market-analysis-reference.md](references/pm-market-analysis-reference.md) before producing any publishable package.

Also load it whenever the task involves:

- Polymarket identity, conditionId, token IDs, outcomes, negative risk, or sibling markets.
- Kalshi identity, event_ticker, market ticker, or YES/NO side.
- Resolution/oracle ambiguity, dispute/challenge status, or rule/source mismatch.
- Liquidity, spread, depth, VWAP, stale/pinned pricing, or event-window liquidity shock.
- A structured `pm_market_analysis.v1` output or PMKNB write matrix.

## Workflow

1. Frame the situation.
   - Identify the subject/world question.
   - Identify exactly one PM event.
   - State whether the event has one child market or multiple child markets.
   - Separate world outcome probability from resolution probability.

2. Verify instrument identity.
   - Never rely on title-only matching.
   - For Polymarket: verify event -> market -> conditionId -> CLOB token IDs/outcomes.
   - For Kalshi: verify event_ticker -> market ticker -> YES/NO side.
   - Do not attach Polymarket fields to Kalshi instruments.
   - If exact identity cannot be verified, choose `proposal` or `no_publish`.

3. Ingest evidence before conclusions.
   - Capture sources, claims, market data snapshots, and rules.
   - Prefer primary sources for rules, resolver/oracle details, market identity, and settlement mechanics.
   - Record snapshot freshness for prices and liquidity.
   - Mark stale, ambiguous, conflicting, or unverified claims explicitly.

4. Analyze market forces.
   - Build an outside view.
   - Identify causal forces, clashing forces, cruxes, scenarios, falsifiers, and coherence checks.
   - Distinguish probability, confidence, and actionability.
   - Apply the practical trading heuristics: crowded obviousness, source advantage, rules-vs-title risk, executable price, sizing, timing, and exit reason.
   - Avoid buy/sell/hold guidance, orders, executions, or dense orderbook history.

5. Assess resolution/oracle risk.
   - Inspect resolver, rules, source finality, ambiguity, challenge/dispute status, and title/rules/source mismatch.
   - Separate what will happen in the world from how the instrument will resolve.
   - If resolution risk dominates, prefer `report`, `brief`, `proposal`, or `no_publish` over `forecast`.

6. Assess liquidity and microstructure.
   - Use current snapshot data only if fresh.
   - Assess spread, depth/VWAP by notional, asymmetry, stale/pinned flags, and event-window liquidity shock risk.
   - Do not provide order placement, execution tactics, or dense orderbook history.

7. Assess platform/counterparty risk.
   - Disclose settlement, custody, oracle, regulatory, and access risk.
   - Do not speculate about hidden solvency, private counterparties, or non-public platform conditions.

8. Handle multi-market and negative risk.
   - List sibling markets separately.
   - Do event-level math only after verifying a same-venue complete MECE set.
   - Treat cross-venue markets as related-only unless verified rules and identity make a narrower relationship explicit.
   - Do not net, merge, or imply equivalence across venues.

9. Choose the product.
   - `forecast`: immutable thesis revision for exact verified instruments.
   - `report`: evidence-led analysis without a new immutable forecast.
   - `brief`: short operational/context package.
   - `proposal`: recommendation to create/update PMKNB records, instruments, or analysis tasks.
   - `no_publish`: required when identity, rules, sources, or validation gates fail badly enough that the package would mislead.

10. Emit the PMKNB package.
    - Use `pm_market_analysis.v1` when structured output is requested.
    - Put evidence before conclusions.
    - Include venue-specific discriminated instrument identity.
    - Include validation gates and failed gates.
    - Include the PMKNB write matrix.
    - Include `run_trace`.

## Product Decision Rule

Produce a forecast only when exact instrument identity, resolution rules, source basis, and minimum evidence gates pass.

Produce a report when analysis is useful but forecast conditions are not met.

Produce a brief when the user needs compact situation/source/claim/instrument context.

Produce a proposal when the main output is a recommended PMKNB action, record, or next research task.

Produce no_publish when the package could misidentify the instrument, misstate rules, collapse non-equivalent markets, or present action guidance.

When working inside a PMKNB runner mode, respect runner-owned writes: inner agents should produce the requested output or apply batch for the runner rather than directly committing KNB changes.

## PMKNB Runner Notes

When this skill is used from a PMKNB workflow runner:

- Read world context first, then market state. Market analysis compares world belief against exact instrument rules and current market state.
- Validate exact venue identity before any forecast: platform, event slug or ticker, market slug or id, condition id, token id when available, exact selection label, outcome, and rules URL or resolution text.
- If no exact instrument is available, emit a proposal or `no_publish`; do not forecast.
- If the trusted market provider is unavailable, emit a blocked result with reason `market_provider_unavailable`; do not fabricate price, liquidity, settlement status, or market freshness.
- Store only selected market snapshots needed to support a forecast, report, or audit trail. Do not retain dense ticks, full orderbooks, or continuous price history.
- Forecasts are immutable thesis revisions. If writing PMKNB records, write a new forecast and link it with `supersedes` rather than mutating the old one.
- Forecast fields should cover thesis type, side, as-of time, current price, fair value or target price, horizon, max entry, exit plan, invalidation, confidence, basis record ids, and basis source ids.
- If a readable synthesis is needed, use a report or brief product. Do not introduce `memo` as a product term.
- Runner-owned writes go to one apply batch for the runner to commit. Do not call `knb apply` or `knb add` from inside the analysis.
- Every meaningful runner-backed package should include one run trace with provider status, instrument id, forecast id if written, snapshot ids, proposal ids, and final status.

## Minimum Output Shape

```yaml
schema: pm_market_analysis.v1
product: forecast | report | brief | proposal | no_publish
pm_event:
  title:
  venue:
  event_identity_status:
instruments:
  - venue:
    identity:
    outcome:
evidence:
  sources: []
  claims: []
  market_snapshot: {}
analysis:
  market_forces: {}
  resolution_oracle_risk: {}
  liquidity_microstructure: {}
  platform_counterparty_risk: {}
conclusion:
  probability_world:
  probability_resolution:
  confidence:
  actionability:
  product_rationale:
validation:
  gates_passed: []
  gates_failed: []
pmknb_write_matrix: []
run_trace: {}
```

## Hard Prohibitions

Do not produce:

- Buy/sell/hold guidance.
- Orders, executions, or trading instructions.
- Dense orderbook history.
- Private solvency speculation.
- Title-only instrument matching.
- Cross-venue equivalence claims without verified identity and rules.
- Forecasts for unverified instruments.

When uncertain, preserve PMKNB integrity over completeness: mark uncertainty, fail the relevant gate, and choose report, proposal, or no_publish instead of forcing a forecast.
