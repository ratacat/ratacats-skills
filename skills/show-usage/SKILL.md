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
| `ait` | `cargo install aitracker --locked` (needs Rust) | Codex OAuth, Gemini OAuth, others |
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
5h          0% used        10m
weekly     51% used        1h 0m
fable-weekly  95% used     1h 0m

Codex
7-day      44% used        2d 8h
5h-spark    0% used        4h 58m
7d-spark    0% used        6d 23h

Kimi Code
7-day       0% used        6d 23h
5-hour      1% used        3h 41m
```

Rules:
- Only subscriptions with live data get a header. Failed/absent ones are omitted (first run is the exception — report login state there).
- Column positions don't need to align perfectly; keep label, `% used`, reset time in that order.
- Reset times as `Nh Nm` / `Nd Nh`; omit seconds.
- Windows map: Claude `fable-weekly` from `aiquokka claude` ("Weekly Fable"); Z.ai 5-hour from `aiquokka zai` or `omp`; MiniMax interval + weekly from `mmx quota` (`100 - current_interval_remaining_percent`, `end_time`/`weekly_end_time` are epoch ms); Kimi/Codex/Grok/Antigravity from `omp usage` if present, else `ait`.
- `omp` provider names in output: Anthropic→Claude, Openai Codex→Codex, Kimi Code, Zai→Z.ai, Xai Oauth→Grok, Google Antigravity→Gemini (one daily line per model family: google/anthropic/openai).
- Qwen token-plan 5h/7d windows need the OMP cookie credential (`{"token":...,"cookie":...}` in `QWENPLAN_API_KEY`); without it omit Qwen or show only `qwencloud usage free-tier` windows that are `status: "valid"`.
- Exit after printing. No follow-up questions on non-first runs.
