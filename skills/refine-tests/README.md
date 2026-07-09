# Refine Tests

This skill audits an existing test suite with fresh eyes and strengthens it.

The organizing question is the mutation thought experiment: if someone introduced a subtle but serious bug in the code a test covers, would the test fail? Coverage tools can't answer that — a test can execute every line and detect nothing. This skill hunts the tests that pass for the wrong reasons: tautological assertions, negatives neutralized before they reach the guard under test, concurrency tests that secretly serialize, validator tests that only ever assert `ok: true`, names that promise scenarios the fixtures never build.

It fixes what it finds rather than just flagging it, under one hard rule: the suite only ever gets strictly more powerful. No assertion is weakened, no coverage removed. When strengthening a test exposes a bug in production code, the behavior is pinned with a `SUSPECTED BUG` marker and surfaced for a human decision instead of being silently "fixed" in either direction.

Good fits:

- Reviewing tests written by another agent or after the code
- Suites with high coverage numbers but low bug-catching trust
- Hardening tests around money, auth, and safety-critical gates
- Finding the error paths, boundaries, and cleanup branches with zero coverage
- Turning flaky tests deterministic without loosening them

## Where it comes from, and how it's tested

The failure taxonomy isn't hypothetical: it was mined from ~25 finding manifests produced by real test-review sessions across several production repos — every pattern in the skill (the neutralized negative, the `ok:true`-only validator test, the concurrency test whose claims secretly serialize, the timer that's forwarded but never fired) is a genericized version of a bug-hiding test actually found and fixed.

The skill is measured the way it tells you to measure tests — would it fail if it were broken?

- **Micro-tests** (per the writing-skills methodology): tempting scenarios — a flaky test under time pressure, a release blocked by a test that caught a real regression, a vacuous secrets-leak test — run as fresh-context completions with and without the skill loaded, 5+ reps per arm, every output read by hand. Pass signal is convergence: with the skill loaded, reps converge on the same doctrinally-correct shape (deterministic flake fixes with assertions intact, refusal to weaken plus the missing accept-path test, vacuity detected and the production leak pinned as a `SUSPECTED BUG` instead of silently "fixed").
- **Planted-defect fixture harness** (the full RED/GREEN gate): a fixture repo seeded with known-bad tests across all seven categories, each keyed to a concealed source mutant. The reviewer's fixes are scored mechanically — apply the mutant, run the revised suite, it must go red. "Strictly more powerful" becomes checkable: killed mutants never decrease, no assertion loosened, suite stays green.

One finding from testing already fed back into the skill: reviewers occasionally landed a red strengthened test when they surfaced a production bug, so the pinning protocol now states it mechanically — the pinned test is what lands, never a red test. Discipline rails are kept maximally explicit on purpose: capable models often resist these temptations unaided; the rails are for the weaker models that will also run this skill.

## Install

```sh
# skills.sh CLI — Claude Code, Codex, Cursor, OpenCode, and more
npx skills add ratacat/ratacats-skills --skill refine-tests

# or the Claude plugin marketplace
/plugin marketplace add ratacat/ratacats-skills
/plugin install refine-tests@ratacats-skills
```
