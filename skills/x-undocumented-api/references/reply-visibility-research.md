# Reply Visibility Research

Last updated: 2026-05-20.

Use this page when investigating X replies that appear to post successfully but are not observed where a human expects them in the parent conversation. This page is intentionally about the issue model and learned experiments, not the baseline endpoint shapes already covered in `endpoint-patterns.md`.

## Issue Definition

The recurring failure mode is not simply "reply failed to post." In the strongest samples:

- `CreateTweet` or the native composer returns a created public tweet ID.
- The posting account can see the reply under the parent conversation.
- Other authenticated viewers can resolve the reply by direct tweet lookup.
- Those same viewers do not see the reply in parent `TweetDetail` under `Relevance` or `Recency`.
- `ModeratedTimeline` for the parent is valid but empty.
- Direct lookup does not show policy wrappers, tombstones, unavailable reasons, or limited-action markers.

Call this `direct-visible but cross-viewer parent-thread absent`, not deleted, hidden, or failed unless another surface proves that stronger claim.

## Surface Vocabulary

- `posted`: mutation/native composer returned a created tweet ID and no GraphQL error.
- `direct-visible`: `TweetResultByRestId` or equivalent tweet-detail lookup resolves the reply for a viewer.
- `self parent-visible`: the posting account sees the reply in parent `TweetDetail`.
- `cross-viewer parent-visible`: a different viewer sees the reply in parent `TweetDetail`.
- `search-discoverable`: `SearchTimeline` finds the reply by `conversation_id` or exact text. This is indexing/discoverability only.
- `profile-visible`: `UserTweetsAndReplies` finds the reply for the author, with cursor depth recorded.
- `first-party hidden`: parent `ModeratedTimeline` returns the reply.
- `policy-wrapped`: response includes `TweetWithVisibilityResults`, `limitedActionResults`, tombstone data, bouncer/unavailable reasons, or other visibility-policy metadata.

Do not collapse these into one boolean.

## What We Actually Learned

### Endpoint And Request Shape

Current query IDs and flags must still be regenerated from the live web bundle. In the 2026-05-20 runs, the observed current operations included `CreateTweet`, `TweetDetail`, `SearchTimeline`, `UserTweetsAndReplies`, and `ModeratedTimeline`.

Native `CreateTweet` reply variables include the parent reply block and current feature/field-toggle metadata. `engagement_request` is conditional, not universal: the web client emitted it only when source/composer state had promoted or impression context with both disclosure type and impression ID. Missing `engagement_request` is therefore a real source-context gap for some targets, but not proof that every direct reply is non-native.

### Search Is A Weak Visibility Oracle

`SearchTimeline` can miss replies that are visible through parent `TweetDetail`, direct lookup, or author timelines. Conversation search and exact-text search are useful discoverability signals, but they are not a source of truth for whether a reply exists or is shown in the conversation product.

### Parent Conversations Are Ranked And Paginated

`TweetDetail` is not a flat list of direct replies. It can return nested conversation modules, bottom cursors, `ShowMoreThreads` cursors, and gap/disconnected-reply affordances. A reply can be absent from page 1 and present after a cursor walk. Always record `rankingMode`, page number, cursor type, item count, direct reply IDs, and policy-marker counts.

### Hidden Replies Are A Separate Surface

First-party hidden replies should be checked through `ModeratedTimeline`. Several sampled parents returned valid empty `ModeratedTimeline` results while other surfaces showed ordinary ranking, pagination, or cross-viewer absence. Absence from the default conversation view is not enough to call a reply hidden.

### Native Composer Does Not Automatically Fix Cross-Viewer Parent Inclusion

A headed native browser composer send and a same-account direct GraphQL send were compared on the same parent. Both replies were:

- visible to the posting account in parent `TweetDetail`
- direct-visible to another authenticated viewer
- absent from that other viewer's parent `TweetDetail` under `Relevance` and `Recency`
- absent from `ModeratedTimeline`

This lowered the odds that stale query IDs, direct GraphQL request shape, or REST fallback behavior are the primary explanation for the self-only pattern.

### Real Google Chrome With Debugger Attachment Reproduced The Pattern

The same self-only pattern was reproduced using `Google Chrome.app` launched with a remote debugging port and an xpool Chrome profile. The interaction used the parent-page reply button. Multiple posting accounts showed:

- poster sees the reply in the parent thread
- other viewer can direct-load the reply
- other viewer does not see it in the parent thread
- hidden-replies timeline remains empty

Caveat: the recorded launcher evidence for these runs reported `proxyConfigured:false`, so treat them as real Chrome plus profile plus external debugger URL, not as full browser/proxy parity.

### One-Way Outgoing Graph Was Not Enough

Two xpool accounts with verified `follow_execute` graph edges to parent authors were selected, then used for real-Chrome parent-page reply sends.

Observed replies:

- `2057216316302631037`
- `2057216912741044338`

For both:

- the graph-connected posting account saw the reply in parent `TweetDetail` under `Relevance` and `Recency`
- two external xpool viewers could direct-load the reply
- those viewers did not see the reply in parent `TweetDetail` under `Relevance` or `Recency`
- `ModeratedTimeline` was empty

This does not falsify graph-based gating. It narrows it: a one-way edge where the poster follows the parent author did not clear the threshold in these samples. Incoming follows, mutual follows, prior interaction, viewer relationship to the poster, and account trust remain open.

## Current Best Thinking

The strongest current model is read-time, viewer-specific parent-conversation distribution or ranking, with account trust/equity and graph distance as likely cofactors.

Less likely as sole explanations:

- deletion: direct lookup resolves the replies
- first-party hidden replies: `ModeratedTimeline` was empty in sampled cases
- simple stale endpoint failure: current GraphQL and native composer paths both produced accepted replies
- SearchTimeline absence: search repeatedly missed replies that existed elsewhere
- request-shape drift alone: native composer and direct GraphQL showed the same cross-viewer parent absence in at least one controlled comparison

Still plausible as cofactors:

- account-level trust or equity buckets
- cold-reply ranking against parent-specific audiences
- incoming or mutual graph thresholds, not merely outgoing follow edges
- prior interaction between poster, parent author, and viewer
- automation/browser fingerprint or proxy mismatch
- delayed distribution that changes after hours
- target/source context such as home timeline, search result, promoted/impression-backed tweet, or exact route context

## Recommended Experiment Matrix

For each created reply, record public tweet IDs and account hashes only:

1. Posting account parent `TweetDetail`: `Relevance`, `Recency`, page/cursor depth.
2. External viewer parent `TweetDetail`: same modes and cursor depth.
3. Direct lookup as poster and as external viewer.
4. Author `UserTweetsAndReplies`, with cursor depth.
5. Parent `ModeratedTimeline`.
6. `SearchTimeline` `conversation_id:<parent_id>` and exact-text search, labeled as discoverability only.
7. Policy markers: `TweetWithVisibilityResults`, `limitedActionResults`, tombstones, bouncer/unavailable reasons, and GraphQL errors.
8. Timing: T+0, T+5m, T+1h, and T+24h where practical.
9. Browser path: native user/manual, real Chrome external debugger, direct GraphQL, REST fallback.
10. Relationship path: no known edge, poster follows parent author, parent author follows poster, mutual, prior interaction, and high-trust account control.

The highest-value next discriminator is a same-parent comparison using a materially higher-trust account or an incoming/mutual graph relationship. A one-way outgoing follow edge has already failed to change the observed result.

## Evidence Hygiene

Never store or print raw cookies, `auth_token`, `ct0`, bearer tokens, proxy credentials, or full upstream payloads. Keep evidence to:

- operation name and dated query ID
- public parent/reply tweet IDs
- hashed account/proxy/profile identifiers
- request method/path shape
- HTTP status and GraphQL error presence
- transaction ID state, not the raw value
- response path presence and item counts
- policy-marker counts
- ranking mode, cursor/page depth, and timing
- Chrome/browser shape and explicit caveats

When a run involves a live mutation, state the user approval, the side effect, the account hash, the parent tweet ID, the created reply ID, and the surfaces checked.
