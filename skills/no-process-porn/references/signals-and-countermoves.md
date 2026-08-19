# Signals and Countermoves

Use this catalog when the language is ambiguous, a workflow has accumulated several layers of process, or project rules need repository-specific countermeasures. Keywords are search leads, not proof.

## Contents

- Status and promotion language
- Gates and holds
- Verification language
- Instrumentation and observability
- Artifact and orchestration language
- Counterfeit progress patterns
- Rationalizations
- Repository-specific countermeasures

## Status and promotion language

Search leads:

`promote`, `promoted`, `promotion`, `advance`, `ready`, `readiness`, `green`, `pass`, `validated`, `verified`, `certified`, `approved`, `closed`, `complete`, `done`, `production-ready`, `release-ready`, `live-verified`, `provisional`, `blocked`, `hold`, `no-go`.

Legitimate when the state transition changes deployment, defaults, capital, exposure, access, scheduling, prioritization, or another owned action.

Warning combinations:

- the new status exists only in a document or database field;
- no authority owns the transition;
- a weaker proof class is presented as a stronger one;
- "complete" means every checklist row has a label, not that the requested behavior works;
- "promoted into docs" substitutes for implementing the decision;
- a failed metric becomes a permanent blocker although the metric cannot be improved or no longer matches the goal.

Countermoves:

- narrow the claim to what the evidence proves;
- demote the status to an annotation;
- name the action unlocked by promotion;
- give a known limitation a re-entry condition instead of a permanent block;
- implement the missing transition rather than polishing its label.

## Gates and holds

Search leads:

`gate`, `quality gate`, `release gate`, `promotion gate`, `acceptance`, `sign-off`, `checkpoint`, `approval`, `hold`, `quarantine`, `eligible`, `readiness`, `conformance`, `policy`, `guard`, `validator`, `proof tier`.

Legitimate when both outcomes have owned consequences. Safety gates may deliberately fail closed.

Warning combinations:

- no consumer or decision owner;
- pass changes nothing;
- held items disappear, accumulate forever, or have no re-entry condition;
- the gate has never seen a real item;
- another gate already controls the same decision;
- a validator validates another validator or evidence format;
- the rule can be weakened by the actor rewarded for passing it;
- a post-hoc synthetic filter is described as a live execution gate.

Countermoves:

- connect the gate to a decision or demote it to evidence;
- route hold/fail to an owner and re-entry condition;
- use an existing control;
- separate the validator owner from the actor being measured when stakes justify it;
- rerun synthetic findings through the real execution path before promotion.

## Verification language

Search leads:

`smoke test`, `smoke-test`, `sanity check`, `green`, `tests pass`, `verified`, `validated`, `proof`, `evidence`, `receipt`, `golden`, `snapshot`, `fixture`, `mock`, `typecheck`, `lint`, `coverage`, `full suite`, `final verification`, `fresh process`, `live readback`.

Legitimate when the check can falsify the claim being made.

Warning combinations:

- mocks presented as live proof;
- typechecking presented as behavior;
- a liveness response presented as dependency readiness;
- one success presented as reliability or performance;
- snapshots regenerated rather than defects fixed;
- repeated checks after the scoped claim is already established;
- full-repository gates run repeatedly during a narrow change;
- test count or coverage percentage substitutes for fault detection.

Countermoves:

- write the smallest exact claim the check proves;
- test through the real boundary when that boundary is the uncertainty;
- add one negative case a naive wrong implementation fails;
- run narrow checks while iterating and broad release checks once;
- stop after proportionate evidence.

## Instrumentation and observability

Search leads:

`instrumentation`, `instrument`, `telemetry`, `metrics`, `logging`, `observability`, `dashboard`, `tracing`, `span`, `counter`, `histogram`, `coverage analyzer`, `health`, `readiness`, `SLO`, `alert`, `monitor`, `status endpoint`, `evidence capture`.

Legitimate when an operator, alert, control loop, incident response, capacity decision, or SLO consumes the signal.

Warning combinations:

- metrics are proposed before the question;
- permanent schema and dashboards are built for a one-time diagnosis;
- the metric has no threshold owner or response action;
- existing logs or a direct query already answer the question;
- instrumentation exceeds the feature or fix in size;
- high-cardinality or durable writes are added without a resource budget;
- a static coverage analyzer counts instrumentation shapes but cannot say whether useful signals exist;
- instrumentation remains after the cause is known although nothing consumes it.

Countermoves:

- state the uncertainty and competing hypotheses;
- instrument only the branch that distinguishes them;
- run once against representative reality and revert;
- preserve only a regression test or the smallest useful ongoing signal;
- define ownership, action, retention, cardinality, and failure behavior before making telemetry permanent.

## Artifact and orchestration language

Search leads:

`ledger`, `manifest`, `certificate`, `report`, `comprehensive report`, `audit`, `fresh eyes`, `handoff`, `worksheet`, `scorecard`, `checklist`, `prompt-to-artifact checklist`, `completion audit`, `status dashboard`, `provenance`, `lineage`, `evidence pack`, `truth pack`, `graveyard`, `bead`, `issue graph`, `review round`, `quiet round`, `consensus`, `vote`, `contribution score`, `swarm`.

Legitimate when the artifact is requested, required for compliance or recovery, used across sessions, or consumed by a named decision.

Warning combinations:

- the same completion audit or checklist is rebuilt every turn;
- a report restates source material without changing action;
- every reviewer must produce a finding;
- reviewers vote or average correlated judgments as if independent;
- a narrow task spawns a swarm, recursive review, or repeated quiet rounds;
- issue prose, dependencies, or graphs are optimized while ready work waits;
- a handoff is written for nobody;
- documentation is counted as product progress when the behavior is absent;
- the artifact's main consumer is another artifact.

Countermoves:

- reuse the existing issue, log, test, or version history;
- allow `NO DISTINCT FINDING`;
- deduplicate findings by mechanism and evidence;
- cap review to the changed files and behavior, plus one independent check when warranted;
- make the next implementation action dominate;
- write a handoff only when another session or person will actually receive it.

## Counterfeit progress patterns

- **Gate self-weakening:** edit the checker or exemption until the work passes.
- **Proof inflation:** present fixture, mock, capture, static inspection, or inserted data as live verification.
- **Golden regeneration:** update expected output instead of fixing the regression.
- **Commit pumping:** split trivial changes or placeholders into visible activity.
- **Tautological testing:** assert whatever the implementation already returns.
- **Easy-work farming:** close safe tasks while high-value blocked or difficult work starves.
- **False closure:** close work before the behavior or consumer exists.
- **Scope splitting:** count types, implementation, and tests as separate delivered capabilities.
- **Spec editing as delivery:** weaken or polish the plan instead of implementing it.
- **Conformance metastasis:** add checks not tied to an observed defect, consumer, or release decision.
- **Dependency smuggling:** bypass a constraint with a wrapper or shim while claiming compliance.
- **Demo-path hardcoding:** special-case the showcased subject and call the system general.
- **Finding inflation:** invent low-value objections because every reviewer is rewarded for contributing.
- **Completion theater:** map every item to a status or receipt while the real outcome remains absent.

## Rationalizations

"It may be useful later." Require a plausible consumer and re-entry condition. Version history can preserve the idea without runtime cost.

"More confidence is always better." Confidence has marginal cost. Name the decision that another check could change.

"We already spent a week on it." Sunk cost is not a consumer.

"The user said be thorough." Thoroughness applies to the requested outcome and its real risks, not unlimited adjacent machinery.

"The tests are green." State which fault each test can detect and which runtime boundary remains untested.

"Every item is accounted for." Accounting is not implementation.

"One more review cannot hurt." It consumes time and can create false findings. Name the distinct uncertainty it addresses.

"This is the established process." Establishment does not prove consumption. Show what breaks if it is removed.

"Instrumentation is cheap." Collection, storage, cardinality, interpretation, alerts, dashboards, and maintenance are costs even when emitting one metric is easy.

"Deleting it wastes the work." Keeping inert machinery taxes every future reader and operator.

## Repository-specific countermeasures

Do not paste a universal policy into every repository. Inspect how this project can counterfeit progress, then encode only observed or credible mechanisms.

For each countermeasure, require:

1. the local proxy being gamed;
2. the real outcome displaced;
3. an observable warning sign;
4. the smallest countermeasure;
5. the consumer of that countermeasure;
6. evidence that anything real has traversed it.

If item 5 is missing, write an annotation or delete the proposed rule. If item 6 remains empty after a realistic opportunity, reassess whether the machinery should exist.
