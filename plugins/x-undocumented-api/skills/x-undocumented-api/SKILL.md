---
name: x-undocumented-api
description: Manual-only skill. Never automatically load or select this skill from task context. Use only when the user explicitly asks to manually reference this skill or names `x-undocumented-api` / `x-api-skill`.
---

# X Undocumented API

## Overview

Use this skill for X.com's frontend web API: GraphQL operations under `https://x.com/i/api/graphql`, supporting REST-like web endpoints under `https://x.com/i/api`, and the browser headers/cookies those calls require.

## First Rules

- Verify operation names and query IDs against the current X web bundle; query IDs rotate.
- Treat `operationName` as the durable conceptual endpoint, and `queryId` as rotating bundle metadata.
- Never print raw cookies, `auth_token`, `ct0`, bearer tokens, proxy credentials, or full upstream payloads.
- Generate `x-client-transaction-id` from the current X web page/bundle material and the exact request method/path.
- Do not test mutations against live accounts unless the user explicitly asks for that mutation and understands the effect.
- Keep endpoint evidence with exact dates, operation IDs, variables, feature flags, response paths, account/access scope, and result counts.
- Separate upstream variables from local caller filters. A runtime or CLI `itemFilter` can be an application-side filter rather than a proven GraphQL variable.

## Reference Map

Read only what the task needs:

- [runtime-and-auth.md](references/runtime-and-auth.md): browser auth, cookies, bearer tokens, CSRF, transaction IDs, headers, guest tokens, and error classes.
- [graphql-discovery.md](references/graphql-discovery.md): extracting operation names, query IDs, feature flags, field toggles, and endpoint inventories from X web bundles.
- [endpoint-patterns.md](references/endpoint-patterns.md): request/response shapes for SearchTimeline, user/list/follower/tweet timelines, timeline instructions, and search operators.
- [community-timelines.md](references/community-timelines.md): X Communities operations, variables, ranking modes, response paths, and community-search caveats.
- [cursor-behavior.md](references/cursor-behavior.md): X timeline cursor semantics, pagination risks, fan-out caveats, and evidence standards.
- [reply-visibility-research.md](references/reply-visibility-research.md): high-fidelity notes from the 2026-05 reply visibility investigation, including observed failure modes, experiments, current best thinking, and next discriminators.

Reusable script:

- `scripts/extract-x-graphql-endpoints.ts`: fetch current X web bundles and save a JSON/CSV operation inventory.

## Investigation Workflow

1. Clarify whether the user needs an API explanation, a current endpoint inventory, a request shape, or a live read-only probe.
2. Extract or inspect the current X web bundle before relying on query IDs, variables, features, or response paths.
3. For unknown GraphQL operations, locate nearby bundle code for variable names, feature flags, field toggles, and response normalization paths.
4. For author-corpus work, compare native timeline operations against `SearchTimeline` author queries and record lane yield per page, not just total pages.
5. For live read probes, use secret-safe output: status code, top-level keys, response path presence, item counts, cursor presence, and example public IDs only.
6. For pagination behavior, record request cursor, returned cursors, item IDs in order, item count, first/last sort index, endpoint, variables, and observed time.
6. Save dated findings outside the skill unless the user explicitly asks to update this skill.

## GraphQL Request Shape

X web GraphQL paths have this form:

```text
https://x.com/i/api/graphql/<queryId>/<operationName>?variables=<json>&features=<json>
```

Some operations also use `fieldToggles=<json>`.

Authenticated reads commonly need these headers:

```text
authorization: Bearer <X web bearer token>
x-csrf-token: <ct0>
cookie: ct0=<ct0>; auth_token=<auth_token>
x-client-transaction-id: <generated for method + full path>
x-twitter-active-user: yes
x-twitter-auth-type: OAuth2Session
x-twitter-client-language: en
origin: https://x.com
referer: https://x.com/
```

The transaction ID path must include the query ID:

```text
/i/api/graphql/<queryId>/<operationName>
```

## Diagnostics

| Symptom | Likely cause | Next check |
| --- | --- | --- |
| HTTP 401 or 403 | Expired cookies, missing `ct0`, bad bearer token, access restriction, account challenge | Refresh browser session material; do not print secrets |
| Empty HTTP 404 | Missing/invalid `x-client-transaction-id` or stale query ID | Verify full path includes query ID and regenerate transaction ID from current X material |
| HTTP 429 | Rate limited account, IP, or operation | Inspect X rate-limit headers and retry windows |
| HTTP 400 | Variable, feature, or field-toggle mismatch | Compare request payload with current bundle caller code |
| HTTP 200 with empty timeline | Access limitation, wrong response path, stale variables, logged-out limitation, or empty source | Inspect top-level keys and instruction path without dumping payload |
| Data is stale or incomplete | Search index behavior or ranking product choice | Prefer native timeline operations when available |
| Mutation returns HTTP 200 but no send captured in the HTTP log, yet the action took effect | The action rode a **WebSocket**, not an HTTP mutation (X Chat sends are WS frames to `wss://chat-ws.x.com/ws`) | Use a WebSocket frame capture (CDP `WebSocketFrameSent`/`Received`), not request logging. HTTP GraphQL capture will never see these sends |
| Reply verification mismatch after REST or fallback send | X may prepend the leading `@handle`; the visible draft text is often the `display_text_range` slice | Compare against `legacy.full_text.slice(display_text_range)` when available |

## Current High-Value Facts

- `SearchTimeline` uses `rawQuery`, `product`, `count`, optional `cursor`, and promoted-content controls.
- `SearchTimeline` author queries can outperform native user timelines for corpus collection. In live xpool probes on 2026-06-18, `from:<handle> -filter:replies -filter:retweets` and `from:<handle> filter:replies` reached 100 lane items in 5 pages for sampled accounts where native timeline crawls hit only 39-47 items after 20 pages.
- Search author-query cursors appear risky across account rotation. In live xpool profile-sample probes, later-page `SearchTimeline` continuations under rotating accounts produced concentrated 404 / timeout / network failures; pinning one account per lane materially reduced that failure mix, though it did not remove empty-page degeneration.
- Native list recency is `ListLatestTweetsTimeline`, not `SearchTimeline list:<id>`.
- Native community posts are `CommunityTweetsTimeline`, not a `SearchTimeline` community operator.
- **Direct messages are now "X Chat": end-to-end-encrypted, PIN-gated, and sent over WebSocket (`wss://chat-ws.x.com/ws?token=<JWT>`), not a GraphQL/REST mutation.** Legacy DM mutations (`useSendMessageMutation`, REST `dm/new2.json`) are gone from current bundles. See the 2026-06-18 notes below.
- `UserTweetsAndReplies` local `itemFilter` handling is not proof of an upstream GraphQL variable. In the 2026-06-18 bundle scan, `itemFilter`, `authored_posts`, and `authored_replies` strings were absent from the current client-web bundle.
- `UserTweets` can include repost surfaces; do not treat it as pure authored root-post history without checking surface kind or local filters. In 2026-06-18 live xpool probes, native `UserTweets` recovered materially more root-post items than author-search for some post-light accounts (`64` vs `20`, `100` vs `74`, `22` vs `2` in early comparisons, later `22` vs `2`, `1` vs `1`, and `18` vs `0` on three more post-light accounts), so a post lane may need native-timeline preference even when reply lanes stay on search.
- Low-yield native post `cursor_loop` is often a corpus-shape signal, not a pure transport failure. In one fresh xpool worker slice, low-yield post loops split into two buckets: sparse accounts where replies also stopped early (average lifetime tweet count about `200`) and reply-heavy accounts where replies still reached target (average lifetime tweet count about `4300` while root-post yield stayed near `7`).
- In a larger hybrid-worker slice after the posts=`UserTweets` / replies=`SearchTimeline` rollout (1,534 samples since the 2026-06-18T21:39:50Z boot), reply lanes were dominated by `target_items_reached` and `source_exhausted`, while posts still split across `target_items_reached`, `max_pages_reached`, and `cursor_loop`. Treat that as evidence for a hybrid endpoint choice, not a single universally best authored-corpus endpoint.
- A short `runner_terminated` burst immediately after a PM2 restart can be rollover noise from in-flight work rather than a steady-state cursor signal. In the same 2026-06-18 investigation, all fresh `runner_terminated` reply-lane rows landed within about one second, 44-45 seconds after restart, with none afterward.
- `TimelineTimelineCursor` entries commonly carry `Top` and `Bottom` cursor values.
- `count` is not always honored by timeline operations; observe returned item counts. Current live author-search probes emitted about 20 items/page even when higher counts were requested.

## 2026-06-18 Direct Messages / X Chat E2E Notes

These notes came from a live investigation (logged-in managed sessions via a CDP-backed browser tool, with WebSocket frame capture). Treat them as the current DM reality, superseding any older "send a DM via GraphQL" assumption.

- **Legacy DM mutations are gone.** `useSendMessageMutation` (query id `MaxK2PKX1F9Z-9SwqwavTw` in the 2023-era `twitter-api-client` registry) and the REST fallback `dm/new2.json` are absent from every current X web bundle chunk. Do not reuse them; they will not work.
- **X has replaced DMs with "X Chat": end-to-end-encrypted and PIN-gated.** Rolled out from Nov 2025 ("X Chat replacing DMs for some X users"). Authenticated `/messages` redirects to `/i/chat/pin/new` until the account is provisioned.
- **Send is a WebSocket frame, not an HTTP mutation.** The send rides `wss://chat-ws.x.com/ws?token=<JWT>`. HTTP GraphQL/REST capture during a real send observed **zero** send calls. There is no send `operationName` to extract — bundle extraction can never surface a DM send query id, by design, not by capture gap.
- **PIN derives encryption keys client-side.** Provisioning the passcode generated **no** server request carrying the PIN; keys are produced locally from it. A fresh browser context (no local key material) is redirected to `/i/chat/pin/recovery` and must re-enter the PIN to re-derive keys before any read or send. Cookie-only / headless sessions are therefore insufficient for X Chat without PIN re-entry.
- **DM-adjacent HTTP mutations that DO remain in current bundles:** `dmBlockUser` (`IYw9u1KEhrS-t-BXsau4Uw`), `dmUnblockUser` (`Krbs6Nak_o7liWQwfV1jOQ`), `DmNsfwMediaFilterUpdate` (`of_N6O33zfyD4qsFJMYFxA`), `ConversationControlChange` (`57WYJNnWH0vM3Ip_gm8B2g`), `ConversationControlDelete` (`OoMO_aSZ1ZXjegeamF9QmA`). These are block/unblock/control, not send.
- **Capture tooling caveats:** CDP `Network.enable` does not capture POST bodies unless `max_post_data_size` is set; and WebSocket frames need dedicated `WebSocketCreated` / `WebSocketFrameSent` / `WebSocketFrameReceived` handlers — request handlers never see them. A CDP tool without WS handlers is blind to X Chat.
- **Reachability:** accounts that have never followed / accepted a message request from each other cannot exchange DMs — recipient search at `/i/chat` compose returns only the sender, and a typed message becomes a self-chat ("You: <text>") the other account never receives.

## 2026-05-20 Reply Publish Visibility Notes

These notes came from a live, user-approved xpool reply probe plus current X web bundle inspection. Treat query IDs as dated facts and regenerate before reusing.

- Current observed `CreateTweet` query ID was `5CdvsV_zjv4L64XFifAglw`; current observed `TweetDetail` query ID was `oCon7R-cgWRFy6EfZjaKfg`.
- A patched direct GraphQL reply send used `POST /i/api/graphql/5CdvsV_zjv4L64XFifAglw/CreateTweet`, returned HTTP 200, had no top-level GraphQL errors, and returned `data.create_tweet.tweet_results`.
- Useful mutation evidence, without secrets: method, path, operation name, query ID, transaction-id state, HTTP status, content type, GraphQL error presence, response path, `ct0` rotation boolean, rate-limit headers, body key names, created public tweet ID, parent tweet ID, and verifier result.
- For replies, native-like variables include `tweet_text`, `media`, `semantic_annotation_ids`, and `reply.in_reply_to_tweet_id` with `exclude_reply_user_ids`.
- Current web metadata includes `fieldToggles` on `CreateTweet`; include the current toggles when the bundle advertises them.
- Native `engagement_request` is conditional, not universal. X web emitted it only when composer/source state had promoted/impression content with both `disclosure_type` and `impression_id`; missing it is a source-context gap for impression-backed targets, not proof every direct reply is non-native.
- `TweetDetail` parent-thread visibility can lag or paginate. In the live probe, the created reply was initially behind a `ShowMoreThreads` cursor in `rankingMode=Relevance`, then appeared on page 1 a few minutes later.
- `SearchTimeline` can be a false negative for newly created replies. In the live probe, the reply was visible through parent `TweetDetail Relevance`, while `SearchTimeline` missed it by both `conversation_id:<parent_id>` and exact-text search.
- Do not use `SearchTimeline` presence as the source of truth for reply visibility. It is a discoverability/indexing signal only.
- First-party hidden replies are a separate surface. Check `ModeratedTimeline` for the parent before labeling a reply hidden; in the live probe it returned a valid empty hidden-replies timeline while parent `TweetDetail` showed the reply.
- Visibility verification should be a vector, not one boolean: direct lookup visible, author replies visible with cursor depth, parent `TweetDetail` seen with ranking mode/page/cursor, search discoverable, `ModeratedTimeline` present/absent, policy wrapper/tombstone/limited-action state.
- Later native-browser, real-Google-Chrome, and graph-connected xpool experiments are summarized in [reply-visibility-research.md](references/reply-visibility-research.md). The short version: accepted replies can be direct-visible to other viewers while absent from those viewers' parent `TweetDetail`; a one-way poster-follows-parent-author edge did not clear that threshold in the sampled runs.
