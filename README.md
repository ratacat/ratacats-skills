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
| [`crystallize`](skills/crystallize/) | Finds repeated agent work that can be removed or turned into reusable procedures, with evidence, exception conditions, and a small first change. |
| [`ebook-extractor`](skills/ebook-extractor/) | Extract plain text from EPUB, MOBI, and PDF files with local Python tools so agents can search, quote, or analyze book content. |
| [`failure-modes`](skills/failure-modes/) | A systematic code-review checklist for finding hidden bugs, stale contracts, weak tests, drift, duplication, and quiet failure paths. |
| [`gpt-pro-loop`](skills/gpt-pro-loop/) | Run a local revision loop that packages project context for GPT Pro review, maps critiques into issues, verifies fixes, and assesses the goal. |
| [`jev`](skills/jev/) | Builds features on TypeSafe's Jev model — typed Choice/Score/Noul judgments with calibrated probabilities that code branches on directly, no text parsing. |
| [`medium-paywall-bypass`](skills/medium-paywall-bypass/) | Fetch readable Medium or Medium-hosted article text through mirror routes so an agent can summarize, compare, or discuss the content. |
| [`name-review`](skills/name-review/) | Boundary-first naming review that maps concepts before recommending small, evidence-backed renames for code, plans, schemas, and docs. |
| [`no-process-porn`](skills/no-process-porn/) | Detects when agent process is substituting for delivery and redirects the work into the smallest concrete next action. |
| [`refine-tests`](skills/refine-tests/) | A methodical test-suite audit that finds tautological, vacuous, weak, brittle, mislabeled, and missing tests, then strengthens them without ever reducing coverage. |
| [`writing-claude-skills`](skills/writing-claude-skills/) | TDD-style skill authoring guide that turns repeatable workflows into focused, tested Claude/Codex skills with clear triggers and resources. |
| [`x-undocumented-api`](skills/x-undocumented-api/) | Safe guide to X.com's private web API: verifies current GraphQL operations, request headers, cursors, and secret-safe evidence. |

### Prediction Markets

| Skill | What it does |
| --- | --- |
| [`kalshi-prediction-market`](skills/kalshi-prediction-market/) | A Kalshi domain primer for understanding series, events, markets, Yes/No pricing, settlement, order books, and API or WebSocket data. |
| [`pm-deep-analysis`](skills/pm-deep-analysis/) | Price-blind prediction-market research: builds evidence-first world reports and calibrated 0-100 resolution estimates without using odds or prices. |
| [`pm-market-analysis`](skills/pm-market-analysis/) | Market-aware prediction-market analysis that verifies exact instruments, rules, liquidity, and risks before producing a forecast, report, or no-publish call. |
| [`pm-research-methodologies`](skills/pm-research-methodologies/) | General deep-research scaffold that turns a broad subject into named nodes, sourced claims, provenance checks, synthesis, and open questions. |
| [`pm-situation-framing`](skills/pm-situation-framing/) | Reusable PMKNB situation frame: separates facts from hypotheses, maps actors, gates, clocks, cruxes, observables, and update rules. |

### Tools

| Skill | What it does |
| --- | --- |
| [`annas-archive-ebooks`](skills/annas-archive-ebooks/) | Finds book records, checks editions and formats, and uses a local Anna's Archive script to download ebooks when a membership key is available. |
| [`conjecture-cascade`](skills/conjecture-cascade/) | Directional thinking engine: fires batches of probes through any bounded target — code, claims, plans, or ideas — and closes each probe with evidence or yield. |
| [`graph-researcher`](skills/graph-researcher/) | Deep web research that stores sources, findings, relationships, contradictions, and open leads in a SQLite knowledge graph. |
| [`ml-learning-methods`](skills/ml-learning-methods/) | Explains how machine-learning methods work, how they relate, and when to choose them, with a detailed BERT-to-MAE guide and cited research chapters. |
| [`prediction-drill`](skills/prediction-drill/) | Vertical two-phase falsification loop for a single bug: rounds of five cheap-to-check predictions drill down to the root cause, then drill back up to a validated fix. |
| [`probe-driven-design`](skills/probe-driven-design/) | Use the smallest useful probe to ground consequential decisions before uncertain detail hardens into design. |
| [`show-usage`](skills/show-usage/) | Reads live quota windows across AI coding subscriptions and prints percent used and time to reset in a minimal fixed format. |

### Writing

| Skill | What it does |
| --- | --- |
| [`dianalokada`](skills/dianalokada/) | Switches the agent into Diana's sharp, blunt social voice, grounded in a real tweet corpus for posts, replies, roasts, and punchy takes. |
| [`julian-writing`](skills/julian-writing/) | Julian Shapiro's Writing Well handbook condensed into a working method: novelty times resonance, hook-first intros, bad first drafts, and rewriting until a reader effortlessly reaches the end. |
| [`remove-ai-sins`](skills/remove-ai-sins/) | Idempotent pass that removes seven prose sins (antithesis frame, named feelings, glossed images, inflated register, moral endings, tied-off questions, meta overload) and otherwise leaves the draft alone. |

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
