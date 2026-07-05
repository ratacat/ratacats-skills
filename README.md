# Ratacat's Skills

Agent skills I use every day, shared. A skill is a folder with a `SKILL.md` — instructions an AI coding agent (Claude Code, Codex, Cursor, OpenCode, …) loads when the task calls for it, plus whatever reference docs and scripts the workflow needs. Install one and your agent picks up the workflow automatically; no prompting ceremony.

The collection leans toward evidence-first engineering (bug hunts, reviews, naming), prediction-market research, and a few sharp tools. Each skill's folder has a README explaining what it does and when to reach for it — click through the table below.

## Install

Every skill installs two ways. Pick whichever fits your setup:

### Claude Code (plugin marketplace)

```sh
/plugin marketplace add ratacat/ratacats-skills
/plugin install <name>@ratacats-skills
```

### Any agent (skills.sh)

Works with Claude Code, Codex, Cursor, OpenCode, and [others](https://skills.sh).

```sh
npx skills add ratacat/ratacats-skills              # choose interactively
npx skills add ratacat/ratacats-skills --skill conjecture-cascade  # install one skill
npx skills add ratacat/ratacats-skills --list       # list everything
```

Use the skill `name` from the table below as the `--skill` value (it matches the directory name).

## Skills

<!-- skills:start -->
### Developer Tools

| Skill | What it does |
| --- | --- |
| [`clarify`](skills/clarify/) | Turns fuzzy repos, plans, diffs, or issue sets into clearer findings, fixes, names, and acceptance criteria using an evidence-first review chain. |
| [`ebook-extractor`](skills/ebook-extractor/) | Extract plain text from EPUB, MOBI, and PDF files with local Python tools so agents can search, quote, or analyze book content. |
| [`failure-modes`](skills/failure-modes/) | A systematic code-review checklist for finding hidden bugs, stale contracts, weak tests, drift, duplication, and quiet failure paths. |
| [`gpt-pro-loop`](skills/gpt-pro-loop/) | Run a local revision loop that packages project context for GPT Pro review, maps critiques into issues, verifies fixes, and assesses the goal. |
| [`medium-paywall-bypass`](skills/medium-paywall-bypass/) | Fetch readable Medium or Medium-hosted article text through mirror routes so an agent can summarize, compare, or discuss the content. |
| [`name-review`](skills/name-review/) | Boundary-first naming review that maps concepts before recommending small, evidence-backed renames for code, plans, schemas, and docs. |
| [`writing-claude-skills`](skills/writing-claude-skills/) | TDD-style skill authoring guide that turns repeatable workflows into focused, tested Claude/Codex skills with clear triggers and resources. |
| [`x-undocumented-api`](skills/x-undocumented-api/) | Safe guide to X.com's private web API: verifies current GraphQL operations, request headers, cursors, and secret-safe evidence. |

### Prediction Markets

| Skill | What it does |
| --- | --- |
| [`kalshi-prediction-market`](skills/kalshi-prediction-market/) | A Kalshi domain primer for understanding series, events, markets, Yes/No pricing, settlement, order books, and API or WebSocket data. |
| [`pm-deep-analysis`](skills/pm-deep-analysis/) | Price-blind prediction-market research: builds evidence-first world reports and 0-100 resolution estimates without using odds or prices. |
| [`pm-market-analysis`](skills/pm-market-analysis/) | Market-aware prediction-market analysis that verifies exact instruments, rules, liquidity, and risks before producing a forecast, report, or no-publish call. |
| [`pm-research-methodologies`](skills/pm-research-methodologies/) | General deep-research scaffold that turns a broad subject into named nodes, sourced claims, provenance checks, synthesis, and open questions. |
| [`pm-situation-framing`](skills/pm-situation-framing/) | Reusable PMKNB situation frame: separates facts from hypotheses, maps actors, gates, clocks, cruxes, observables, and update rules. |
| [`polymarket-event-research`](skills/polymarket-event-research/) | Price-blind event-resolution research that maps people, offices, procedures, deadlines, and proof sources behind a Polymarket-style outcome. |

### Tools

| Skill | What it does |
| --- | --- |
| [`annas-archive-ebooks`](skills/annas-archive-ebooks/) | Finds book records, checks editions and formats, and uses a local Anna's Archive script to download ebooks when a membership key is available. |
| [`conjecture-cascade`](skills/conjecture-cascade/) | Directional thinking engine: fires batches of probes through any bounded target — code, claims, plans, or ideas — and closes each probe with evidence or yield. |
| [`graph-researcher`](skills/graph-researcher/) | Deep web research that stores sources, findings, relationships, contradictions, and open leads in a SQLite knowledge graph. |

### Writing

| Skill | What it does |
| --- | --- |
| [`dianalokada`](skills/dianalokada/) | Switches the agent into Diana's sharp, blunt social voice, grounded in a real tweet corpus for posts, replies, roasts, and punchy takes. |

### Games

| Skill | What it does |
| --- | --- |
| [`duris-game-knowledge`](skills/duris-game-knowledge/) | Gives practical Duris MUD knowledge for navigation, combat, spells, gear, recovery, and parsing live game output without inventing commands. |
| [`duris-group-combat`](skills/duris-group-combat/) | Models Duris group fights around roles, assists, caster readiness, adds, flee risk, and survival-first command pacing. |

### Art

| Skill | What it does |
| --- | --- |
| [`ansi-art`](skills/ansi-art/) | Guides terminal-safe CP437/ANSI art from first sketch to validated fixed-width output, with glyph, palette, format, and rendering references. |
<!-- skills:end -->

## How this repo works

- `skills/<name>/SKILL.md` — the skill itself: frontmatter (name, trigger description, metadata) plus the workflow the agent follows.
- `skills/<name>/README.md` — the human-facing page: what it does, when to use it, how to install it.
- `skills/<name>/...` — reference docs and scripts the skill uses.
- `.claude-plugin/marketplace.json` and the skills table above are **generated** from skill frontmatter by `bun scripts/sync.ts` — edit the skill, run sync, never hand-edit the generated parts. CI fails if they drift.

No `plugins/` tree, no symlinks: what you browse is exactly what installs. Contributor gates live in [AGENTS.md](AGENTS.md); one stable handle per skill — directory name, frontmatter `name`, and install name are always identical.

## License

[MIT](LICENSE).
