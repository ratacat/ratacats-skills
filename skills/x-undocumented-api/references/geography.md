# Geography readers

Use this reference to request trends for a city or country, resolve a
coordinate to a trend location, or compare geographic coverage.

For keyword searches or volume measurements over posts, use
[Geographic post search](geographic-post-search.md). That interface uses a
third location identifier: the hexadecimal place ID attached to a post.

September 5, 2026: 49 authenticated GET probes across three authorized
accounts. Sixteen selected location snapshots yielded 321 distinct display
names, or 320 terms after Unicode NFKC normalization, trimming, and case folding.
No account settings changed. The earlier failed `guide` overrides do not
apply to the separate working `trends/place` endpoint.

## Request trends by location

```text
GET https://x.com/i/api/1.1/trends/place.json?id=2487956
```

`id` is a WOEID, Yahoo's Where On Earth ID. San Francisco is `2487956`.
Other verified examples: New York `2459115`, London `44418`, Tokyo `1118370`,
São Paulo `455827`, Paris `615702`, Sydney `1105779`, worldwide `1`.
Get supported IDs from `trends/available`; do not substitute the newer
Explore `place_id` values.

Use the existing authorized web-session headers, cookies, sticky proxy, and
a transaction ID generated for `GET /i/api/1.1/trends/place.json`.
The xpool web bearer worked. These probes did not require developer API
OAuth credentials or a saved Explore-location change.

Response shape:

```text
[0].locations[]: name, woeid
[0].trends[]: name, query, url, promoted_content, tweet_volume
[0].as_of
[0].created_at
```

Verify that `locations[].woeid` matches the requested ID. Also compare names
with other locations and with same-location repeat controls. A matching
location label alone does not establish a distinct topic set.

The selected snapshots returned 45–50 rows. Most returned 50. A `count=200`
probe still returned 50. The source caller exposes `id` and optional
`exclude`, not a pagination cursor. No deeper page was demonstrated.

`exclude=hashtags` removed five hashtag rows from the SF response and
returned 45 rows. It did not replace them to reach 50.

`id=0` returned HTTP 404 with JSON code 34, `Sorry, that page does not exist.`
This is a content/identifier error, not an empty transaction-ID failure.

September 5 follow-up (20:29–20:33 UTC): US, Japan, Australia, and Canada
returned 50 rows each; Australia had 49 distinct terms because
`#aflcrowsdogs` appeared twice. China was absent from the fetched
`TrendLocations` catalogue; `PlaceTrends` with China WOEID `23424781` returned
code 34. Do not substitute another region or claim that this means no Chinese
conversation exists. These are observations of this endpoint's coverage.

## Resolve coordinates

```text
GET https://x.com/i/api/1.1/trends/closest.json?lat=37.7749&long=-122.4194
```

The parameter is `long`, not `lon`. The response is an array of location
objects containing `name`, `woeid`, `country`, `countryCode`, `parentid`,
and `placeType`.

Measured coordinates resolved as follows:

- SF → San Francisco, `2487956`.
- Oakland → San Francisco, `2487956`; Oakland is absent from the catalogue.
- San Jose → San Jose, `2488042`.
- New York → New York, `2459115`.
- London → London, `44418`.
- Tokyo → Tokyo, `1118370`.
- `lat=0&long=0` → worldwide, `1`.
- `lat=91&long=0` → HTTP 400, code 3, `Invalid coordinates.`

The result selects a supported trend location. It does not define a post
search radius or prove municipality-level coverage. Check for worldwide
fallback instead of assuming every coordinate produces local trends.

## Keep the two location catalogues separate

`GET /i/api/1.1/trends/available.json` returned the same ordered 467-location
catalogue when supplied SF or Tokyo coordinates. Use `closest` for coordinate
resolution; those parameters did not reorder `available` in the probes.

`GET /i/api/2/guide/explore_locations_with_auto_complete.json` takes `prefix`
and returns newer `place_id`, `name`, and `location_type` objects.

Observed name ambiguity and matching limits:

- `San Francisco` included SF city, South SF, and the
  `SAN FRANCISCO-OAK-SAN JOSE` metro label, plus foreign namesakes.
- `New York` returned three different entries, with both Region and City types.
- `Paris` included regional, city, and foreign namesake entries.
- `California` included Baja California and California City.
- `Tokyo` returned 52 matches; `東京` returned none in the English-client probe.
- `Sao Paulo` returned one match; `São Paulo` returned none.

An empty localized/accented lookup does not establish that a location is
unsupported. Try the catalogue's spelling and inspect name, type, and ID.
Do not select the first substring match automatically.

Keep `place_id` as a string. It can be negative and can exceed JavaScript's
safe integer range. It is not interchangeable with a WOEID. A City label
can describe a metro area; do not infer precise boundaries from the type.

## Compare content before expanding coverage

Selected first-snapshot overlaps, using exact distinct display names:

- SF / New York: 45 shared names out of 50 in each.
- SF / US: 44 shared, six unique to each.
- New York / US: 47 shared, three unique to each.
- London / UK: 48 shared out of 49 distinct names in each.
- Paris / France: the same 50-name set, with different order.
- Sydney / Australia: 49 shared out of 50 in each.
- São Paulo / Brazil: 44 shared; three additional city names, one country name.
- Tokyo / Japan: 28 shared; 21 additional city names, 22 country names.
- Los Angeles / San Jose: the same 50-name set, with different order.

The London/UK difference was only `#TOTP` versus `#totp`; their case-folded
sets match. SF/San Jose differed by three names each, but a same-account SF
repeat also changed three names. That difference alone does not prove added
geographic topics.

Nearby cities do not necessarily supply independent topics. Country selection
often adds more breadth than adding a similar city, but Tokyo/Japan shows
that city diversity can matter. Measure incremental unique names in the
intended regions and time window instead of extrapolating from one pair.

SF account A → B → A retained the same 50-name set. Tokyo B matched the later
A set, while earlier A differed by two names. Those controls did not establish
an account-specific effect beyond ordinary time variation. They do not prove
that every account receives identical results.

## Counts, duplicates, and timestamps

- Every `tweet_volume` was null in the place-trend probes. Do not convert
  rank, row count, or display text into a measured post volume.
- London and UK each contained two identical `Reform` rows, including the
  same query and URL. Count distinct names separately from response rows.
- `as_of` advanced near request time. `created_at` ranged from August 29 to
  September 4 and remained unchanged when the same-location content changed.
  Neither field alone establishes content freshness. Keep local observation
  time and compare actual item sets over time.
- These location trends were broad conversation lists, not filters for an
  industry or occupation. SF was strongly similar to national US trends.

## Reproduce with xpool

The read-only manual command supports `PlaceTrends`, `ClosestTrendLocations`,
`TrendLocations`, and `ExploreLocations`:

```json
[
  {"name":"sf","operation":"PlaceTrends","variables":{"id":2487956}},
  {"name":"london","operation":"PlaceTrends","variables":{"id":44418}},
  {"name":"tokyo","operation":"PlaceTrends","variables":{"id":1118370}}
]
```

```sh
bun scripts/manual/trend-probe.ts /tmp/geography-requests.json /tmp/geography-probe
```

Use a fresh output directory. The first account stays pinned unless a request
selects another account. Record whether selection came from requested WOEIDs
or existing settings. Account-settings POSTs remain outside read-only exploration.

Evidence: private Backchannel `reports/x-geography-probes-2026-09-05.json`
and `reports/x-geography-probes-2026-09-05.md`, captured from
`2026-09-05T06:12:02.682Z` through `2026-09-05T06:18:57.675Z`.
The legacy GET names and parameters were located in
[Tweepy's v4.14.0 source](https://raw.githubusercontent.com/tweepy/tweepy/v4.14.0/tweepy/api.py)
and then verified against X. Library documentation alone was not treated as
proof of current endpoint behavior.
