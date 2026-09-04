# Show Usage

One command, all your AI coding subscriptions: which quota windows you're burning (5-hour, weekly, monthly), percent used, and time until reset.

Covers Claude (including the Fable weekly sub-pool), OpenAI Codex, Gemini/Antigravity, Kimi Code, MiniMax, Z.ai, Qwen, and Grok — only showing subscriptions you actually have.

Good fits:

- "How much quota do I have left?"
- "When does my Kimi weekly reset?"
- Pre-flight check before a long agent run

## How it works

Installs small read-only CLIs on first run (`ait`, `aiquokka`, `mmx`, `qwencloud`) and reuses credentials your official coding CLIs already store. Never installs `omp` — uses it only if you already have it. First run shows what's logged in and asks you to confirm the provider set; after that it just prints.

## Requirements

- Rust (`cargo`), Go, and Node/npm for the respective installers
- Existing logins or env keys: `KIMI_API_KEY`, `MINIMAX_API_KEY`, `ZAI_API_KEY`; Claude/Z.ai/Kimi OAuth credentials are auto-discovered from their CLIs
- Qwen needs a one-time `qwencloud auth login`

## Output

```
Claude
5h             0% used   10m
weekly        51% used   1h 0m
fable-weekly  95% used   1h 0m
```

## Install

```sh
# skills.sh CLI — Claude Code, Codex, Cursor, OpenCode, and more
npx skills add ratacat/ratacats-skills --skill show-usage

# or the Claude plugin marketplace
/plugin marketplace add ratacat/ratacats-skills
/plugin install show-usage@ratacats-skills
```
