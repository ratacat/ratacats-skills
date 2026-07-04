# Clarify

This skill turns fuzzy work into crisp work. It helps when a plan, code change, issue set, or repo feels close but not solid enough to implement or trust.

Clarify runs a chained review: frame the target, inspect evidence, review likely correctness failures, defuzz plans or work items, look for deep-module opportunities, audit DRY/cruft, tighten naming, and consolidate the result into edits, issues, or a clear report. The goal is not taste; it is fewer loose parts and clearer next actions.

Good fits:

- Defuzzing a plan before implementation
- Reviewing recent agent work or uncommitted changes
- Finding naming, boundary, and concept drift
- Turning loose ideas or beads into concrete issues
- Combining code review, DRY/cruft, and naming passes in one workflow

## Install

```sh
# skills.sh CLI — Claude Code, Codex, Cursor, OpenCode, and more
npx skills add ratacat/ratacats-skills --skill clarify

# or the Claude plugin marketplace
/plugin marketplace add ratacat/ratacats-skills
/plugin install clarify@ratacats-skills
```
