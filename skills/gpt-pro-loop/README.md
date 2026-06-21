# GPT Pro Loop

This skill runs a project revision loop where GPT Pro acts as an adversarial reviewer from outside the repo, while the local agent owns context, design, edits, local verification, and the go/no-go decision.

Use it when you want sustained outside review pressure on a system you are building: a `pro review loop` rebuilds a context package each round and feeds Pro's critique back into a single design map and issue vocabulary, and a `main loop` turns that into revisions, verification, and a goal assessment that decides what happens next.

Good fits:

- Hardening a design against an outside critic before shipping
- Surfacing overlooked bugs, schema risks, and test gaps
- Driving a focused revision loop with a clear stop condition

It stops when the goal assessment chooses `satisfied`, `pivot`, `handoff`, or `blocked`.

## Setup (required)

This skill drives GPT Pro through the `pro-cli` tool. Before the loop can run, two things must be true:

1. **`pro-cli` is installed.**
2. **`pro-cli` is authenticated to your account** so reviews can be submitted.

> **TODO:** ship a single `setup` command that installs `pro-cli` if missing and walks through connecting it to the user's account. The exact mechanism is still being worked out — for now, install and authenticate `pro-cli` manually before using the skill.

Never send secrets, raw cookies, tokens, `.env` files, or private keys through `pro-cli`. The skill redacts these from the context package.
