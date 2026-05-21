---
name: polymarket-event-research
description: Use when the user asks for price-blind research on the real-world resolution mechanics of a specific Polymarket or prediction-market event, including actors, institutions, legal/procedural paths, local context, source discovery, proof standards, structured research handoffs, or KNB world-mode mapping. Do not use for odds, prices, portfolios, trade decisions, market microstructure, or forecast/EV analysis.
---

# Polymarket Event Research

## Overview

Use this for price-blind world research on one prediction-market event or a tightly related event cluster. The job is to explain how the world would make the event true or false through named people, offices, institutions, procedures, localities, incentives, veto points, and information channels.

This is not market analysis. Do not discuss prices, odds, fair value, EV, edge, trades, buy/sell/hold, liquidity, positions, exposure, allocation, volume, order books, CLOB data, or mispricing. If the user asks for value, mispricing, trading, or forecasting, produce only the world-research brief and stop unless a separate market-analysis skill or mode is invoked.

Durable handoff is for world context in a prediction-market knowledge base, pmknb if available. If writing to pmknb or another durable store, use world-mode records only. If no store is available, include the same information in the brief.

## Context Boundary

Use target-provided resolution rules, user-pasted market text, existing instrument metadata, or a price-blind rule source when available. Do not browse into live market pages, APIs, order books, CLOB data, charts, market movement, holder data, or trader data just to get rules if that exposes prices, odds, volume, liquidity, or market behavior.

When a page contains both static rules and live market data, use it only if the tool can retrieve a price-blind rules-only representation. Do not inspect, summarize, or mention page regions containing prices, odds, volume, liquidity, order books, charts, market movement, holder data, or trader data.

If the exact resolution rule is unavailable without exposing market data, do not infer it from the headline. Produce a `Predicate unavailable` brief: known title, missing rule source, ambiguity list, safe source targets, and the next rule-capture step.

## Report Contract

Treat a substantial research result as a durable `report` when pmknb or another compatible KNB is available. The report stores the full authored artifact in one place and links to the structured evidence graph underneath it.

Every substantial output has two layers:

1. **Report artifact** - human-readable full research output, stored as `report.body_markdown` with typed `sections`.
2. **Evidence graph** - `source`, `claim`, `entity`, `signal`, `review_item`, `run_trace`, embedded `open_questions`, and links cited by the report.

Do not create canonical `research_packet`, `source_pack`, `resolution_rule`, `mechanism_step`, `timeline_event`, or `question` records. Store the whole authored research artifact as a `report`; decompose important durable facts into sources and claims linked from that report. Put uncertain, provisional, or user-judgment-dependent writes into `review_item`.

Load `references/research-formats.md` when the user asks for structured research output, durable KNB handoff, or a research type other than the default event-resolution report.

## When To Use

Use when the user asks to research a concrete Polymarket or prediction-market event, understand what would resolve it, find sources, map power, prepare a deep dive, or create durable world context.

Do not use for pure market mechanics, order books, portfolio review, forecast writing, trade recommendations, or broad topic research not tied to a concrete event or event cluster.

## Core Invariant

No brief is valid unless it names the concrete source channel that would resolve or materially update the event: docket URL or name, gazette, calendar, board, agency page, court, clerk, filing system, certification body, official account, or named publication channel. If the channel is unknown, the brief must be primarily about finding that channel.

Every run must explain:

- the exact world condition that resolves the event, or why the predicate is unavailable
- who can make it happen
- who can stop or delay it
- which locality, office, docket, calendar, or enforcement body matters
- which source would prove it, and which expected source is missing

If a knowledgeable local reporter, court clerk, legislative staffer, agency official, or beat analyst would say the brief misses the machinery, the research is still too shallow.

## Forbidden Language

Avoid market and forecast vocabulary:

- probability, likely, unlikely, over/underpriced, cheap, expensive, value, edge, signal-to-price, market believes, implied, priced in, consensus odds
- tradeable, position, exposure, allocation, bet, side, long, short, buy, sell, hold, fade, arb
- liquidity, volume, order book, CLOB, expected value, fair value
- numeric confidence that functions as a forecast

Allowed mechanism language:

- mechanism complete/incomplete
- source confirmed/unconfirmed
- procedurally possible
- blocked by a named step
- deadline-sensitive
- unresolved ambiguity
- proof source missing

Use "what new evidence would change the mechanism status," not "what would change the current read."

## Workflow

### 1. Preflight

Before researching, capture:

```text
Event identifier or title:
User-provided market text or rules:
Live market pages off-limits?:
Known deadline:
Jurisdiction/locality hypotheses:
Tools available:
Tool/source limits:
```

If the predicate or rules are unavailable without exposing prices, produce the `Predicate unavailable` brief and stop after listing safe source targets and the next rule-capture step.

### 2. Extract The Resolution Predicate

Start from the exact predicate, not the headline topic.

Capture:

| Field | Requirement |
| --- | --- |
| Exact title | Preserve the market/event wording. |
| Required condition | Minimum observable world state that makes the event true. |
| Deadline | Normalize date, timezone, cutoff, and whether inclusive. |
| Settlement source | Official source, oracle, rule page, docket, certification body, or named publication channel. |
| Ambiguous terms | Words like `ban`, `blocked`, `approved`, `resigned`, `won`, `attended`, `launched`, `passed`, `in effect`, `deal`. |
| Non-counting events | Announcements, rumors, partial steps, or media calls that do not satisfy the rule. |
| Proof standard | Document, filing, order, certification, notice, publication, or physical-world evidence that proves it. |

Separate announcement, legal effect, implementation, enforcement, and settlement proof. A decree announced is not a decree published; a bill passed by one chamber is not a law; a media call is not certification unless the resolution rules say so.

### 3. Build The Mechanism Chain

Decompose the outcome into necessary steps. For each step, fill this card:

```text
Step:
Current status:
Formal controller:
Practical controller:
Required action or document:
Calendar/deadline:
Veto or delay actor:
Source that proves completion:
Source that proves blockage:
Open question:
```

Date handling must normalize publication date, effective date, deadline timezone, business days, holidays, legislative recesses, court calendar limits, and certification periods when relevant.

### 4. Map Power At Two Levels

Keep formal authority and practical power separate.

Formal power:

- office or body legally able to act
- statute, rule, procedure, charter, contract, or court order
- votes, signatures, hearings, filings, publication, certification, or effective dates

Practical power:

- agenda setters, committee chairs, whips, party officials, judges, clerks, prosecutors, police, regulators, coalition partners, unions, donors, local elites, media gatekeepers, foreign institutions
- incentives, constraints, reputational costs, and likely information sources

For every important actor, write:

```text
Actor:
Formal role:
Stated position:
Material incentive:
Political/legal/reputational incentive:
Constraint:
What new evidence would change the mechanism status:
Evidence for this assessment:
Inference vs fact:
```

Label incentives and beliefs as inference unless directly sourced.

### 5. Force Geographic Specificity

Do not stop at national-level sourcing when a local body controls, enforces, litigates, counts, certifies, or reports the outcome.

Identify when applicable, or explain why narrower geography is irrelevant:

- country, state/province/region, district, county, municipality, neighborhood, or facility
- administrative subdivisions and local-language names
- relevant court, agency, election board, police office, regulator, council, gazette, docket, calendar, or clerk
- local media market and beat reporters

Local-language research is required when the controlling institution, locality, official records, or media are not primarily English. It is optional only if the relevant channels are entirely English-language or unavailable after a documented search.

### 6. Generate Search Packs

Read `exa-cli --help` once per environment before web research in repos that require it. If `exa-cli` is unavailable, record the substitute search tool.

For a full run, execute or propose at least one query from each applicable pack and state why any pack does not apply:

| Pack | Example shape |
| --- | --- |
| Official | `site:.gov "<bill/case/agency>"`, official gazette, docket, calendar, commission page |
| Locality | city/county/province/district plus procedure term |
| Actor | named officials, committee chairs, judges, clerks, candidates, agencies |
| Procedure | bill number, case number, docket, agenda, hearing, certification, regulation, order |
| Opposition/veto | opposition actor, lawsuit, injunction, boycott, delay, veto, amendment |
| Recent check | date-bounded query for latest official or local update |
| Local language | translated actor, office, locality, procedure, and ambiguous predicate terms |

For every query run, record:

```text
Query:
Date/time:
Top useful result:
Dead end, if none:
Next derived query:
```

Useful commands:

```bash
exa-cli search "<query>" -n 8 -t auto -c 10000
exa-cli search "<query>" -n 10 -t deep -l preferred
exa-cli deep-search "<objective>" -q "<official angle>" "<local-language angle>" "<veto angle>"
```

### 7. Source Priority

Prefer sources in this order:

1. Resolution rule, oracle, or official market rule text provided price-blind.
2. Official legal/procedural source: docket, gazette, statute, agency notice, election board, court order, filing, calendar, certification.
3. Direct participant or institution statement.
4. Credentialed local or beat reporting.
5. Specialist analyst with transparent sourcing.
6. Social media for discovery only unless confirmed by a higher-priority source.

Newer official procedural records control over older secondary reporting unless the resolution rule says otherwise.

### 8. Use X/xpool As Signal Discovery

Use X/xpool when real-time local or elite information may precede official confirmation: resignations, appointments, court/local reporting, whip counts, protests, military/police events, small jurisdictions, or weak official feeds.

Before xpool, read `xpool --help`. Submit focused jobs, check back, and collect results through the CLI. Do not treat social posts as durable facts by themselves.

Classify social material:

```text
Official account:
Direct participant:
Credentialed journalist:
Beat/local reporter:
Party/agency insider:
Activist/witness:
Aggregator/commentator:
Anonymous or bot-like:
Original source:
Echoes from same origin:
Confirmed / unconfirmed / contradicted:
```

Use social posts to discover names, documents, locations, primary sources, and accounts to monitor. Trace viral claims back to the original source before writing factual claims.

### 9. Maintain An Evidence Ledger

Every important claim needs provenance and limits.

| Claim | Source | Type | Time | Actor/location | Reliability | Implication | Does not prove |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Committee hearing scheduled May 21 | State senate calendar | official procedural | 2026-05-16 | Senate committee | high | bill is still active | floor passage or signature |

Include negative evidence when important: no docket entry, no agenda item, no gazette publication, no certification document, no enforcement notice, no official schedule update.

For conflicts, identify the controlling source, timestamp, and reason it controls. Mark older or contradicted sources stale instead of silently dropping them.

### 10. Synthesize Mechanism Paths

A useful brief explains paths, not vibes. Do not rank likelihoods or predict market movement.

Required paths:

- event becomes true
- event fails
- event gets delayed past deadline
- ambiguous-resolution path
- new evidence that would change the mechanism status

For each path, cite the mechanism step, actor, evidence, and watch item that would update it.

### 11. Produce Handoff Output

Choose output depth:

- **Minimal Report**: predicate, source channel, current status, proof/missing proof, next source to check.
- **Full Report**: all sections below.
- **Report + KNB Handoff**: full report plus proposed durable records, review items, open-question updates, and links. Use the report contract in `references/research-formats.md`.

Use this structure for a full brief:

```text
# Event Research Brief

## Resolution Predicate
Exact condition, deadline, source, ambiguities, what does not count.

## Current World State
Dated evidence for what has already happened.

## Mechanism Map
Necessary steps, responsible actors, veto points, calendars, proof sources.

## Actor / Institution / Geography Map
Named people, offices, agencies, localities, enforcement bodies, practical power.

## Source Map
Official sources, local sources, local-language queries, xpool handles/jobs, documents.

## Evidence Ledger
Claims with sources, reliability, implications, limits, conflicts, and stale sources.

## Mechanism Paths
True path, false path, delay path, ambiguous path, and evidence that changes status.

## Watchlist
Specific calendars, dockets, meetings, accounts, agencies, dates, and missing documents.

## Open Questions
Unknowns that materially affect the outcome.

## Next Searches
Concrete exa-cli, local-language, official-domain, and xpool searches to run next.
```

In pmknb, durable outputs should be world-mode records: `report`, `source`, `claim`, `entity`, `signal`, `review_item`, `run_trace`, and lightweight `memo` records as appropriate. Sources come before claims. Reports store the full authored artifact; important durable facts still become linked atomic claims. Memos remain for brief guidance or short synthesis. Cheap or uncertain automation proposes review items instead of writing durable claims.

## Domain Checks

| Event type | Must identify |
| --- | --- |
| Bill/law/policy | chamber path, committee, executive signature/veto, publication, effective date, enforcement body |
| Court/rule blocked | court, case number, judge/panel, docket, motion type, order type, stay/appeal path |
| Election | boundaries, candidates, counting body, provisional results, recount/challenge path, certification source/date |
| Appointment/removal | legal authority, required cause/hearing/confirmation, successor rules, effective record |
| Ban/enforcement | legal basis, regulator/police, jurisdiction, penalties, injunction risk, observed enforcement channel |
| Summit/attendance | official schedules, host/foreign ministry, credentialed correspondents, arrival/security ambiguity |
| Protest/security | command structure, local police/military units, locations, casualty/arrest reporting, hospital/court channels |
| Corporate/institutional | board/committee authority, filing/disclosure source, effective date, regulator/exchange notice |

## Quality Gates

Before finishing, check:

- No market-analysis leakage or forbidden vocabulary.
- Predicate is exact, or a `Predicate unavailable` brief explains the gap.
- A concrete proof channel is named, or the brief is primarily about finding it.
- At least one formal proof source and one practical information channel are named.
- Veto/delay mechanisms are explicit.
- Date, timezone, deadline, recess, holiday, publication, and effective-date issues are handled when relevant.
- Local-language and locality-specific sourcing is present, or absence is justified.
- Social claims are classified by source type and confirmation status.
- Evidence ledger includes what each source does not prove.
- Watchlist names concrete pages, accounts, calendars, dockets, offices, document types, or dates.
- Output is reusable by the next agent without rediscovering actors and sources.

For political/legal/institutional events, avoid under-mapping when applicable, or explain why narrower coverage is enough:

- 5 named people or offices
- 3 institutions
- 2 localities or administrative units when geographic
- 3 official or primary source targets
- 5 concrete follow-up queries
- 3 veto/delay mechanisms

## Shallow-Research Tripwires

Fail and deepen the brief if:

- it only names national leaders, famous actors, or generic institutions while resolution depends on a clerk, docket, board, committee, gazette, local court, regulator, certification body, or publication channel
- every source is secondary and no official or primary target is named
- the watchlist says "monitor news" without exact page, calendar, docket, account, office, or document type
- ambiguous rule terms are not defined against concrete evidence
- a mechanism-status conclusion reads like a forecast

Good mechanism-status conclusions:

- `Mechanism incomplete: committee hearing is scheduled, but no floor vote or signed order exists.`
- `Proof source missing: the certification board calendar names the next meeting, but no certification document is posted.`
- `Deadline-sensitive: publication in the gazette must occur before the rule cutoff; announcement alone does not satisfy the predicate.`

## Failure Modes

| Failure | Correction |
| --- | --- |
| Headline research instead of resolution research | Restart from predicate and proof standard. |
| English-only or capital-only sourcing | Add official, local, and local-language packs. |
| Announcement treated as completion | Separate announcement, legal effect, implementation, enforcement. |
| Famous-person bias | Ask who touches the paper, docket, calendar, certification, or enforcement. |
| Formal authority confused with practical control | Split formal and practical power maps. |
| X rumor laundering | Trace original source, classify account, seek primary confirmation. |
| Missing negative evidence | Look for expected-but-absent docket, agenda, gazette, certification, or notice. |
| Bad time handling | Normalize deadline, timezone, effective date, publication date, holidays, recesses. |
| One-sided mechanism path | Add true, false, delay, and ambiguous-resolution paths. |
| Generic watchlist | Replace with specific URLs, offices, accounts, dates, and documents. |

## Pressure Tests

Use these to test an agent or a draft brief:

1. User includes odds and asks if the market is mispriced. Pass only if output stays price-blind and mechanism-focused.
2. `Will Bill X become law by Dec 31?` Pass only if chambers, signature/veto, publication, effective date, and deadline are distinguished.
3. `Will the mayor of Springfield resign before June 1?` Pass only if the agent identifies which Springfield and the filing/succession channel.
4. `Will Country A ban Product B?` Pass only if announcement, regulation, gazette, effective date, enforcement, and injunction risk are separated.
5. `Rumors on X say the minister resigned.` Pass only if the original rumor, official accounts, reporters, echo map, and confirmation status are separated.
6. `Will Candidate X win the regional election?` Pass only if media calls, provisional results, challenges/recounts, and certification are distinct.
7. Two sources conflict, with an updated official docket contradicting an older English article. Pass only if the official updated docket controls and the older article is labeled stale.
8. Another agent must continue tomorrow. Pass only if named actors, sources, queries run, next queries, dates, open questions, and watchlist are explicit.
