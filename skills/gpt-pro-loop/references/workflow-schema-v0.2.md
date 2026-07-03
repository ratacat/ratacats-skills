# GPT Pro Loop Workflow Schema V0.2

Schema id: `gpt-pro-loop.workflow.v0.2`

Status: draft

Purpose: define the artifact names, object shapes, issue states, and decision fields used by the GPT Pro Loop skill.

## Core Object

```yaml
schema_version: gpt-pro-loop.workflow.v0.2

loop:
  id: string
  project: string
  artifact_root: string
  started_at: iso_datetime
  updated_at: iso_datetime
  loop_goal: LoopGoal
  design_map: DesignMap
  iterations: Iteration[]
  current_goal_assessment: GoalAssessment | null
```

## Loop Goal

`loop_goal` is a domain term for this workflow. It is distinct from `/goal`, goal-ledger commands, or any tool-specific goal object.

```yaml
LoopGoal:
  statement: string
  success_criteria: string[]
  scope:
    included: string[]
    excluded: string[]
  stop_condition: string
  operating_mode: string | null
  notes: string[]
```

## Design Map

The design map is the live state of the loop's thinking.

```yaml
DesignMap:
  path: string
  summary: string
  current_system_theory: string
  prior_context: PriorContext[]
  assumptions: DesignAssumption[]
  design_tensions: DesignTension[]
  issues: Issue[]
  decisions: Decision[]
  open_questions: OpenQuestion[]
  revisions: RevisionPass[]
  verification_records: VerificationRecord[]
  artifacts: Artifact[]
  carried_forward: CarryForwardItem[]
  user_steering: UserSteering[]
```

```yaml
PriorContext:
  id: string
  source_type: handoff | design_map | goal_ledger | pro_report | session_search | worktree | other
  source_ref: string
  used_for: string
  omitted_reason: string | null

DesignAssumption:
  id: string
  statement: string
  status: active | challenged | replaced | retired
  evidence: string[]

DesignTension:
  id: string
  statement: string
  options: string[]
  current_resolution: string | null
  linked_issue_ids: string[]

Decision:
  id: string
  statement: string
  rationale: string
  decided_at: iso_datetime
  source: user | local_agent | pro | test | runtime
  linked_issue_ids: string[]

OpenQuestion:
  id: string
  question: string
  owner: user | local_agent | pro | unknown
  blocks_goal_assessment: boolean

UserSteering:
  id: string
  captured_at: iso_datetime
  summary: string
  impact: string

CarryForwardItem:
  id: string
  statement: string
  reason: string
  target_context: string
  linked_issue_ids: string[]
```

## Issue

An issue is one concrete critique, bug, weak point, oversight, contradiction, or risk.

```yaml
Issue:
  id: string
  title: string
  source: pro | local | user | test | runtime
  severity: P0 | P1 | P2 | P3
  score: 8 | 5 | 3 | 1
  status: candidate | active | addressed | verified | disregarded | accepted | carried_forward
  claim: string
  local_judgment: string
  evidence: string[]
  linked_artifacts: string[]
  addressed_by_revision_pass_ids: string[]
  verified_by_record_ids: string[]
```

Status meanings:

- `candidate` - awaiting local judgment.
- `active` - valid and in scope.
- `addressed` - changed, awaiting verification.
- `verified` - fixed and checked locally.
- `disregarded` - invalid, stale, duplicate, or not applicable.
- `accepted` - real and acceptable under the current loop goal.
- `carried_forward` - real and belongs to later work.

## Iteration

An iteration is one main-loop cycle. It can contain zero or one Pro review run and one or more revision passes.

```yaml
Iteration:
  index: integer
  artifact_dir: string
  started_at: iso_datetime
  completed_at: iso_datetime | null
  pro_review_run: ProReviewRun | null
  revision_passes: RevisionPass[]
  local_verification: LocalVerification
  goal_assessment: GoalAssessment
  handoff: Handoff | null
```

## Pro Review Run

```yaml
ProReviewRun:
  id: string
  status: planned | submitted | running | completed | failed | cancelled
  context_package: ContextPackage
  gpt_pro_prompt: GPTProPrompt
  adversarial_review: AdversarialReview | null
```

## Context Package

The context package is rebuilt for each Pro review run.

```yaml
ContextPackage:
  path: string
  generated_at: iso_datetime
  package_format: xml | markdown | text | archive | other
  loop_goal_ref: string
  included_sections: string[]
  omitted_sections: string[]
  code_refs: string[]
  schema_refs: string[]
  data_samples: string[]
  test_refs: string[]
  validation_refs: string[]
  prior_review_refs: string[]
  design_map_refs: string[]
  prior_context_refs: string[]
  redaction_summary: string
  user_approval_for_pro_cli: boolean
```

## GPT Pro Prompt

```yaml
GPTProPrompt:
  path: string
  generated_at: iso_datetime
  model_target: chatgpt_pro
  prompt_goal: string
  requested_outputs: string[]
  severity_scale_ref: string | null
  issue_schema_ref: string
  evidence_standard: string
  attached_context_package_path: string
```

## Adversarial Review

```yaml
AdversarialReview:
  path: string
  generated_at: iso_datetime
  pro_cli_command: string
  pro_cli_job_id: string | null
  pro_cli_result_path: string | null
  status: completed | failed | partial
  summary: string
  extracted_issue_ids: string[]
  raw_output_preserved: boolean
```

## Revision Pass

```yaml
RevisionPass:
  id: string
  iteration_index: integer
  summary: string
  addressed_issue_ids: string[]
  changed_files: string[]
  design_changes: string[]
  implementation_changes: string[]
  tests_added_or_changed: string[]
  notes: string[]
```

## Local Verification

```yaml
LocalVerification:
  summary: string
  records: VerificationRecord[]
  result: passed | failed | mixed | not_run
```

```yaml
VerificationRecord:
  id: string
  recorded_at: iso_datetime
  kind: test | typecheck | lint | script | runtime | database | screenshot | manual | other
  command: string | null
  result: passed | failed | mixed
  output_ref: string | null
  interpretation: string
  linked_issue_ids: string[]
```

## Goal Assessment

The goal assessment is owned by the local agent.

```yaml
GoalAssessment:
  path: string
  written_at: iso_datetime
  loop_goal_result: satisfied | partially_satisfied | unsatisfied
  next_action: continue | repackage | pivot | handoff | blocked | satisfied
  review_pressure_summary: string
  remaining_issue_score: integer
  remaining_issues_by_severity:
    P0: integer
    P1: integer
    P2: integer
    P3: integer
  accepted_risks: string[]
  disregarded_issues: string[]
  carried_forward_issue_ids: string[]
  verification_summary: string
  rationale: string
  next_work: string[]
```

Recommended next action meanings:

- `continue` - run another local revision pass before repackaging.
- `repackage` - rebuild the context package and ask Pro for another adversarial review.
- `pivot` - stop this loop because a different goal now matters more.
- `handoff` - stop active work and preserve state for a human or future agent.
- `blocked` - stop because a required input, access, or decision is missing.
- `satisfied` - stop because the loop goal is met for the declared scope.

## Artifact

```yaml
Artifact:
  id: string
  kind: design_map | context_package | gpt_pro_prompt | adversarial_review | revision_pass | verification_record | goal_assessment | handoff | evidence | other
  path: string
  created_at: iso_datetime
  iteration_index: integer | null
  summary: string
```

## Handoff

```yaml
Handoff:
  path: string
  written_at: iso_datetime
  current_state: string
  next_work: string[]
  unresolved_issue_ids: string[]
  key_artifacts: string[]
  verification_summary: string
```
