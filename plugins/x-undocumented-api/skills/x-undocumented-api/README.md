# X Undocumented API

This skill helps an agent work with X.com's private web API surface when the user explicitly asks for it.

Use it for GraphQL operation discovery, rotating query IDs, browser-style headers, feature flags, cursor behavior, timeline endpoints, and the practical details needed to reproduce what the X web app is doing.

Undocumented APIs move, and mistakes can leak credentials or hit live account actions. This skill makes the agent verify current web bundles, preserve evidence, and keep secrets out of output.

Good fits:

- Inspecting X web GraphQL operations
- Understanding timeline and cursor behavior
- Updating request shapes after query IDs rotate
- Building tooling around read-only X endpoints
- Documenting endpoint evidence with dates and scopes
- Verifying operation IDs against current web bundles

This is manual-only. The agent should not load it from vague social-media context. Default to read-only work: no credential capture and no authenticated or live-account actions unless the user explicitly provides a safe scope.
