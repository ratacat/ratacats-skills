# Ratacat's Skills

Claude and Codex skills authored or locally maintained by Ratacat.

This repository is a Claude marketplace-style collection. Each plugin lives in `plugins/<name>`, and `skills/<name>` is a GitHub-friendly skill page with links back to the plugin source.

## Skills

| Skill | Description |
| --- | --- |
| [`annas-archive-ebooks`](skills/annas-archive-ebooks/) | Use when needing to look up book content, find a book by title/author, download an ebook, or reference material from a published book. Triggers on book lookups, ebook downloads,... |
| [`ansi-art`](skills/ansi-art/) | Use when creating, reviewing, converting, or embedding terminal text art: ASCII art, ANSI art, CP437/code page 437 glyph art, block ASCII, BBS-style logos, CLI banners, NFOs, fixed-width art, or SAUCE/XBIN/BIN/ANS output. |
| [`clarify`](skills/clarify/) | Run a chained clarity review across a target repo, plan, or work items. Use when the user asks to clarify, defuzz, audit, review, harden, distill, de-duplicate, inspect naming, ... |
| [`conjecture-cascade`](skills/conjecture-cascade/) | Use when inspecting a software target for hidden bugs, dropped behavior, missing records, stale state, unclear failures, broad reliability risks, or likely issue classes across a bounded scope. |
| [`dianalokada`](skills/dianalokada/) | Become Diana. Ukrainian software engineer in NYC. KGB accent. Zero filter. Real corpus mode with full main tweets and top-ranked replies. Once invoked there is no going back. |
| [`duris-game-knowledge`](skills/duris-game-knowledge/) | Use whenever working on Duris MUD — connecting to the game, navigating, exploring, fighting, parsing game output, writing commands, understanding zones, combat mechanics, spellc... |
| [`duris-group-combat`](skills/duris-group-combat/) | Use when designing or operating Duris group combat with tanks, assists, assumed targets, caster memorization readiness, bash risk, tracking enemies, aggro adds, or command spam ... |
| [`ebook-extractor`](skills/ebook-extractor/) | Use when user wants to extract text from ebooks (EPUB, MOBI, PDF). Use for converting ebooks to plain text for analysis, processing, or reading. Handles all common ebook formats. |
| [`failure-modes`](skills/failure-modes/) | Use when reviewing a codebase, uncommitted changes, recent agent work, or one subsystem for hidden bugs, flawed assumptions, drift, duplication, weak tests, broken contracts, or... |
| [`graph-researcher`](skills/graph-researcher/) | Deep web research with relevance scoring and knowledge graph storage. Use when researching topics, companies, people, or concepts. Performs Graph-of-Thoughts style exploration w... |
| [`kalshi-prediction-market`](skills/kalshi-prediction-market/) | Context and working knowledge for Calci’s prediction-market domain, which is powered by Kalshi. Use this skill whenever the user asks about Calci prediction markets, Kalshi mark... |
| [`medium-paywall-bypass`](skills/medium-paywall-bypass/) | Use when user shares a Medium article URL behind a paywall and wants to read the full content. Also use for articles on Medium-hosted publications like towardsdatascience.com, b... |
| [`name-review`](skills/name-review/) | Use when reviewing or designing names for plans, beads, work items, architecture docs, codebases, APIs, schemas, modules, states, or domain vocabulary where terminology drift, o... |
| [`pm-deep-analysis`](skills/pm-deep-analysis/) | Use when an agent needs price-blind deep research for a Polymarket or prediction-market event, market URL, event URL, market question set, or PMKNB situation, including fresh an... |
| [`pm-market-analysis`](skills/pm-market-analysis/) | Use when Codex must analyze one prediction-market PM event for PMKNB: ingest subject/world research and market data, identify exact Polymarket or Kalshi instruments, assess mark... |
| [`pm-mispricing-analysis`](skills/pm-mispricing-analysis/) | Use when an agent needs a bounded market-aware scan of one Polymarket or prediction-market event to fetch current prices, do quick subject research, estimate resolution likeliho... |
| [`PM Situation Framing`](skills/pm-situation-framing/) | Use when explicitly invoked to create or update a PMKNB situation frame. Direct-invocation-only; not a general market-analysis trigger. |
| [`polymarket-event-research`](skills/polymarket-event-research/) | Use when the user asks for price-blind research on the real-world resolution mechanics of a specific Polymarket or prediction-market event, including actors, institutions, legal... |
| [`tdd`](skills/tdd/) | Test-driven development with red-green-refactor loop. Use when user wants to build features or fix bugs using TDD, mentions "red-green-refactor", wants integration tests, or ask... |
| [`writing-claude-skills`](skills/writing-claude-skills/) | Use when user asks to create, write, edit, or test a skill. Also use when documenting reusable techniques, patterns, or workflows for future Claude instances. |
| [`x-undocumented-api`](skills/x-undocumented-api/) | Manual-only skill. Never automatically load or select this skill from task context. Use only when the user explicitly asks to manually reference this skill or names `x-undocumen... |

## Local Layout

- `plugins/<name>/skills/<name>/SKILL.md` is the Claude marketplace plugin shape.
- `skills/<name>/README.md` is the GitHub-facing skill page.
- `skills/<name>/SKILL.md` and helper files point back to the marketplace plugin source.
- The local `agent-skills` collection links these skills back from this repo so existing agents can keep using them.
