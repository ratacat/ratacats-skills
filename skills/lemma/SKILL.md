---
name: lemma
description: Answer a hard question by building a persistent graph of atomic claims, each given a 0-1 credence by Jev from a shared evidence ledger. Keeps false and unexamined claims. Use for research questions, codebase questions, hypothesis testing, or any claim that needs careful, skeptical support.
metadata:
  category: tools
  keywords:
    - research
    - hypothesis
    - evidence
    - credence
    - epistemics
    - jev
  blurb: Breaks a hard question into a persistent graph of small claims, links each to evidence, and has Jev give every claim a 0-1 credence; false and open claims stay on record.
---

# Lemma

A question becomes a pyramid of claims. The root is the claim we want to settle. Each claim below it holds the root up or pulls it down. Evidence lives in its own ledger and links to claims. Jev gives each claim one number, its credence. The agent finds evidence, splits claims, and links them. Nothing is deleted.

## Stance

- You do not know the answer. Act as if you do not.
- "Experts say X" is evidence that experts say X. It is not evidence of X. Record who says it and what they could observe.
- Look for evidence against a claim before evidence for it.
- Ask how much more expected the evidence is if the claim is true than if a rival is true. Evidence that every rival also predicts is weak.
- Compare with a base rate. "Only 2 kings were found in their pyramids" means little until you know how often kings are found in tombs that are certainly tombs.
- To state a rate, count the cases into one tally evidence item. Jev weighs examples; it does not count them.
- Prefer a physical find, a primary document, or a measurement over a summary of one.
- Many claims will never be proven. A credence is the result, not a step toward proof.
- A false claim is a result. Keep it. An unexamined claim is a gap. Name it.
- Do not score claims in your head. Jev scores. You gather, split, and link.

## Graph

File: `~/.lemma/<name>.json` (set `LEMMA_HOME` to change the folder).

```json
{
  "name": "pyramids-tombs",
  "question": "Were the pyramids used as tombs?",
  "root": "n0",
  "claims": {
    "n0": {"text": "...", "evidence": [{"id": "e1"}]}
  },
  "evidence": {
    "e1": {"source": "citation or URL", "says": "...", "origin": "the underlying source, e.g. Lehner 1997", "kind": "find|primary|measurement|secondary|testimony", "access": "how the source could know this"}
  },
  "edges": [{"from": "n1", "to": "n0", "type": "required_by"}]
}
```

- A claim can be true or false. Write a question as the claim that would answer it.
- Say "as a rule" or "some" when you mean it. A claim about every case falls to one exception.
- To reword a claim, push the old text onto its `was` list. Do not delete it.
- One evidence item is one finding from one source. Link it to every claim it bears on.
- `origin` names the underlying source, not the website. A Wikipedia page that summarizes Lehner has origin Lehner. `next` warns when half the evidence under a claim shares one origin.
- Edge types, read `from <type> to`:
  - `required_by`: if `from` is false, `to` falls. Code caps `to` at the credence of `from`. Use it only for a necessary premise that a rival disputes.
  - `sufficient_for`: if `from` is true, `to` is true. Code raises `to` to at least the credence of `from`. Use it for "one case proves it".
  - `supports`, `undermines`: evidence-like weight. Jev weighs these.
  - Rival hypotheses link to the root with `undermines`.
- A claim can have many parents. The graph is a DAG, not a tree.

## Credence

One number from 0 to 1. 0 = established false, 0.5 = no lean, 1 = established true. Thin or second-hand evidence cannot reach the ends. So the strength of the evidence is part of the number. A claim without a judgment shows `open`. `judged.jev` is Jev number before the `required_by` and `sufficient_for` bounds.

Each evidence link also gets `bears`, from -1 (strongly undermines) to 1 (strongly supports).

## Loop

1. **Frame.** Write the root claim and the strongest rivals. Link them. Settling the root must answer the question as asked. Check for a shift between intent and outcome, possible and actual, some and all, or one case and the rule. `next` prints the question above the root on every loop so drift stays visible.
2. **Next.** Run `python3 lemma.py next <name>`. It prints the shape of the graph and a ranked list of steps. Do step 1. Run `next` again. Repeat.
3. **Report.** When you stop, show the graph. List what is probably true, what is probably false, and what is still open.

`next` gives four actions:

- **research**: find evidence for a claim. Search for evidence against it first. Prefer a find, a primary document, or a measurement. Read sources yourself; do not trust search summaries.
- **break down**: split a claim into smaller claims below it. The `atomic` score is a hint. You decide when a claim is small enough: one observation or one source could settle it.
- **expand**: add claims the graph is missing: premises, rivals, or a link for an orphan claim.
- **judge**: get a new credence from Jev after the evidence or the claims below it change.

Ranking: judge first (deepest claims first), then by leverage on the root and closeness to 0.5. `required_by` passes full leverage, `sufficient_for` passes the room its parent has left to rise, `supports` and `undermines` pass half. You can do a different step if you have a reason. Say what the reason is.

## Commands

`lemma.py` is in this skill's folder.

```bash
python3 lemma.py next <name> [k]   # graph shape and the top k steps (default 5)
python3 lemma.py judge <name> <id> # one Jev call: credence, atomic, and bears for each linked evidence item
python3 lemma.py show <name>       # the pyramid, from the root down
```

Needs `TYPESAFE_API_KEY`. For large graphs, judging many claims in parallel with Python's `ThreadPoolExecutor` is a possible future step.
