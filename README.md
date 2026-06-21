# Ratacat's Skills

Claude and Codex skills authored or locally maintained by Ratacat.

This repository is a Claude marketplace-style collection. Each plugin lives in `plugins/<name>`, and `skills/<name>` is a GitHub-friendly skill page that symlinks back to the plugin source.

## Install

Skills here are installable two ways.

### Claude Code (plugin marketplace)

```sh
/plugin marketplace add ratacat/ratacats-skills
/plugin install <name>
```

### Any agent (skills.sh)

Works with Claude Code, Codex, Cursor, OpenCode, and [others](https://skills.sh).

```sh
npx skills add ratacat/ratacats-skills              # choose interactively
npx skills add ratacat/ratacats-skills --skill tdd  # install one skill
npx skills add ratacat/ratacats-skills --list       # list everything
```

Use the skill `name` from the table below as the `--skill` value (it matches the directory name).

## Skills

| Skill | Description |
| --- | --- |
| [`annas-archive-ebooks`](skills/annas-archive-ebooks/) | Use when needing to look up book content, find a book by title/author, download an ebook, or reference material from a published book. Triggers on book lookups, ebook downloads, "find the book", "get the PDF/EPUB of". Downloads produce PDF/EPUB/MOBI files - use ebook-extractor skill to convert to text. |
| [`ansi-art`](skills/ansi-art/) | Use when creating, reviewing, converting, or embedding terminal text art: ASCII art, ANSI art, CP437/code page 437 glyph art, block ASCII, BBS-style logos, CLI banners, NFOs, fixed-width art, or SAUCE/XBIN/BIN/ANS output. |
| [`clarify`](skills/clarify/) | Run a chained clarity review across a target repo, plan, or work items. Use when the user asks to clarify, defuzz, audit, review, harden, distill, de-duplicate, inspect naming, apply fresh eyes to recent code, or combine code review, plan refinement, deep-module architecture, DRY/cruft, and naming analysis into one reusable workflow. |
| [`conjecture-cascade`](skills/conjecture-cascade/) | Use when inspecting a software target for hidden bugs, dropped behavior, missing records, stale state, unclear failures, broad reliability risks, or likely issue classes across a bounded scope. |
| [`dianalokada`](skills/dianalokada/) | Become Diana. Ukrainian software engineer in NYC. KGB accent. Zero filter. Real corpus mode with full main tweets and top-ranked replies. Once invoked there is no going back. |
| [`duris-game-knowledge`](skills/duris-game-knowledge/) | Use whenever working on Duris MUD — connecting to the game, navigating, exploring, fighting, parsing game output, writing commands, understanding zones, combat mechanics, spellcasting, geography, equipment, mobs, recovery, or any other gameplay question. Load this skill for any task involving Duris. |
| [`duris-group-combat`](skills/duris-group-combat/) | Use when designing or operating Duris group combat with tanks, assists, assumed targets, caster memorization readiness, bash risk, tracking enemies, aggro adds, or command spam risk. |
| [`ebook-extractor`](skills/ebook-extractor/) | Use when user wants to extract text from ebooks (EPUB, MOBI, PDF). Use for converting ebooks to plain text for analysis, processing, or reading. Handles all common ebook formats. |
| [`failure-modes`](skills/failure-modes/) | Use when reviewing a codebase, uncommitted changes, recent agent work, or one subsystem for hidden bugs, flawed assumptions, drift, duplication, weak tests, broken contracts, or other failure modes. |
| [`gpt-pro-loop`](skills/gpt-pro-loop/) | Use when running a GPT Pro or pro-cli assisted project revision loop: build a context package, write a GPT Pro prompt, request adversarial review, map issues into a design map, run revision passes, verify locally, write goal assessments, and hand off the loop. |
| [`graph-researcher`](skills/graph-researcher/) | Deep web research with relevance scoring and knowledge graph storage. Use when researching topics, companies, people, or concepts. Performs Graph-of-Thoughts style exploration with parallel branching, relevance scoring, and synthesis into themed reports. |
| [`kalshi-prediction-market`](skills/kalshi-prediction-market/) | Context and working knowledge for Calci’s prediction-market domain, which is powered by Kalshi. Use this skill whenever the user asks about Calci prediction markets, Kalshi markets, tickers, order books, pricing, settlement, or the Kalshi API/WebSocket. |
| [`medium-paywall-bypass`](skills/medium-paywall-bypass/) | Use when user shares a Medium article URL behind a paywall and wants to read the full content. Also use for articles on Medium-hosted publications like towardsdatascience.com, betterprogramming.pub, levelup.gitconnected.com, etc. |
| [`name-review`](skills/name-review/) | Use when reviewing or designing names for plans, beads, work items, architecture docs, codebases, APIs, schemas, modules, states, or domain vocabulary where terminology drift, overloaded concepts, boundary ambiguity, or AI-confusing naming may exist. |
| [`pm-deep-analysis`](skills/pm-deep-analysis/) | Use when an agent needs price-blind deep research for a Polymarket or prediction-market event, market URL, event URL, market question set, or PMKNB situation, including fresh analysis, updating existing deep research, resolution mechanics, source discovery, and 0-100 likelihood estimates independent of market odds. |
| [`pm-market-analysis`](skills/pm-market-analysis/) | Use when Codex must analyze one prediction-market PM event for PMKNB: ingest subject/world research and market data, identify exact Polymarket or Kalshi instruments, assess market forces, resolution/oracle risk, liquidity, and platform/counterparty risk, then output a forecast, report, brief, proposal, or no-publish result. Triggers include prediction market, Polymarket, Kalshi, PM event, instrument identity, conditionId, token IDs, event_ticker, market ticker, YES/NO, PMKNB market_analysis, resolution risk, negative risk, or multi-market event analysis. |
| [`pm-research-methodologies`](skills/pm-research-methodologies/) | Manual-only. Never auto-load or auto-select this skill from task context. Load only when the user explicitly names pm-research-methodologies, or asks for the general research methodology framework, to structure deep research on a subject that has no dedicated methodology skill. |
| [`pm-situation-framing`](skills/pm-situation-framing/) | Use when the user or router explicitly names PM Situation Framing or pm-situation-framing to create or update a PMKNB situation frame. This skill is direct-invocation-only and must never be automatically loaded for general market, forecasting, research, or news-analysis requests. |
| [`polymarket-event-research`](skills/polymarket-event-research/) | Use when the user asks for price-blind research on the real-world resolution mechanics of a specific Polymarket or prediction-market event, including actors, institutions, legal/procedural paths, local context, source discovery, proof standards, structured research handoffs, or KNB world-mode mapping. Do not use for odds, prices, portfolios, trade decisions, market microstructure, or forecast/EV analysis. |
| [`tdd`](skills/tdd/) | Test-driven development with red-green-refactor loop. Use when user wants to build features or fix bugs using TDD, mentions "red-green-refactor", wants integration tests, or asks for test-first development. |
| [`writing-claude-skills`](skills/writing-claude-skills/) | Use when user asks to create, write, edit, or test a skill. Also use when documenting reusable techniques, patterns, or workflows for future Claude instances. |
| [`x-undocumented-api`](skills/x-undocumented-api/) | Manual-only skill. Never automatically load or select this skill from task context. Use only when the user explicitly asks to manually reference this skill or names `x-undocumented-api` / `x-api-skill`. |

## Layout

- `plugins/<name>/.claude-plugin/plugin.json` — plugin manifest.
- `plugins/<name>/skills/<name>/SKILL.md` — the canonical skill (Claude marketplace shape).
- `skills/<name>/README.md` — the GitHub-facing skill page (a real file).
- `skills/<name>/SKILL.md` and helper files — symlinks back to the plugin source.
- `.claude-plugin/marketplace.json` — registers every plugin.

Every skill must satisfy the gates in [AGENTS.md](AGENTS.md). The directory name, plugin name, marketplace name, and `SKILL.md` frontmatter `name` are kept identical so the skill installs under one stable handle.
