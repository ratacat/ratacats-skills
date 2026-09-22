---
name: crystallize
description: Use when asked to crystallize a workflow, skill, codebase, or agent runs, or to find where agents repeatedly rediscover methods, apply stable rules, or do unnecessary work. Analysis of opportunities to replace repeated agent effort with reusable procedures; not a general code cleanup or an automatic implementation run.
metadata:
  category: developer tools
  blurb: Finds repeated agent work that can be removed or turned into reusable procedures, with evidence, exception conditions, and a small first change.
  keywords:
    - crystallize
    - workflow-distillation
    - repeated-reasoning
    - agent-workflows
    - automation
    - cost-reduction
---

# Crystallize

Find where an agent repeatedly figures out something the system could learn to do once. Recommend small replacements that preserve the task's outcome and leave open-ended work to an agent where needed.

Default to analysis and proposals. Implement only when the user's request includes implementation. Use existing code, instructions, records, and run histories; do not require a new tracing system or workflow engine.

## Find the repeated work

Establish the requested outcome and the consequences of a wrong result before proposing shortcuts. Read the relevant procedure, code, or skill, then inspect available runs, including failures and exceptions. Follow an input through the steps that produce the outcome.

Look for repeated reasoning with a stable method, even when each case has a different answer. Identify what stays fixed, what varies, and what the next step actually needs. Cite the specific instructions, code, or runs behind each finding.

Code and prompts reveal candidates. Runs establish recurrence and expose variation. Without run evidence, label the opportunity a hypothesis and identify the smallest observation that would settle it. Never invent frequencies, costs, or savings.

## Choose the smallest replacement

Consider these changes, starting with work that can disappear:

- Remove a step when its result cannot affect any required outcome. Include required evidence and reporting in that outcome; an unchanged verdict alone may not justify skipping research.
- Reorder work or stop early when the remaining results cannot change the outcome. State why that condition holds and what would invalidate it.
- Retain a discovered method, address, query, or retrieval route. State when it must be refreshed or rediscovered. Reusing a method does not make yesterday's facts current.
- Turn explicit rules, parsing, calculations, polling, and mechanical actions into ordinary code or an existing tool.
- Isolate a narrow judgment with clear inputs and possible answers. Carry the relevant criteria, exceptions, and blockers into that judgment. Keep uncertain cases on a path that can resolve them.
- Keep an agent for investigation or decisions whose scope remains open. A short reusable instruction can be sufficient when code would be brittle.

Do not prescribe a model vendor, DSL, or framework. Use the project's existing tools where they fit. A model's stated confidence is not evidence of calibration; any routing threshold needs support from representative outcomes.

## Find where the replacement breaks

For each serious candidate, look for an actual exception or construct a clearly labeled counterexample. Repeated successful answers may share an accidental condition.

Describe the inputs the replacement handles and the observable condition that returns work to an agent or person. Identify silent failures as well as explicit errors. If the system cannot recognize the exception reliably, narrow the proposed replacement or retain the current investigation.

Do not assume the current agent's output is correct. Compare against the task's requirements and reviewed outcomes where available. Propose a bounded comparison using ordinary cases and relevant exceptions. Use cases outside those that suggested the shortcut when available. Preserve any asymmetry in the cost of mistakes.

Retained evidence can support replay only for decisions it still contains the necessary facts to answer. A new question, policy requirement, or freshness requirement may need new research.

## Return a short ranked list

Rank by recurrence, avoidable effort, consequences of mistakes, and maintenance burden. Distinguish observed savings from estimates, and account for fallback work and upkeep. Prefer a few supported opportunities; no worthwhile candidate is a valid result.

For each recommendation, give:

- The repeated work and its evidence.
- The stable part and the smallest replacement.
- The exception condition and where that case goes.
- The likely benefit, with the basis for any estimate.
- The smallest comparison or observation needed before adopting it.

Recommend one starting point. Keep speculative candidates visibly separate from findings supported by runs. Return the analysis in the conversation unless the user requests another artifact.

## Example

An agent repeatedly navigates an organization's website to find the same calendar. Save the calendar address and retrieval method so later runs can start there. Return to discovery if retrieval fails or the page no longer contains the expected listings. Check freshness separately; a successful fetch may return an abandoned calendar. Compare later runs against independent discovery before treating the shortcut as dependable.
