# Trends and Explore

Use this reference to collect trending terms, inspect personalized Explore
recommendations, expand topic coverage, or investigate location controls.

The measured results below come from 62 authenticated GET probes on three
authorized xpool accounts on September 4, 2026, Mountain time. They cover
one short observation window. Counts are observations, not permanent caps.
No account settings, follows, interests, or public posts were changed.

September 5 follow-up: [Geography](geography.md) verifies direct location
selection through `trends/place.json?id=<WOEID>`. The unsuccessful location
overrides below apply to `guide`, not to every geography reader.

## Choose the read by the question

- Broad trending-term collection: REST `guide` with `candidate_source=trends`.
- Current Explore tabs and AI stories: `ExplorePage`, then returned tab IDs
  through `GenericTimelineById`.
- Sidebar selection: `ExploreSidebar`.
- Updates to a known AI story: `TrendHistory`.
- Relevant people for a known AI story: `TrendRelevantUsers`.
- Available geographic selectors: `trends/available` or the newer Explore
  location autocomplete. These return locations, not trending terms.
- Trends for a specific location: `trends/place` with a WOEID. See
  [Geography](geography.md) for the measured regional comparisons.

Do not treat X's ranked selection as a complete trend catalogue. Displayed
post counts are not a defined posts-per-hour rate or an activity multiplier.

## Broad collection through REST guide

```text
GET https://x.com/i/api/2/guide.json
```

Measured request parameters:

```json
{
  "candidate_source": "trends",
  "count": 200,
  "entity_tokens": false
}
```

Use the authorized account's session and sticky proxy, the current web bearer
token, CSRF cookie, and a transaction ID generated for
`GET /i/api/2/guide.json`. Shared transport/auth rules remain in
[runtime-and-auth.md](runtime-and-auth.md).

Read parent trends from:

```text
timeline.instructions[].addEntries.entries[].content.timelineModule.items[].item.content.trend
```

The result also has `globalObjects` and may have `pageConfiguration`. Count
the selected timeline once. Do not recursively count repeated copies of
initial content inside page configuration.

Useful trend fields:

- `name` and `url`: display name and search destination.
- `trendMetadata.domainContext`: category or context label.
- `trendMetadata.metaDescription`: optional displayed count/context text.
- `groupedTrends`: related names and search destinations.

Keep parent trends and their aliases distinct. In three near-contemporaneous
large responses, the accounts returned 120, 120, and 119 parent trends. Their
union had 122 parents. Including aliases produced 144 unique terms. Each
response had 23 aliases that were additional to its own parent names.

### Count and cursor boundaries

Observed on one account:

- `count=1`, `20`, and `50`: 1, 20, and 50 parent trends.
- `count=100`: 64, then 65 parent trends.
- `count=200` and `1000`: 122 each in one comparison.
- `count=10000`: 120 in a later snapshot.
- A later `count=200` snapshot: 115.

Count behavior is not linear. A large count can expose more of the current
selection, but it does not promise that many results. The observed ceiling
is not a server-wide constant.

The guide returned `DefaultTopCursorValue` and `DefaultBottomCursorValue`.
Submitting the bottom value returned HTTP 200 with no trends. Do not loop
over these sentinels. Repeat snapshots at a useful interval and retain
observation times instead of assuming deep pagination.

Omitting `candidate_source=trends` selected different content. One large
default guide request returned 14 trends. An `initial_tab_id=news_unified`
request returned no trend items. Legacy and GraphQL tabs need separate parsing.

## GraphQL Explore

These IDs were verified in the current bundle during the probe window.
Regenerate them before reuse:

- `ExplorePage`: `jo4rJIWiO5pQlMk6FYphZQ`.
- `GenericTimelineById`: `ee4dBLWL8a8qg6n19m1htQ`.
- `ExploreSidebar`: `qjhLfJKwuRiKMQ6zBgkfYQ`.
- `TrendHistory`: `ww7Oqt_UpuAcJ0e2xuqpOw`.
- `TrendRelevantUsers`: `hYe9H8LpXQV2fa1r-YQU0g`.

Each operation advertises 38 feature switches and eight field toggles.
Extract the names from its metadata and boolean values from the active
client's feature configuration. These probes supplied 37 feature values and
`fieldToggles={}`. The advertised `rweb_conversational_replies_downvote_enabled`
had no boolean value in the captured configuration and was omitted; the reads
still succeeded. Record supplied values separately from advertised names.

### ExplorePage and tab timelines

Initial variables `{"cursor":""}` succeeded. The response is
`data.explore_page`. The formatter handles either `body.__typename=Timeline`
or `SegmentedTimelines`.

For segmented pages:

```text
Initial content: data.explore_page.body.initialTimeline.timeline.timeline
Tab labels:     data.explore_page.body.timelines[].labelText
Tab IDs:        data.explore_page.body.timelines[].timeline.id
```

The sampled page advertised `for_you`, `trending`, `news`, `sports`, and
`entertainment`. Copy the returned opaque timeline ID for each tab.

`GenericTimelineById` variables:

```json
{
  "timelineId": "<returned timeline ID>",
  "count": 100,
  "withQuickPromoteEligibilityTweetFields": true
}
```

Add `cursor` only when following a returned cursor. Read
`data.timeline.timeline.instructions` and normalize entry types before counting.
The initial Explore page and tab responses mix trends with events, frames,
users, and other content.

Observed first pages:

- For You: nine trend items, including three AI stories.
- Trending: 31 trend items, including one promoted item.
- News, Sports, Entertainment: five trend items each.
- Sidebar: four trend items, including one promoted item.

The Trending tab still returned 31 items with counts 1 and 500. All five tab
second pages returned only cursors and no content. The bottom cursor changed
on these empty pages. Cursor change is not progress.

The normal `ExploreSidebar` caller has no count or cursor inputs. Supplying
extra `count=500` and a cursor still returned the same four-item shape.

### Context and invented tabs

`ExplorePage`'s wrapper accepts `context` and `cursor`. It drops the legacy
REST options built by the shared Explore module. In particular,
`candidate_source`, `display_location`, `initial_tab_id`, `profile_user_id`,
and `focal_tweet_id` are not proven GraphQL inputs.

`context:"FETCH_EXPLORE_GQL"` in client source is local request metadata,
not the upstream context value. The standard UI supplies no context value.
Probe results:

- Object context `{"candidate_source":"trends"}`: HTTP 422,
  `GRAPHQL_VALIDATION_FAILED`, error path `variable.context`.
- String `"trending"` and a JSON-encoded string containing that object:
  HTTP 200, with the ordinary segmented page. No selection effect established.

The returned timeline IDs have an encoded category. Substituting `ai` or
`technology` produced HTTP 200 with GraphQL code 214 and
`BadRequest: invalid trending category`. Use advertised IDs. Do not equate
transport success with a valid category or useful content.

## AI story enrichment

AI trend links can use `twitter://trending/<id>`, not only
`https://x.com/i/trending/<id>`. Preserve the ID while normalizing the link.

Both enrichment operations accept `{"trendId":"<observed AI trend ID>"}`.

`TrendHistory` reads:

```text
data.ai_trend_by_rest_id.result.trend_history.timeline
```

The current UI calls this **Story History**. Both tested stories returned one
`TimelineMessagePrompt`, containing `TimelineCompactPrompt` content with
`headerText` and timestamped `bodyText`. This is a story summary/history
surface. It is not a numerical time series.

`TrendRelevantUsers` reads:

```text
data.ai_trend_by_rest_id.result.trend_relevant_users.timeline
```

Both tested IDs returned three `TimelineUser` entries with public user
objects. Neither tested enrichment response had pagination cursors.

## Location and personalization

X documents personalized For You recommendations and geographic Trending
lists. Account interests, follows, engagement, and location can affect the
personalized selection. Similar results across three pool accounts do not
disprove personalization or establish diversity across interest groups.

GET `/i/api/2/guide/get_explore_settings.json` needs no explicit parameters.
The three accounts reported:

```json
{
  "use_personalized_trends": true,
  "use_current_location": true,
  "use_fun_mode_stories": false,
  "is_stories_available": false,
  "places": [],
  "is_unified_trends": true
}
```

GET `/i/api/1.1/trends/available.json` returned 467 WOEID locations.

GET `/i/api/2/guide/explore_locations_with_auto_complete.json` takes `prefix`.
It returned 201 countries for `prefix=""`, 44 matches for `London`, 15 for
`Canada`, eight for `United Kingdom`, and one for `United States`.
Results contain `place_id`, `name`, and `location_type`.

The newer `place_id` is a signed decimal string, not a WOEID. Keep it as a
string: values can exceed JavaScript's safe integer range.

Adding `woeid`, `place_id`, or `use_personalized_trends=false` to individual
guide GET requests did not establish an override. US and UK `place_id`
responses contained the same 117-name set; the Canada response shared 116.
Minor order/term changes also occur in ordinary repeat snapshots.

The UI changes location with POST
`/i/api/2/guide/set_explore_settings.json`, serializing selected places as a
list of `place_id` strings. That is an account mutation. Do not perform it
as a read-only geography probe. The original account's settings were checked
again and remained unchanged.

## Reads that remain unresolved

- `GET /i/api/2/guide/topic.json` is still present in the bundle. A request
  without parameters returned HTTP 400, code 214, `Bad request.` No current
  invocation or valid selector was found. Do not advertise guessed `topic_id`
  parameters as supported.
- `TopicToFollowSidebar` is a separate persistent-topic recommendation read.
  Current ID `Tya4DNkHLANh4o7T7VLKZA`, variables `{"userId":"<public user ID>"}`,
  path `data.user.result.timeline.timeline`. One public-profile probe returned
  an empty timeline. This does not establish useful yield or personalization.
- `TopicByRestId` is bundle-verified only: ID `4OUZZOonV2h60I0wdlQb_w`, variables
  `{"topicId":"<observed topic ID>"}`, result `data.topic`, no feature switches
  or field toggles. No valid topic ID was available for a live probe.
- The documented developer API is separate. Its 50-trends-per-WOEID limit
  does not apply to the measured private guide endpoint.

## Reproduce with xpool

In the xpool repository, the manual command is:

```sh
bun scripts/manual/trend-probe.ts /tmp/x-trend-requests.json /tmp/x-trend-probe
```

Example request file:

```json
[
  {
    "name": "broad-trends",
    "operation": "Guide",
    "variables": {
      "candidate_source": "trends",
      "count": 200,
      "entity_tokens": false
    }
  },
  {
    "name": "explore",
    "operation": "ExplorePage",
    "variables": {"cursor": ""}
  }
]
```

The command reuses xpool's account/session/proxy code, reads current bundle
metadata and client features, and permits only an explicit GET-operation list.
It does not start services or initialize schemas. The first account stays
pinned unless a request supplies `accountId` or `newAccount`. A verified
public `bundleUrl` can supply metadata for an operation in a lazy chunk.

Use a fresh output directory. Raw response files use mode 600 and cannot overwrite
an existing response file.
Inspect selected paths and counts; do not print full raw responses. Summaries
record request variables, feature values, status, errors, and rate headers.
Keep negative responses and empty pages as evidence, not reasons to invent
new defaults or rotate accounts indefinitely.

## Sources and evidence

- Current X bundles and authenticated probes, `2026-09-05T05:26:37.894Z`
  through `2026-09-05T05:41:42.150Z`.
- Private Backchannel evidence: `reports/x-trend-live-probes-2026-09-04.json`
  and `reports/x-trend-live-probes-2026-09-04.md`.
- [X Trends Recommendations](https://help.x.com/en/resources/recommender-systems/trends-recommendations).
- [X Explore Recommendations](https://help.x.com/en/resources/recommender-systems/explore-recommendations).
- [X Trends FAQ](https://help.x.com/en/using-x/x-trending-faqs).
