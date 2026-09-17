---
name: show-usage
description: "Show rate-limit and quota usage across the user's AI coding subscriptions (Claude, Codex, Gemini, Kimi, MiniMax, Z.ai, Qwen, Grok) with per-window percent used and time to reset. Use when the user asks about usage, quotas, rate limits, or when subscriptions reset."
metadata:
  category: tools
  blurb: "Reads live quota windows across AI coding subscriptions and prints percent used and time to reset in a minimal fixed format."
  keywords:
    - usage
    - quota
    - rate-limit
    - subscriptions
    - claude
    - codex
    - kimi
    - minimax
    - zai
    - qwen
---

# Show Usage

Report the user's AI subscription quota windows in one fixed format. First run sets up tooling and confirms the provider list; later runs just print.

## Tools

Install any that are missing (skip silently if present):

| Tool | Install | Reads |
| --- | --- | --- |
| `ait` | `cargo install aitracker --locked` (needs Rust) | Codex CLI login (`~/.codex/auth.json` — may be a different account than omp's), Gemini OAuth, others |
| `aiquokka` | `go install github.com/McKean/aiquokka@latest` (needs Go; binary at `~/go/bin/aiquokka`) | Claude 5h/weekly/fable, Kimi (`KIMI_API_KEY`), Z.ai (`ZAI_API_KEY`) |
| `mmx` | `npm install -g mmx-cli` | MiniMax (`mmx quota --api-key "$MINIMAX_API_KEY" --output json`) |
| `qwencloud` | `npm install -g @qwencloud/qwencloud-cli` | Qwen free tier / plans (needs `qwencloud auth login` once) |
| `omp` | never install — use only if already on PATH | Kimi, Codex, Z.ai, Antigravity, Grok in one call (`omp usage`) |

Env vars: `KIMI_API_KEY`, `MINIMAX_API_KEY`, `ZAI_API_KEY`. `ait` names differ (`KIMI_TOKEN`, `MINIMAX_API_TOKEN`, `Z_AI_API_KEY`) — alias inline when calling it.

## First run

1. Install missing tools.
2. Run the collectors, show which subscriptions are logged in / have working credentials, and which failed (bad key, needs login, no plan).
3. Ask the user: any other subscriptions to include, and whether the detected set is right.
4. Record the confirmed list in `~/.config/show-usage/providers` (one provider per line) so later runs don't ask.

## Every run

Fetch fresh data, then print exactly this format — one header per subscription the user actually has, one line per quota window, percent used and time to reset. No tables, no parentheses, no notes, no cost data, no extra blank commentary:

```
Claude
  5h                  0% used   10m
  weekly             51% used   1h 0m
  fable-weekly       95% used   1h 0m

Codex (cheshire)
  7-day              44% used   2d 8h
  5h-spark            0% used   4h 58m
  7d-spark            0% used   6d 23h

Kimi Code
  7-day               0% used   6d 23h
  5-hour              1% used   3h 41m
```

Rules:
- Only subscriptions with live data get a header. Failed/absent ones are omitted (first run is the exception — report login state there).
- Spacing: 2-space indent, label padded right to 18 chars, percent right-aligned in 3 chars, ` % used`, 3 spaces, then reset time. No reset time → end the line after `% used`.
- Reset times as `Nh Nm` / `Nd Nh` with the space; omit seconds. `omp usage` prints compact `2d6h` — normalize to `2d 6h`.
- Claude at 0% used returns no reset timestamp (window clock starts on first use) — print those lines without a time.
- Windows map: Claude `fable-weekly` from `aiquokka claude` ("Weekly Fable"); Z.ai 5-hour from `aiquokka zai` or `omp`; MiniMax interval + weekly from `mmx quota` (`100 - current_interval_remaining_percent`, `end_time`/`weekly_end_time` are epoch ms); Kimi/Grok/Antigravity from `omp usage` if present, else `ait`; Codex from `ait usage --json`, once per `~/.codex*` dir containing `auth.json` (discover with a glob, don't hardcode; set `CODEX_HOME=<dir>` per call — the `codex1`/`codex2` shell aliases are interactive-zsh only and invisible to scripts and agents). omp's stored Codex credentials are access-token-only and die on expiry — `omp usage` Codex is fallback only.
- MiniMax interval windows are rolling and variable-length (observed 5h and 4h on consecutive runs) — label from the actual window duration (`general-4h`), never hardcode `5h`. `mmx` prints a `Detecting region...` line before the JSON — parse from the first `{`.
- `ait` Codex: label windows by `window_minutes` (300 → `5h`, 10080 → `7-day`); its display names are unreliable.
- `omp` provider names in output: Anthropic→Claude, Openai Codex→Codex, Kimi Code, Zai→Z.ai, Xai Oauth→Grok, Google Antigravity→Gemini (one daily line per model family: google/anthropic/openai).
- Qwen: no installed tool fetches token-plan 5h/7d windows (`QWENPLAN_API_KEY` is not read by any tool; `qwencloud subscription` returns empty for API-key-only accounts). Print one `free-tier` line: max `used_pct` across `qwencloud usage free-tier` models with `status: "valid"`, soonest `resetDate`.
- Exit after printing. No follow-up questions on non-first runs.

## Accuracy

Collectors read different credentials for the same provider, and those can be different accounts. `omp usage` reports only omp's own auth store; `ait` reads CLI auth dirs (`~/.codex`); env keys are a third identity. Same email displayed ≠ same data source. Verify before printing:

- The same window from two sources must agree within a few points AND share the same absolute reset instant. A mismatch means a different account, stale cache, or different bucket — investigate, don't silently pick one.
- Two live accounts for one provider → one header per account (`Codex (cheshire)`, `Codex (neuralsplash)`). Never merge or average across identities.
- Prefer the provider's own usage endpoint (first-party OAuth/CLI credential) over aggregator estimates.
- If a collector can't name the account it read (e.g. `ait` shows null identity), resolve the identity (decode the token, check the auth file) before trusting its numbers.
- Codex refresh tokens are single-use rotating: two tools writing to the same `auth.json` break both logins (`refresh_token_reused`). One `CODEX_HOME` dir per account, and never share a dir between tools that both refresh.
