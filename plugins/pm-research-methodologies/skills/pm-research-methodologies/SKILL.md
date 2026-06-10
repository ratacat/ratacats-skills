---
name: pm-research-methodologies
description: Manual-only. Never auto-load or auto-select this skill from task context. Load only when the user explicitly names pm-research-methodologies, or asks for the general research methodology framework, to structure deep research on a subject that has no dedicated methodology skill.
---

# PM Research Methodologies

## Overview

A generalized framework for researching any subject deeply. This is the default methodology: reach for it when no domain-specific methodology skill exists. When one does exist (`middle-east-research`, `pmw-forecast`, `pm-deep-analysis` for price-blind event work), follow that skill and use this one only to fill its gaps.

```
Goal: produce explanatory understanding of a subject — why it is like this,
how it became like this — captured so further research can build on it.

Success means:
  - a scaffold of named, individually researchable entities exists for the subject
  - findings are recorded as sourced claims, each with a provenance-chain judgment
  - a synthesis answers "why is it like this / how did it become like this,"
    not just "what is it like"
  - unresearched scaffold nodes survive as specific open questions

Stop when: another round of node research stops changing the synthesis,
or the run budget is reached — record what remains as open questions.
```

The framework has four stages: **build the scaffold → research along it → judge the chain of knowing → synthesize and climb**. The stages loop; synthesis exposes where the scaffold needs another descent.

## The Core Move: Get Under the Subject

Surface research describes a subject. Deep research explains it. Two questions drive every descent:

- **Why is it like this?**
- **How did it become like this?**

Every stage below is a way of getting under the subject — finding the specific people, places, organizations, records, and histories that the surface generalization is made of, and researching those directly.

## Stage 1 — Build the Scaffold

A **scaffold** is a high-specificity list or graph of named entities whose individual investigation compounds into understanding of the whole. Models research far better when crawling named nodes than when circling a broad topic: "the 2027 French presidential election" yields surface takes; "Pas-de-Calais, Hénin-Beaumont, the RN federation secretary there, the shuttered Metaleurop smelter" yields understanding.

Build the scaffold **before** running research queries. The scaffold is the research plan.

### Root into the question's context

A research question arrives wrapped in context, and the context is part of the subject. Before researching the world, understand the question: who is asking, what would actually settle it, and whether its premises still hold. For prediction markets, resolution context is central — read the rules text, learn who or what resolves the market, what counts and what is excluded, and what has counted before. For re-issued or series markets, how earlier versions actually resolved outweighs textual analysis: the resolver's past behavior is the best evidence of how the rules will be read. The world and the resolution can diverge; research serves the question as it will actually be settled, not the question as it appears.

### Node types

| type | examples |
|---|---|
| people | candidates, officials, negotiators, executives, judges, local power brokers |
| places | regions, departments/counties, cities, districts, facilities |
| organizations | parties, companies, unions, churches, nonprofits, militias, courts, agencies |
| economic structures | industries, major employers, supply chains, ownership networks |
| events | past elections, strikes, scandals, rulings, defaults — the precedent record |
| rules & instruments | statutes, treaties, procedures, charters, resolution criteria |

### Descent moves

Apply whichever moves fit the subject; most subjects reward two or three:

- **Spatial descent** — nation → region → county/department → city → neighborhood. Each level has its own actors, records, and press. A national election is millions of people and pure noise; a county has a newspaper, a dominant employer, a mayor, a history.
- **Institutional descent** — government → ministry → agency → office → the named officials who sign the documents.
- **Economic slice** — what do the people there actually do? Industries → major employers → owners → whether those livelihoods are growing or dying, and since when.
- **Social slice** — demographics, congregations, unions, clubs, schools, local media. Who gathers whom.
- **Temporal descent** — how did it become like this? Prior analogous events, base rates, turning points, the moment the trajectory bent.
- **Network expansion** — from each node, walk the edges: who funds, owns, employs, regulates, opposes, succeeded, or married whom. New nodes come from edges of old ones.

### Right-sizing the scaffold

Descend until nodes become individually researchable; ascend when they stop being findable.

- A node that returns only national-level commentary sits too high to learn from — descend a level.
- A node that returns nothing at all is a **dark node** — ascend one level or approach it through a neighboring node's edges.
- The **specificity test**: scaffold nodes are proper nouns or near-proper nouns. A list of categories ("local industries, key politicians") is a template, not a scaffold. A list of names ("Hénin-Beaumont; Steeve Briois; the CGT local at the former Metaleurop site") is a scaffold.

Size the scaffold to the run budget: 8–25 nodes for a bounded run, organized in 2–3 levels. Record nodes you cut — they become open questions.

## Stage 2 — Research Along the Scaffold

Work node by node, with bounded passes:

1. Run 2–5 queries per node. Vary the query form: the node's name alone, the name + the subject question, the name + each slice (economic, political, historical).
2. Capture findings as atomic claims with the source attached. One claim, one statement, one provenance.
3. Mark dark nodes and move on. Darkness is information: absence of coverage is itself a finding worth one line.
4. At every finding, take the **going-deeper juncture**: a report cites a dataset — get the dataset. A story quotes a person — that person is a new node. A filing references a docket — open the docket.

### Insider vocabulary

Every domain has an insider vocabulary, and the insider terms unlock a stratum of sources the lay terms can never reach. Search the lay term, harvest the terms of art from the first good source, then re-search with the terms of art. That single move is often worth more than ten additional lay-term queries.

Examples: "election lawsuit" → the docket number and the legal doctrine name; "weather forecast" → "MOS guidance", the station identifier; "Fed decision" → the specific facility, the dot plot, the named alternates. Each one drops you into trade press, dockets, registries, and practitioner forums.

### Slices

Run the same scaffold through different lenses and compare what each lens returns: the economic story of a place, the political story, the historical story. Where the slices disagree — a town whose press is optimistic while its largest employer's filings show decline — the disagreement is the finding.

## Stage 3 — The Chain of Knowing

Every statement reaches you through a chain: event → witness → reporter → editor → publisher → aggregator → you. Each link has interests, and each link can transform the statement. *Where did this come from?* is always the question. Trace reports back to their origin — apparent corroboration often launders a single origin, one leaker's claim quoted by an aggregator quoted by three more outlets. Credit corroboration only across independent origins.

Treat every source as answering two questions at once: *what does this say about the subject?* and *what does this say about the speaker?* A statement is evidence about its speaker at least as much as about its subject.

### Interest mapping

For each load-bearing source, write one line: **who benefits if this is believed?** Campaign-adjacent outlets, state media, short sellers, litigants, officials managing expectations — their statements are moves in a game, and the game is often more informative than the statement. Sources with no visible stake in the claim earn more weight; sources whose stake aligns with the claim earn a discount; sources speaking **against** their own interest earn a premium.

### Actor reads

For recurring public actors, the historical record supports a precedent-grounded theory of mind — an **actor read**. Build it from the record and use it to weight statements:

- Example: Trump's record establishes that his positions are instantaneous and reversible, his statements frequently conflict, and he treats prior commitments as non-binding. Therefore weight any single Trump statement as a move, not a commitment — and weight markets that resolve on his *actions* very differently from markets that resolve on his *words*.
- Build the same kind of read for any actor who appears repeatedly in your subject: does this institution pre-announce or surprise? Does this CEO ship on announced dates? Does this ministry's spokesman ever contradict the leader?

### Knowability tiers

Calibrate how much chain-judgment is even possible:

- **Tracked actors** (politicians, agencies, listed companies, established outlets): long public records — build real actor reads.
- **Identifiable but thin** (local figures, small outlets, named analysts): judge from affiliation and incentive structure.
- **Anonymous or new** (unattributed claims, fresh accounts, single-source stories): the chain is dark — weight the claim by its checkability, and check it.

Trust is also **claim-type specific**: an outlet can be reliable on schedules and unreliable on causes; a ministry can be honest about numbers and dishonest about reasons. Assign trust per claim type, never per source as a whole.

## Stage 4 — Synthesize and Climb

Climb back up the scaffold. Node-level findings answer level-above questions: what twenty county findings say about the region, what the region says about the nation.

- Write the synthesis as explanation: *why it is like this, how it became like this*, with the claims that carry the explanation cited inline.
- Preserve contradictions as contradictions. Two well-sourced claims that disagree are a finding; pick neither, record both, and state what evidence would settle them.
- State what would change your mind: the specific observation that would break the synthesis. That sentence becomes a signal worth monitoring.
- Include the scaffold you actually used in the report, with dark nodes marked. The research plan is part of the deliverable; it makes the run auditable and gives the next run its starting map.
- Convert every dark node into a specific open question, phrased so a future bounded run can execute it directly.

## Source Genres and Discovery Moves

Conceptualize sources by genre, and use lateral and spatial questions to find them:

| genre | examples | reach them via |
|---|---|---|
| primary records | filings, dockets, registries, budgets, transcripts, datasets, election returns | insider terms of art; institutional descent |
| institutional output | agency reports, minutes, inspection records, procurement notices | the issuing office, found by descent |
| local press & media | county papers, local radio, regional TV, municipal newsletters | spatial descent; search in local language |
| trade & practitioner | industry press, conference talks, job postings, technical forums | search with the insider lexicon |
| social listening | X/Twitter questions and chatter (`x-questions` skill via xpool), Reddit, local Facebook groups, Telegram | search the node names, not the topic |
| adversarial | opposition research, short-seller reports, litigation discovery, leaked documents | search the node + "lawsuit / investigation / report" |

The two discovery questions to ask at any node:

- **Lateral:** who else would *have* to know this? (regulators, suppliers, neighbors, former employees, opposing counsel, the losing bidder)
- **Spatial:** what exists *at the place*? (the local paper, the chamber of commerce, the parish bulletin, the planning office)

## Polymarket Domain Directions

Leading directions per genre of the active Polymarket board. These are pointers; when a domain accumulates real craft, promote it into its own methodology skill and trim this table.

On price-blind runs, market prices, odds, and order books are out-of-scope inputs; the market's rules text is always in scope.

- **Elections & domestic politics** (US races, primaries, appointments, "will X happen by date"): descend spatially to the decisive jurisdictions; research named local actors and machines; pull precedent base rates for the event class; map the procedural mechanics — who certifies, who counts, what deadlines and legal challenges exist. Polling is one source genre, never the scaffold.
- **Global elections** (Sweden, France, by-elections): same descent plus local-language press, coalition arithmetic, and the country's specific electoral law (thresholds, rounds, seat formulas — markets often resolve on these mechanics).
- **Geopolitics & conflict** (Iran, Israel, Ukraine, Hormuz, ceasefires, treaties): actor reads and interest mapping carry the most weight here — most sources are parties to the conflict. Find local and regional media in original languages; name the actual negotiators and commanders; map the procedural path a deal must travel (ratification, cabinet votes, oversight). Defer to `middle-east-research` for its region.
- **Macro & rates** (Fed, global central banks, inflation prints): the calendar is the scaffold — meetings, release dates, blackout periods; named voters and their speech records; revision history of the data series; the resolution source's exact print (which index, which release).
- **Equities & company events** (price levels, valuations, IPOs, M&A): filings over news — 8-Ks, S-1s, prospectuses; precedent behavior of the specific company; the mechanics of the trigger (whose print resolves it, intraday or close).
- **Tech & AI** (model releases, benchmarks, product launches): the company's release precedent (announced vs shipped dates); insider telemetry — job postings, GitHub activity, app-store metadata, conference schedules; benchmark mechanics (who scores it, what counts as a result).
- **Legal & courts** (rulings, confirmations, criminal cases): dockets are primary — CourtListener/PACER equivalents; procedural timelines set hard date floors; judge and panel histories; named-party incentives to settle, delay, or appeal.
- **Science, health & space** (launches, trials, approvals): registries and regulators — launch licenses, trial registries, approval calendars; the named facility and vehicle; precedent slip rates for the specific program.
- **Culture & social-count** (mentions, tweets, celebrity actions): normally blocked in PMKNB discovery; when explicitly user-directed, research the resolution mechanics first — the counting source defines the market, and the subject's posting/behavior base rate is the only real signal.
- **Sports, crypto, weather**: out of scope — blocked in PMKNB discovery or owned by a dedicated system (pm-weather).

## Domain Lexicon

Shared terms for this framework, usable across prompts, reports, and discussion:

| term | meaning |
|---|---|
| **scaffold** | the named-entity list/graph built before querying; the research plan |
| **node** | one individually researchable entity on the scaffold |
| **descent** | moving down a specificity level (nation → county → town) |
| **slice** | one lens run across the whole scaffold (economic, social, temporal) |
| **dark node** | a node left unlit — searched and empty, or cut for budget; itself a finding |
| **chain of knowing** | the transmission path of a statement from event to reader |
| **interest map** | the one-line answer to "who benefits if this is believed?" |
| **actor read** | a precedent-grounded theory of mind for a named actor or group |

## Quick Reference

1. Root into the question's context — for markets, the resolution context: rules, resolver, series precedent — and write the outcome block.
2. Build the scaffold: pick 2–3 descent moves, list 8–25 proper-noun nodes.
3. Research node by node: bounded queries, atomic sourced claims, deeper at every juncture, re-search with insider terms of art when they show themselves.
4. Judge each load-bearing source's chain: where it came from, independent origins, interest map, actor read, knowability tier, per-claim-type trust.
5. Synthesize upward: explain why/how-it-became, keep contradictions, show the scaffold, state what would change your mind, file dark nodes as open questions.

## Rules

- Root into the question's context before researching the subject; for markets, resolution context comes first.
- Build the scaffold before running queries; queries without a scaffold produce surface takes.
- Make every node a proper noun; descend until that is true.
- Trace reports to their origin; credit corroboration only across independent origins.
- Take the going-deeper juncture every time a source cites something more primary.
- Write the interest map for every source that carries weight in the synthesis.
- Treat statements by tracked actors through their actor reads, and statements against interest as premium evidence.
- Keep contradictions; resolving them prematurely destroys the most valuable finding.
- End every run with open questions specific enough to execute directly.
