# Lemma

Answer a hard question by breaking it into a graph of small claims. Each claim links to evidence in a shared ledger. [Jev](https://docs.typesafe.ai/) gives each claim one credence from 0 (established false) to 1 (established true), and gives each evidence link a `bears` score from -1 to 1. Claims that turn out false and claims that nobody has examined yet stay in the graph, so the next session knows what is settled and what is still open.

Inspired by Arbor's hypothesis tree ([arXiv 2606.11926](https://arxiv.org/abs/2606.11926)). Arbor optimizes an artifact. Lemma estimates what is true.

## Good fits

- "Were the pyramids actually used as tombs?"
- "Why does this service drop requests under load?" as a graph of hypotheses about the codebase.
- A research question where the answer may never be proven, only weighed.

## Install

```text
/plugin marketplace add ratacat/ratacats-skills
/plugin install lemma@ratacats-skills
```

```sh
npx skills add ratacat/ratacats-skills --skill lemma
```

## Setup

`TYPESAFE_API_KEY` ([console.typesafe.ai](https://console.typesafe.ai/)) and Python 3. `lemma.py` uses only the standard library. Graphs are saved in `~/.lemma/`.
