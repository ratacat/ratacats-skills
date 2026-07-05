---
name: pm-research-methodologies
description: Manual-only. Never auto-load or auto-select this skill from task context. Load only when the user explicitly names pm-research-methodologies, or asks for the general research methodology framework, to structure deep research on a subject that has no dedicated methodology skill.
metadata:
  category: prediction markets
  blurb: "General deep-research scaffold that turns a broad subject into named nodes, sourced claims, provenance checks, synthesis, and open questions."
  keywords:
    - pm
    - research
    - methodology
    - scaffolding
    - provenance
---

# PM Research Methodologies

## Overview

The fallback methodology for researching any subject deeply. When a dedicated skill covers the domain (in this repo: `pm-situation-framing`, `pm-deep-analysis`, `polymarket-event-research`, `pm-market-analysis`; where installed: `middle-east-research`, the `pmw-*` weather family), follow it and use this skill only to fill its gaps.

```
Inputs: subject/question · run budget in queries or time (ask if not given) ·
price-blind? (if yes, follow the governing skill's price-blind protocol,
including what may be browsed) · output destination for the run's artifacts.

Goal: explanatory understanding — why it is like this, how it became like
this — captured so the next run can build on it.

Deliverables: synthesis · scaffold with dark nodes marked · claim ledger ·
open questions. Ledger mode (claims + scaffold, no narrative) when the
output feeds another agent — a narrative bakes in one framing prematurely.

Stop: a full pass changed no load-bearing claim and minted no node worth
researching, or the budget is spent. File what remains as open questions.
```

Surface research describes a subject; deep research explains it. Two questions drive every move: **why is it like this?** and **how did it become like this?** The core discipline is specificity — "the 2027 French presidential election" yields surface takes; "Hénin-Beaumont, the RN federation secretary there, the shuttered Metaleurop smelter" yields understanding. A list of categories is a template; a list of searchable keys is a plan.

## Stage 0 — Root the Question

The question arrives wrapped in context, and the context is part of the subject.

- **Resolution first (markets).** Read the rules text; identify the resolver; retrieve how earlier versions of the series actually resolved — resolver precedent outweighs textual analysis. Precedent lives in the platform's resolved-market pages and the resolver's archive; retrieve it, don't recall it.
- **Key assumptions check.** List the premises the question rests on; tag each solid / caveated / questionable. Questionable premises become scaffold nodes.
- **Reference class.** Before any inside-view research, write: what counts as an instance of this event (one sentence), how many opportunities existed, and the resulting base rate. Findings adjust this anchor; they never replace it.
- **Seed map.** Draft a scaffold from what is already at hand — parametric knowledge plus the Wikipedia article's entities and footnotes — with every claim tagged `unverified`. Three to five orientation queries are licensed here; their only job is harvesting names.
- **Skip conditions.** A single-document or single-entity subject needs no scaffold: read the artifact end to end, then scaffold only its references. A short-clock breaking question gets the quick pass (below) first; scaffold what remains.

## Stage 1 — Build the Scaffold

A **scaffold** is the list of searchable keys whose individual investigation compounds into understanding of the whole; it is the research plan. A **node** is one key: an entity (person, place, organization, event), an instrument (statute, docket number, data series), or a term of art — anything that drops into a specific document stratum. The specificity test: a node naming a category ("local industries") must descend until it names a key ("the CGT local at the former Metaleurop site").

Node types: people · places · organizations · economic structures · events and precedents · rules and instruments.

Descent moves — most subjects reward two or three:

- **Spatial** — nation → region → county → town. Each level has its own actors, records, and press; where the local press is dead, substitute the actors who must still know: the clerk, the chamber of commerce, the planning office.
- **Institutional** — government → ministry → agency → the named officials who sign the documents.
- **Money** — industries → employers → owners: ownership registries, campaign-finance filings, grant and contract awards, procurement notices. Every payment names two nodes, dated and budgeted.
- **Social** — demographics, congregations, unions, schools, local media. Who gathers whom.
- **Temporal** — prior analogous events, base rates, the moment the trajectory bent.
- **Network** — walk the edges of known nodes: who funds, owns, employs, regulates, opposes, succeeded whom. Personnel churn — job postings, executive exits — is an organizational X-ray.

Sizing and order: quick pass = 3 nodes (resolver, top actor, closest precedent); standard run = 8–25 nodes in 2–3 levels; a bigger subject federates into multiple runs. Rank nodes by decision-relevance × expected surprise × findability and work in that order. The scaffold is revisable: Stage 2 mints new nodes; triage them against the same ranking instead of following every edge. Keep each node record self-contained (key, handles, open question) — ready to hand to a parallel worker.

## Stage 2 — Research the Nodes

Work in triage order, one bounded pass per node:

1. **Harvest handles at the first good source**: names, machine identifiers (dockets, tickers, registration numbers, series IDs), and terms of art. Every later query pivots on a harvested handle, never the lay topic — insider vocabulary unlocks strata lay terms cannot reach.
2. **Documents first.** Search the node's primary-record genre before its press; use press as an index that points to documents.
3. **2–5 queries per node**, logged verbatim with hit or miss — a node is only dark relative to the queries actually run. Date-restrict for live subjects. Non-English nodes: translate the query out, search native engines, translate results back. A dead link is not dark until archive.org has been checked.
4. **Ledger claims as found**, never reconstructed at synthesis:

   `claim | node | source + pub date | origin (traced?) | interest note | confidence (confirmed / probable / reported / rumor)`

   Open before citing — no source enters the ledger from a search snippet. Record negative evidence: the docket entry or agenda item that should exist and doesn't. When five or more findings share a shape (dates, votes, slip rates), tabulate them and compute.
5. **Going-deeper juncture** — a report cites a dataset, a story quotes a person, a filing names a docket. Take it only for load-bearing claims, at most two levels deep per node; ledger other leads as open questions.
6. **Stop the node** after two consecutive queries yield no new claims, or when its findings repeat another node's.

Node states:

- **Dark** — declare only after a term-of-art retry, a local-language retry, and an edge approach (query the node's relationship to a lit neighbor) all fail. Then darkness is a finding; record it. Nodes cut for budget are not dark — file them straight to open questions.
- **Flooded** — thousands of hits are the surface takes the scaffold exists to avoid: pivot to identifiers and terms of art, date-restrict, read only primary records until the noise drops.

Source genres:

| genre | examples |
|---|---|
| primary records | filings, dockets, registries, budgets, transcripts, datasets, returns |
| institutional output | agency reports, minutes, inspection records, procurement notices |
| local press | county papers, radio, municipal newsletters — in the local language |
| trade & practitioner | industry press, conference talks, job postings, technical forums |
| social listening | X/Reddit/Telegram — search node names, not the topic; one early crowd pass harvests the consensus narrative, named skeptics, and terms of art |
| adversarial | opposition research, short-seller reports, litigation discovery |
| admissions | one query per key actor for concessions: "X admits / acknowledges / concedes" — the densest evidence per query of any search form |

At any node, two discovery questions: **lateral** — who else would have to know this (regulators, suppliers, former employees, opposing counsel, the losing bidder)? **spatial** — what exists at the place (the paper, the chamber, the parish bulletin, the planning office)?

## Stage 3 — Judge the Chain of Knowing

Every statement arrives through a chain: event → witness → reporter → editor → aggregator → you. Each link has interests and can transform the statement. Judge in proportion: load-bearing and contested claims get the full treatment; uncontested mechanical facts (calendars, rules text, registry entries) pass on one good source.

- **Trace to origin.** Find the earliest appearance: first online timestamp, wire attribution, whose quotes these actually are. Apparent corroboration usually launders one origin through many outlets — credit corroboration only across independent origins, and record the origin in the ledger so the count is auditable.
- **Origins can be manufactured.** Content farms and sockpuppet outlets forge "independent" corroboration cheaply. An origin counts only if it demonstrably existed and covered the beat before the claim — archived snapshots anchor this. On social sources: young accounts and near-identical phrasing across accounts equal one origin. Judge the page before the chain: real byline, domain age, any information the other results lack.
- **Time axis.** Record when the source spoke relative to the event; contemporaneous accounts and later retellings weigh differently.
- **Interest map.** For each load-bearing source, one line: who benefits if this is believed? Discount stake-aligned sources; premium for statements against interest — after asking who benefits from appearing candid, since small confessions buy credibility for large claims. "No visible stake" means no discoverable stake after looking. A checkable claim gets checked no matter who said it.
- **Actor reads.** For recurring actors, build a precedent-grounded theory of mind from the record: does this institution pre-announce or surprise? Do this CEO's announced ship dates hold? Weight what resolves on an actor's *actions* differently from what resolves on their *words*. Validate reads against outcomes; they stale.
- **Knowability tiers.** Tracked actors (long public records) support real actor reads; identifiable-but-thin sources are judged from affiliation and incentives; anonymous or new sources leave the chain dark — weight the claim by its checkability, and check it. Trust is claim-type specific: an outlet reliable on schedules can be unreliable on causes.
- **Media.** A load-bearing photo or video gets a reverse-image search for its first appearance; recycled footage is an origin finding.

## Stage 4 — Synthesize and Climb

- Build a dated timeline from the ledger before writing causal prose; ordering errors surface mechanically.
- Write the synthesis as explanation — why it is like this, how it became like this — citing ledger claims inline. Only `confirmed` and `probable` claims may load-bear.
- State the consensus narrative, where the findings diverge from it, and the trigger observation that would prove the divergence.
- Preserve contradictions between well-sourced claims — after checking they share timeframe, referent, and genre priors (filings are systematically pessimistic, press optimistic). A surviving contradiction is a finding: record both sides and what would settle them.
- Premortem, three lines: assume the synthesis is wrong — which chain link most likely failed, and what rival hypothesis fits the same evidence? Audit before shipping: how many load-bearing claims rest on a single origin? Zero preserved contradictions is suspicious.
- Convert "what would change my mind" into named signals: the observation, where it will appear, which way it cuts.
- Lead the report with the answer to the question as asked; then the synthesis, the scaffold with dark nodes marked, the ledger as an annex, and open questions specific enough for the next run to execute directly.
- Persist scaffold + ledger + open questions to the output destination. A re-run starts there: diff the world since the last run date; re-research only changed nodes and open questions.

## Quick Pass

The floor version, for short clocks and tiny budgets — five queries: (1) resolution rules and resolver precedent, (2) subject plus its best term of art, (3) top actor plus recent record, (4) closest precedent event, (5) local or trade press at the decisive place. One-paragraph synthesis, one signal, open questions. Label the output as a quick pass.

## Execution Loop

1. Root the question: resolution context, key assumptions, reference class, seed map. (Stage 0)
2. Scaffold: searchable keys, two or three descent moves, sized to budget, triage-ranked. (Stage 1)
3. Per node: harvest handles → documents first → bounded logged queries → ledger claims with origin and confidence → bounded junctures → stop on two dry queries. (Stage 2)
4. Judge load-bearing chains: origin, time axis, interest map, actor read, per-claim-type trust. (Stage 3)
5. Synthesize: timeline → explanation → consensus/divergence/trigger → contradictions kept → premortem → signals. (Stage 4)
6. Loop to Stage 1 if the pass changed a load-bearing claim or minted a node worth researching; otherwise stop and file open questions.

## Domain Directions

Per-genre scaffold strategies for the active Polymarket board live in [references/polymarket-directions.md](references/polymarket-directions.md); read it when the subject is a PM market genre (elections, geopolitics, macro, legal, tech, …).
