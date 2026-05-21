# PM Mispricing Analysis

This skill is for a bounded, market-aware scan that asks, "Is anything far enough off to care?"

Use it when a full deep analysis would be too much, but the agent still needs current prices, exact instrument identity, quick world checks, and a practical estimate of whether a market looks meaningfully mispriced.

Not every event deserves a full report. This skill gives the agent a smaller workbench: fetch the market, understand the rule, make a quick resolution estimate, and surface only candidates with a large enough gap.

Good fits:

- Looking for 15+ point candidate mispricings
- Scanning one event with multiple child markets
- Producing operator-facing trade candidates
- Deciding whether deeper research is worth it

Expected output: exact market ID, current price context, quick rule summary, agent estimate, gap size, key risks, and candidate trade terms or no-action note. It can use prices, unlike price-blind research. It should still stay grounded in rules, evidence, and exact market identity.
