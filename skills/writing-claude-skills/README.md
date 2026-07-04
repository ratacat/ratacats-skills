# Writing Claude Skills

This skill helps an agent write better Claude and Codex skills by treating process documentation like a tested system.

Use it when creating, editing, or tightening a skill. The core idea is simple: a skill should change agent behavior in pressure scenarios. If you never watched an agent fail without the skill, you do not know what the skill needs to teach.

Practical skill design pushes the author away from vague advice and toward triggers, concrete workflow steps, common failure modes, and tests that show the instruction actually works. Companion docs: [Anthropic best practices](anthropic-best-practices.md), [testing skills with subagents](testing-skills-with-subagents.md), and [examples](examples/).

Good fits:

- Creating a new skill from a repeated workflow
- Improving a skill that agents ignore
- Writing pressure tests for skill behavior
- Splitting a big skill into focused pieces
- Making skill descriptions trigger at the right time

## Install

```sh
# skills.sh CLI — Claude Code, Codex, Cursor, OpenCode, and more
npx skills add ratacat/ratacats-skills --skill writing-claude-skills

# or the Claude plugin marketplace
/plugin marketplace add ratacat/ratacats-skills
/plugin install writing-claude-skills@ratacats-skills
```
