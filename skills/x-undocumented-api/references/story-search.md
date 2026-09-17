# Story search and the separate News surface

## What is established

Fresh public client-web inspection on 2026-09-05 at about 20:40 UTC covered
six bootstrap scripts and 40 lazy chunks selected by Search, Explore, Trend,
LiveEvent, News, and Story names. Search, Explore, and LiveEvent hashes matched
the earlier September 4–5 snapshots. The coverage gap was omitted News chunks
and Relay metadata, not demonstrated age of those bundles.

No free-text story-search operation or caller was found in this selection.
This is a bounded negative result, not proof that a private endpoint does not
exist. Do not equate post search, a story-topic identifier, or filtering already
collected stories with searching X's full story catalogue.

## Relay operations missed by the older extractor

Some bundles describe persisted operations as:

```js
params: {id: "<query ID>", metadata: {}, name: "<operation name>",
         operationKind: "query", text: null}
```

An inventory matching only `queryId` / `operationName` misses them. The bundled
extractor now recognizes this Relay shape too: the same six bootstrap scripts
yielded 114 operations instead of 105. Three news operations above were also
checked against the downloaded lazy chunks. It still fetches only scripts
listed in source HTML. Fetch relevant lazy chunks separately.

| Operation | Query ID observed | Caller variables | Selected response |
| --- | --- | --- | --- |
| `useStoryTopicQuery` | `I3V_Tt32aTZdw7cBdKUJbg` | `rest_id`, `limit` | `story_topic.stories.items[].trend_results.result` |
| `useHomeNewsArticlesQuery` | `gTItUBXHQzDYz5zGcfHOSw` | `limit` | alias `deepsearchArticlesHomePageResult`, schema field `deepsearch_articles_home_page` |
| `useNewsArticleQuery` | `KVlJUSCh1B-KfOe1HxZ9kA` | `trendId` | alias `newsArticleResult`, schema field `ai_trend_by_rest_id`; result includes `deepsearch_news_articles`, sentiment, and post timelines |

## Live web-session results, September 5

All three operations were verified with 24 authenticated GET reads on one
existing xpool session at approximately 20:47–20:50 UTC. Every response was
HTTP 200 with no GraphQL errors; some valid envelopes contained empty lists.
No account settings were changed. Evidence:
`/Users/jaredsmith/Projects/backchannel/reports/relay-story-news-probes-2026-09-05.json`.

### Transport

Current main-bundle Relay transport maps `params.id/name/operationKind` to the
ordinary GraphQL dispatcher. Persisted queries use GET unless the caller sets
`forcePost`; these three callers did not. Their `metadata` is empty, so no
feature-switch or field-toggle parameters are sent. Request shape:

```text
GET /i/api/graphql/<params.id>/<params.name>?variables=<JSON>
```

Use the existing authenticated session, CSRF and transaction-ID transport.
The xpool `scripts/manual/trend-probe.ts` now allowlists all three operations,
extracts their empty-metadata Relay descriptors from `bundleUrl`, and omits
legacy feature/field-toggle parameters for those reads. A future descriptor
with non-empty metadata needs fresh inspection; do not silently discard it.

### Topic lists: useStoryTopicQuery

`loader.NewsSidebar` defaults to `rest_id: "Top Stories", limit: 3`.
The same reader supports substantially larger lists:

| Selector | Requested → returned |
| --- | --- |
| `Top Stories` | 3→3, 20→20, 100→100, 200→200, 500→250 |
| `AI` | 10→10, 100→100 |
| `Technology` | 10→10, 100→100 |
| `News`, `Sports` | 10→10 each |
| `ai`, `artificial intelligence`, `OpenAI`, `Tesla`, `UFC`, `Keita`, `Canada`, made-up topic | empty |

This supports exact named-topic lookup, not arbitrary keyword search. In
particular `AI` works while `ai` does not. The existence of a returned
`story_topic.id` is not proof that its list has content. 250 is an observed
ceiling for Top Stories in this window, not a proven universal limit.
No cursor is exposed in this operation's inspected selection.

Across all tested topic lists there were 396 distinct story IDs. Only six
of the AI-100 IDs and 12 of the Technology-100 IDs overlapped Top Stories-250,
so these topic lists add breadth beyond the main ranking. They remain
account-selected lists, not verified country rankings. Topic/category fit is
imperfect; do not treat membership as a precise subject classifier.

Items include `rest_id`, `core.name`, `core.hook`, `core.category`,
`core.created_at_ms`, `social_proof`, and **unrounded string `post_count`**.
Keep this separate from rounded Explore display labels. Its counting scope
and time window remain unknown; it is not a geographic or hourly measure.

### Finding the topic catalogue

No complete catalogue was found in the inspected website chunks or official
help pages as of September 5. A fresh scan of `bundle.Topics`, `bundle.Routes`,
and the topic-follow prompt did not establish a story-topic enumeration read.
The separate followable Topics system is not a verified source of selector
names for `useStoryTopicQuery`.

The sidebar reads feature setting `responsive_web_trends_ui_sidebar_topic_id`;
public bootstrap configurations contained `Top Stories` and `For You`. Its
News/Sports/Entertainment/Other/Personalized translation map labels returned
categories; it does not establish that each label is a populated selector.

Twelve additional limit-1 requests at 20:56 UTC returned stories for `For You`,
`Science`, `Politics`, and `Gaming`. `Entertainment`, `Other`, `Personalized`,
`Business`, `Finance`, `World`, `Crypto`, and `Health` returned empty lists.
All were HTTP 200 without GraphQL errors. Empty means no observed yield, not
proven unsupported. The confirmed nonempty names across both studies are:
`Top Stories`, `For You`, `News`, `Sports`, `AI`, `Technology`, `Science`,
`Politics`, and `Gaming`. This is a working list, not an exhaustive catalogue.
Evidence: Backchannel `reports/story-topic-candidates-2026-09-05.json`.

### Home news and article lookup

`useHomeNewsArticlesQuery({limit})` returned 3→3, 20→20, 100→25 articles.
Home entries supply title, summary, update time, post references, and section
skeletons. Some `TextBlock` objects contain only `__typename`, and source
objects can be `{}` because the home query does not select the full fields.
Do not interpret that as a missing upstream article or missing source URLs.

`useNewsArticleQuery({trendId})` adds the full section text and source details.
Two successful examples:

- Keita story `2096326513272525081`: 269 article words across nine text
  sections, seven embedded post references, two external source links, and
  Top/Latest feed IDs.
- Lagway story `2096330161712951564`: 356 article words across 11 text
  sections, five embedded post references, two sources, and both feed IDs.

The article response includes a short summary plus the longer section body.
Post references are IDs, not hydrated post objects. Source fields include
`url`, `site_name`, `media_name`, and `time_accessed`. Story text is generated
by X and is not independently verified reporting.

`total_trend_posts` was `"7"` and `"5"` in those two articles, matching their
embedded-post counts; this is not the topic reader's much larger `post_count`.
Do not conflate those fields. General semantics beyond these samples remain
unverified. `key_points` was empty and sentiment was absent in these examples.

### Larger snapshot and embedded-post hydration (2026-09-05)

A limit-500 sweep returned: `Top Stories` 250, `For You` 25, `News` 250,
`Sports` 230, `AI` 221, `Technology` 250, `Science` 37, `Politics` 250,
`Gaming` 250. These are observed snapshot sizes, not documented fixed caps.
Combining this sweep with earlier session discoveries yielded 1,531 distinct
story IDs. Topic lists overlap, change over time, and can be personalized;
this collection does not establish an exhaustive global inventory. The full
article reader subsequently returned nonempty text for all 1,531 IDs. Their
6,262 distinct embedded-post references yielded 6,230 retrievable posts and
32 unavailable/empty/subscriber-preview results; articles cited 2,437 unique
external URLs. These are snapshot measurements, not endpoint guarantees.

Hydrate article post references with `TweetResultsByRestIds`, discovered in
the current main bundle as query ID `Pho4sg8jLcrVlMeclMayrg`. Tested variables:

```json
{"tweetIds":["2095972669313429832"],"includePromotedContent":false,"withBirdwatchNotes":false,"withVoice":true,"withCommunity":true}
```

Use the current operation's feature metadata and authenticated transaction ID.
A 100-ID batch returned 100 result slots at `data.tweetResult[]`; this is a
working batch size, not a proven maximum. Slots can contain `result` with
`Tweet`, `TweetWithVisibilityResults`, `TweetUnavailable`, or
`TweetPreviewDisplay`, or no result. `TweetWithVisibilityResults.tweet` can
omit `__typename` even though it contains `rest_id`, `core`, and `legacy`.
Unwrap it before extracting post text; do not drop it just because the nested
object lacks the `Tweet` type marker. Preserve unavailable IDs as explicit
placeholders. Author name/handle and avatar may live in `core` and `avatar`
on the user object rather than its legacy fields.

Observed response quotas: article/topic Relay operations 50 requests per
15 minutes; `TweetResultsByRestIds` 500 per 15 minutes. Treat headers as
session-specific observations and honor current limits. Pool reservation or
bootstrap failure is not evidence that a story has no article.

## Official API: separate evidence

X documents `GET https://api.x.com/2/news/search` with required `query`,
`max_results` 1–100 (default 10), and `max_age_hours` 1–720 (default 168).
Fields include name, summary, keywords, contexts, and associated post IDs.
No country-ranking selector is documented there. Searching `Canada` is not
proof of popularity among Canadian users. Access through Backchannel's
credentials has not been tested; official API documentation does not establish
an equivalent web-session endpoint.

Source: https://docs.x.com/x-api/news/search-news (checked 2026-09-05).

## Current public bundle sources

- Story topics: https://abs.twimg.com/responsive-web/client-web/loader.NewsSidebar.61161271c2526cd3a.js
- Home news: https://abs.twimg.com/responsive-web/client-web/ondemand.News.4a7c4b65965cdaeea.js
- Article lookup: https://abs.twimg.com/responsive-web/client-web/shared~bundle.News~ondemand.News.012fb99ec27f6b2ea.js
- Search: https://abs.twimg.com/responsive-web/client-web/bundle.Search.965098fbbbfb864fa.js
- Story pages: https://abs.twimg.com/responsive-web/client-web/bundle.LiveEvent.ae3cbdc299ddff14a.js

Refresh filenames and IDs from the current webpack resolver before reuse.
Local inspection artifacts: `/tmp/backchannel-story-search-fresh/` (temporary).
