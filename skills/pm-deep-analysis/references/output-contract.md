# PM Deep Analysis — Output Contract

Schema `pm_deep_analysis.v1`, unchanged from prior versions of this skill. The structured fields are what make the output useful to PMKNB projections and the HTML cockpit.

## Output Shape

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

## Apply Batch And ID Rules

Inside PMKNB, `apply_batch.records` must contain the canonical report and run trace writes that the runner can commit. Every record must have a stable `id` or `client_id`, and links, basis IDs, and patches must reference those IDs. Do not emit only a separate report sidecar and assume it will become durable. The readable `report` block may be repeated for human readability, but the apply batch is authoritative.

Use `report.fields.status="current"` for a completed deep-analysis report. Use `run_trace.fields.status="completed"`, `"blocked"`, `"skipped"`, or `"failed"` for the run trace. Blocked, skipped, or failed runs should write a diagnostic run trace and no likelihood rows; a diagnostic report may be written only with empty `market_questions`.

Use `market_question_id` for a row in the deep-analysis likelihood table. Use `target_open_question_id` or `apply_batch.open_question_patches[].question_id` only for embedded PMKNB open questions. Never reuse one embedded open-question id for multiple child market rows unless every row is explicitly answering that same open question.

For `question_fingerprint`, use normalized identity fields: platform, event slug or Kalshi event ticker, market slug/id or Kalshi market ticker, normalized title, normalized resolution text, deadline, and resolver/source. Hash text fields with SHA-256 of lowercase whitespace-collapsed text when tools are available; otherwise include the normalized text in `fingerprint_basis`.

Include `outcome_label` or `selection_label` in every `question_fingerprint`; multi-outcome events must not collapse distinct outcomes into one assessment row.

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
