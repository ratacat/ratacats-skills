# GPT Pro Loop Operating Guide

Use this reference for the concrete operating rules behind the skill.

## Artifact Layout

Use the repo's existing agent-artifact or review-artifact folder when one exists. Otherwise use:

```text
.agent/pro-loop/<yyyy-mm-dd>-<loop-slug>/
  design-map.md
  goal-assessment.md
  handoff.md
  iterations/
    001/
      context-package.xml
      gpt-pro-prompt.md
      pro-result.json
      adversarial-review.md
      revision-pass.md
      verification-record.md
    002/
      context-package.xml
      gpt-pro-prompt.md
      pro-result.json
      adversarial-review.md
      revision-pass.md
      verification-record.md
```

Keep `design-map.md` at the loop root because it is the live map across all iterations. Keep per-iteration artifacts in `iterations/<n>/` because each Pro round gets a freshly rebuilt context package.

When using goal-ledger, link this artifact root from `implementation-notes.html` and keep the ledger concise.

## Prior Context Search

Before building a context package, inspect the local context that can change the loop:

- current worktree status and changed files
- nearest repo instructions
- existing handoffs
- prior design maps
- goal-ledger `GOAL.md` and `implementation-notes.html`
- prior Pro reports and revision passes
- session search when available, such as `cass search`

Record prior context in the design map as `PriorContext` entries. Include what was used and what was intentionally omitted.

## Context Package Selection Rules

A useful context package lets Pro attack the system without local repo access.

Include:

- loop goal, operating mode, success criteria, and stop condition
- relevant repo instructions and agent constraints
- architecture docs or system overview
- high-value code paths that own the loop goal
- schemas, migrations, typed contracts, event shapes, and API surfaces
- representative data samples, fixtures, reports, or database query results
- tests, test gaps, recent validation output, and known failing checks
- design map summary, active issues, decisions, assumptions, and design tensions
- prior adversarial reviews and what changed since then
- known omissions and why they were omitted
- redaction summary and user approval for `pro-cli`

Use direct excerpts for small critical files. Use file references plus concise summaries for large files. Prefer structured samples over loose dumps.

Redact secrets, tokens, cookies, credentials, private keys, raw `.env` files, and account material before sending.

## GPT Pro Prompt Output Shape

Ask Pro to return findings in this shape:

```yaml
issues:
  - title: string
    severity: P0 | P1 | P2 | P3
    claim: string
    evidence: string[]
    affected_artifacts: string[]
    suggested_revision: string
    verification_idea: string
open_questions:
  - question: string
    why_it_matters: string
design_tensions:
  - tension: string
    options: string[]
summary: string
```

Ask Pro to separate direct evidence from inference. Ask it to mark items that require local verification.

## Goal Assessment Rubric

Write the goal assessment after each meaningful revision pass or Pro review.

Use `satisfied` when:

- success criteria are met for the declared scope
- local verification passes at the right scope
- no active P0/P1 issues remain
- remaining P2/P3 issues are verified, accepted, disregarded, or carried forward with rationale
- the handoff is unnecessary or already written

Use `continue` when:

- active issues remain and the next revision pass is clear
- local verification points to a concrete fix
- the loop goal still matches the user's priority

Use `repackage` when:

- material changes landed since the last Pro review
- local verification passed or the remaining failures are clearly documented
- another adversarial review can plausibly find different issues

Use `pivot` when:

- the user's priority changed
- the current loop goal no longer pays rent
- a different goal now dominates the work

Use `handoff` when:

- work should pause with state preserved
- another agent or human can continue from the artifact root
- remaining issues and next work are explicit

Use `blocked` when:

- required access, input, decision, or external state is missing
- the agent has recorded what is blocked, what was attempted, and what would unblock it

Score remaining unresolved issues with the host project's severity scale. If no project scale exists, use P0=8, P1=5, P2=3, P3=1.

Scope the assessment to the operating mode. A system can be `satisfied` for manual review or paper trading while still carrying issues that block live execution.
