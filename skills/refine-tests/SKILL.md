---
name: refine-tests
description: Use when auditing, scrutinizing, or strengthening an existing test suite — unit, integration, or e2e — because tests pass but bugs still ship, coverage looks high while trust is low, tests were written after the code or by another agent, tests are flaky and need fixing without loosening them, or the user asks to review, harden, or refine tests with fresh eyes.
metadata:
  category: developer tools
  blurb: "A methodical test-suite audit that finds tautological, vacuous, weak, brittle, mislabeled, and missing tests, then strengthens them without ever reducing coverage."
  keywords:
    - test
    - review
    - assertions
    - tautological
    - vacuous
    - mock
    - coverage
    - mutation
    - flaky
    - brittle
    - audit
    - strengthen
---

# Refine Tests

Audit an existing test suite with fresh eyes and make it strictly more powerful. The goal is not more tests for their own sake — it is tests that would actually fail if the code under them were broken.

## Core Principle: The Mutant Question

For every test, ask the Mutant Question — the mutation-testing thought experiment:

> If a competent junior developer introduced a subtle but serious bug in the code this test covers — flipped a comparison, dropped a branch, inverted a condition, hardcoded a return value, ignored an argument — would this test fail?

If no assertion would fail, the test is decorative. Coverage tools cannot see this: a test can execute every line and detect nothing. Reaching the code is not the same as checking an observable result that would reveal the defect.

The strongest form of the question: **could the function under test be replaced with a constant (`return ok: true`, `return []`, a no-op) and the test still pass?** Verified checkers, validators, filters, and guards deserve this exact question — a tamper-detection suite where every test asserts `ok: true` is passed by a checker that unconditionally returns `ok: true`.

## Hard Rules: Strictly More Powerful

- **Never weaken or simplify a test.** Never loosen an assertion to make something pass.
- **Never remove coverage.** Every change is additive or a strengthening rewrite.
- **When in doubt, add assertions** — do not remove them.
- **The suite stays green.** Strengthening ends with the modified files passing and the full suite, typecheck, and lint clean.
- A flaky test is fixed by removing the nondeterminism (injected clock, real synchronization), never by widening tolerances or deleting the assertion.

## Process

1. **Reread the repo's agent instructions** (`AGENTS.md`, `CLAUDE.md`, testing conventions) before judging anything. Note the test runner and the command to run a single file.
2. **Inventory.** Glob all test files. Map each to the source it exercises (filename convention first, then imports). Note source files with no counterpart test — missing coverage is a first-class finding, not an aside.
3. **Triage.** Skim each test file for the high-yield hunting grounds below. Mark suspects; judge nothing yet.
4. **Deep-read pairs.** For each suspect, read the test AND its source side by side. You cannot judge a test without the source: whether an assertion is tautological, whether a fixture actually reaches the guard under test, and which branches exist are properties of the source.
5. **Classify** every finding against the taxonomy. Record each in a running findings ledger: file, line, category, severity, the issue, and the class of real bug that would slip through.
6. **Fix immediately.** Do not just flag. Strengthen the test, add the missing case, rename the lie.
7. **Verify narrowly** — run the modified file after each fix — then run the full suite, typecheck, and lint at the end.
8. **Report** in the format below.

Severity: **H** = a vacuous or absent test on a money, auth, data-integrity, or concurrency path; **M** = weak assertions or an untested branch in real logic; **L** = naming, hygiene, or incidental gaps.

For large suites, work in batches by directory and carry the findings ledger across batches so late batches benefit from patterns found early. Fan out to parallel reviewers only if the user asks for parallelism.

## Finding Taxonomy

### Cat 1 — Tests that test the wrong thing

The assertions pass for a reason unrelated to the behavior the test claims to verify.

- **The neutralized negative.** A "must not leak / must not include" test whose fixture is stripped, empty, or normalized away by an *earlier* stage, so the guard under test never runs. A secrets-don't-flow test using empty-string credentials passes even if the config leaks them, because an env compactor drops empties regardless.

  ```ts
  // ❌ Vacuous: empty strings are stripped by compactEnv before the guard runs,
  // so this passes even if the config leaks credentials
  const env = buildTraderEnv({ apiKey: "", apiSecret: "" });
  expect(env).not.toHaveProperty("API_KEY");
  ```

  ```ts
  // ✅ Real values that would survive compaction; assert none reach the env
  const env = buildTraderEnv({ apiKey: "k-live-1", apiSecret: "s-live-1" });
  expect(Object.values(env)).not.toContain("k-live-1");
  expect(Object.values(env)).not.toContain("s-live-1");
  ```

- **The pre-empted negative.** In a combined-filter test, the negative fixture is rejected by an earlier filter than the one under test. Filter N could be deleted and the test passes. Each negative fixture must differ from a passing fixture in exactly the dimension under test.
- **Fixture equals derived value.** The input fixture happens to equal the expected computed output, so copy-instead-of-compute passes.
- **Asserting against a hand-written mock of the unit itself.** The behavior "verified" is the mock author's imagination, not real code.

*Bug class that slips through:* the guard, filter, or computation is entirely broken or bypassed; the suite stays green.

### Cat 2 — Tautological or vacuous tests

The assertion is true by construction and cannot fail.

- Asserting a property the code guarantees structurally — e.g. asserting output is sorted by RMSE when the function sorts by RMSE, while the fitted parameters (the actual math) go unchecked.
- `expect(x).toEqual(literal)` where `x` *is* that local literal.
- Regex assertions with an escape hatch: `/expected message|^$/` matches everything including empty.
- Checker/validator tests that only assert `ok: true`. Inject a real disagreement and assert the exact mismatch record.
- **Grep-the-source tests**: asserting a file's text contains a substring. Passes with dead or commented-out code. Execute the code path or import the artifact instead.
- Snapshots of mocks, or snapshot tests nobody would read on failure.

*Bug class:* anything. These tests catch nothing by definition.

### Cat 3 — Insufficient assertions

The test exercises real code but checks too little of the result.

- Bare `.toThrow()` when callers branch on error type — a decode error regressing from a typed 400 to a generic 500 passes.
- `toMatchObject` verifying 3 of 12 fields on a persistence round-trip; the unchecked mapper fields can silently drop.
- Asserting `ok: false` without the error code, status, or message that consumers dispatch on.
- Client tests asserting URL and headers but never method, body, or abort signal.
- Passing an out-of-range input (`limit=500`) without asserting the clamped value (`limit=100`) reached the downstream call.
- Substring-absence "leak" checks that cannot fail in the test context. Pin the exact key allowlist instead.
- Seeded-but-never-asserted invariants: setup plants "unrelated key" to imply operations don't clobber it, but no assertion checks it survived.

*Bug class:* wrong error taxonomy, dropped fields, ignored parameters, silent contract drift.

### Cat 4 — Brittle for the wrong reasons

Coupled to implementation details that can change without affecting correctness — while the actual contract goes unpinned.

- Asserting generated query text or internal call sequences instead of execution semantics against representative data.
- Tests reading committed build artifacts — they validate the last build, not current source; stale artifacts pass silently.
- Sleeps tuned to implementation timing (a 25ms sleep against a 1000ms poll is doubly wrong: brittle *and* vacuous — a no-op `stop()` still passes). Use injected clocks and real synchronization points.
- Mocking internal collaborators so any refactor breaks the test while behavior bugs don't.

*Bug class:* refactors cause false alarms until someone "fixes" the test by weakening it; real behavior changes pass unnoticed.

### Cat 5 — Missing tests entirely

Important paths with zero coverage. Highest-severity findings usually live here.

- **Money, auth, and safety gates:** kill switches, double-submit protection, quota/settlement logic, admin secret checks. A dropped `already_exists` guard double-submits live orders silently.
- **Error and cleanup branches:** fetch failure, parse error, claim race, the `finally` that releases a lease after a throw, the catch that releases then rethrows.
- **Timers that never fire.** Asserting a timeout value was *forwarded* is config pass-through; nothing proves the timeout branch works. Fire it with fake timers.
- **Expiry/TTL paths:** nothing proves a stale credential falls through to re-probe instead of wedging.
- **Boundary values, both sides:** the exact threshold and one step past it; inclusive bounds at both ends; rounding at half-steps; DST transitions; window-end-exactly; crossed/degenerate inputs (bid == ask).
- **One-sided suites (inverted bias):** every test asserts the reject path, none proves a valid input is accepted — a reject-everything regression passes. Every guard needs both a firing and a non-firing test.
- **Serialization/hash sensitivity:** for each field claimed to affect a hash or canonical form, one test that changing it changes the output; declared order-independence gets an order-shuffled test.

*Bug class:* exactly the production incidents that hurt most — silent data corruption, duplicate side effects, stuck lifecycles.

### Cat 6 — Setup/teardown hazards

State that leaks between tests, masking failures or making passes order-dependent.

- Shared module singletons, env vars, fake timers, or global fixtures not restored after each test.
- Fixtures mutated by one test and consumed by another.
- Cleanup that swallows errors or misses an `await`, hiding real failures.
- **Fake concurrency:** a "concurrent claims" test issuing N parallel calls over one connection that serializes queries — the operations never interleave, so a non-atomic check-then-write passes. Give each simulated actor its own connection.

*Bug class:* races and atomicity bugs invisible in tests; a test that fails only when run alone (or only in suite).

### Cat 7 — Misleading names and descriptions

The name promises something the body doesn't do. Names are documentation; a lying name actively misleads the next maintainer into believing a behavior is covered.

- "handles concurrent claims" — nothing overlaps.
- "clamps budgets across endpoints" — exercises one endpoint.
- Comments describing a scenario the fixtures never construct.
- A `describe` named for function X containing tests of Y and Z.

*Fix:* rename to what is actually proven, or better, make the body earn the name.

## High-Yield Hunting Grounds

Where weak tests cluster. Check these first:

| Ground | What to ask |
| --- | --- |
| Negative tests | Does the fixture reach the guard under test, or is it pre-empted/normalized away earlier? Would it pass with the guard deleted? |
| Validator/checker/tamper tests | Is a disagreement ever actually injected? Would `return ok:true` pass? |
| Concurrency tests | Do operations actually interleave, or does shared infrastructure serialize them? |
| Error paths | Are throw/cleanup/release branches executed, or only the happy path? |
| Timeouts and timers | Fired, or merely forwarded? |
| Boundaries | Tested at the edge and one step past, on both sides? |
| Money/auth/admin surfaces | Any coverage at all? |
| Round-trips | All fields asserted, or a `toMatchObject` subset? |
| Mock-heavy files | Is anything real still executing? Does any assertion touch non-mock output? |

## Fix Patterns

- **Isolating negative fixture:** differs from a known-passing fixture in exactly one dimension — the one under test.
- **Exact-failure asserts:** error class + code + message; the specific mismatch record; the mapped HTTP status.
- **Both-sides boundary:** threshold value and one epsilon past it, in each direction.
- **Asymmetric fixtures:** symmetric win/loss pairs net to zero and hide sign flips; use values where a sign error changes the total.
- **Real interleaving:** one connection/clock per simulated actor; injected clocks over sleeps; fire timers with fake-timer advance.
- **Guard fakes:** a fake for a dangerous external (exchange, mailer, poster) that *throws on any mutating call* — every test through it doubles as a no-side-effects guard.
- **Complete-shape asserts:** `toEqual` the full mapped object on round-trips, or assert every field the mapper writes.
- **Pin the contract:** exact key allowlist instead of substring absence; executed script output instead of grepped source text.
- **Contract tests exercise the real producer path:** mock only values a real producer actually writes. A feature shipped behind a mocked, never-produced key is dead code with green tests.

## Suspected Production Bugs

Strengthening tests will surface cases where the *code* is wrong. Do not silently fix production code mid-review, and do not silently assert the broken behavior either. Pin it:

```ts
// SUSPECTED BUG: decimal() emits "-0.0" for small negatives; the canonical-form
// check rejects that form, so equal values can hash-split. Pinned at current
// behavior pending a decision.
expect(decimal(-0.0004, 1)).toBe("-0.0");
```

The pinned test is what lands — never a red test. Write the intended-contract assertions as comments beside the pin, ready to flip once the human decides. The suite stays green, the anomaly is impossible to miss, and the human decides. List every pinned bug prominently in the report.

## Report Format

```md
# Test Refinement Report

Scope: files scanned / deep-read / clean
Counts: N tests → M tests; suite green; typecheck/lint status

Findings:
| ID | File:Line | Cat | Sev | Issue | Bug class that slipped through | Fix |

Suspected production bugs (pinned, not fixed):
1. file:line — behavior, why it looks wrong, decision needed

Residual risks / coverage still missing:
```

Every finding carries the *why* — the class of real bug the weakness would let through. A finding without a bug class is taste, not a finding.

## Rationalizations

| Excuse | Reality |
| --- | --- |
| "The test passes, so it's fine" | Passing is the weakest possible signal. Decorative tests pass forever. |
| "Adding assertions makes tests brittle" | Brittleness comes from coupling to implementation, not from assertion strength. Assert outputs harder, internals less. |
| "This error branch can't happen" | Untested error branches are where silent corruption lives. If it truly can't happen, delete the branch, not the test. |
| "The mock is simpler than the real path" | A test of a mock proves the mock. Mock at the boundary; keep the unit under test real. |
| "I'll just relax the tolerance to fix the flake" | That's weakening. Remove the nondeterminism instead. |
| "Coverage is already 90%" | Coverage measures execution, not detection. The Mutant Question measures detection. |
| "Renaming is cosmetic" | A lying test name is documentation asserting coverage that doesn't exist. |

## Red Flags — Stop and Re-examine

- A negative test whose fixture would also be rejected/ignored for a different reason
- Any assertion that survives replacing the function with a constant
- `.toThrow()` with no argument; `toMatchObject` on a round-trip; regex with `|^$`
- A "concurrency" test with shared serialized infrastructure
- Assertions on source text, committed artifacts, or mock elements
- A suite where every test asserts the same verdict (all-reject or all-accept)
- Sleeps standing in for synchronization
- Setup that seeds state no assertion ever checks

## When Not to Use

- Writing tests for new code — use a TDD skill; refine-tests is for auditing what exists.
- Diagnosing one failing test — that's debugging, not refinement.
- This skill never justifies deleting or weakening a test to "clean up." Its output is strictly additive power.
