# Jev

Build features on [TypeSafe's](https://docs.typesafe.ai/) Jev System One model: send application state plus typed questions, get structured judgments back — a chosen option, a probability-weighted score, or a yes/no probability — with calibrated confidences your code branches on directly. No text generation to parse.

The skill teaches the agent the HTTP contract, both SDKs, question-design rules (atomic judgments, state-vs-questions separation, criteria writing), confidence-gated routing, and when to read the live docs and cookbooks instead of guessing.

## Good fits

- "Replace this fragile regex/parser step with a typed classification call."
- "Route inbound support messages to a team and escalate uncertain ones."
- "Score these documents on several dimensions and rank them in code."
- "Add LLM guardrails: jailbreak screening and harm scoring."
- "Turn this prompt-and-parse LLM call into structured decisions."

## Install

From this local checkout, point a compatible agent at [SKILL.md](SKILL.md).

Install through either supported route:

```text
/plugin marketplace add ratacat/ratacats-skills
/plugin install jev@ratacats-skills
```

```sh
npx skills add ratacat/ratacats-skills --skill jev
```

## Setup

Calling the API needs a TypeSafe key in `TYPESAFE_API_KEY` ([console.typesafe.ai](https://console.typesafe.ai/)) and one of `pip install typesafe-sdk` (Python ≥3.10) or `npm install @typesafe-ai/sdk` (Node ≥20). The Playground needs only a login. Reading docs and designing questions needs neither.
