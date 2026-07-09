# World Research Craft

Depth tools for the World Research stage, folded in from the retired `polymarket-event-research` skill. Use them when an event's resolution runs through institutions, procedures, or localities — they sharpen the scaffold and the evidence ledger; the estimation method is unchanged.

## Mechanism Chain Card

Decompose the outcome into necessary steps. Per step:

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

Separate announcement, legal effect, implementation, enforcement, and settlement proof. A decree announced is not a decree published; a bill passed by one chamber is not a law; a media call is not certification unless the rules say so. Normalize publication date, effective date, deadline timezone, business days, holidays, recesses, court calendars, and certification periods when relevant.

## Formal vs Practical Power

Keep two maps. Formal: the office or body legally able to act, and the statute, rule, votes, signatures, filings, publication, or certification it needs. Practical: agenda setters, committee chairs, whips, judges, clerks, prosecutors, regulators, coalition partners, unions, local elites, media gatekeepers — their incentives and constraints.

Per important actor:

```text
Actor:
Formal role:
Stated position:
Material incentive:
Political/legal/reputational incentive:
Constraint:
What new evidence would change the picture:
Evidence for this assessment:
Inference vs fact:
```

Label incentives and beliefs as inference unless directly sourced. Famous-person bias check: ask who touches the paper, docket, calendar, certification, or enforcement — not who is in the headline.

## Geographic Specificity

Do not stop at national-level sourcing when a local body controls, enforces, litigates, counts, certifies, or reports the outcome. Identify (or justify skipping): the administrative subdivision and its local-language name; the relevant court, agency, election board, regulator, council, gazette, docket, calendar, or clerk; the local media market and beat reporters.

Local-language research is required when the controlling institution, records, or media are not primarily English; optional only when the relevant channels are entirely English or unavailable after a documented search.

## Search Packs

For a full run, execute or propose at least one query per applicable pack and state why any pack does not apply:

| Pack | Example shape |
| --- | --- |
| Official | `site:.gov "<bill/case/agency>"`, gazette, docket, calendar, commission page |
| Locality | city/county/province/district plus procedure term |
| Actor | named officials, committee chairs, judges, clerks, candidates, agencies |
| Procedure | bill number, case number, docket, agenda, hearing, certification, order |
| Opposition/veto | opposition actor, lawsuit, injunction, boycott, delay, veto, amendment |
| Recent check | date-bounded query for latest official or local update |
| Local language | translated actor, office, locality, procedure, and ambiguous predicate terms |

Record per query: query, date/time, top useful result (or dead end), next derived query.

## X/xpool Source Classification

Use X/xpool when real-time local or elite information may precede official confirmation: resignations, appointments, whip counts, protests, small jurisdictions, weak official feeds. Read `xpool --help` before first use. Social posts discover names, documents, locations, and accounts to monitor — they are not durable facts by themselves.

Classify each social claim:

```text
Account type: official / direct participant / credentialed journalist / beat-local reporter / insider / activist-witness / aggregator / anonymous-bot-like
Original source:
Echoes from same origin:
Confirmed / unconfirmed / contradicted:
```

Trace viral claims to the original source before writing factual claims; apparent corroboration usually launders one origin through many outlets.

## Evidence Ledger Discipline

Every important claim carries: source, type, time, actor/location, reliability, implication, and **what it does not prove**.

| Claim | Source | Type | Time | Reliability | Implication | Does not prove |
| --- | --- | --- | --- | --- | --- | --- |
| Committee hearing scheduled May 21 | State senate calendar | official procedural | 2026-05-16 | high | bill still active | floor passage or signature |

Include negative evidence when important: no docket entry, no agenda item, no gazette publication, no certification document, no schedule update. For conflicts, name the controlling source and why it controls; mark superseded sources stale instead of dropping them.

## Domain Checks

Per event type, the mechanism map must identify:

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

## Shallow-Research Tripwires

Deepen the research if:

- it only names national leaders or generic institutions while resolution depends on a clerk, docket, board, committee, gazette, local court, regulator, or certification body
- every source is secondary and no official or primary target is named
- the watch items say "monitor news" without an exact page, calendar, docket, account, office, or document type
- ambiguous rule terms are not defined against concrete evidence
