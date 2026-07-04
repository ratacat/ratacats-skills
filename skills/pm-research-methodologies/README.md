# PM Research Methodologies

This skill is a general-purpose framework for structuring deep research on a subject that has no dedicated methodology skill of its own.

It helps an agent build a named-entity scaffold, research along that scaffold, judge each source's chain of knowing, and synthesize the result into an explanation of why the subject is like this and how it became like this. The output preserves sourced claims, provenance judgments, contradictions, dark nodes, and open questions for future runs.

Note: this skill is manual-only. Load it only when you explicitly name `pm-research-methodologies`, or when you ask for the general research methodology framework for a subject with no dedicated playbook. Family role: for prediction-market events, prefer `pm-situation-framing` → `pm-deep-analysis` or `polymarket-event-research` → `pm-market-analysis`; use this skill only as the fallback research methodology.

Good fits:

- Structuring research on a subject with no existing playbook
- Turning a broad topic into named people, places, organizations, records, and histories
- Recording sourced claims with provenance-chain judgments
- Synthesizing why something works the way it does, not just what happened
- Leaving specific open questions for the next bounded research run

## Install

```sh
# skills.sh CLI — Claude Code, Codex, Cursor, OpenCode, and more
npx skills add ratacat/ratacats-skills --skill pm-research-methodologies

# or the Claude plugin marketplace
/plugin marketplace add ratacat/ratacats-skills
/plugin install pm-research-methodologies@ratacats-skills
```
