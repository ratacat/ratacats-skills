# Failure Modes

This skill is for the slow, careful review pass that asks, "How could this be wrong?"

Use it when a repo, diff, subsystem, or recent agent change needs more than a normal code review. It looks for hidden assumptions, stale contracts, boundary drift, weak tests, duplicated behavior, misleading success states, and other quiet ways software fails.

Many bugs are not dramatic. They live in a stale generated file, a copied helper, a missing cleanup path, or a probe that proves the wrapper but not the behavior. This skill gives the agent a checklist and a stance for finding those.

Good fits:

- Reviewing uncommitted changes
- Auditing recent agent work
- Finding deep risks before shipping
- Turning vague concern into concrete findings

The best output is evidence-heavy: file paths, behavior, risk, small fixes, and verification. Avoid speculative findings without proof.
