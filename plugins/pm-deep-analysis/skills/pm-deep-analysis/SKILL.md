---
name: pm-deep-analysis
description: Use when an agent needs price-blind deep research for a Polymarket or prediction-market event, market URL, event URL, market question set, or PMKNB situation, including fresh analysis, updating existing deep research, resolution mechanics, source discovery, and 0-100 likelihood estimates independent of market odds.
---

# PM Deep Analysis

## Overview

Use this skill for high-effort, price-blind world research on a prediction-market event. The output is a durable research report plus structured per-market likelihood estimates that can feed PMKNB records and HTML/projection views.

This is not PM market analysis. It does not use prices, odds, order books, liquidity, volume, positions, PnL, or market-implied probabilities.

## PMKNB Runner Integration

When used inside PMKNB, first read only world-safe context:

- situation metadata, scope, guidance, signals, open questions, and current brief
- existing world reports, sources, claims, entities, proposals, and run traces
- sanitized market-question stubs containing only event title, market question/title, outcome labels, rules, resolver/source, deadline, and venue identity needed for disambiguation

Do not read market snapshots, forecasts, positions, exposure projections, prices, odds, orderbooks, or PnL. If the only available market identity source contains visible odds, extract only allowed rule/title fields and mark this in `price_blind_audit` without recording the odds.

When reading prior PMKNB context, consume only world-safe records. Market refreshes, position briefs, market analysis reports, forecasts, positions, exposure-derived reports, market snapshots, and run trace fields containing price, odds, PnL, spread, liquidity, current price, average price, fair value, edge, forecast-market gap, or market-implied language must be excluded or redacted before use.

## Non-Negotiable Price Blindness

Polymarket and Kalshi may be used only to identify the event and its questions:

- Event title, event slug, and market/question titles.
- Kalshi event ticker and market ticker when needed for identity.
- Outcome labels such as YES/NO or named choices.
- Resolution text, rules, deadlines, resolver/oracle text, and linked official sources.
- Market URL, rules URL, and resolution source URL when needed for identity or resolution mechanics.
- Child-market grouping when one event contains several market questions.
- Event and child-market lifecycle timestamps needed for resolution mechanics: `createdAt`, `creationDate`, `startDate`, `acceptingOrdersTimestamp`, `active`, `closed`, `archived`, and deadline/end-date fields.

Do not read, record, cite, summarize, compare against, or reason from:

- displayed odds, percentages, prices, probabilities, charts, volume, liquidity, spreads, order books, trades, comments about price movement, or trader positioning
- any user-provided odds in the prompt
- any market-implied "consensus" language

If odds are visible while extracting titles/rules, treat them as irrelevant visual noise. Do not mention them in the output. Prefer selectors, copied rule text, or alternate pages/API fields that avoid price nodes when practical.

If forbidden market fields materially enter reasoning, do not emit likelihood rows. Produce a blocked diagnostic report or run trace with `price_blind_audit.status="contaminated_blocked"` and request a clean rerun from sanitized inputs. If `price_blind_audit.forbidden_fields_used` is non-empty, the status must be `contaminated_blocked`.

Prediction-market platform pages may be cited only as identity/rules sources. Source records derived from those pages must store only allowed identity/rule fields. Do not summarize, quote, or cite visible odds, comments, charts, volumes, liquidity, or price movement.

## First Branch: Fresh Or Update

Before researching, determine whether there is already substantial current research.

Look for:

- A PMKNB situation matching the event or subject.
- Recent `report` records with `report_kind` such as `deep_dive`, `event_resolution`, `source_discovery`, `actor_map`, or `question_research`.
- Existing sources, claims, entities, signals, open questions, and run traces linked to the situation or event.
- A current brief if the user supplied one, but treat briefs as synthesis, not as the evidence base.

Choose the branch:

- `fresh`: no substantial report exists, the existing report is obsolete for the event phase, or the market questions/rules have changed enough that the old structure no longer fits.
- `update`: a substantial report exists and its static foundation is still useful, but dynamic facts, open questions, deadlines, or source feeds may have changed.

Do not create a named run type for the branch. Use it only as `research_mode` in the output.

## Update Branch

When updating existing research, spend time where reality could have changed. Do not re-research stable foundations unless the original report was weak, uncited, contradicted, or the market rules changed.

Classify prior material:

- `static`: definitions, historical facts, institutional roles, legal text, constitutional rules, market resolution wording, and fixed deadlines. Preserve with citations unless changed or suspect.
- `slow_moving`: incentives, coalition alignments, litigation posture, agency process, weather seasonality, structural constraints. Sample for changes, but do not redo from scratch.
- `dynamic`: filings, votes, certifications, official counts, injury reports, weather model runs, negotiations, military events, earnings, releases, statements, court orders, polls, schedules, and deadlines.
- `ambiguous`: resolution-rule edge cases, contested source authority, conflicting official statements, unclear event boundaries.
- `open`: unanswered questions from the existing report or linked records.

Ask these questions of the existing research:

- Which conclusions depended on future observations that may now exist?
- Which claims had `as_of`, `freshness_until`, dates, or source cadences?
- Which source was expected to update next, and did it?
- Which assumptions were weak, contested, or based on secondary reporting?
- Which market question has the most resolution ambiguity?
- Which facts could change the 0-100 likelihood for each market question?
- Which old uncertainty is now settled enough to convert into a sourced claim?
- Which static sections can be carried forward unchanged with their existing citations?

The update pass should produce a compact change map: unchanged foundations, changed facts, newly answered questions, still-open questions, and revised likelihoods. Do not mutate an old `deep_dive` report. When a new report replaces prior deep analysis, link it to the prior report with `rel="supersedes"` or set `supersedes_report_ids`; use `linked_report_ids` only for related reports that are not replaced. For changed claims, write new claims and link, support, contradict, or supersede as appropriate.

## Fresh Branch

For fresh research, build the foundation before estimating likelihoods.

1. Identify the input.
   - Extract the Polymarket event name and child market questions without using odds.
   - If the user gives only a title, infer the subject but mark the exact PM identity as unverified.
   - If multiple child markets exist, keep them separate.
   - Extract event and child-market lifecycle timestamps when available: `createdAt`, `creationDate`, `startDate`, `acceptingOrdersTimestamp`, `active`, `closed`, `archived`, and deadline/end-date fields. Keep these as allowed identity/resolution fields, not market-sentiment fields.

2. Build a resolution predicate for each market question.
   - State what must happen for YES or the named outcome to resolve.
   - Identify resolver, proof source, deadline, timezone, challenge/dispute process, and edge cases.
   - Separate "what happens in the world" from "how the market resolves."
   - Build a market live-time gate before considering historical events as resolution triggers:
     - Define `market_live_at` for each child market from the best available lifecycle timestamp. Prefer the earliest verified time the child market was actually live/accepting orders; otherwise use child `startDate`; otherwise child `createdAt`; otherwise event `startDate`/`createdAt`.
     - Treat events whose underlying action and required confirmation window were fully completed before `market_live_at` as background context, not as already-triggered resolution events, unless the rule text explicitly says retroactive/pre-live events count.
     - For ongoing-state markets that reference a state beginning before market launch, distinguish the pre-launch state baseline from post-launch break/confirmation events. The baseline may matter; stale pre-launch break events normally should not settle the market.
     - If the rules are ambiguous about retroactive coverage, surface that as a resolution uncertainty and do not make it the dominant driver without explaining why a resolver would count pre-live evidence.
     - When a report discusses a pre-live event, label it `pre_live_context` or `pre_live_ambiguity`, not `already_triggered`, unless retroactivity is explicit.

3. Build the world model.
   - Identify relevant actors, institutions, procedural paths, constraints, incentives, and timelines.
   - Prefer primary sources, official records, direct statements, datasets, transcripts, filings, and high-signal reporting.
   - Use secondary sources mainly for discovery and context unless they are the best available evidence.

4. Create evidence before synthesis.
   - Capture material sources with provenance.
   - Extract atomic claims with confidence, caveats, and `as_of` when time-sensitive.
   - Preserve conflicting evidence as separate claims rather than smoothing it away.

5. Estimate each market question.
   - Start from base rates or structural priors when relevant.
   - Adjust using current evidence, procedural mechanics, timing, actor incentives, and resolution rules.
   - Account for source quality, missing evidence, and ambiguity.
   - Output a 0-100 likelihood for the question resolving YES or for the named outcome happening, depending on the market wording.

## Likelihood Rules

The likelihood table is required whenever the input contains one or more market questions.

Use `likelihood_0_100` as a price-blind resolution assessment of the market question resolving true. It is not a trading forecast and not a market-aware fair value.

Calibration:

- `0`: logically impossible or already definitively false.
- `5`: very unlikely, but not impossible.
- `25`: live minority path.
- `50`: genuinely balanced or underdetermined.
- `75`: likely but with meaningful failure paths.
- `95`: very likely, only exceptional failure paths remain.
- `100`: logically certain or already definitively true.

Prefer 5-point increments unless there is unusually strong quantitative support. Include `confidence` separately from likelihood. Do not force probabilities across child markets to sum to 100 unless the child markets are verified mutually exclusive and exhaustive under the same rules.

When resolution mechanics differ from the intuitive world event, estimate `resolution_true_likelihood_0_100` and optionally include `world_event_likelihood_0_100` as a supporting field. `likelihood_0_100` must equal `resolution_true_likelihood_0_100` when both are present. `resolution_yes_likelihood_0_100` is accepted only as a transitional alias for YES/NO markets.

These likelihoods are price-blind resolution assessments, not PMKNB forecasts. This skill must not write `forecast` records.

## Output Shape

Produce both readable report content and structured fields. The structured fields are what make the output useful to PMKNB projections and the HTML cockpit.

```yaml
schema_version: pm_deep_analysis.v1
research_mode: fresh | update
status: completed | blocked | skipped | failed
price_blind: true
as_of: "ISO-8601 timestamp"
price_blind_audit:
  status: clean | allowed_identity_only | contaminated_blocked
  allowed_market_fields_used:
    - platform
    - event_title
    - event_url
    - event_slug
    - market_url
    - market_title
    - market_slug
    - market_id
    - outcome_label
    - resolution_text
    - rules_url
    - resolution_source_url
    - deadline
    - resolver_or_source
    - event_created_at
    - event_start_date
    - market_created_at
    - market_start_date
    - accepting_orders_timestamp
    - active_closed_archived_status
    - kalshi_event_ticker
    - kalshi_market_ticker
  forbidden_fields_used: []
  notes:
input_identity:
  platform: polymarket | kalshi | other | unknown
  event_url:
  event_title:
  event_slug:
  event_created_at:
  event_start_date:
  market_slug:
  market_id:
  market_created_at:
  market_start_date:
  accepting_orders_timestamp:
  kalshi_event_ticker:
  kalshi_market_ticker:
  identity_status: verified | partial | unverified
existing_research:
  report_ids: []
  carried_forward_claim_ids: []
  changed_claim_ids: []
  stale_or_open_question_ids: []
update_change_map:
  carried_forward_static_claim_ids: []
  refreshed_dynamic_claim_ids: []
  superseded_claim_ids: []
  contradicted_claim_ids: []
  newly_answered_question_ids: []
  still_open_question_ids: []
  likelihood_changes:
    - market_question_id:
      previous_likelihood_0_100:
      revised_likelihood_0_100:
      reason:
market_questions:
  - market_question_id:
    target_open_question_id:
    question_fingerprint:
      venue:
      event_slug:
      market_slug:
      title_hash:
      resolution_text_hash:
      deadline:
      resolver_or_source:
      outcome_label:
      selection_label:
    market_title:
    outcome_label:
    selection_label:
    market_live_at:
    live_time_basis:
      event_created_at:
      event_start_date:
      market_created_at:
      market_start_date:
      accepting_orders_timestamp:
    pre_live_events_considered:
      - event:
        occurred_at:
        confirmation_window_closed_at:
        treatment: background_context | retroactive_trigger | ambiguous
        reason:
    resolution_predicate:
    resolver_or_source:
    deadline:
    likelihood_0_100:
    resolution_true_likelihood_0_100:
    confidence: low | medium | high
    rationale:
    key_supporting_claim_ids: []
    key_contrary_claim_ids: []
    main_uncertainties: []
    what_could_change: []
    next_sources_to_check:
      - source_name:
        source_kind:
        expected_update_time:
        check_reason:
        linked_signal_candidate: true | false
    source_basis:
      source_ids: []
      claim_ids: []
report:
  pmknb_type: report
  fields:
    schema_version: pm_deep_analysis.v1
    report_kind: deep_dive
    title:
    situation_id:
    context_mode: world
    format_id: pm.world.report.deep_analysis.v1
    price_blind: true
    research_mode: fresh | update
    as_of: "ISO-8601 timestamp"
    generated_at: "ISO-8601 timestamp"
    event_title:
    input_identity: {}
    body_markdown:
    sections:
      event_frame:
      resolution_predicates:
      evidence_ledger:
      likelihood_table:
        rows: []
      change_map:
      open_questions:
      next_checks:
    market_questions: []
    price_blind_audit: {}
    update_change_map: {}
    basis_record_ids: []
    basis_run_ids: []
    linked_report_ids: []
    supersedes_report_ids: []
    open_questions: []
    status: draft | current
apply_batch:
  records:
    - kind: source | claim | entity | report | signal | proposal | run_trace
      id:
      client_id:
      qualifiers:
        pmknb_type:
        fields: {}
  links: []
  patches:
    - target_id:
      patch: []
  open_question_patches:
    - owner_record_id:
      question_id:
      disposition: answered | partial | refined | retired | still_open
      last_pursued_at:
      answer_claim_ids: []
      report_id:
      next_action:
      priority:
      depth:
```

Inside PMKNB, `apply_batch.records` must contain the canonical report and run trace writes that the runner can commit. Every record must have a stable `id` or `client_id`, and links, basis IDs, and patches must reference those IDs. Do not emit only a separate report sidecar and assume it will become durable. The readable `report` block may be repeated for human readability, but the apply batch is authoritative.

Use `report.fields.status="current"` for a completed deep-analysis report. Use `run_trace.fields.status="completed"`, `"blocked"`, `"skipped"`, or `"failed"` for the run trace. Blocked, skipped, or failed runs should write a diagnostic run trace and no likelihood rows; a diagnostic report may be written only with empty `market_questions`.

Use `market_question_id` for a row in the deep-analysis likelihood table. Use `target_open_question_id` or `apply_batch.open_question_patches[].question_id` only for embedded PMKNB open questions. Never reuse one embedded open-question id for multiple child market rows unless every row is explicitly answering that same open question.

For `question_fingerprint`, use normalized identity fields: platform, event slug or Kalshi event ticker, market slug/id or Kalshi market ticker, normalized title, normalized resolution text, deadline, and resolver/source. Hash text fields with SHA-256 of lowercase whitespace-collapsed text when tools are available; otherwise include the normalized text in `fingerprint_basis`.

Include `outcome_label` or `selection_label` in every `question_fingerprint`; multi-outcome events must not collapse distinct outcomes into one assessment row.

For plain-English answers, still include the per-question likelihood table near the end:

```markdown
| Market question | Resolution predicate | Likelihood 0-100 | Confidence | Main reason | What could change |
| --- | --- | ---: | --- | --- | --- |
```

## HTML And Projection Fit

Shape the output for PMKNB's view layer:

- Keep the report self-contained in `body_markdown`, but expose table-ready `market_questions`.
- Use stable IDs for sources, claims, reports, and run traces when available.
- Put each market question on its own row with title, likelihood, confidence, source basis, uncertainty, and next checks.
- Keep provenance visible: source title/domain, published or observed time, captured time, actor/model, confidence, and basis ids.
- Put unresolved items in `open_questions` fields or proposals so the research queue can surface them.
- Do not create UI-only canonical records. HTML is a disposable presentation over projections.

Useful PMKNB projection targets:

- `report_index`: the authored report and section summaries.
- `deep_analysis_index`: table-ready price-blind resolution assessment rows from clean deep-analysis reports.
- `record_search`: sources, claims, entities, signals, proposals, and report records.
- `question_backlog`: unresolved questions and next checks.
- `run_trace_index`: what the run read, wrote, skipped, and produced.

## PMKNB Write Discipline

When working inside a PMKNB runner:

- Use world context only.
- Create `source` records before durable `claim` records.
- Keep claims atomic and cited.
- Write a `report` for the standalone research artifact.
- Write signals only for specific future world data points worth monitoring.
- Do not create price or volume signals. If research suggests a price/volume watch would be useful, create a proposal for market-mode handling instead.
- Use proposals for uncertain claims, instrument attachments, guidance, or operator decisions.
- If `target.question_id` was supplied, include an `apply_batch.open_question_patches` entry that marks it answered, partial, refined, retired, or still open.
- Also produce the canonical JSON Patch entry in `apply_batch.patches` against `target.question_owner_record_id`, or mark the run blocked with the reason the owning record could not be patched. `open_question_patches` is explanatory metadata unless mirrored by canonical patch entries.
- If `next_sources_to_check.linked_signal_candidate=true`, create a `signal` record or a proposal/open question explaining why no signal was written.
- Include exactly one `run_trace`.
- Put all writes in the runner's apply batch. Do not call `knb apply` or `knb add` yourself.

Do not write forecasts, positions, orders, executions, dense market snapshots, or market-aware analyses from this skill.

## Common Mistakes

- Using Polymarket odds as a prior or sanity check.
- Treating a market title as the resolution rule.
- Treating pre-launch events as already-triggered resolution events without first applying the child market's `market_live_at` gate and checking whether the rules explicitly allow retroactive coverage.
- Re-researching static foundations during an update pass while ignoring dynamic sources.
- Giving one event-level likelihood when the PM event has several distinct child questions.
- Hiding likelihood estimates in prose instead of a structured table.
- Writing a trading recommendation instead of a price-blind resolution estimate.
- Creating broad keyword signals instead of specific future triggers.
