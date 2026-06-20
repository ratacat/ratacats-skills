---
name: gpt-pro-loop
description: "Use when running a GPT Pro or pro-cli assisted project revision loop: build a context package, write a GPT Pro prompt, request adversarial review, map issues into a design map, run revision passes, verify locally, write goal assessments, and hand off the loop."
---

# GPT Pro Loop

Goal: Use GPT Pro as an adversarial reviewer while the local agent owns project context, design thinking, implementation, local verification, and goal assessment.

Success means:
- The `loop goal` is explicit and scoped.
- The `design map` is the live state of design thinking.
- The `main loop` moves through revision, verification, and goal assessment.
- The nested `pro review loop` rebuilds the `context package` for each Pro round.
- Issues from Pro, local review, tests, runtime checks, and the user land in one issue vocabulary.
- The local agent writes the `goal assessment` and decides the next action.

Stop when: the goal assessment chooses `satisfied`, `pivot`, `handoff`, or `blocked`.

Workflow schema: `gpt-pro-loop.workflow.v0.2`. Read [workflow-schema-v0.2.md](references/workflow-schema-v0.2.md) when creating artifacts, checking field names, or updating the workflow vocabulary.

Operating detail:
- Read [operating-guide.md](references/operating-guide.md) for artifact layout, context package selection rules, prior-context search, Pro prompt output shape, and the goal assessment rubric.
- Read [templates.md](references/templates.md) when drafting a design map, context package, GPT Pro prompt, verification record, goal assessment, or handoff.

## Doctrine

Pro creates review pressure. The local agent owns readiness.

Use Pro to attack the system from outside the repo. Use local tools to inspect, edit, run, verify, and decide. Treat Pro findings as inputs to the design map and goal assessment.

## Vocabulary

- `loop goal` - the outcome this loop is trying to reach; distinct from the `/goal` command or any goal-ledger tool.
- `main loop` - the local agent-owned loop: design map, revision pass, local verification, goal assessment, next action.
- `pro review loop` - the nested loop that rebuilds context, writes the GPT Pro prompt, runs Pro, and maps the adversarial review back into the design map.
- `context package` - the rebuilt project snapshot sent to Pro for one review round.
- `gpt pro prompt` - the prompt attached to the context package.
- `adversarial review` - Pro's critique output.
- `design map` - the live map of design thinking, issues, decisions, tensions, assumptions, revisions, verification, and remaining work.
- `issue` - one concrete bug, risk, oversight, weak point, contradiction, or critique.
- `revision pass` - local work that addresses selected issues or design changes.
- `local verification` - tests, checks, runtime probes, data queries, screenshots, or manual checks run locally.
- `verification record` - saved evidence from local verification.
- `goal assessment` - the local agent's judgment of whether the loop goal is satisfied and what happens next.
- `handoff` - compact saved state for a human or future agent.

## The Two Loops

Keep the branch model simple. Run one main loop. Invoke the Pro review loop inside it when external adversarial pressure is useful.

### Main Loop

1. Define or resume the loop goal.
   - Write one goal, success criteria, scope, operating mode, and stop condition.
   - Completion: the local agent can distinguish satisfied, unsatisfied, pivoted, handed off, and blocked.

2. Open the design map.
   - Record the current system theory, assumptions, design tensions, issues, decisions, revisions, verification, user steering, and remaining work.
   - Completion: current design state has one live place to land.

3. Gather prior context.
   - Inspect existing handoffs, design maps, goal ledgers, prior Pro reports, current worktree state, and local session search when available.
   - Completion: the design map names the prior context used and the context intentionally omitted.

4. Choose the next local action.
   - Run a revision pass, run local verification, invoke the Pro review loop, write a goal assessment, or write a handoff.
   - Completion: the next action follows from the loop goal, issue state, and verification state.

5. Run a revision pass.
   - Select active issues or design changes in scope for this pass.
   - Change code, tests, schemas, docs, prompts, or process artifacts as needed.
   - Completion: each selected issue is addressed, verified, accepted, disregarded, or carried forward.

6. Run local verification.
   - Execute checks that prove the revision at the right scope.
   - Save commands, outputs, failures, and interpretation in the verification record.
   - Completion: the revision pass has local evidence.

7. Write the goal assessment.
   - Judge the loop goal against the design map, issue state, and verification record.
   - Choose `continue`, `repackage`, `pivot`, `handoff`, `blocked`, or `satisfied`.
   - Completion: the assessment explains what remains, what is accepted, what is disregarded, and why the next action follows.

### Pro Review Loop

1. Build the context package.
   - Rebuild it for the current iteration from repo instructions, design map state, current code, schemas, tests, data samples, validation, prior reviews, and known omissions.
   - Redact secrets, credentials, private keys, cookies, tokens, and raw environment files.
   - Record the user's approval or repo instruction that authorizes sending project context through `pro-cli`.
   - Completion: Pro can review the system without repo access.

2. Write the gpt pro prompt.
   - Open with an outcome block: goal, success criteria, stop condition, and hard constraints.
   - Ask Pro to return issues in the workflow issue schema.
   - Request weak points, overlooked bugs, data or schema risks, test gaps, design contradictions, operating-mode concerns, and concrete improvements.
   - Completion: the prompt names the review target, requested output shape, and evidence standard.

3. Run the adversarial review.
   - Use the approved `pro-cli` command shape for the repo: durable jobs for long reviews, direct asks for short blocking reviews.
   - Save job id, status, command metadata, raw output, and extracted review.
   - Completion: the adversarial review is persisted as an artifact.

4. Update the design map.
   - Convert material Pro points into issues, decisions, assumptions, design tensions, open questions, or disregarded items.
   - Attach severity, status, evidence, and local judgment to each issue.
   - Completion: every material point from the review is accounted for.

5. Return to the main loop.
   - Use the updated design map to choose revision, verification, another Pro round, handoff, pivot, blocked, or satisfied.
   - Completion: Pro review pressure has become local design state.

## Issue Discipline

Use the host project's severity scale when available. If the project has none, use:

- `P0` / score `8` - dangerous, system-down, data-loss, financial-risk, or unrecoverable core workflow failure.
- `P1` / score `5` - severe impairment, silent logic failure, or major subsystem reliability risk.
- `P2` / score `3` - moderate degradation, confusing behavior, missing retry, weak test, or isolated edge case.
- `P3` / score `1` - minor issue, cosmetic problem, documentation gap, or low-risk tech debt.

Use these issue statuses:

- `candidate` - awaiting local judgment.
- `active` - valid and in scope.
- `addressed` - changed, awaiting verification.
- `verified` - fixed and checked locally.
- `disregarded` - invalid, stale, duplicate, or not applicable.
- `accepted` - real and acceptable under the current loop goal.
- `carried_forward` - real and belongs to later work.

## Completion Standard

Before reporting completion, inspect the current artifacts and prove:

- the design map reflects current work
- active issues have a status and local judgment
- the latest revision pass has local verification
- the latest goal assessment chooses a next action with rationale
- the handoff exists when the next action is `handoff`
- the skill validates when skill files changed
