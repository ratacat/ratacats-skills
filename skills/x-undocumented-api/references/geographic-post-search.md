# Geographic post search

Use this reference to search posts by location metadata, combine that filter
with keywords, or measure observed volume over a fixed time window.

## Three different identifiers

- WOEID: numeric location ID for `trends/place`. SF is `2487956`.
- Explore `place_id`: signed decimal string used by the location picker and
  saved settings. SF city is `6489983042664404591`.
- Post `place.id`: hexadecimal ID attached to post metadata. SF is
  `5a110d312052166f`.

Do not interchange these identifiers. Read post-place IDs from returned
`legacy.place` objects or a verified geographic lookup. Similar display names
do not establish that IDs or geographic boundaries are equivalent.

## Working SearchTimeline queries

Verified on September 5, 2026:

```text
place:5a110d312052166f
AI place:5a110d312052166f lang:en
"Claude Code" place:5a110d312052166f lang:en
coffee place_country:US lang:en
coffee place_country:GB lang:en
```

These use the standard `SearchTimeline` variables:

```json
{
  "rawQuery": "place:5a110d312052166f",
  "product": "Latest",
  "count": 20,
  "querySource": "typed_query"
}
```

The place-only query returned 20 posts with matching SF place metadata.
Country queries returned matching country codes. This is location metadata
attached to the post, not a requirement that its text or author's bio mention
the location. Assignment of that tag and physical presence are separate facts.

Contemporary author/time control queries retrieved the same place metadata
without including the place filter. The tag was not derived from a city-name
substring by the collector.

### Avoid unverified operator substitutions

The tested `near:`, `within:`, and `geocode:` combinations mostly returned
empty pages. A `near:London` query returned posts discussing search syntax,
not proof of geographic selection. `place:"San Francisco"` also returned
no results, while the hexadecimal ID worked.

Do not promote historical help-page examples or HTTP 200 into proof that an
operator currently filters the private web search. Inspect returned place
fields and use a known-positive post when validating a filter.

## Measure a fixed window

Use explicit time boundaries and state the timezone. The SF study used seven
complete Mountain-time days, August 29 through September 4, 2026:

```text
since_time:1787983200 until_time:1788588000
```

The upper boundary is exclusive. Apply the same bounds to broad and keyword
queries. Count unique primary post IDs and keep replies, quotes, and other
post kinds distinguishable. Unwrap `TweetWithVisibilityResults.tweet` before
reading `legacy.place` and `legacy.created_at`; the inner object can omit
`__typename` while still being a valid post.

A broad Latest crawl returned 3,000 distinct posts across 150 pages, with all
149 cursor links matching the previous next cursor. A manual next-cursor
request returned 20 more older posts. The 3,000-item stop was the requested
budget, not a demonstrated upstream pagination limit.

The broad crawl included 2,200 posts inside the seven-day window. Independent
term/day queries added one more, yielding an observed lower bound of 2,201
posts from 589 authors. This is not total activity by SF residents.

## Triangulate IDs, not only counts

The study compared coffee, food, work, love, today, music, AI, startup, hiring,
Codex, Claude Code, and open source.

Every original week-long keyword result was in the broad crawl. That did
not prove completeness. The week-long `love` query returned nine August 29
posts; a one-day query returned 13. Three were already in the broad crawl
and one was new. Query-window size changed the retrieved set.

X keyword matching is not the same as a local word scan. The AI query and
local full-text scan both counted 46 posts, but their ID sets differed by
one post in each direction. Work and today counts differed as well.
Keep the matching method and query alongside each count. Treat keyword
matches as strings until topic meaning has been checked.

For a word map over an already retrieved corpus, deterministic local counts
avoid repeated searches for every term. Independent searches and smaller
time slices remain useful completeness checks and sources of missed IDs.

### City mentions are a separate population

Queries such as `AI ("San Francisco" OR "Bay Area")` match discussion about
the city. They do not establish the author's location.

In the same seven-day window, coffee city mentions returned 106 posts, with
only one shared ID with the SF-place corpus. The SF-place coffee query
returned six. An AI city-mention sample hit a 200-post budget while still
covering less than the last day of the window; none had SF place metadata.

Do not extrapolate total local activity from the ratio or overlap. These are
different selections, not independent random captures of one population.

## Historical city-filter false negatives

SF city-filter date probes retrieved posts from August 15, 2026. Queries
ending at August 14, 6:00 PM Mountain time or earlier returned no results in
this observation window. Do not make that a permanent retention rule.

Older posts with the same SF place ID still existed:

- US country searches retrieved December 2019 posts.
- Country plus city-text search retrieved posts carrying SF `place.id`.
- Public post `1212116034578190336` was retrieved with an author/time query
  and carried `place.id=5a110d312052166f`.
- Adding that exact place filter to the otherwise identical query returned
  no results.

Top versus Latest, `until:` versus `until_time:`, and added common/city words
did not recover the old city-filtered post. The city filter therefore had
observed historical false negatives. An empty old city query is not a
zero-volume measurement. Broader archive queries can recover examples, but
their different selection does not establish a complete city census.

## Empty-page behavior

Check new item IDs, not only cursor changes. The current xpool Query Job
runner continued through empty SearchTimeline pages until its page budget:
coffee emitted six posts and then 39 empty pages; Claude Code emitted zero
across 40 pages. This is tracked as `x-intelligence-c6g5` in Backchannel.

Use small initial budgets for sparse terms and inspect the last pages before
extending them. Stop a manual traversal when it yields no new items. Preserve
the empty response and request/returned cursors so future changes can be checked.

Evidence: private Backchannel `reports/sf-place-volume-2026-09-05.md`,
`reports/sf-place-volume-2026-09-05.json`, and
`reports/sf-place-volume-2026-09-05.csv`.
