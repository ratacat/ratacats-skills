# Runtime And Auth

Use this reference for X web browser auth, headers, cookies, transaction IDs, guest tokens, and request execution.

## Authenticated Web Calls

Authenticated X web API calls commonly require:

- `authorization: Bearer <X web bearer token>`
- `auth_token` cookie
- `ct0` cookie and matching `x-csrf-token` header
- `x-client-transaction-id` generated for the request method and path
- browser-like origin, referer, language, and active-user headers

Do not log raw cookies, bearer tokens, CSRF tokens, authorization headers, or proxy credentials.

## Bearer Token

The X web bearer token is embedded in current client-web JavaScript. A typical extraction flow:

1. Fetch `https://x.com`.
2. Extract `https://abs.twimg.com/responsive-web/client-web/*.js` script URLs.
3. Search those scripts for the web bearer token string.
4. Treat the token as sensitive even though it is bundled into the web client.

Bearer tokens can rotate. Re-extract when HTTP 401/403 behavior changes or after a large client-web deployment.

## Cookies And CSRF

Authenticated browser sessions use:

- `auth_token`: login session cookie
- `ct0`: CSRF cookie

For authenticated state-changing calls and many reads, send:

```text
cookie: ct0=<ct0>; auth_token=<auth_token>
x-csrf-token: <ct0>
x-twitter-auth-type: OAuth2Session
```

`ct0` can rotate through `set-cookie`; callers should capture the latest value.

## x-client-transaction-id

Some X web endpoints return empty 404 responses if the transaction ID is missing or invalid.

The generator depends on current X page/bundle material, request method, request path, and time. Generate for the exact path:

```text
/i/api/graphql/<queryId>/<operationName>
```

Do not generate for only the operation name. Do not reuse a transaction ID after changing query ID, operation name, method, or path.

Known input material includes:

- `https://x.com` HTML
- `twitter-site-verification` metadata
- SVG loading animation paths
- ondemand bundle code
- current time
- HTTP method
- full request path

## Guest Tokens

Logged-out or guest endpoints may require:

```text
authorization: Bearer <X web bearer token>
x-guest-token: <guest token>
x-twitter-active-user: yes
x-twitter-client-language: en
```

Guest-token success does not imply authenticated success, and authenticated success does not imply logged-out visibility.

## Common Headers

```text
accept: */*
authorization: Bearer <redacted>
content-type: application/json
origin: https://x.com
referer: https://x.com/
user-agent: <browser UA>
x-client-transaction-id: <generated>
x-csrf-token: <ct0>
x-twitter-active-user: yes
x-twitter-auth-type: OAuth2Session
x-twitter-client-language: en
```

## Rate-Limit Headers

Capture these headers when present:

- `x-rate-limit-limit`
- `x-rate-limit-remaining`
- `x-rate-limit-reset`
- `retry-after`

Rate limits may vary by operation, account state, IP, and auth mode.

For mutation probes, also capture secret-safe runtime/network facts:

- HTTP method and GraphQL path
- operation name and query ID
- transaction-id generation state, without the raw value
- HTTP status and content type
- GraphQL `errors` presence/count
- response path used to extract the public entity ID
- `ct0` rotation boolean, without the token
- rate-limit limit/remaining/reset
- request body top-level keys and variable key names
- public parent/created tweet IDs when relevant

## Status Interpretation

| Status | Common meaning |
| --- | --- |
| 400 | Variables, features, or field toggles do not match the current web client |
| 401/403 | Bad auth material, missing CSRF, expired session, challenge, or access restriction |
| 404 with empty body | Often stale query ID or invalid/missing transaction ID |
| 429 | Rate limited |
| 5xx | X-side service failure or transient edge failure |

Always inspect JSON `errors` when present; some GraphQL failures return HTTP 200.
