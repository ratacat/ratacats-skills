# Research Reports

Use this reference when a run needs structured output beyond the default event-resolution report, or when mapping research into pmknb/KNB.

## Shared World Report Record

Use `report` as the durable authored artifact. It stores the whole report in one place, while sources, claims, entities, signals, review items, and run traces remain the structured evidence graph underneath it.

```json
{
  "pmknb_type": "report",
  "fields": {
    "report_kind": "event_resolution",
    "title": "...",
    "situation_id": "...",
    "as_of": "ISO-8601",
    "context_mode": "world",
    "format_id": "pm.world.report.v1",
    "body_markdown": "...full rendered report...",
    "sections": {
      "resolution_predicate": "...",
      "current_world_state": "...",
      "mechanism_map": "...",
      "actor_institution_geography_map": "...",
      "source_map": "...",
      "evidence_ledger": "...",
      "mechanism_paths": "...",
      "watchlist": "...",
      "open_questions": "...",
      "next_searches": "..."
    },
    "basis_record_ids": ["source-or-claim-id"],
    "basis_run_ids": ["run-trace-id"],
    "linked_report_ids": ["related-report-id"],
    "status": "draft | current | superseded | archived"
  }
}
```

Required meaning:

- `report_kind` - `event_resolution`, `actor_map`, `source_discovery`, `question_followup`, `deep_dive`, or `brief_refresh`.
- `title` - human-readable title.
- `situation_id` - owning situation when available.
- `as_of` - ISO-8601 time the report represents.
- `context_mode` - `world` for this skill. Never put market-sensitive fields in a world report.
- `format_id` - stable report contract id; default to `pm.world.report.v1`.
- `body_markdown` - complete authored report, readable on its own.
- `sections` - structured slices of the same report for UI and projections.
- `basis_record_ids` - sources, claims, entities, reports, or other records cited by the report.
- `basis_run_ids` - run traces that produced or materially informed the report.
- `linked_report_ids` - related, parent, child, or prior reports.
- `status` - lifecycle state for display and supersession.

Report kinds change which sections are emphasized. They do not change the canonical evidence graph.

## Evidence Graph Mapping

Map report sections to existing KNB primitives:

| Report content | KNB target |
| --- | --- |
| full authored artifact | `report.body_markdown` plus `sections` |
| user-supplied text, official page, article, filing, transcript, social post, selected document | `source` if used as evidence; `review_item` if only proposed |
| factual atomic statement | `claim` linked to supporting or contradicting `source` |
| person, organization, office, court, agency, locality, informal group reused across records | thin `entity` |
| actor role, legal authority, incentive, constraint, capability, status, conflict, negative evidence | `claim` if sourced; `review_item` if uncertain; report synthesis if cross-claim |
| event-resolution mechanism, source map, actor map, or answer synthesis | `report` |
| high-value future proof point or trigger | `signal` only if specific and monitorable |
| proposed guidance, uncertain claim, source candidate, market attachment, entity merge | `review_item` |
| run inputs, output counts, writes, skipped/blocked status | `run_trace` |
| remaining uncertainty | embedded `open_questions` on the owning situation, claim, entity, instrument, forecast, report, or memo |

Never use a report as an excuse to skip structured evidence. If a fact matters durably, write it as a sourced claim and cite it from the report.

## Link Pattern

Use links when available:

- report `cites` source
- report `cites` claim
- report `about` entity
- report `summarizes` situation
- report `supersedes` report
- report `produced_by` run_trace
- situation `includes` report
- claim `answers` an embedded question when applicable

Also keep `basis_record_ids`, `basis_run_ids`, and `linked_report_ids` in report fields so agents can recover provenance even when link traversal is unavailable.

## Report Kind Overlays

### event_resolution

Use for a concrete prediction-market event. Required sections:

- exact predicate, deadline, timezone, and proof standard
- settlement or proof channel
- current world state
- true, false, delay, and ambiguous-resolution paths
- formal controller, practical controller, veto/delay actor, source proving completion, source proving blockage

### actor_map

Use when the hard part is who can act or block action. Required sections:

- formal role vs practical power
- stated position vs inferred incentive
- constraints, dependencies, rival actors, local intermediaries
- evidence that would change the mechanism status

Write entities thinly. Store incentives and constraints as sourced claims, guidance proposals, or report synthesis.

### source_discovery

Use when the proof channel is unknown. Required sections:

- candidate official channels
- local and local-language source targets
- exact queries run, dead ends, and derived queries
- missing expected source

Do not create durable source records for every search result. Create sources only for material actually used or propose source records through review items.

### question_followup

Use when answering one embedded open question. Required sections:

- owning record id and question id when available
- answer status: `answered`, `refined`, `retired`, or `blocked`
- evidence ledger
- question update with `status`, `next_action`, `last_pursued_at`, and `source_record_ids`

Do not broaden into a full deep dive unless the caller asks.

### deep_dive

Use when researching several linked world questions for a situation. Required sections:

- bounded research agenda
- records written or proposed
- questions answered, refined, retired, or newly added
- signal candidates and review items

### brief_refresh

Use when producing a current synthesis over existing records. Required fields or sections:

- `quality_tier`, `model_or_actor`, `generated_at`, `replacement_policy`, `freshness_until`
- basis record ids and run ids
- what changed
- stale or superseded prior conclusions

Brief refresh must not introduce uncited facts. If new evidence is needed, write sources and claims first or leave next checks.

## Output Modes

- `brief_only` - user-readable report only; include enough source detail for reuse.
- `report_plus_handoff` - report plus proposed KNB writes and links; default when pmknb context is available.
- `apply_batch_ready` - exact KNB apply rows only when the caller explicitly asks and the repo runner contract is available.

When in doubt, produce `report_plus_handoff` and keep uncertain writes as review items.
