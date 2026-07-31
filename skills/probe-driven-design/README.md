# Probe-Driven Design

Probe-driven design is a process for making consequential uncertainty concrete before designing around it. It identifies the next decision, selects the smallest useful probe, captures the result, and updates or branches the design from what the probe reveals.

A probe may use code, but it does not have to. Useful probes include targeted queries, temporary implementations, simulations, workflow walkthroughs, interviews, role-play, traces, benchmarks, mocked boundaries, and shadow operations. The probe is only as broad and realistic as its question requires.

Good fits:

- Choosing among architectures before the decisive constraints are known
- Deciding what to prototype and how much fidelity it needs
- Comparing multiple credible implementations without treating one as the default
- Exploring product, policy, organizational, or operational workflows through concrete trials
- Sequencing branching investigations through dependencies, parallel paths, convergence, and invalidation
- Pruning overbuilt learning programs whose studies, evidence machinery, or future branches do not change the next decision
- Using independent checks selectively to reduce anchoring and hidden-context bias

It is not a general brainstorming or audit skill. Use it when the result of a probe must change a design decision or determine which branch to pursue next.

## Install

```sh
# skills.sh CLI — Claude Code, Codex, Cursor, OpenCode, and more
npx skills add ratacat/ratacats-skills --skill probe-driven-design

# or the Claude plugin marketplace
/plugin marketplace add ratacat/ratacats-skills
/plugin install probe-driven-design@ratacats-skills
```

No additional setup or dependencies are required.
