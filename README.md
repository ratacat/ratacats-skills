# Ratacat's Skills

Claude and Codex skills authored or locally maintained by Ratacat.

This repository is a Claude marketplace-style collection. Each plugin lives in `plugins/<name>`, and `skills/<name>` is a compatibility symlink for direct Claude/Codex skill roots.

## Skills

| Skill | Description |
| --- | --- |
| `agent-browser` | Browser automation using Vercel's agent-browser CLI. Use when you need to interact with web pages, fill forms, take screenshots, or scrape data. Alternative to Playwright MCP - ... |
| `annas-archive-ebooks` | Use when needing to look up book content, find a book by title/author, download an ebook, or reference material from a published book. Triggers on book lookups, ebook downloads,... |
| `beautiful-mermaid-ascii` | Render Mermaid diagrams as readable ASCII/Unicode art in the terminal (from .mmd/.mermaid files, stdin, or Markdown ```mermaid fences). Use when installing or using lukilabs/bea... |
| `brave-search` | Use when user asks to search the web, look something up online, find current/recent/latest information, or needs cited answers. Triggers on "search", "look up", "find out about"... |
| `caveman` | > Ultra-compressed communication mode. Cuts token usage ~75% by dropping filler, articles, and pleasantries while keeping full technical accuracy. Use when user says "caveman mo... |
| `clarify` | Run a chained clarity review across a target repo, plan, or work items. Use when the user asks to clarify, defuzz, audit, review, harden, distill, de-duplicate, inspect naming, ... |
| `data-systems-architecture` | Use when designing databases for data-heavy applications, making schema decisions for performance, choosing between normalization and denormalization, selecting storage/indexing... |
| `debugging` | Systematic debugging that identifies root causes rather than treating symptoms. Uses sequential thinking for complex analysis, web search for research, and structured investigat... |
| `deepen-plan` | Enhance a plan with parallel research agents for each section to add depth, best practices, and implementation details |
| `design-patterns` | Use when designing software architecture, refactoring code structure, solving recurring design problems, or when code exhibits symptoms like tight coupling, rigid hierarchies, s... |
| `diagnose` | Disciplined diagnosis loop for hard bugs and performance regressions. Reproduce → minimise → hypothesise → instrument → fix → regression-test. Use when user says "diagnose this"... |
| `dianalokada` | Become Diana. Ukrainian software engineer in NYC. KGB accent. Zero filter. Real corpus mode with full main tweets and top-ranked replies. Once invoked there is no going back. |
| `duris-game-knowledge` | Use whenever working on Duris MUD — connecting to the game, navigating, exploring, fighting, parsing game output, writing commands, understanding zones, combat mechanics, spellc... |
| `duris-group-combat` | Use when designing or operating Duris group combat with tanks, assists, assumed targets, caster memorization readiness, bash risk, tracking enemies, aggro adds, or command spam ... |
| `ebook-extractor` | Use when user wants to extract text from ebooks (EPUB, MOBI, PDF). Use for converting ebooks to plain text for analysis, processing, or reading. Handles all common ebook formats. |
| `failure-modes` | Use when reviewing a codebase, uncommitted changes, recent agent work, or one subsystem for hidden bugs, flawed assumptions, drift, duplication, weak tests, broken contracts, or... |
| `frontend-design` | This skill should be used when creating distinctive, production-grade frontend interfaces with high design quality. It applies when the user asks to build web components, pages,... |
| `graph-researcher` | Deep web research with relevance scoring and knowledge graph storage. Use when researching topics, companies, people, or concepts. Performs Graph-of-Thoughts style exploration w... |
| `grill-me` | Interview the user relentlessly about a plan or design until reaching shared understanding, resolving each branch of the decision tree. Use when user wants to stress-test a plan... |
| `grill-with-docs` | Grilling session that challenges your plan against the existing domain model, sharpens terminology, and updates documentation (CONTEXT.md, ADRs) inline as decisions crystallise.... |
| `human-tweet-editor` | Grade, critique, rewrite, and strengthen tweets or X threads in a natural human voice for tech, AI, developer, startup, product, and builder audiences. Use when Codex is asked t... |
| `improve-codebase-architecture` | Find deepening opportunities in a codebase, informed by the domain language in CONTEXT.md and the decisions in docs/adr/. Use when the user wants to improve architecture, find r... |
| `kalshi-prediction-market` | Context and working knowledge for Calci’s prediction-market domain, which is powered by Kalshi. Use this skill whenever the user asks about Calci prediction markets, Kalshi mark... |
| `medium-paywall-bypass` | Use when user shares a Medium article URL behind a paywall and wants to read the full content. Also use for articles on Medium-hosted publications like towardsdatascience.com, b... |
| `name-review` | Use when reviewing or designing names for plans, beads, work items, architecture docs, codebases, APIs, schemas, modules, states, or domain vocabulary where terminology drift, o... |
| `pm-deep-analysis` | Use when an agent needs price-blind deep research for a Polymarket or prediction-market event, market URL, event URL, market question set, or PMKNB situation, including fresh an... |
| `pm-market-analysis` | Use when Codex must analyze one prediction-market PM event for PMKNB: ingest subject/world research and market data, identify exact Polymarket or Kalshi instruments, assess mark... |
| `pm-mispricing-analysis` | Use when an agent needs a bounded market-aware scan of one Polymarket or prediction-market event to fetch current prices, do quick subject research, estimate resolution likeliho... |
| `pm-situation-framing` | Use when the user or router explicitly names pm-situation-framing to create or update a PMKNB situation frame. This skill is direct-invocation-only and must never be automatical... |
| `polymarket-event-research` | Use when the user asks for price-blind research on the real-world resolution mechanics of a specific Polymarket or prediction-market event, including actors, institutions, legal... |
| `postgres-query-expert` | A comprehensive guide for interacting with PostgreSQL 16 databases. Use this skill for constructing standard and advanced SQL queries, optimizing performance, debugging errors, ... |
| `process-research` | Use when working in the Polymarket research repo and you need to process queued targets from spinal_cord.jsonl, especially for batch queue runs or periodic research sweeps. |
| `run-simulations` | Use BEFORE and AFTER running trading engine simulations. Helps with: (1) SETUP - choosing configs, selecting segments via segment collections, batch sizing (recommend 2,000-3,00... |
| `senior-architect` | This skill should be used when the user asks to "design system architecture", "evaluate microservices vs monolith", "create architecture diagrams", "analyze dependencies", "choo... |
| `setup-matt-pocock-skills` | Sets up an `## Agent skills` block in AGENTS.md/CLAUDE.md and `docs/agents/` so the engineering skills know this repo's issue tracker (GitHub or local markdown), triage label vo... |
| `spec-flow-analyzer` | Use this agent when you have a specification, plan, feature description, or technical document that needs user flow analysis and gap identification. This agent should be used pr... |
| `systematic-debugging` | Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes |
| `tdd` | Test-driven development with red-green-refactor loop. Use when user wants to build features or fix bugs using TDD, mentions "red-green-refactor", wants integration tests, or ask... |
| `to-issues` | Break a plan, spec, or PRD into independently-grabbable issues on the project issue tracker using tracer-bullet vertical slices. Use when user wants to convert a plan into issue... |
| `to-prd` | Turn the current conversation context into a PRD and publish it to the project issue tracker. Use when user wants to create a PRD from the current context. |
| `triage` | Triage issues through a state machine driven by triage roles. Use when user wants to create an issue, triage issues, review incoming bugs or feature requests, prepare issues for... |
| `twitter` | Write viral, persuasive, engaging tweets and threads. Uses web research to find viral examples in your niche, then models writing based on proven formulas and X algorithm optimi... |
| `writing-claude-skills` | Use when user asks to create, write, edit, or test a skill. Also use when documenting reusable techniques, patterns, or workflows for future Claude instances. |
| `writing-documentation` | Produces concise, clear documentation by applying Elements of Style principles. Use when writing or improving any technical documentation (READMEs, guides, API docs, architectur... |
| `x-undocumented-api` | Manual-only skill. Never automatically load or select this skill from task context. Use only when the user explicitly asks to manually reference this skill or names `x-undocumen... |
| `zoom-out` | Tell the agent to zoom out and give broader context or a higher-level perspective. Use when you're unfamiliar with a section of code or need to understand how it fits into the b... |

## Local Layout

- `plugins/<name>/skills/<name>/SKILL.md` is the Claude marketplace plugin shape.
- `skills/<name>` points at the same skill for agent skill roots.
- The local `agent-skills` collection links these skills back from this repo so existing agents can keep using them.
