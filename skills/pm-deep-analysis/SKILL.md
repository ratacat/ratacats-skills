---
name: pm-deep-analysis
description: "Price-blind deep research for a Polymarket/prediction-market event or PMKNB situation — fresh or updated analysis, resolution mechanics, mechanism-only briefs, source discovery, 0-100 likelihood independent of market odds."
metadata:
  category: prediction markets
  blurb: "Price-blind prediction-market research: builds evidence-first world reports and calibrated 0-100 resolution estimates without using odds or prices."
  keywords:
    - pm
    - deep
    - analysis
    - likelihood
    - estimation
    - resolution
    - price-blind
    - polymarket
    - kalshi
---

# PM Deep Analysis

## Overview

This skill is event-shaped research with two output modes. **Estimation**, the default: given a prediction-market event, produce a durable price-blind research report plus a calibrated 0-100 likelihood per market question — the answer to "will this exact predicate fire by this deadline?". **Mechanism-only**: when the ask is to explain how the event resolves — resolution mechanics, proof channels, actor and veto maps, source discovery — rather than to estimate it, produce the same report with no likelihood rows and no forecast language. Either way, it does not answer "what is true about this subject?"; world research is an input, not the deliverable.

A defensible likelihood requires six things, and the method below is organized around them:

1. the exact resolution predicate
2. the causal paths to YES and to NO
3. a reference-class base rate
4. current-state evidence
5. the estimation horizon — time-to-deadline dynamics
6. a resolver behavior model

Vocabulary contract: **estimation** is the activity; **likelihood** is the 0-100 value; the **likelihood table** is the artifact. A **forecast** is a PMKNB market-aware record this skill must never write.

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

An update is a diff of the world since the last run date: re-research only changed nodes and open questions. Do not re-research stable foundations unless the original report was weak, uncited, contradicted, or the market rules changed.

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

## Identify The Input

- Extract the event name and child market questions without using odds.
- If the user gives only a title, infer the subject but mark the exact PM identity as unverified.
- If multiple child markets exist, keep them separate.
- Extract event and child-market lifecycle timestamps when available: `createdAt`, `creationDate`, `startDate`, `acceptingOrdersTimestamp`, `active`, `closed`, `archived`, and deadline/end-date fields. Keep these as allowed identity/resolution fields, not market-sentiment fields.
- Route the event to a domain playbook (below) before researching.

## Resolution Mechanics

Per market question, in order:

1. **Resolution predicate.** State exactly what must happen for YES or the named outcome. Decompose the predicate into elements — the action, the actor, the timeframe, the confirmation source — each an independently necessary condition. Elements that can fail independently get estimated separately.

2. **Resolver, proof source, deadline.** Identify the resolver, the proof source it will consult, the deadline with timezone, and the challenge/dispute process.

3. **Live-time gate.** Build a market live-time gate before considering historical events as resolution triggers:
   - Define `market_live_at` for each child market from the best available lifecycle timestamp. Prefer the earliest verified time the child market was actually live/accepting orders; otherwise use child `startDate`; otherwise child `createdAt`; otherwise event `startDate`/`createdAt`.
   - Platform lifecycle timestamps are not always accurate. Polymarket slug datestamps, `createdAt`, `startDate`, and `acceptingOrdersTimestamp` can disagree or be backfilled. Cross-check at least two fields plus the event's news context; when they conflict, say so and reason from the most conservative (earliest-plausible-live) reading for NO paths and the latest for YES paths.
   - Treat events whose underlying action and required confirmation window were fully completed before `market_live_at` as background context, not as already-triggered resolution events, unless the rule text explicitly says retroactive/pre-live events count. A market created *after* a widely reported action is presumptively asking whether it happens *again* (or gets post-live confirmation of a genuinely new kind) — venues create these markets in reaction to news, and the pre-creation occurrence is out of scope.
   - The ACTION timestamp governs, not the report timestamp. Post-live coverage, official confirmations, anniversaries, or the actor's own later account of a pre-live action do not convert it into a post-live event. Do not launder a pre-live action through its post-live reporting.
   - For ongoing-state markets that reference a state beginning before market launch, distinguish the pre-launch state baseline from post-launch break/confirmation events. The baseline may matter; stale pre-launch break events normally should not settle the market.
   - If the rules are ambiguous about retroactive coverage, surface that as a resolution uncertainty and do not make it the dominant driver without explaining why a resolver would count pre-live evidence. An "already happened before creation" YES case caps out as a rules-interpretation bet, never a near-lock: the likelihood should anchor on the post-live re-occurrence path plus a discounted retroactive-resolution term, and the report must say which term dominates.
   - When a report discusses a pre-live event, label it `pre_live_context` or `pre_live_ambiguity`, not `already_triggered`, unless retroactivity is explicit.

4. **Resolver precedent.** Retrieve how this resolver actually decided prior and edge cases — UMA dispute history, Kalshi settlement record, platform clarifications, the resolver's archive. Resolver precedent outweighs textual analysis of the rules; retrieve it, don't recall it.

5. **Series precedent.** When the market belongs to a series (monthly prints, recurring events, numbered instances), retrieve how prior instances resolved, especially the contested ones. Series conventions often override a naive reading of this instance's rules.

6. **Resolution-gap analysis.** Separate "what happens in the world" from "what fires the predicate," and name each gap: definitional ambiguity, confirmation-source lag, deadline vs event timing, resolver discretion. Resolution gaps are why `world_event_likelihood_0_100` and `resolution_true_likelihood_0_100` can diverge; every named gap belongs in the question's uncertainties.

## World Research

Build the world model that the paths to YES and NO run through: actors, institutions, procedural paths, constraints, incentives, timelines.

If the `pm-research-methodologies` skill is available, load it and run its execution loop for this stage, with these overrides: this skill's price-blind protocol governs what may be browsed; scaffold nodes are ranked by their power to move a likelihood, not by general interest; outputs land in this skill's report and PMKNB records.

If it is not available, use this fallback loop:

1. **Scaffold.** List the searchable keys whose investigation compounds into understanding: named people, institutions, instruments (statutes, dockets, data series), precedents, places. Descend from categories to keys — "the certifying official in the decisive county," not "election officials." 8–25 nodes for a full run; rank by decision-relevance to the market questions.
2. **Per node.** Harvest handles at the first good source — names, machine identifiers, terms of art — and pivot every later query on a handle, never the lay topic. Search primary records (filings, dockets, registries, transcripts, datasets) before press; use press as an index pointing to documents. 2–5 queries per node; stop after two consecutive dry queries.
3. **Ledger claims as found**, never reconstructed at synthesis: claim, source with publication date, whether the origin was traced, and confidence (`confirmed` / `probable` / `reported` / `rumor`). Preserve conflicting evidence as separate claims rather than smoothing it away.
4. **Judge load-bearing chains.** Trace the claim to its earliest origin; apparent corroboration usually launders one origin through many outlets, so count corroboration only across independent origins. Map who benefits if the claim is believed; premium for statements against interest; record when the source spoke relative to the event.

Either way: prefer primary sources, official records, direct statements, datasets, transcripts, and filings; use secondary sources mainly for discovery and context unless they are the best available evidence. Capture material sources with provenance and extract atomic claims with confidence, caveats, and `as_of` when time-sensitive — evidence before synthesis.

### Geographic And Foreign-Language Forcing

Do not stop at national-level, English-only sourcing when a local body controls, enforces, litigates, counts, certifies, or reports the outcome. Descend to the controlling subdivision — county, municipality, court, election board, regulator, gazette, docket, clerk — and name it in the scaffold. Local-language research is required when the controlling institution, official records, or media are not primarily English: translate the actor, office, locality, procedure, and ambiguous predicate terms, and search in that language. It is optional only when the relevant channels are entirely English-language or unavailable after a documented search. English-only research on a non-English event is a tripwire, not a style choice — the decisive evidence usually lives in local press and official registers.

### Search Tooling

Prefer `wideband` when installed: `wideband scan "<query>"` for fast source discovery, `wideband research "<query>"` for richer retrieval; it fans out across providers and merges unique sources. If unavailable, use another embedding/neural search provider such as `exa-cli`; otherwise plain web search. Read the tool's `--help` once per environment and record the tool used in the run trace.

For institution- or procedure-heavy events, load [references/world-research-craft.md](references/world-research-craft.md): mechanism chain cards, formal-vs-practical power maps, search packs, X/xpool source classification, evidence-ledger discipline, and per-event-type Domain Checks.

## Estimation

Complete an estimation worksheet per market question before writing the likelihood. The worksheet is the rationale's skeleton; it lives in the report body, not in new schema fields.

| Worksheet field | Content |
| --- | --- |
| Predicate | one sentence, element-decomposed |
| Reference class + base rate | what counts as an instance, how many opportunities existed, the resulting rate |
| Paths to YES | enumerated, rough weight each |
| Paths to NO | failure modes, same treatment |
| Horizon pressure | time remaining vs time the YES paths need |
| Resolution gap | named world-vs-predicate divergences |
| Likelihood + confidence | the output row |

**Outside view first.** The base rate is the starting number. Each adjustment away from it must name its evidence; findings adjust the anchor, they never replace it. A narrative with no base rate behind it is a red flag in your own rationale.

**Estimation horizon.**

- Short horizon (days): state-tracking dominates — current state, what is scheduled, what can mechanically still change before the deadline.
- Long horizon (months+): base rates and hazard dominate — inside-view narratives decay; weight structural constraints and calendars over statements.

**Techniques** — pick by question shape:

- **Deadline markets** ("will X happen by date Y"): estimate a per-period hazard of the trigger and integrate to the deadline. A steady 2%/month hazard over ten months is ~18, not "unlikely, call it 10." State the hazard and the periods.
- **Procedural events** (votes, confirmations, certifications, rulings): enumerate the discrete paths to YES, assign a probability per path, likelihood = sum over YES paths. Procedural date floors trump narrative urgency.
- **Bucket markets** (counts, ranges, dates split across child markets): estimate the underlying quantity's distribution once — e.g., a rate-based count as Poisson — then read each bucket's likelihood off that distribution. Never estimate buckets independently.
- **Multi-outcome contests**: build a competing-hypotheses matrix (ACH) — outcomes as columns, evidence as rows, score each cell for consistency; weight the outcomes that survive the most evidence.
- **Quantitative markets** get an explicit model: a computed number with stated inputs, not prose-only rationale. Prose is where sloppy numbers hide.

**Coherence across child markets.** After estimating rows independently, check the implied joint picture: verified mutually-exclusive-and-exhaustive sets should sum near 100; nested deadlines must be monotone ("X by March" ≤ "X by June"); the same world assumption must not appear on both sides of two rows. A contradiction means at least one worksheet is wrong — fix the worksheet, not just the number.

## Likelihood Rules

The likelihood table is required whenever the input contains one or more market questions and the run is in estimation mode. Choose mechanism-only mode when the ask is to explain how the event resolves without an estimate; emit the full report — predicate, resolver, mechanism map, sources, open questions — with no likelihood rows and no forecast language, set `output_mode: mechanism_brief` (top level and `report.fields`), and label it a mechanism-only brief in the body. `research_mode` stays the fresh/update axis. When in doubt, estimate.

Use `likelihood_0_100` as a price-blind resolution assessment of the market question resolving true. It is not a trading forecast and not a market-aware fair value.

Calibration:

- `0`: logically impossible or already definitively false.
- `5`: very unlikely, but not impossible.
- `25`: live minority path.
- `50`: genuinely balanced or underdetermined.
- `75`: likely but with meaningful failure paths.
- `95`: very likely, only exceptional failure paths remain.
- `100`: logically certain or already definitively true.

Prefer 5-point increments unless there is unusually strong quantitative support (a computed model output justifies finer values). Include `confidence` separately from likelihood. Do not force probabilities across child markets to sum to 100 unless the child markets are verified mutually exclusive and exhaustive under the same rules.

When resolution mechanics differ from the intuitive world event, estimate `resolution_true_likelihood_0_100` and optionally include `world_event_likelihood_0_100` as a supporting field. `likelihood_0_100` must equal `resolution_true_likelihood_0_100` when both are present. `resolution_yes_likelihood_0_100` is accepted only as a transitional alias for YES/NO markets.

In `main_uncertainties`, label each entry as world uncertainty (the event itself is uncertain) or resolution uncertainty (the predicate/resolver behavior is uncertain) — plain text in the entry, no new fields.

These likelihoods are price-blind resolution assessments, not PMKNB forecasts. This skill must not write `forecast` records.

## Domain Playbooks

Route the event to its domain, apply the playbook's deltas, then run the standard method. Playbooks carry deltas only — world directions and recurring resolution gaps — never full research guides. Defer to dedicated skills where installed: `middle-east-research` for its region; the `pmw-*` family owns weather; sports and crypto are out of scope.

**Elections & domestic politics** (races, primaries, appointments, "will X happen by date")
- World: descend to the decisive jurisdictions; named local actors and machines; procedural mechanics — who certifies, who counts, deadlines, legal challenge paths. Polling is one input, never the scaffold.
- Gaps: certification vs media call; recount and challenge windows; "wins" vs "takes office."
- Technique: path-sum over procedural outcomes; for margins, a distribution around polling with historical polling error.

**Global elections** (national elections, by-elections, coalition outcomes)
- World: the domestic-politics playbook plus local-language press, coalition arithmetic, and the country's electoral law — thresholds, rounds, seat formulas.
- Gaps: seat formula vs vote share; coalition formation vs election result; markets often resolve on the legal mechanics, not the headline.
- Technique: path-sum over coalition/round outcomes.

**Geopolitics & conflict** (ceasefires, treaties, strikes, territorial control)
- World: actor reads and interest mapping carry the most weight — most sources are parties to the conflict. Local and regional media in original languages; name the actual negotiators and commanders; map the procedural path a deal must travel (ratification, cabinet votes, oversight).
- Gaps: who confirms a ceasefire "holds"; definitional ambiguity ("strike," "invasion," "control"); confirmation lag vs deadline.
- Technique: hazard for by-date questions; path-sum for negotiated outcomes.

**Macro & rates** (central banks, inflation prints, jobs numbers)
- World: the calendar is the spine — meetings, release dates, blackout periods; named voters and their speech records; revision history of the data series.
- Gaps: which print resolves it — exact index, exact release, first print vs revision; rounding conventions.
- Technique: distribution over the print; bucket likelihoods read off the distribution.

**Equities & company events** (price levels, IPOs, M&A)
- World: filings over news — 8-Ks, S-1s, prospectuses; the specific company's precedent behavior.
- Gaps: whose print resolves it (which source, intraday vs close); announcement vs completion for M&A.
- Technique: hazard for by-date announcements; distribution for price levels.

**Tech & AI** (model releases, benchmarks, product launches)
- World: the company's release precedent — announced vs shipped dates; insider telemetry: job postings, GitHub activity, app-store metadata, conference schedules.
- Gaps: what counts as "released" — public, API-only, waitlist; benchmark scoring authority and what counts as a result.
- Technique: hazard with the company's historical slip rate as the base rate.

**Legal & courts** (rulings, confirmations, criminal cases)
- World: dockets are primary — CourtListener/PACER equivalents; procedural timelines; judge and panel histories; named-party incentives to settle, delay, or appeal.
- Gaps: ruling vs mandate issuance; stay mechanics; "convicted" vs "sentenced" vs "final."
- Technique: path-sum over procedural outcomes, with docket-derived hard date floors.

**Science, health & space** (launches, trials, approvals)
- World: registries and regulators — launch licenses, trial registries, approval calendars; the named facility and vehicle; the specific program's slip history.
- Gaps: "launch" vs "success"; approval vs availability.
- Technique: hazard from the program's precedent slip rate.

**Culture & social-count** (mentions, tweets, celebrity actions)
- World: the counting source defines the market — research its mechanics first; the subject's posting/behavior base rate is the only real signal.
- Gaps: counting-source methodology changes; deleted or edited posts; timezone of the counting window.
- Technique: Poisson or empirical distribution from the subject's base rate.

**No-domain fallback** (novel one-offs with no reference class)
- Construct a reference class by analogy: name the analogy and its disanalogies explicitly. Widen confidence downward. Weight resolution mechanics research more heavily — for novel markets, how it resolves is often less knowable than whether the event happens.

## Quick Estimate

The floor version, for short clocks: five lookups — (1) rules text plus resolver/series precedent, (2) reference-class base rate, (3) top actor's current state and record, (4) closest precedent event, (5) deadline math. Complete the worksheet from these alone, emit likelihood rows with `confidence: low`, and label the report a quick estimate in the body. Same output contract; nothing changes in the schema.

## Output

Produce both readable report content and structured fields. Before emitting output, read [references/output-contract.md](references/output-contract.md) — it defines the `pm_deep_analysis.v1` schema, the `output_mode` flag, apply-batch rules, ID and fingerprint conventions, projection fit, and PMKNB write discipline.

For plain-English answers in estimation mode, still include the per-question likelihood table near the end; mechanism-only briefs omit it:

```markdown
| Market question | Resolution predicate | Likelihood 0-100 | Confidence | Main reason | What could change |
| --- | --- | ---: | --- | --- | --- |
```

## Common Mistakes

- Using Polymarket odds as a prior or sanity check.
- Treating a market title as the resolution rule.
- Reasoning only from rules text when resolver or series precedent is retrievable.
- Treating pre-launch events as already-triggered resolution events without first applying the child market's `market_live_at` gate and checking whether the rules explicitly allow retroactive coverage.
- Letting an inside-view narrative replace the base rate instead of adjusting it.
- "Unlikely, call it 10" on a long-horizon deadline market instead of hazard math.
- Estimating bucket markets independently instead of from one underlying distribution.
- Child-market rows that contradict each other — non-monotone nested deadlines, MECE sets far from 100.
- Skipping the worksheet and writing rationale prose that hides where the number came from.
- Re-researching static foundations during an update pass while ignoring dynamic sources.
- Giving one event-level likelihood when the PM event has several distinct child questions.
- Hiding likelihood estimates in prose instead of a structured table.
- Writing a trading recommendation instead of a price-blind resolution estimate.
- Creating broad keyword signals instead of specific future triggers.
