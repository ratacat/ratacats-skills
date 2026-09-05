# X Undocumented API

This skill helps an agent work with X.com's private web API surface when the user explicitly asks for it.

Use it for GraphQL operation discovery, rotating query IDs, browser-style headers, feature flags, cursor behavior, timeline endpoints, and the practical details needed to reproduce what the X web app is doing. Undocumented APIs move, and mistakes can leak credentials or hit live account actions, so the skill makes the agent verify current web bundles, preserve evidence, and keep secrets out of output.

Note: this skill is manual-only. The agent should not load it from vague social-media context. Default to read-only work: no credential capture and no authenticated or live-account actions unless the user explicitly provides a safe scope.

Good fits:

- Inspecting X web GraphQL operations
- Understanding timeline and cursor behavior
- Collecting trends, Explore recommendations, related terms, and AI story context
- Updating request shapes after query IDs rotate
- Building tooling around read-only X endpoints
- Documenting endpoint evidence with dates and scopes

## Install

```sh
# skills.sh CLI — Claude Code, Codex, Cursor, OpenCode, and more
npx skills add ratacat/ratacats-skills --skill x-undocumented-api

# or the Claude plugin marketplace
/plugin marketplace add ratacat/ratacats-skills
/plugin install x-undocumented-api@ratacats-skills
```

## Requirements

For live authenticated probes, use only an X browser session the user is authorized to use. Keep cookies, `auth_token`, `ct0`, bearer tokens, proxy credentials, and raw upstream payloads out of output.

Query IDs rotate. Before relying on an operation ID, inspect the current X web bundle or use [`scripts/extract-x-graphql-endpoints.ts`](scripts/extract-x-graphql-endpoints.ts) to build a current operation inventory.

The extractor starts at `https://x.com/explore`; the logged-out homepage now
uses a different web app. See [Trends and Explore](references/trends-and-explore.md)
for measured collection limits, location controls, and authenticated probe results.
