# PM Research Methodologies

This skill is a general-purpose framework for structuring deep research on a subject that has no dedicated methodology skill of its own.

It helps an agent root the question (resolution context, key assumptions, base rate), build a scaffold of searchable keys, research node by node into a claim ledger, judge each load-bearing source's chain of knowing, and synthesize an explanation of why the subject is like this and how it became like this. The output preserves sourced claims with origins and confidence, contradictions, dark nodes, and open questions that seed the next run.

Note: this skill is manual-only. Load it only when you explicitly name `pm-research-methodologies`, or when you ask for the general research methodology framework for a subject with no dedicated playbook. Family role: when a dedicated skill covers the domain (`pm-situation-framing`, `pm-deep-analysis`, `pm-market-analysis`; where installed, `middle-east-research` and the `pmw-*` weather family), follow it and use this skill only as the fallback methodology that fills its gaps.

Good fits:

- Structuring research on a subject with no existing playbook
- Turning a broad topic into searchable keys: named people, places, organizations, records, dockets, data series, terms of art
- Recording sourced claims in a ledger with origin tracing and confidence tags
- Synthesizing why something works the way it does, not just what happened
- Leaving signals to watch and open questions for the next bounded run

## Install

```sh
# skills.sh CLI — Claude Code, Codex, Cursor, OpenCode, and more
npx skills add ratacat/ratacats-skills --skill pm-research-methodologies

# or the Claude plugin marketplace
/plugin marketplace add ratacat/ratacats-skills
/plugin install pm-research-methodologies@ratacats-skills
```
