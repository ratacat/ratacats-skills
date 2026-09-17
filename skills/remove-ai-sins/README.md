# remove-ai-sins

Idempotent revision pass for literary and narrative nonfiction. Removes seven craft sins and otherwise leaves the draft alone. A second run on the result is a no-op.

The seven:

- **frame** — "not X but Y" antithesis
- **name** — labeling a feeling the detail already carries
- **explain** — glossing an image or joke
- **intensify** — inflating a moment that was written small
- **summary** — a last sentence that moralizes
- **resolve** — tying shut a question the text opened
- **meta** — prose about the prose instead of the subject

Good fits:

- A continuation or chapter that sounds like a base LLM
- Blind-read leftovers: lots of "not this but that"
- A draft you want cleaned without a restyle

Not for first drafts, annotation, or general AI-slop word lists (`no-ai-slop` / `unslop`).

## Install

```sh
# skills.sh CLI — Claude Code, Codex, Cursor, OpenCode, and more
npx skills add ratacat/ratacats-skills --skill remove-ai-sins

# or the Claude plugin marketplace
/plugin marketplace add ratacat/ratacats-skills
/plugin install remove-ai-sins@ratacats-skills
```

Invoke with `/remove-ai-sins` and a draft.
