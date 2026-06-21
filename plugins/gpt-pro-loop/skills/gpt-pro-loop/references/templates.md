# GPT Pro Loop Templates

Use these as starting points. Trim fields that do not apply.

## Design Map

```md
# Design Map: <loop title>

Schema: gpt-pro-loop.workflow.v0.2
Artifact root: <path>
Updated: <iso datetime>

## Loop Goal

<one sentence>

Success criteria:
- <criterion>

Scope:
- Included: <items>
- Excluded: <items>

Operating mode: <mode or none>
Stop condition: <condition>

## Current System Theory

<how the system currently appears to work>

## Prior Context

| ID | Source | Used For | Omitted Reason |
| --- | --- | --- | --- |
| PC-001 | <path/search/report> | <use> | <none/reason> |

## Assumptions

| ID | Status | Statement | Evidence |
| --- | --- | --- | --- |
| A-001 | active | <statement> | <evidence> |

## Design Tensions

| ID | Tension | Options | Current Resolution |
| --- | --- | --- | --- |
| T-001 | <tension> | <options> | <resolution or open> |

## Issues

| ID | Sev | Score | Status | Source | Title | Local Judgment |
| --- | --- | ---: | --- | --- | --- | --- |
| I-001 | P2 | 3 | active | pro | <title> | <judgment> |

## Decisions

| ID | Source | Decision | Rationale |
| --- | --- | --- | --- |
| D-001 | user | <decision> | <why> |

## Revision Passes

| ID | Issues | Summary | Verification |
| --- | --- | --- | --- |
| R-001 | I-001 | <summary> | <record id> |

## Verification Records

| ID | Kind | Result | Interpretation |
| --- | --- | --- | --- |
| V-001 | test | passed | <meaning> |

## Open Questions

- <question>

## Carried Forward

- <item and target context>
```

## Context Package

```xml
<context_package schema="gpt-pro-loop.workflow.v0.2">
  <metadata>
    <loop_goal><![CDATA[...]]></loop_goal>
    <iteration>001</iteration>
    <generated_at>...</generated_at>
    <operating_mode>...</operating_mode>
    <user_approval_for_pro_cli>true</user_approval_for_pro_cli>
    <redaction_summary>Secrets, raw env files, tokens, cookies, and private keys excluded.</redaction_summary>
  </metadata>

  <repo_instructions>
    <![CDATA[Relevant AGENTS/CLAUDE/project instructions.]]>
  </repo_instructions>

  <prior_context>
    <![CDATA[Handoffs, design maps, goal ledgers, prior Pro reports, CAS/session-search findings.]]>
  </prior_context>

  <system_overview>
    <![CDATA[Architecture and current system theory.]]>
  </system_overview>

  <design_map_snapshot>
    <![CDATA[Active issues, decisions, assumptions, design tensions, carried-forward work.]]>
  </design_map_snapshot>

  <code>
    <file path="src/example.ts"><![CDATA[...]]></file>
  </code>

  <schemas_and_contracts>
    <![CDATA[Schema excerpts, migrations, API/event shapes.]]>
  </schemas_and_contracts>

  <data_samples>
    <![CDATA[Representative structured samples and query results.]]>
  </data_samples>

  <tests_and_validation>
    <![CDATA[Test files, recent command output, known gaps.]]>
  </tests_and_validation>

  <known_omissions>
    <![CDATA[What is absent and why.]]>
  </known_omissions>
</context_package>
```

## GPT Pro Prompt

````md
Goal: Perform a deep adversarial review of the attached context package for <loop goal>, with simplification as the primary lens.

Primary lens — simplify:
- Treat reducing complexity and code volume as the main objective.
- For every issue and suggestion, prefer the simplest, most elegant form that still meets all design requirements and goals in full.
- Look hard for code, abstractions, indirection, and state that can be removed, merged, or collapsed while capability and purpose are fully preserved.
- Never trade away required capability, correctness, or purpose to make something smaller.

Success means:
- Return issues using the issue schema below.
- Separate direct evidence from inference.
- Identify weak points, oversights, bugs, data/schema risks, test gaps, design contradictions, and operating-mode concerns.
- Suggest concrete revisions and local verification ideas, biased toward simplification.

Stop when: every material concern from the provided context is represented as an issue, open question, design tension, or summary note.

Constraints:
- The user has approved sending this context through `pro-cli`.
- Treat the context package as the available evidence.
- Mark claims that require local verification.

Issue output shape:

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
````

## Revision Pass

```md
# Revision Pass <id>

Iteration: <n>
Addressed issues: <ids>

## Summary

<what changed>

## Design Changes

- <change>

## Implementation Changes

- <file>: <change>

## Tests Added Or Changed

- <test>

## Notes

- <tradeoff or sequencing note>
```

## Verification Record

```md
# Verification Record <id>

Recorded: <iso datetime>
Result: passed | failed | mixed

| Kind | Command / Check | Result | Interpretation |
| --- | --- | --- | --- |
| test | `<command>` | passed | <meaning> |

Linked issues: <ids>
Output refs: <paths>
```

## Goal Assessment

```md
# Goal Assessment

Written: <iso datetime>
Loop goal result: satisfied | partially_satisfied | unsatisfied
Next action: continue | repackage | pivot | handoff | blocked | satisfied

## Review Pressure

<what Pro/local review still pressures>

## Remaining Issues

| Severity | Count | Score |
| --- | ---: | ---: |
| P0 | 0 | 0 |
| P1 | 0 | 0 |
| P2 | 0 | 0 |
| P3 | 0 | 0 |

Remaining issue score: <n>

## Accepted Risks

- <risk and why acceptable for current operating mode>

## Disregarded Issues

- <issue id and rationale>

## Verification Summary

<commands/checks and interpretation>

## Rationale

<why this next action follows>

## Next Work

- <next action>
```

## Handoff

```md
# Handoff: <loop title>

Artifact root: <path>
Current state: <summary>
Latest goal assessment: <path>
Latest verification: <path>

## Next Work

- <next step>

## Unresolved Issues

- <issue id>: <status and next action>

## Key Artifacts

- <path>: <why it matters>
```
