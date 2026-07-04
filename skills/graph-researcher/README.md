# Graph Researcher

This skill is for research that should build up over time instead of disappearing into one long answer.

Use it when the agent needs to research a topic, person, company, technology, or question across multiple branches. It records search queries, sources, findings, relationships, contradictions, entities, and open leads in a SQLite knowledge-graph workflow backed by [schema.sql](schema.sql).

Normal research can become a pile of tabs. This skill turns it into a map: what supports what, what conflicts, what is still open, and where to dig next.

Good fits:

- Multi-angle web research
- Comparing claims across sources
- Tracking unresolved questions
- Building a reusable knowledge base
- Producing a final report from evidence

Do not use it for quick factual lookups. It is heavier than that. Use it when the topic deserves a bench with labeled parts, not a sticky note.

## Install

```sh
# skills.sh CLI — Claude Code, Codex, Cursor, OpenCode, and more
npx skills add ratacat/ratacats-skills --skill graph-researcher

# or the Claude plugin marketplace
/plugin marketplace add ratacat/ratacats-skills
/plugin install graph-researcher@ratacats-skills
```

## Requirements

Requires SQLite. Before research begins, initialize the research database with the skill schema:

```sh
sqlite3 research.db < schema.sql
```

The schema creates sessions, findings, relationships, explored URLs, search queries, entities, and summary views for the research graph.
