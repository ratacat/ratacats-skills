# GPT Pro Loop

This skill helps your local coding agent run a revision loop while it builds. As the agent works on a plan, project, or goal, it assembles context packets and systematically sends them to **GPT Pro** through the terminal via [`pro-cli`](https://github.com/ratacat/pro-cli), recruits Pro's feedback, and integrates it as it goes.

In short: it gathers live feedback from GPT Pro while a local agent builds. That's powerful because Pro on extended thinking offers top-tier insight into software and project design. Normally you would have to assemble context packets by hand and paste them into Pro, or pay steep API fees — this runs on your ChatGPT subscription, and the skill makes it automatic. Call it when a coding agent starts work on a project or plan, and it knows how to pull Pro's feedback into the build loop on its own. More than almost anything else, it upgrades the quality of your coding agent's output.

Under the hood: a `pro review loop` rebuilds a context package each round and feeds Pro's critique back into a single design map and issue vocabulary, while a `main loop` turns that into revisions, verification, and a goal assessment that decides what happens next.

Good fits:

- Pulling live Pro feedback into a build while a coding agent works
- Hardening a design against an outside critic before shipping
- Surfacing overlooked bugs, schema risks, and test gaps

It stops when the goal assessment chooses `satisfied`, `pivot`, `handoff`, or `blocked`.

## Setup (required)

This skill drives GPT Pro through [`pro-cli`](https://github.com/ratacat/pro-cli). Before the loop can run, two things must be true:

1. **`pro-cli` is installed.**
2. **`pro-cli` is authenticated to your account** so reviews can be submitted.

> **TODO:** ship a single `setup` command that installs `pro-cli` if missing and walks through connecting it to the user's account. The exact mechanism is still being worked out — for now, install and authenticate `pro-cli` manually before using the skill.

Never send secrets, raw cookies, tokens, `.env` files, or private keys through `pro-cli`. The skill redacts these from the context package.
