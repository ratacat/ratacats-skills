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
    "e1": {"source": "citation or URL", "says": "...", "kind": "find|primary|measurement|secondary|testimony", "access": "how the source could know this"}
  },
  "edges": [{"from": "n1", "to": "n0", "type": "required_by"}]
}
```

- A claim can be true or false. Write a question as the claim that would answer it.
- One evidence item is one finding from one source. Link it to every claim it bears on.
- Edge types, read `from <type> to`: `required_by` (if `from` is false, `to` falls), `supports`, `undermines`. Rival hypotheses link to the root with `undermines`.
- A claim can have many parents. The graph is a DAG, not a tree.

## Credence

One number from 0 to 1. 0 = established false, 0.5 = no lean, 1 = established true. Thin or second-hand evidence cannot reach the ends. So the strength of the evidence is part of the number. A claim without a judgment shows `open`.

Each evidence link also gets `bears`, from -1 (strongly undermines) to 1 (strongly supports).

## Loop

1. **Frame.** Write the root claim. Add the strongest rival claims.
2. **Split.** Add claims under each claim. The `atomic` score is a hint. You decide when a claim is small enough: one observation or one source could settle it.
3. **Investigate.** Pick a claim from `frontier`. Search for evidence against it, then for it. Add evidence items and link them. Read sources yourself; do not trust search summaries.
4. **Judge.** `python3 lemma.py judge <name> <id>`. Follow `next`:
   - `investigate`: credence is between 0.2 and 0.8, or Jev is not sure. Get more or better evidence.
   - `find primary evidence`: every linked item is `secondary` or `testimony`.
   - `settled`: move up.
5. **Propagate.** Judge each parent again after its children change.
6. **Report.** Show the graph. List what is probably true, what is probably false, and what is still open.

## Commands

`lemma.py` is in this skill's folder.

```bash
python3 lemma.py show <name>       # the pyramid, from the root down
python3 lemma.py frontier <name>   # open claims and claims between 0.2 and 0.8
python3 lemma.py judge <name> <id> # one Jev call: credence, atomic, and bears for each linked evidence item
```

Needs `TYPESAFE_API_KEY`. For large graphs, judging many claims in parallel with Python's `ThreadPoolExecutor` is a possible future step.
