# pro-cli Setup & Recovery

This skill drives GPT Pro through [`pro-cli`](https://github.com/ratacat/pro-cli). Use this flow whenever `pro-cli` is missing, not logged in, or failing. The agent can run the install and verification steps; the **user** completes the one-time browser login. Get the user's confirmation before installing software or taking temporary access to their browser.

## 1. Check health first (no Pro quota)

```sh
pro-cli doctor --json
```

- Command not found → `pro-cli` is not installed. Go to **Install**.
- Runs but reports auth/session problems → go to **Authenticate**.
- Reports healthy → setup is done; proceed with the loop.

Always use `doctor` for health checks. Never spend Pro quota on smoke-test `ask` calls.

## 2. Install

`pro-cli` is a Bun/TypeScript CLI and **requires [Bun](https://bun.sh)**.

```sh
curl -fsSL https://raw.githubusercontent.com/ratacat/pro-cli/main/scripts/install.sh | bash
```

The installer clones or fast-forwards `~/Projects/pro-cli`, runs `bun install` and `bun link`, and prints the version. It does not touch auth, cookies, or Chrome. If Bun is missing, install it first, then rerun.

Update an existing install:

```sh
pro-cli update --json
```

## 3. Authenticate

`pro-cli` needs one logged-in ChatGPT Chrome window; it sends requests from that tab over Chrome DevTools Protocol, on the user's own ChatGPT subscription. Pick one path — both end in the same local auth state.

### Path A — existing Chrome profile (lowest friction)

Use when the user is already logged in to ChatGPT in Chrome and trusts the agent with temporary local browser access. Set up auth from the existing profile, storing **only scoped ChatGPT/OpenAI auth** under `~/.pro-cli`, never printing raw cookies or tokens, then verify:

```sh
pro-cli doctor --json
```

### Path B — dedicated Chrome profile (separate, long-running)

```sh
pro-cli auth command --json                              # prints a Chrome launch command
# run that command, then sign in to ChatGPT in the window it opens
pro-cli auth capture --cdp http://127.0.0.1:9222 --json
pro-cli doctor --json
```

This creates `~/.pro-cli/chrome-profile`, keeping ChatGPT auth separate from the personal profile. Port `9222` is the default; if you use another, pass the same `--cdp`/`--port` to `doctor`, `ask`, and `job create`.

## 4. Keep it running

Keep the ChatGPT Chrome window open while jobs run.

- Chrome closed → rerun `pro-cli auth command --json`.
- ChatGPT logged out → sign in, then `pro-cli auth capture --cdp <url> --json`.
- Anything unclear → `pro-cli doctor --json`.

## Guardrails

- Confirm with the user before installing software or accessing their browser.
- Never store, print, or transmit raw cookies, tokens, `.env` files, or private keys. `pro-cli` keeps only scoped auth under `~/.pro-cli`.
- Re-run `pro-cli doctor --json` until it reports healthy before sending a review.
