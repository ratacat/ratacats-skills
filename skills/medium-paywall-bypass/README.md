# Medium Article Access

This skill helps an agent read a Medium article when the user has a link but not usable page content.

Use it for Medium and Medium-hosted publications such as Towards Data Science, Better Programming, and similar sites. The skill tries mirror and archive routes in a practical order, then brings back enough article content for the task at hand.

The user asked about the article, not about the page furniture. This skill keeps the agent focused on readable text without turning the task into browser fuss.

Good fits:

- Summarizing a linked Medium post
- Extracting ideas from an article the user wants to discuss
- Comparing an article with other sources
- Pulling short quotes or claims for review

Prefer summaries, short excerpts, archives, or user-provided text when the full article text is not needed for the user's request.

## Install

```sh
# skills.sh CLI — Claude Code, Codex, Cursor, OpenCode, and more
npx skills add ratacat/ratacats-skills --skill medium-paywall-bypass

# or the Claude plugin marketplace
/plugin marketplace add ratacat/ratacats-skills
/plugin install medium-paywall-bypass@ratacats-skills
```
