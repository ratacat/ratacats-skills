# GPT Pro Loop

This skill helps your local coding agent run a revision loop while it builds. As the agent works on a plan, project, or goal, it assembles context packets and systematically sends them to **GPT Pro** through the terminal via [`pro-cli`](https://github.com/ratacat/pro-cli), recruits Pro's feedback, and integrates it as it goes.

In short: it gathers live feedback from GPT Pro while a local agent builds. That's powerful because Pro on extended thinking offers top-tier insight into software and project design. Normally you would have to assemble context packets by hand and paste them into Pro, or pay steep API fees — this runs on your ChatGPT subscription, and the skill makes it automatic. Call it when a coding agent starts work on a project or plan, and it knows how to pull Pro's feedback into the build loop on its own. More than almost anything else, it upgrades the quality of your coding agent's output.

Under the hood: a `pro review loop` rebuilds a context package each round and feeds Pro's critique back into a single design map and issue vocabulary, while a `main loop` turns that into revisions, verification, and a goal assessment that decides what happens next.

Good fits:

- Pulling live Pro feedback into a build while a coding agent works
- Hardening a design against an outside critic before shipping
- Surfacing overlooked bugs, schema risks, and test gaps

It stops when the goal assessment chooses `satisfied`, `pivot`, `handoff`, or `blocked`.

## Install

```sh
# skills.sh CLI — Claude Code, Codex, Cursor, OpenCode, and more
npx skills add ratacat/ratacats-skills --skill gpt-pro-loop

# direct path to just this skill
npx skills add https://github.com/ratacat/ratacats-skills/tree/main/skills/gpt-pro-loop

# or the Claude plugin marketplace
/plugin marketplace add ratacat/ratacats-skills
/plugin install gpt-pro-loop
```

## Setup (required)

This skill drives GPT Pro through [`pro-cli`](https://github.com/ratacat/pro-cli), which must be installed and logged in to your ChatGPT account. You do not have to do this by hand: when you run the skill, the agent checks `pro-cli doctor --json` and, if it is missing or not logged in, installs it and walks you through the one-time browser login. The full flow is in [references/pro-cli-setup.md](references/pro-cli-setup.md).

Quick version:

```sh
pro-cli doctor --json    # health check (no Pro quota): installed + logged in?
# if missing (requires Bun):
curl -fsSL https://raw.githubusercontent.com/ratacat/pro-cli/main/scripts/install.sh | bash
# then authenticate one logged-in ChatGPT Chrome window and re-run doctor
```

`pro-cli` runs on your ChatGPT subscription via your own logged-in web session. Never send secrets, raw cookies, tokens, `.env` files, or private keys through it — the skill redacts these from the context package, and `pro-cli` stores only scoped auth under `~/.pro-cli`.
