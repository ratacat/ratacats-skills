# PM Market Analysis Reference

Use this reference when producing PMKNB market analysis, exact instruments, structured `pm_market_analysis.v1` output, or any forecast/report/proposal/no_publish decision.

## Table Of Contents

1. Vocabulary and product rules
2. Structured schema
3. Venue-specific instrument identity
4. Gate and block conditions
5. Evidence and source gates
6. Market forces checklist
7. Resolution/oracle risk checklist
8. Liquidity and microstructure checklist
9. Multi-market and negative-risk rules
10. Platform/counterparty risk checklist
11. Product selection gates
12. PMKNB write matrix
13. Semantic validation
14. Output templates
15. Common failure modes

## 1. Vocabulary And Product Rules

Required PMKNB terms:

- situation: monitored world subject.
- source: raw material/provenance.
- claim: sourced atomic statement or assessment.
- instrument: exact tradable YES/NO outcome.
- forecast: immutable thesis revision for one exact instrument.
- position: wallet exposure, not a forecast.
- report: durable authored research artifact.
- brief: highest-value current synthesis for a situation.
- proposal: uncertain automation output needing acceptance.
- run_trace: lightweight audit summary.
- PM event: prediction-market event containing one or more child markets.

Forbidden substitutions:

- Do not use contract for instrument.
- Do not use venue event for PM event.
- Do not use memo as this skill's product language.
- Do not infer positions from forecasts.

## 2. Structured Schema: `pm_market_analysis.v1`

Every structured package should put evidence before conclusions. Unknown values are `null` plus a short `unknown_reason` when the field matters.

```json
{
  "schema_version": "pm_market_analysis.v1",
  "as_of": "ISO-8601",
  "run": {
    "run_id": "string",
    "research_type": "market",
    "run_profile": "string|null",
    "subject_input": "string",
    "skill_version": "string"
  },
  "situation": {
    "situation_id": "string|null",
    "name": "string",
    "monitored_subject": "string",
    "scope_note": "string"
  },
  "sources": [],
  "claims": [],
  "pm_event": {},
  "instruments": [],
  "event_structure": {},
  "related_markets": [],
  "resolution_risk": {},
  "liquidity": [],
  "platform_counterparty_risk": {},
  "market_forces": {},
  "gates": [],
  "decision": {},
  "writes": [],
  "run_trace": {}
}
```

Required top-level sections:

- `sources`: `source_id`, `kind`, `title`, `publisher`, `url|null`, `retrieved_at`, `source_as_of|null`.
- `claims`: `claim_id`, `source_ids`, `claim_type`, `text`, `as_of`, `confidence`.
- `pm_event`: `venue`, `pm_event_key`, `title`, `url|null`, `status`, `resolution`.
- `instruments`: venue-specific exact instruments.
- `event_structure`: `child_market_count`, `sibling_instrument_keys`, `mece_status`, `negative_risk_status`, `event_math_allowed`.
- `related_markets`: `relationship`, `venue`, `title`, `instrument_key|null`, `why_related`.
- `resolution_risk`: `risk_level`, `resolver`, `rules_summary`, `source_of_truth`, `ambiguities`, `challenge_status`.
- `liquidity`: compact per-instrument snapshots only.
- `platform_counterparty_risk`: `settlement`, `custody`, `oracle`, `regulatory`, `access`, `risk_level`.
- `market_forces`: outside view, causal forces, clashing forces, cruxes, scenarios, falsifiers, coherence checks.
- `gates`: machine-checkable gate results.
- `decision`: `forecast`, `report`, `brief`, `proposal`, or `no_publish`.
- `writes`: PMKNB write objects.
- `run_trace`: lightweight audit summary.

## 3. Venue-Specific Instrument Identity

Use a discriminated union. Common wrapper:

```json
{
  "instrument_key": "string",
  "venue": "polymarket|kalshi",
  "pm_event_key": "string",
  "market_title": "string",
  "market_question": "string|null",
  "side": "YES|NO",
  "status": "open|closed|resolved|halted|unknown",
  "identity": {}
}
```

### Polymarket

Required path:

```text
event -> market -> conditionId -> CLOB token IDs -> outcomes
```

Required identity:

```json
{
  "instrument_key": "polymarket:{condition_id}:{clob_token_id}",
  "venue": "polymarket",
  "side": "YES|NO",
  "identity": {
    "kind": "polymarket",
    "gamma_event_id": "string|null",
    "gamma_event_slug": "string|null",
    "gamma_market_id": "string|null",
    "gamma_market_slug": "string|null",
    "condition_id": "string",
    "clob_token_id": "string",
    "venue_outcome_label": "string",
    "rules_url": "string|null",
    "resolution_text_or_summary": "string",
    "verification": {
      "gamma_seen": true,
      "clob_seen": true,
      "condition_id_matches": true,
      "token_id_matches_outcome": true,
      "verified_at": "ISO-8601",
      "source_ids": ["source_id"]
    }
  }
}
```

Blocking failures:

- Title-only match.
- Missing `condition_id`.
- Missing `clob_token_id`.
- Mismatched outcome label/token.
- Ambiguous sibling market.
- Stale or unverified market data.

### Kalshi

Required path:

```text
event_ticker -> market ticker -> YES/NO side
```

Required identity:

```json
{
  "instrument_key": "kalshi:{market_ticker}:{side}",
  "venue": "kalshi",
  "side": "YES|NO",
  "identity": {
    "kind": "kalshi",
    "event_ticker": "string",
    "market_ticker": "string",
    "series_ticker": "string|null",
    "rules_url": "string|null",
    "resolution_text_or_summary": "string",
    "verification": {
      "event_seen": true,
      "market_seen": true,
      "market_belongs_to_event": true,
      "verified_at": "ISO-8601",
      "source_ids": ["source_id"]
    }
  }
}
```

Blocking failures:

- Missing event ticker.
- Missing market ticker.
- Side not specified.
- Polymarket fields present.
- Title/rules/source mismatch.

## 4. Gate And Block Conditions

Gate result format:

```json
{
  "gate_id": "G_EXACT_INSTRUMENT",
  "status": "pass|warn|block",
  "severity": "info|warning|fatal",
  "reason": "string",
  "claim_ids": ["claim_id"]
}
```

Forecast-blocking gates:

- `G_SINGLE_PM_EVENT`: exactly one PM event is centered.
- `G_EXACT_INSTRUMENT`: target instrument has exact venue identity.
- `G_NO_TITLE_ONLY_MATCH`: identity does not depend only on title/question similarity.
- `G_VENUE_IDENTITY_VALID`: Polymarket/Kalshi fields are not mixed and required venue fields exist.
- `G_RESOLUTION_RULES_KNOWN`: resolver, rules, source finality, and ambiguity status are known.
- `G_RESOLUTION_PROBABILITY_SEPARATED`: world outcome and venue resolution are not conflated.
- `G_SOURCE_GROUNDED`: key claims have source IDs and `as_of`.
- `G_LIQUIDITY_FRESH`: liquidity snapshot is fresh enough or limitation is explicit.
- `G_SLIPPAGE_MEASURED`: spread/depth/VWAP by notional is present for target instrument when liquidity matters.
- `G_MECE_VERIFIED_FOR_EVENT_MATH`: event-level probability math only uses verified same-venue complete MECE sets.
- `G_RELATED_MARKETS_SEPARATED`: cross-venue/non-MECE markets are not treated as siblings in event math.
- `G_MARKET_FORCES_COMPLETE`: outside view, forces, cruxes, scenarios, falsifiers, and coherence checks are present.
- `G_COHERENCE`: thesis, probabilities, scenario weights, and claims do not contradict each other.
- `G_PLATFORM_RISK_DISCLOSED`: settlement/custody/oracle/regulatory/access risks are included.
- `G_NO_PRIVATE_SOLVENCY_SPECULATION`: no hidden-solvency or private-counterparty speculation.
- `G_NO_TRADE_INSTRUCTION_FIELDS`: no buy/sell/hold, orders, executions, or dense book history.

## 5. Evidence And Source Gates

Use primary sources for venue identity, rules, resolver/oracle details, settlement source, and market status when available.

Record:

- `retrieved_at` for every source.
- `as_of` for every market, rules, or time-sensitive claim.
- Confidence for each claim.
- Source IDs for each thesis, risk, gate, and conclusion.
- Analyst inference separately from source claims.

If sources conflict, keep the conflict visible and fail or warn the relevant gate. Do not smooth conflicts into an unsupported average.

## 6. Market Forces Checklist

Include:

- Outside view and base rates.
- Causal forces pushing YES and NO.
- Clashing forces and their relative strength.
- Key cruxes.
- Scenarios and rough likelihoods.
- Falsifiers and review triggers.
- Coherence checks against sourced claims, market structure, and resolution rules.
- Separate probability, confidence, and actionability.

Do not let market price substitute for a world model. Market state may inform liquidity and disagreement, but claims and forces need their own basis.

## 7. Resolution/Oracle Risk Checklist

Assess:

- Resolver/oracle identity.
- Resolution source finality.
- Exact rules and rule source.
- Title/rules/source mismatch.
- Ambiguous terms or edge cases.
- Challenge/dispute status.
- Timing risk and publication deadlines.
- Source availability risk.
- Whether the venue can resolve differently from the intuitive world outcome.

Always distinguish:

- `probability_world`: probability the world event happens.
- `probability_resolution`: probability this exact instrument resolves YES.
- `resolution_gap`: difference caused by rules, ambiguity, source finality, or oracle process.

If resolution risk dominates, prefer report/proposal/no_publish over forecast.

## 8. Liquidity And Microstructure Checklist

Compact liquidity snapshot:

```json
{
  "instrument_key": "string",
  "snapshot_as_of": "ISO-8601",
  "freshness_seconds": 0,
  "top_of_book": {
    "best_yes_bid": 0.0,
    "best_yes_ask": 0.0,
    "spread": 0.0
  },
  "depth_vwap": [
    {
      "notional_usd": 100,
      "side": "YES|NO",
      "estimated_vwap": 0.0,
      "slippage_vs_mid": 0.0
    }
  ],
  "asymmetry_note": "string|null",
  "stale_or_pinned_flags": ["string"],
  "event_window_liquidity_shock_risk": "low|medium|high|unknown"
}
```

Assess:

- Snapshot freshness.
- Best bid/ask and spread.
- Depth/VWAP by notional.
- Outcome asymmetry.
- Stale/pinned flags.
- Wide-spread flags.
- Event-window liquidity shock risk.
- Liquidity confidence.

Do not output orders, execution tactics, or dense orderbook history.

## 9. Multi-Market And Negative-Risk Rules

List sibling markets separately from the target instrument.

Event-level probability math is allowed only when:

- The set is same venue.
- The set is complete.
- Outcomes are mutually exclusive and collectively exhaustive.
- "Other" or residual buckets are accounted for.
- Negative-risk adapter mechanics are understood well enough for the analysis.
- Closed, resolved, pinned, or illiquid members are handled explicitly.

Cross-venue markets are related-only unless a narrower verified relationship is explicitly proven. Do not merge Polymarket and Kalshi instruments or imply clean equivalence across venues.

Risk flags:

- `RELATED_ONLY`
- `CROSS_VENUE_RESOLUTION_RISK`
- `INCOMPLETE_OUTCOME_SET`
- `OVERLAPPING_OUTCOMES`
- `MISSING_OTHER_BUCKET`
- `NEG_RISK`
- `NEG_RISK_AUGMENTED`
- `ADAPTER_MECHANICS_RISK`
- `PINNED_OR_STALE_MARKET`
- `ILLIQUID_SIBLING`
- `EXPIRED_OR_CLOSED_MEMBER`
- `RESOLUTION_MISMATCH`
- `EVENT_MATH_BLOCKED`

## 10. Platform/Counterparty Risk Checklist

Disclose:

- Settlement risk.
- Custody risk.
- Oracle/resolver risk.
- Regulatory/access risk.
- Platform-specific operational risk.

Do not speculate about hidden solvency, private counterparties, non-public internal conditions, or guaranteed hedges.

Cross-venue positions are correlated cross-venue exposure, not clean arbitrage, unless identity, access, settlement, and resolution equivalence are all verified.

## 11. Product Selection Gates

Forecast is allowed only if:

- Identity gates pass.
- Resolution rules are verified.
- Evidence threshold passes.
- Liquidity snapshot is fresh enough or limitations are explicit.
- Forecast is stated as immutable thesis revision for exact instruments.
- No action guidance is included.

Report when useful analysis exists but forecast gates fail or a forecast is unnecessary.

Brief when the user needs compact situation/source/claim/instrument context.

Proposal when the main output is a PMKNB write, update, next research task, or acceptance request.

No_publish when:

- Identity is uncertain.
- Rules are uncertain.
- Sources are insufficient.
- Market equivalence would be implied incorrectly.
- Safety/product prohibitions would be breached.

## 12. PMKNB Write Matrix

Decision outcome writes:

- `forecast`: sources, claims, verified instruments, supporting report, immutable forecast, optional brief update, run_trace.
- `report`: sources, claims, verified instruments if available, report, optional brief update, run_trace. No forecast.
- `brief`: sources/claims as needed, compact brief, run_trace. No forecast unless separately justified.
- `proposal`: grounded sources/claims if available, proposal, candidate instrument fields if uncertain, blocked gate IDs, acceptance requirements, run_trace. No forecast.
- `no_publish`: run_trace plus diagnostic reason. No forecast and no brief update.

Write dependencies:

- Claims depend on sources.
- Instruments depend on verified venue identity.
- Forecasts depend on exact instruments plus grounded claims.
- Positions are wallet exposure only and should not be produced by this skill unless explicitly supplied by a position-sync or position-brief input.
- run_trace should summarize source count, claim count, instrument count, decision outcome, blocked gates, and validation result.

## 13. Semantic Validation

Run these checks after schema validation:

1. `pm_event` count is exactly one.
2. `decision.outcome = forecast` implies exactly one `target_instrument_key`.
3. `target_instrument_key` exists in `instruments`.
4. Venue identity is discriminated: Polymarket has no Kalshi tickers; Kalshi has no `condition_id` or CLOB token fields.
5. Polymarket `instrument_key` equals `polymarket:{condition_id}:{clob_token_id}`.
6. Kalshi `instrument_key` equals `kalshi:{market_ticker}:{side}`.
7. Every claim used in thesis, risks, gates, or liquidity references at least one source.
8. Every source has `retrieved_at`; every market/rules/price claim has `as_of`.
9. Liquidity snapshot is no older than the configured freshness threshold or is explicitly marked stale.
10. Any probability is in `[0, 1]`.
11. Forecast includes both `probability_world` and `probability_resolution`.
12. If `event_math_allowed = true`, then `mece_status = verified_complete_mece`, same venue is verified, and all sibling instrument keys are listed.
13. Cross-venue markets appear only in `related_markets`.
14. Resolution risk includes resolver, rules summary, source of truth, ambiguity list, and challenge/dispute status.
15. Platform risk is limited to settlement, custody, oracle, regulatory, and access risks.
16. Forecast output is invalid if any fatal gate is `block`.
17. Report output is allowed with blocked forecast gates, but must include why no forecast was produced.
18. Proposal output is required when suggesting uncertain PM event, instrument identity, source mapping, or forecast candidate needing acceptance.
19. No_publish is required when the run lacks enough verified material even for a useful report/proposal.
20. Final wording uses PMKNB vocabulary.

Schema or semantic failure should trigger one repair attempt when feasible. Remaining fatal failures downgrade `forecast` to `report`, `proposal`, or `no_publish` based on verified usefulness.

## 14. Output Templates

### Forecast

```yaml
product: forecast
target_instrument_key:
pm_event:
instruments:
evidence:
  sources:
  claims:
analysis:
  market_forces:
  resolution_oracle_risk:
  liquidity_microstructure:
  platform_counterparty_risk:
forecast:
  probability_world:
  probability_resolution:
  confidence:
  actionability:
  thesis:
  falsifiers:
validation:
  gates_passed:
  gates_failed:
pmknb_write_matrix:
run_trace:
```

### Report

```yaml
product: report
pm_event:
instruments:
evidence:
analysis:
key_findings:
why_no_forecast:
validation:
pmknb_write_matrix:
run_trace:
```

### Brief

```yaml
product: brief
situation:
pm_event:
current_synthesis:
what_changed:
market_implications:
risks:
next_checks:
basis_sources:
basis_claims:
run_trace:
```

### Proposal

```yaml
product: proposal
proposal_type: pm_event_identity | instrument_identity | forecast_candidate | brief_update | other
summary:
uncertainties:
candidate_pm_event:
candidate_instruments:
blocked_gate_ids:
acceptance_requirements:
claim_ids:
run_trace:
```

### No Publish

```yaml
product: no_publish
reason:
blocked_gate_ids:
minimum_missing_evidence:
safe_next_step:
run_trace:
```

## 15. Common Failure Modes

- A market title is not an instrument identity.
- A PM event is not always a single child market.
- A Polymarket event is not enough; verify market, conditionId, token IDs, and outcomes.
- A Kalshi event_ticker is not enough; verify market ticker and YES/NO side.
- Do not mix Polymarket and Kalshi identity fields.
- Cross-venue markets are related, not interchangeable.
- Event-level math is allowed only for a verified same-venue complete MECE set.
- World probability and resolution probability are different.
- A forecast is an immutable thesis revision for exact instruments.
- A position is wallet exposure, not a forecast.
- Liquidity is part of analysis quality, not trading guidance.
- Platform/counterparty risk may be disclosed, but hidden solvency speculation is forbidden.
- If exact identity or rules fail, produce no_publish when proposal/report would mislead.
- Evidence must appear before conclusions.
- Do not output buy/sell/hold guidance, orders, executions, or trading instructions.
- Do not call the product a memo.
