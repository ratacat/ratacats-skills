# Conjecture Cascade

This skill runs a structured bug hunt over a bounded software target by sending many small, falsifiable probes, called conjectures, through it. Each conjecture closes with evidence and a status: disproved, fixed, confirmed, intentional, or incomplete.

Use it when inspecting code for hidden bugs, dropped behavior, missing records, stale state, unclear failures, or broad reliability risks across a defined scope. The lens list keeps coverage visible, and the final report leads with confirmed issues, proof, incomplete checks, and residual risks.

Good fits:

- Auditing a subsystem or recent changes for hidden defects
- Surfacing likely issue classes before a release
- Verifying that failures are loud, recorded, and recoverable
- Producing an evidence-backed issue report with fixes and residual risks

## Install

```sh
# skills.sh CLI — Claude Code, Codex, Cursor, OpenCode, and more
npx skills add ratacat/ratacats-skills --skill conjecture-cascade

# or the Claude plugin marketplace
/plugin marketplace add ratacat/ratacats-skills
/plugin install conjecture-cascade@ratacats-skills
```
