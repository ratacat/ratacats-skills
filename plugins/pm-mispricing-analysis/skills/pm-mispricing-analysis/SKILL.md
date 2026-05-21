---
name: pm-mispricing-analysis
description: Use when an agent needs a bounded market-aware scan of one Polymarket or prediction-market event to fetch current prices, do quick subject research, estimate resolution likelihoods, and surface suspected 15+ point mispricings with candidate trade terms for PMKNB.
---

# PM Mispricing Analysis

## Overview

Use this skill for a cheaper, shorter, market-aware pass over one PM event. The goal is not to build the full world model. The goal is to decide whether any child market appears mispriced by enough to deserve operator attention.

Default threshold: surface only suspected mispricings of **15 points or more** between current executable market price and the agent's quick resolution estimate.

This skill may use market prices. It is the opposite of price-blind deep analysis. It should still use evidence, exact instrument identity, and resolution rules before producing a candidate trade.

## Scope

Analyze one PM event at a time. A PM event may contain many child markets; each child market gets its own row.

Use this skill when:

- the user gives a Polymarket/Kalshi event URL, market URL, event title, instrument set, or PMKNB situation;
- the system wants a cheap scan across many events;
- current price matters to the output;
- the main question is "does anything here look badly mispriced?"

Do not use this skill for:

- price-blind world research;
- a full deep research report;
- portfolio sizing, order execution, wallet management, or automated trading;
- dense orderbook storage or high-frequency market history.

## Inputs

Expected inputs:

- `target`: PM event URL, PMKNB situation id, venue event id, or market-question set.
- `as_of`: analysis timestamp.
- current market state from a trusted provider when available:
  - YES price or best executable YES price;
  - NO price or best executable NO price;
  - spread, liquidity/depth, stale flag, and snapshot time;
  - exact venue identity fields.
- optional world context: existing brief, reports, claims, sources, entity records, and open questions.

If current price cannot be fetched from a trusted provider, return `status: blocked` with `blocked_reason: market_provider_unavailable`. Do not invent prices from memory or stale screenshots.

## Workflow

1. Verify event and instrument identity.
   - Confirm platform, event slug/ticker, market slug/id/ticker, selection label, outcome, rule text, resolver/source, and deadline.
   - Keep each child market separate.
   - If identity or rules are ambiguous, mark that child `blocked` or `watch_only`.

2. Pull current market state.
   - Record `snapshot_as_of`.
   - Prefer executable price over headline midpoint.
   - Include spread and depth when available.
   - Mark stale, wide, tiny, or unavailable books.

3. Do bounded subject research.
   - Read enough primary or high-signal sources to form a quick resolution estimate.
   - Focus on actors, institutions, rules, incentives, history, deadlines, and latest dynamic facts.
   - Reuse existing PMKNB world context when available, but check dynamic facts that could have changed.
   - Keep the pass small: usually 3-8 high-signal sources unless the event is genuinely complex.

4. Estimate resolution likelihood.
   - Estimate the probability of the market resolving YES or the named outcome resolving true.
   - Separate world likelihood from resolution likelihood when rules differ from intuition.
   - Use 5-point increments by default.
   - State confidence separately from probability.

5. Compare to market price.
   - For YES: `yes_edge_points = estimated_resolution_likelihood_0_100 - current_yes_price_0_100`.
   - For NO: `no_edge_points = (100 - estimated_resolution_likelihood_0_100) - current_no_price_0_100`.
   - Surface the side with the larger positive edge only if it is at least the threshold.
   - If neither side clears the threshold, output `no_candidate`.

6. Produce candidate trade terms.
   - Candidate side: `YES` when YES appears underpriced; `NO` when YES appears overpriced.
   - `max_entry_price_0_100` should preserve the threshold edge:
     - YES candidate: `estimated_resolution_likelihood_0_100 - threshold_points`.
     - NO candidate: `(100 - estimated_resolution_likelihood_0_100) - threshold_points`.
   - Include invalidation, exit reason, time horizon, liquidity caveat, and source basis.
   - This is a proposed trade thesis, not an order or execution instruction.

## Research Depth

This skill is intentionally bounded. Prefer useful triage over exhaustive certainty.

Minimum evidence gates for a surfaced candidate:

- exact child market identity is verified;
- resolution rule/source/deadline are known or the uncertainty is explicitly included;
- current market price is fresh enough for the venue and event speed;
- at least one credible source supports the quick estimate;
- the estimated edge is at least `threshold_points`;
- the result includes why the market might be wrong, not just why the event may happen.

If those gates fail, produce `watch_only`, `blocked`, or `no_candidate`.

## Crowdedness And Humility

Large apparent edge is not enough. Ask why the market has not already corrected.

Check:

- Is the reason obvious from the title, popular news, or the market page?
- Is the price stale, tiny-size, wide-spread, or not executable?
- Is there a title/rules mismatch?
- Is there a popular narrative that creates a false obvious trade?
- Is the resolving source obscure enough to create an information edge?
- Is the event window so near that liquidity or last-look behavior dominates?

Down-rank or reject candidates that rely on obvious public reasoning with no source advantage.

## Output Shape

Emit concise readable analysis plus structured fields.

```yaml
schema_version: pm_mispricing_analysis.v1
status: completed | blocked | skipped | failed
analysis_kind: mispricing_analysis
threshold_points: 15
as_of: "ISO-8601 timestamp"
target:
  situation_id:
  platform: polymarket | kalshi | other
  event_url:
  event_title:
  event_slug:
  event_ticker:
market_snapshot:
  provider:
  snapshot_as_of:
  freshness_status: fresh | stale | unavailable
  notes:
event_summary:
  short_take:
  main_entities: []
  key_history: []
  current_state:
  resolution_notes:
market_rows:
  - market_question_id:
    instrument_id:
    platform:
    market_url:
    market_title:
    outcome_label:
    side_evaluated: YES
    resolution_predicate:
    rules_url:
    resolver_or_source:
    deadline:
    current_yes_price_0_100:
    current_no_price_0_100:
    executable_price_basis: best_ask | midpoint | last_trade | provider_quote | unknown
    spread_points:
    depth_notes:
    estimated_resolution_likelihood_0_100:
    confidence: low | medium | high
    yes_edge_points:
    no_edge_points:
    disposition: candidate | no_candidate | watch_only | blocked
    reason:
    why_market_might_be_wrong:
    why_this_might_be_false:
    source_ids: []
    claim_ids: []
    next_checks: []
mispricing_candidates:
  - candidate_id:
    market_question_id:
    instrument_id:
    side: YES | NO
    current_entry_price_0_100:
    max_entry_price_0_100:
    estimated_resolution_likelihood_0_100:
    edge_points:
    threshold_points: 15
    confidence: low | medium | high
    horizon: to_resolution | catalyst | timeboxed
    exit_reason:
    invalidation:
    liquidity_caveat:
    basis_record_ids: []
    proposed_record:
      pmknb_type: forecast
      fields:
        thesis_type: settlement_value
        instrument_id:
        side:
        as_of:
        current_price:
        fair_value:
        horizon:
        max_entry:
        exit_plan:
        invalidation:
        confidence:
        basis_record_ids: []
report:
  pmknb_type: report
  fields:
    schema_version: pm_mispricing_analysis.v1
    report_kind: mispricing_analysis
    title:
    situation_id:
    context_mode: market
    format_id: pm.market.report.mispricing_analysis.v1
    body_markdown:
    sections:
      event_summary:
      market_table:
      candidate_trades:
      caveats:
      next_checks:
    status: draft | current
apply_batch:
  records:
    - kind: source | claim | report | proposal | run_trace
      id:
      client_id:
      qualifiers:
        pmknb_type:
        fields: {}
  links: []
  patches: []
run_trace:
  run_type: market_analysis
  status: completed | blocked | skipped | failed
```

## PMKNB Write Discipline

Use existing PMKNB record types. Do not introduce a new canonical `mispricing` record type unless the user explicitly approves it later.

For large sweeps, prefer:

- one `report` per event with `report_kind="mispricing_analysis"`;
- one `proposal` per surfaced candidate trade, where `proposed_record.pmknb_type="forecast"`;
- one selected market snapshot `source` only when it supports a candidate or audit trail;
- one `run_trace` for the event pass.

Write a direct `forecast` only if the runner explicitly permits direct forecast writes and all gates pass. Otherwise create a proposal. Cheap or uncertain scans should not silently enter canonical forecasts.

Do not call `knb apply` or `knb add` from inside a PMKNB runner. Emit the apply batch for the runner to commit.

## Reporting Style

Keep the report short:

- one paragraph event summary;
- one table with every child market checked;
- a short section for candidates that clear the threshold;
- a short caveat section explaining resolution, liquidity, and confidence risks;
- next checks only when they could change the edge.

If nothing clears the threshold, say so plainly and preserve the useful scan log.

## Hard Stops

Return `blocked` or `watch_only` instead of a candidate when:

- price is unavailable, stale, or non-executable;
- exact child market identity is not verified;
- the resolution rule is materially ambiguous;
- the only apparent edge comes from title-only reading;
- liquidity is too thin to support the stated entry price;
- the estimate depends on uncited or unverifiable facts;
- the candidate side cannot preserve at least `threshold_points` at the proposed max entry.

Never produce orders, execution instructions, wallet sizing, or automated trade commands.
