---
name: jev
description: Build with Jev, TypeSafe's System One model — fast structured judgments (Choice, Score, Noul) that code consumes directly. Use when replacing fragile parsing or prompt-and-parse LLM steps with typed decisions, or when designing routing, ranking, classification, extraction, verification, or guardrail flows on the TypeSafe API.
metadata:
  category: developer tools
  keywords:
    - typesafe
    - system-one
    - structured-output
    - classification
    - llm-api
    - confidence
    - routing
  blurb: Builds features on TypeSafe's Jev model — typed Choice/Score/Noul judgments with calibrated probabilities that code branches on directly, no text parsing.
---

# Build with Jev (TypeSafe)

Jev is TypeSafe's flagship System One model. You send a `state` and typed `questions`; it returns structured answers — chosen options, probability distributions, confidence — that code can branch, sort, and route on. No text generation, no parsing.

**The live docs are the source of truth.** Discover pages at [docs.typesafe.ai/llms.txt](https://docs.typesafe.ai/llms.txt); append `.md` to any docs URL for clean Markdown. Read the relevant primitive, SDK, or cookbook page as part of the task before writing an integration. Never invent request or response fields beyond what this skill or the live docs state.

## The three primitives

| Need | Question type | Returns |
| --- | --- | --- |
| One of a defined set | `choice` | `choice`, `probabilities`, `confidence` |
| Position on ordered levels | `score` | `score`, `legend`, `probabilities`, `confidence` |
| Is this true? | `noul` | `noul` (0–1, probability of yes) |

Mix all three in one request — every question sees the same state, evaluated independently and in parallel. Adding questions barely changes latency; no context rot.

## HTTP contract

```http
POST https://api.typesafe.ai/v1/systemone
Authorization: Bearer $TYPESAFE_API_KEY
Content-Type: application/json
```

```json
{
  "state": "My running shoes arrived in the wrong size. Can I swap them for a size 10?",
  "model": "jev-latest",
  "questions": {
    "department": {
      "type": "choice",
      "instructions": "Which team should handle this?",
      "criteria": {
        "returns": "Exchanges, refunds, wrong or damaged items",
        "shipping": "Delivery status, delays, lost packages",
        "billing": "Charges, invoices, payment problems"
      }
    },
    "frustration": {
      "type": "score",
      "instructions": "How frustrated the customer appears",
      "criteria": ["Calm, just stating facts", "Frustrated but civil", "Very angry, strong language"]
    },
    "is_urgent": { "type": "noul", "instructions": "The message conveys urgency or time-sensitivity" }
  }
}
```

Answer shapes, keyed by your question ids:

- choice → `{ "type": "choice", "choice": "returns", "probabilities": { … sums to 1 }, "confidence": 0.82 }`
- score → `{ "type": "score", "score": 1.035, "legend": { "0": …, "1": … }, "probabilities": { "0": … }, "confidence": 0.842 }` — `score` is probability-weighted and can land between levels; criteria is 2–10 ordered levels, low to high
- noul → `{ "type": "noul", "noul": 0.91 }` — no confidence field
- top-level `usage`: `{ "input_tokens": N, "output_tokens": N }`

## SDKs

Python (`pip install typesafe-sdk`, ≥3.10) reads `TYPESAFE_API_KEY`, defaults to `jev-latest`:

```python
from typesafe_sdk import Choice, Noul, Score, TypeSafeClient

with TypeSafeClient() as client:
    response = client.system_one(
        state=ticket,
        questions={
            "department": Choice(instructions="Which team should handle this?", criteria={…}),
            "frustration": Score(instructions="How frustrated the customer appears", criteria=[…]),
            "is_urgent": Noul(instructions="The message conveys urgency or time-sensitivity"),
        },
    )
response.answers["department"].choice  # "returns"
```

JavaScript/TypeScript (`npm install @typesafe-ai/sdk`, Node ≥20):

```ts
import { choice, TypeSafeClient } from "@typesafe-ai/sdk";
const client = new TypeSafeClient();
const response = await client.systemOne({
  state: { document: ticket },
  questions: { category: choice("What is this ticket about?", { billing: null, technical: null, other: null }) },
});
response.answers.category.choice;
```

## Question design

- **One snap judgment per question.** If it needs extended reasoning or weighs several factors, decompose: ask each factor separately, combine in code. Change a coefficient, not a prompt, when priorities shift.
- **State carries content; questions carry judgment.** Prefer named JSON fields (`{"ticket": …, "policy": …}`) when context has parts. Reference nested state with backticked paths like `` `ticket.messages[0].text` ``.
- **Question ids are for your code** — the model never sees them. Write complete meaning in `instructions`.
- Choice `criteria` values are descriptions shown to the model — write what separates options; `null` is allowed when a name suffices. Include an `other`/`none` option when the list might not cover every input.
- Score levels must describe concrete situations that stand on their own.
- Noul: phrase so high probability means "yes". ~0.5 means equal yes/no probability, not "medium" — measure degrees with a Score instead. Optional `criteria: {true, false}` clarifies nuance.

## Confidence

`confidence` (0–1) is derived from the answer's probability distribution: concentrated → confident; flat → uncertain. Use it as a second axis:

- High → act automatically. Medium → confirm/flag/gather more. Low → route to a human or fall back.
- Thresholds scale with risk: a read-only action needs a lower bar than a destructive one (approve-transfer at >0.9, show-balance above the ~0.5 floor). Tune on your own data.
- If you only want the best option, take `choice` — don't threshold. Use raw `probabilities` when implementing your own statistical rule. Noul answers carry none.

## Patterns and cookbooks

Start from the behavior the app must show, select, or hand off; work backward to the judgments; keep known rules, exact lookups, and execution in code. [Patterns](https://docs.typesafe.ai/patterns.md): speculative fan-out (many questions, one call, code picks relevant answers), confidence-gated routing, composite scoring, intent routing. [Cookbooks index](https://docs.typesafe.ai/llms.txt) covers reranking, function calling, extraction cascades, citation checks, guardrails, hierarchical classification, entity alignment — read the closest one before inventing a decomposition.

Keep questions and thresholds in one file so humans can review them in one place; agents write mediocre questions — expect collaborative edits. Batch extra questions still costs tokens; measure end-to-end. Typed output guarantees the interface, not truth: validate in your domain. Keep API keys server-side.
