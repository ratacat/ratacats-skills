# Endpoint Patterns

Use this reference when calling or comparing X web GraphQL operations.

## Timeline Normalization

X timeline responses usually contain instruction arrays. Common paths:

| Operation | Instruction path |
| --- | --- |
| `SearchTimeline` | `data.search_by_raw_query.search_timeline.timeline.instructions` |
| `ListLatestTweetsTimeline` | `data.list.tweets_timeline.timeline.instructions` |
| `UserTweets` | `data.user.result.timeline_v2.timeline.instructions` |
| `UserTweetsAndReplies` | `data.user.result.timeline_v2.timeline.instructions` |
| `UserMedia` | `data.user.result.timeline_v2.timeline.instructions` |
| `Followers` | `data.user.result.timeline.instructions` |
| `Following` | `data.user.result.timeline.instructions` |
| `CommunityTweetsTimeline` | `data.communityResults.result.ranked_community_timeline.timeline.instructions` |

Instruction types to handle:

- `TimelineTimelineCursor`: `Top` is usually previous/newer; `Bottom` is usually next/older.
- `TimelineTimelineItem`: one tweet/user/list/community item.
- `TimelineTimelineModule`: module containing nested items.
- `TimelineTerminateTimeline`: terminal state marker.

`sortIndex` is observation metadata, not a caller-controlled boundary.

## SearchTimeline

Variables commonly include:

```json
{
  "rawQuery": "from:someuser",
  "count": 20,
  "querySource": "typed_query",
  "product": "Latest",
  "cursor": "<optional>"
}
```

Products commonly include `Top`, `Latest`, `People`, `Photos`, and `Videos`, depending on the active web client.

Useful observed query patterns:

| Pattern | Notes |
| --- | --- |
| `from:<screen_name>` | User-authored corpus search; often stronger than native user timelines for bounded corpus collection. |
| `from:<screen_name> filter:replies` | Author replies only; useful when native replies crawls have low lane yield. |
| `from:user1 OR from:user2` | Multi-author search; query length is the practical constraint. |
| `since_time:<unix_sec>` | Precise lower time boundary. |
| `until_time:<unix_sec>` | Precise upper time boundary. |
| `list:<list_id>` | Accepted, but can lag native list timelines. |
| `-filter:nativeretweets -filter:retweets -filter:quote -filter:replies` | Useful exclusion pattern. |
| `-is:reply -is:retweet` | Accepted in some cases but less reliable. |
| `community:<community_id>` | Not a reliable way to fetch posts inside a community. |

For list recency, prefer `ListLatestTweetsTimeline`. For community posts, prefer `CommunityTweetsTimeline`.

Live xpool probes on 2026-06-18 found that author-search lanes can be dramatically more page-efficient than native mixed timelines for profile corpus collection. Sampled results: `from:CosmicDude3000 -filter:replies -filter:retweets` reached 100 posts in 5 pages while `UserTweetsAndReplies` local post filtering hit 39 posts after 20 pages; `from:Presto_Research filter:replies` and `from:knust_src filter:replies` reached 100 replies in 5 pages while `UserTweetsAndReplies` local reply filtering stopped at 47 and 46 replies after 20 pages. Later the same day, direct comparisons also showed post-light accounts where native `UserTweets` recovered more root posts than author-search (`64` vs `20`, `100` vs `74`, `22` vs `2`, then `22` vs `2`, `1` vs `1`, and `18` vs `0` on three more post-light accounts). Treat that as dated evidence tied to X web behavior and re-check with your own access mode.

## ListLatestTweetsTimeline

Variables:

```json
{
  "listId": "<rest id>",
  "count": 20,
  "cursor": "<optional>"
}
```

Response path:

```text
data.list.tweets_timeline.timeline.instructions
```

Caveats:

- Access depends on list visibility and account relationship.
- Some lists can return an empty timeline object if inaccessible.
- Query ID rotates with X client builds.

## User Timelines

Common variables:

```json
{
  "userId": "<rest id>",
  "count": 20,
  "cursor": "<optional>",
  "includePromotedContent": false,
  "withQuickPromoteEligibilityTweetFields": false,
  "withVoice": true
}
```

Common operations:

- `UserTweets`
- `UserTweetsAndReplies`
- `UserMedia`
- `UserHighlightsTweets`
- `UserArticlesTweets`
- `UserSuperFollowTweets`

User timeline pagination is cursor-led. Do not assume cursors are stable partitions across time or accounts.

Do not assume app-side `itemFilter` values are real GraphQL variables. In the 2026-06-18 client-web bundle scan, `itemFilter`, `authored_posts`, and `authored_replies` strings were absent, and live xpool probes showed that local-only filtering on `UserTweetsAndReplies` can spend 20 pages to emit fewer than 50 target lane items.

For `SearchTimeline`, later-page cursors are risky under account rotation. In 2026-06-18 live xpool profile-sample probes, rotating-account continuation produced concentrated 404 / timeout / network failures on cursor-bearing pages; pinning one account per lane materially improved stability.

`UserTweets` can include repost surfaces. If you need authored root posts only, verify or filter `surfaceSourceKind` rather than assuming the endpoint is already clean. Low-yield `UserTweets` cursor loops do not automatically mean search will do better; in fresh xpool profile-sample slices, many such cases were either truly sparse or reply-heavy accounts. On the same investigation, a larger live hybrid slice kept posts distributed across `target_items_reached`, `max_pages_reached`, and `cursor_loop`, while reply search mostly settled into `target_items_reached` and `source_exhausted`, which is a stronger argument for a hybrid lane choice than for a universal search fallback.

## Followers And Following

Common variables:

```json
{
  "userId": "<rest id>",
  "count": 20,
  "cursor": "<optional>",
  "includePromotedContent": false
}
```

Common operations:

- `Followers`
- `Following`
- `FollowersYouKnow`
- `BlueVerifiedFollowers`

Returned counts may differ from requested `count`. Treat `Bottom` cursors as sequential traversal state, not durable shard keys.

## Tweet Lookup And Detail

Common operations:

- `TweetDetail`: conversation/detail page.
- `TweetResultByRestId`: single tweet by REST ID.
- `TweetResultsByRestIds`: batch tweet lookup.
- `ModeratedTimeline`: first-party hidden replies for a root tweet.

Typical variables include tweet IDs plus booleans controlling quote/source/community/card/voice/note-tweet fields. Copy the current variable set from the bundle before probing.

Observed `TweetDetail` context variables can include `focalTweetId`, `cursor`, `rankingMode`, `referrer`, `controller_data`, `rux_context`, and `with_rux_injections`. Persist only opaque fingerprints for controller/rux values unless the user explicitly needs raw local debugging.

`TweetDetail` is not a flat reply list. It can return `TimelineTimelineModule` entries, nested replies, `Bottom` cursors, `ShowMoreThreads` cursors, and gap/disconnected-reply affordances. Record the ranking mode, page number, cursor type, direct reply IDs, and policy/tombstone counts.

`ModeratedTimeline` variables observed on 2026-05-20:

```json
{
  "rootTweetId": "<parent tweet id>",
  "count": 20,
  "cursor": "<optional>",
  "includePromotedContent": false
}
```

Use `ModeratedTimeline` to distinguish first-party hidden replies from ordinary parent-thread ranking, pagination, or search-index absence.

## Mutations

Examples:

- `CreateTweet`
- `DeleteTweet`
- `CreateRetweet`
- `DeleteRetweet`
- `FavoriteTweet`
- `UnfavoriteTweet`
- `CreateBookmark`
- `DeleteBookmark`
- `JoinCommunity`
- `LeaveCommunity`

Mutation probes cause live side effects. Do not run them unless explicitly requested and scoped.

### CreateTweet Replies

Observed 2026-05-20 live reply publish shape:

```text
POST /i/api/graphql/5CdvsV_zjv4L64XFifAglw/CreateTweet
```

Current request body shape:

```json
{
  "queryId": "<current CreateTweet query id>",
  "variables": {
    "tweet_text": "<draft>",
    "media": { "media_entities": [], "possibly_sensitive": false },
    "semantic_annotation_ids": [],
    "reply": {
      "in_reply_to_tweet_id": "<parent tweet id>",
      "exclude_reply_user_ids": []
    }
  },
  "features": {},
  "fieldToggles": {}
}
```

Always fill `features` and `fieldToggles` from the current X bundle, not from this example.

For reply verification, do not compare the full text blindly. X can include a leading `@handle` in `legacy.full_text`; use `legacy.display_text_range` to extract the visible draft slice when present.

Suggested reply visibility checks after a mutation:

1. Check HTTP status and GraphQL `errors`.
2. Extract the created public tweet ID from `data.create_tweet.tweet_results`.
3. Resolve the created tweet directly by ID.
4. Walk parent `TweetDetail` with explicit `rankingMode`, page count, and cursor types.
5. Check author `UserTweetsAndReplies` with cursor depth.
6. Check parent `ModeratedTimeline`.
7. Treat `SearchTimeline` conversation/exact-text results as discoverability only.

## Endpoint Evaluation Checklist

Before calling an operation "works":

- Was `queryId` extracted from the current X bundle?
- Were variables copied from current web code?
- Were feature switches and field toggles included?
- Was `x-client-transaction-id` generated for the full path?
- Did JSON parse?
- Were GraphQL `errors` inspected?
- Did the expected response path contain data?
- Were item IDs and cursors normalized?
- Was access scope documented?
- Was evidence saved without secrets or raw payloads?
