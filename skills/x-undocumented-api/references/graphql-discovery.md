# GraphQL Discovery

Use this reference to find current X web GraphQL operations, query IDs, feature flags, field toggles, variables, and response paths.

## Extraction Pattern

Fetch `https://x.com/explore`, find client-web script URLs, then scan each script for operation metadata:

```regex
queryId:"([^"]+)",operationName:"([^"]+)",operationType:"([^"]+)"
operationName:"([^"]+)",operationType:"([^"]+)",queryId:"([^"]+)"
```

Also recognize Relay persisted-operation metadata:

```regex
params:\{id:"([^"]+)",metadata:\{[^{}]*\},name:"([^"]+)",operationKind:"([^"]+)"
```

The extractor supports both formats. News/topic queries found in September 5
lazy chunks used Relay metadata; an `operationName`-only scan missed them.
See [story-search.md](story-search.md) for the bounded findings and callers.

Use the bundled script:

```bash
bun /Users/jaredsmith/Projects/agent-skills/skills/x-undocumented-api/scripts/extract-x-graphql-endpoints.ts --out-dir /tmp/x-graphql
```

The default source is `https://x.com/explore`; `--source-page <url>` overrides it. On 2026-09-04 Mountain time, a logged-out request redirected to `https://x.com/i/flow/login?redirect_after_login=%2Fexplore`. That page exposed six client-web scripts with 105 operations, including `ExplorePage`, `ExploreSidebar`, `GenericTimelineById`, `TrendHistory`, and `TrendRelevantUsers`.

The logged-out `https://x.com/` homepage instead loaded `https://abs.twimg.com/x-web/x-web/entry-client-logged-out-DJ1gyf49.js`. It exposed no client-web script URLs, so the old default failed with `No X client-web script URLs found in https://x.com`. A failed homepage harvest is not evidence that an operation was removed.

The script writes:

- `x-graphql-endpoints-<date>.json`
- `x-graphql-endpoints-<date>.csv`
- `x-graphql-community-endpoints-<date>.md`

### Structural limits of bundle extraction

The script scans only client-web script URLs present in the source HTML. Its output is a partial bootstrap inventory, not a complete API inventory.

1. **Lazy chunks.** Additional operations and caller code can be in on-demand chunks. The public login HTML can expose webpack's chunk-name and hash maps. Inspect its filename resolver, select chunks related to the requested feature, and fetch those exact URLs. This can work without account cookies. If the available map omits the required chunk, visit the feature in an authenticated browser and inspect scripts listed by `performance.getEntriesByType('resource')`. Access to a bundle does not establish access to its data endpoints.
2. **WebSocket operations.** Some actions are not GraphQL. X Chat sends are WebSocket frames to `wss://chat-ws.x.com/ws?token=<JWT>`. There is no send `operationName` or `queryId` to extract. Capture those operations with CDP WebSocket frame handlers.

Use the exact filename expression from the current runtime. On 2026-09-04 Mountain time, the resolver appended the literal `a.js` after the hash. `https://abs.twimg.com/responsive-web/client-web/bundle.Explore.2a293193d547b00fa.js` returned HTTP 200; `https://abs.twimg.com/responsive-web/client-web/bundle.Explore.2a293193d547b00f.js` returned HTTP 404. Do not assume `.js`, or make `a.js` a universal suffix.

In that scan, 14 public lazy chunks whose names contained `Explore`, `Trend`, or `GenericTimeline` added 40 operations to the bootstrap inventory, for 145 unique operations. This was a selected subset, not an exhaustive scan. Refresh query IDs from current bundles before use.

## What Metadata Gives You

Operation metadata usually gives:

- `operationName`
- `queryId`
- `operationType`
- feature switch names
- field toggle names

It usually does not fully explain variables or response semantics. For those, search nearby bundle code for:

- the operation name
- semantic caller names, such as `fetchCommunityTweets`
- variable names, such as `communityId`, `listId`, `rawQuery`, `rankingMode`, `displayLocation`
- response fragments and paths, such as `tweets_timeline`, `ranked_community_timeline`, `search_timeline`

## Feature Flags

Common web GraphQL feature flags include:

- `responsive_web_graphql_exclude_directive_enabled`
- `verified_phone_label_enabled`
- `responsive_web_graphql_skip_user_profile_image_extensions_enabled`
- `responsive_web_graphql_timeline_navigation_enabled`
- `tweetypie_unmention_optimization_enabled`
- `responsive_web_edit_tweet_api_enabled`
- `graphql_is_translatable_rweb_tweet_is_translatable_enabled`
- `view_counts_everywhere_api_enabled`
- `longform_notetweets_consumption_enabled`
- `freedom_of_speech_not_reach_fetch_enabled`
- `standardized_nudges_misinfo`
- `tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled`
- `responsive_web_enhance_cards_enabled`

Timeline, media, community, and list operations often need broader modern web flags, including:

- `rweb_video_screen_enabled`
- `rweb_cashtags_enabled`
- `profile_label_improvements_pcf_label_in_post_enabled`
- `responsive_web_profile_redirect_enabled`
- `rweb_tipjar_consumption_enabled`
- `creator_subscriptions_tweet_preview_api_enabled`
- `premium_content_api_read_enabled`
- `communities_web_enable_tweet_community_results_fetch`
- `c9s_tweet_anatomy_moderator_badge_enabled`

Do not guess flags after a 400 or empty response. Extract them from the current operation metadata.

## Field Toggles

Common field toggles seen in current metadata:

- `withPayments`
- `withAuxiliaryUserLabels`
- `withArticleRichContentState`
- `withArticlePlainText`
- `withArticleSummaryText`
- `withArticleVoiceOver`
- `withGrokAnalyze`
- `withDisallowedReplyControls`

If a metadata block advertises field toggles, include them unless a fresh browser trace shows otherwise.

## 2026-06-18 Inventory Snapshot

A scan of current X client-web scripts found 157 operations from 6 scripts:

| Category | Count |
| --- | ---: |
| bookmark | 2 |
| community | 37 |
| direct-message | 3 |
| list | 20 |
| other | 37 |
| search | 4 |
| tweet | 26 |
| user | 28 |

High-value operation families from that scan:

- search: `SearchTimeline`, `BookmarkSearchTimeline`, `ListSearchTimeline`
- list: `ListLatestTweetsTimeline`, list metadata, list membership, list subscribe/update operations
- tweet: tweet detail, result-by-ID, create/delete/retweet/favorite/bookmark operations
- user: identity, profile, followers/following, verification, follow relationship operations

For current work, regenerate instead of trusting an old snapshot.

## Selected Query IDs From 2026-06-18

These are examples from one bundle scan and can drift:

| Operation | Type | Query ID |
| --- | --- | --- |
| `SearchTimeline` | query | `yIphfmxUO-hddQHKIOk9tA` |
| `ListLatestTweetsTimeline` | query | `27HKUy8ulrflZ9Tole038g` |
| `UserTweets` | query | `RyDU3I9VJtPF-Pnl6vrRlw` |
| `UserTweetsAndReplies` | query | `plVqzvVGaDxbFEPoOe_i-A` |
| `Followers` | query | `9jsVJ9l2uXUIKslHvJqIhw` |
| `Following` | query | `OLm4oHZBfqWx8jbcEhWoFw` |
| `UserByRestId` | query | `IBScZCvFJadZC25ubLYNRQ` |
| `UserByScreenName` | query | `681MIj51w00Aj6dY0GXnHw` |
| `TweetDetail` | query | `meGUdoK_ryVZ0daBK-HJ2g` |
| `TweetResultByRestId` | query | `8CEYnZhCp0dx9DFyyEBlbQ` |
| `TweetResultsByRestIds` | query | `Sc9EUQTZNEH-wzegn-nHvQ` |

One additional 2026-06-18 finding: the extracted current client-web bundle did not surface `itemFilter`, `authored_posts`, or `authored_replies` strings near the user-timeline operation inventory. Treat any runtime-side `itemFilter` as unproven until you confirm it in current bundle caller code.

## Discovery Checklist

1. Extract a fresh operation inventory.
2. Confirm `operationName`, `queryId`, and `operationType`.
3. Search bundle source for caller functions and variable names.
4. Copy feature switches and field toggles from metadata.
5. Identify the response path to timeline instructions or object result.
6. Probe read-only calls with secret-safe output.
7. Save exact date, query ID, variables, features, field toggles, status, response path, counts, and caveats.

## Common Mistakes

- Using official API v2 docs as proof of web GraphQL behavior.
- Assuming `SearchTimeline` operators match official X API search operators.
- Reusing stale query IDs from old snapshots.
- Sending a transaction ID for `/OperationName` instead of `/i/api/graphql/<queryId>/<OperationName>`.
- Treating HTTP 200 as success without checking GraphQL `errors`, response path, and item count.
- Treating one account or guest-token result as global endpoint behavior.
- Assuming every write has a GraphQL `operationName`. X Chat (DM) sends are WebSocket frames, not mutations — no send query id exists to extract (see Structural limits above).
