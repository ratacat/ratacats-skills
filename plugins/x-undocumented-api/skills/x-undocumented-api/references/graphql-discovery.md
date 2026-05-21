# GraphQL Discovery

Use this reference to find current X web GraphQL operations, query IDs, feature flags, field toggles, variables, and response paths.

## Extraction Pattern

Fetch `https://x.com`, find client-web script URLs, then scan each script for operation metadata:

```regex
queryId:"([^"]+)",operationName:"([^"]+)",operationType:"([^"]+)"
operationName:"([^"]+)",operationType:"([^"]+)",queryId:"([^"]+)"
```

Use the bundled script:

```bash
bun /Users/jaredsmith/Projects/agent-skills/skills/x-undocumented-api/scripts/extract-x-graphql-endpoints.ts --out-dir /tmp/x-graphql
```

The script writes:

- `x-graphql-endpoints-<date>.json`
- `x-graphql-endpoints-<date>.csv`
- `x-graphql-community-endpoints-<date>.md`

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

## 2026-05-18 Inventory Snapshot

A scan of current X client-web scripts found 158 operations from 6 scripts:

| Category | Count |
| --- | ---: |
| bookmark | 2 |
| commerce | 1 |
| community | 37 |
| direct-message | 3 |
| list | 20 |
| other | 37 |
| search | 4 |
| tweet | 26 |
| user | 28 |

High-value operation families from that scan:

- community: `CommunityTweetsTimeline`, `CommunityTweetsLoggedOutTimeline`, `CommunityTweetsRankedLoggedOutTimeline`, `CommunityMediaTimeline`, `CommunityByRestId`
- list: `ListLatestTweetsTimeline`, list metadata, list membership, list subscribe/update operations
- search: `SearchTimeline`, `BookmarkSearchTimeline`, `ListSearchTimeline`, global communities post search timelines
- tweet: tweet detail, result-by-ID, create/delete/retweet/favorite/bookmark operations
- user: identity, profile, followers/following, verification, follow relationship operations

For current work, regenerate instead of trusting an old snapshot.

## Selected Query IDs From 2026-05-18

These are examples from one bundle scan and can drift:

| Operation | Type | Query ID |
| --- | --- | --- |
| `SearchTimeline` | query | `Yw6L66Pw54NHKuq4Dp7b4Q` |
| `ListSearchTimeline` | query | `YTkV8GjFNGfgnhRNP6kDbQ` |
| `ListLatestTweetsTimeline` | query | `7UuJsFvnWuZo0HmxrzU42Q` |
| `ListRankedTweetsTimeline` | query | `k6XNxM7f9JrrqcITWhkv0Q` |
| `UserTweets` | query | `36rb3Xj3iJ64Q-9wKDjCcQ` |
| `UserTweetsAndReplies` | query | `D5eKzDa5ZoJuC1TCeAXbWA` |
| `UserMedia` | query | `9EovraBTXJYGSEQXZqlLmQ` |
| `Followers` | query | `_orfRBQae57vylFPH0Huhg` |
| `Following` | query | `F42cDX8PDFxkbjjq6JrM2w` |
| `UserByRestId` | query | `VQfQ9wwYdk6j_u2O4vt64Q` |
| `UserByScreenName` | query | `IGgvgiOx4QZndDHuD3x9TQ` |
| `TweetDetail` | query | `oCon7R-cgWRFy6EfZjaKfg` |
| `TweetResultByRestId` | query | `2Acdg-VztGlHX7MjX67Ysw` |
| `TweetResultsByRestIds` | query | `BwuN_YTc9eeI25mH_qjqPw` |
| `CommunityTweetsTimeline` | query | `gabM2RYROuhItXzDYUdjyA` |
| `CommunityMediaTimeline` | query | `cMhAbdDdk-pZKGwqi5FY_g` |
| `CommunityByRestId` | query | `vLS7mhOqMLtGZdXqFP1DEg` |

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
