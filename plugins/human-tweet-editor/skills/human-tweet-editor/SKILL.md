---
name: human-tweet-editor
description: Grade, critique, rewrite, and strengthen tweets or X threads in a natural human voice for tech, AI, developer, startup, product, and builder audiences. Use when Codex is asked to write a high-quality tweet, make a tweet sound less AI-generated, score a tweet, improve hooks, adjust tone, edit launch/build-in-public posts, or compare a draft against a corpus of high-relative-engagement builder tweets.
---

# Human Tweet Editor

## Core Rule

Optimize for a real person saying something specific. Do not optimize for generic virality.

If the draft sounds like content marketing, remove polish before adding tactics. The best outputs should feel observed, situated, and slightly uneven in a human way.

## Workflow

1. Identify the job: grade, rewrite, generate, thread edit, launch post, build-in-public update, or voice cleanup.
2. Run `scripts/tweet_checks.py` on the draft when text is available. Use its output as mechanical evidence, not as the final judgment.
3. Read `references/rubric.md` for the scoring rubric when grading or giving critique.
4. Use the corpus when examples would help:
   - Run `scripts/sample_corpus.py --help`.
   - Sample by query/topic rather than loading all 2,000 records.
   - Prefer examples with high `selection_score`, high relative engagement, and a similar format.
5. Return the most useful artifact first: a grade, a rewrite, or a set of options. Keep explanation short unless the user asks for analysis.

## Scoring

Use a 100-point grade:

- Human voice: 25
- Specificity and evidence: 20
- Hook and opening pressure: 15
- Substance: 15
- Fit for audience: 10
- Engagement affordance: 10
- Mechanics: 5

When grading, include:

- Overall score and one-line verdict.
- 3-5 concrete issues.
- A rewritten version.
- Optional alternates only when materially different.

Do not praise vague qualities. Name the exact words, claims, or structures that are doing work.

## Rewrite Principles

- Preserve the user's actual belief, taste, and level of certainty.
- Prefer concrete nouns, active verbs, and lived details.
- Keep one main idea per tweet.
- Cut throat-clearing: "in today's world", "game changer", "unlock", "revolutionize", "delve", "seamless", "robust", "leverage", "powerful".
- Avoid engagement begging. If adding a question, make it a real question the author might care about.
- Use numbers only when they are real or explicitly framed as placeholders.
- Do not invent metrics, customers, product names, benchmarks, or personal experiences.
- For launch/project tweets, make the object visible in the first line: what was built, for whom, and why it matters.

## Corpus

The skill includes a scored corpus of 2,000 high-relative-engagement tweets in `references/corpus/tech-builder-tweets.jsonl`.

Each row includes:

- tweet text and URL
- author handle, follower count, following count, and follower bucket
- likes, replies, retweets, views, and weighted engagement
- engagement per 1k followers
- domain labels: `ai`, `dev`, `builder`, `stack`
- format labels: `launch`, `build-log`, `project-signal`, `hiring`, `opinion`, `question`, `thread`, `has-link`

Use `references/corpus/manifest.json` for corpus provenance and summary stats. Use `references/corpus-guide.md` for schema and sampling guidance.

## Output Shapes

For a quick grade:

```text
Score: 74/100
Verdict: The idea is good, but it reads like a launch blurb instead of a person noticing a real thing.

Main fixes:
- ...

Rewrite:
...
```

For multiple rewrites:

```text
Option 1 - plainspoken:
...

Option 2 - sharper:
...

Option 3 - founder/build log:
...
```

For a fresh tweet:

```text
Best version:
...

Why this shape:
...
```

## Guardrails

- Do not fabricate social proof.
- Do not overfit to the corpus by copying phrasing from examples.
- Do not quote long tweet corpus passages in user-facing output.
- Do not make every tweet contrarian.
- Do not default to threads. Use a thread only when the idea has multiple real steps, examples, or receipts.
