# Community Timelines

Use this reference for X Communities: community IDs, community metadata, community posts, community media, community membership, and community search.

## Native Community Timeline Operations

The 2026-05-18 X web bundle exposed:

| Operation | Query ID | Type | Use |
| --- | --- | --- | --- |
| `CommunityTweetsTimeline` | `gabM2RYROuhItXzDYUdjyA` | query | Authenticated community posts timeline |
| `CommunityTweetsLoggedOutTimeline` | `XSecWy_EYKNum_wDxOiSgw` | query | Logged-out community posts timeline |
| `CommunityTweetsRankedLoggedOutTimeline` | `BKvjKir30Khfu5dFo0YWgA` | query | Logged-out ranked community posts timeline |
| `CommunityMediaTimeline` | `cMhAbdDdk-pZKGwqi5FY_g` | query | Authenticated community media timeline |
| `CommunityMediaLoggedOutTimeline` | `RJLmja51UdSwatzo-h8-HQ` | query | Logged-out community media timeline |
| `CommunityByRestId` | `vLS7mhOqMLtGZdXqFP1DEg` | query | Community metadata by ID |

Query IDs rotate; re-extract before use.

## CommunityTweetsTimeline

Likely variables:

```json
{
  "communityId": "1471580197908586507",
  "count": 20,
  "cursor": "<optional>",
  "displayLocation": "Community",
  "rankingMode": "Recency",
  "withCommunity": true
}
```

Observed ranking modes:

- `Recency`
- `Relevance`
- `Likes`

Expected response path:

```text
data.communityResults.result.ranked_community_timeline.timeline.instructions
```

## Community Metadata

`CommunityByRestId` fetches community metadata by REST ID. Use it to validate:

- community existence
- name and description
- visibility/access state
- membership affordances
- rules/about modules when exposed

## Community Search Caveat

`SearchTimeline` queries such as these can find posts linking to or mentioning a community ID, but should not be treated as native community-post timelines:

```text
community:<community_id>
"<community_id>"
url:x.com/i/communities/<community_id>
url:twitter.com/i/communities/<community_id>
```

Use `CommunityTweetsTimeline` for posts inside a community.

## Community Operation Inventory

Community operations found in the 2026-05-18 scan:

| Operation | Type | Query ID |
| --- | --- | --- |
| `CommunitiesExploreTimeline` | query | `FpA1LTcHu3vk4JQjDvp4Tg` |
| `CommunitiesMainDiscoveryModule` | query | `xm1irSse72yjs3GX_zaUhg` |
| `CommunitiesMainPageTimeline` | query | `ka9urimVUngifjNmpj3I2A` |
| `CommunitiesMembershipsSlice` | query | `keBi-IFOHQFR59XV8-JCbw` |
| `CommunitiesMembershipsTimeline` | query | `MogKlpyJ2Gjm3EkO9ySqIQ` |
| `CommunitiesRankedTimeline` | query | `dGPLIKm6Fz896eIOXHLcPg` |
| `CommunityAboutTimeline` | query | `snxS27FfPG3wo5zHl9oGeA` |
| `CommunityByRestId` | query | `vLS7mhOqMLtGZdXqFP1DEg` |
| `CommunityCreateRule` | mutation | `-oxunWxVyyfBA7MkGMQqMQ` |
| `CommunityDiscoveryTimeline` | query | `xvMjMGVFUWrFT-7GxLK94Q` |
| `CommunityEditBannerMedia` | mutation | `GQ8By90KSKh4iUSgrsj0hw` |
| `CommunityEditName` | mutation | `QzEcwyG5-ePH_IFvN92Xgg` |
| `CommunityEditPurpose` | mutation | `9TYpgbkD-c2rKmpeF_PZCw` |
| `CommunityEditQuestion` | mutation | `Ps0w6za_U2yyixe8a3hCHA` |
| `CommunityEditRule` | mutation | `ASqVyMPbvWMO2Jl2udvXcw` |
| `CommunityHashtagsTimeline` | query | `4a4shWGCv930ZLsClUUIEg` |
| `CommunityMediaLoggedOutTimeline` | query | `RJLmja51UdSwatzo-h8-HQ` |
| `CommunityMediaTimeline` | query | `cMhAbdDdk-pZKGwqi5FY_g` |
| `CommunityMemberRelationshipTypeahead` | query | `wLq8nJhuzS5Tzq2p-dgIlw` |
| `CommunityModerationKeepTweet` | mutation | `QWQ2Z2nw2H3KiD3qqMb6UQ` |
| `CommunityModerationTweetCasesSlice` | query | `cI7NEW0bCgYXfY2fsq6h0A` |
| `CommunityRemoveBannerMedia` | mutation | `7W5Im-Z2q-v81NbUkiAvKQ` |
| `CommunityRemoveRule` | mutation | `0SkYzk2GE0vpHbvpZt1Ruw` |
| `CommunityReorderRules` | mutation | `SrCOaQHd6cmGFa0W3Q2rBg` |
| `CommunityTweetModerationLogSlice` | query | `rB5JjjcOg_-PpiHqwSEcag` |
| `CommunityTweetsLoggedOutTimeline` | query | `XSecWy_EYKNum_wDxOiSgw` |
| `CommunityTweetsRankedLoggedOutTimeline` | query | `BKvjKir30Khfu5dFo0YWgA` |
| `CommunityTweetsTimeline` | query | `gabM2RYROuhItXzDYUdjyA` |
| `CommunityUpdateRole` | mutation | `7SZnPJ1qwHqUsFVjbLEVig` |
| `CommunityUserInvite` | mutation | `bz8uZZOzk3SUQUKTPioZpQ` |
| `CommunityUserRelationshipTypeahead` | query | `_qsnOaYZy00m-KSiTIFyEA` |
| `CreateCommunity` | mutation | `uL--Q0pdGxf9qKuHQpKXdw` |
| `GlobalCommunitiesLatestPostSearchTimeline` | query | `mVQneZqcoJ8cq6KyPhOaVw` |
| `GlobalCommunitiesPostSearchTimeline` | query | `tFCoI0yNtVLK9nhz0teG4w` |
| `JoinCommunity` | mutation | `TQ-ErN9XPSjNkSY4ZB7W6Q` |
| `LeaveCommunity` | mutation | `q9LMMKLXMQ5t9AdHYjm7Ew` |
| `RequestToJoinCommunity` | mutation | `u9NzT5-wCdzObx7_tGd5bg` |

## Safety Notes

- Community mutations have live effects.
- Some communities require membership or logged-in access.
- Logged-out community operations can return HTTP 200 but no timeline items due to access, variables, feature flags, or response path differences.
- Public community cards in ordinary tweets are not evidence that the community timeline was fetched.
