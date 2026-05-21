# Corpus Guide

## Files

- `corpus/tech-builder-tweets.jsonl`: final 2,000-row corpus used for examples and pattern checks.
- `corpus/live-xpool-top-search.jsonl`: live xPool Top-search candidates collected on 2026-05-09.
- `corpus/top-sample.json`: top 40 rows from the final corpus for quick inspection.
- `corpus/manifest.json`: source, filters, formulas, and summary statistics.

## Record Shape

Important fields:

- `text`: tweet text.
- `url`: original X URL.
- `author.follower_count`: author audience size at collection time.
- `author.follower_bucket`: `micro:<1k`, `small:1k-10k`, `mid:10k-100k`, or `large:100k+`.
- `metrics.weighted_engagement`: likes + 2*replies + 1.5*retweets. Live xPool rows also include quote/bookmark weighting.
- `metrics.engagement_per_1k_followers`: relative engagement normalized by follower count.
- `metrics.selection_score`: ranking score used to choose the corpus.
- `labels.domain`: `ai`, `dev`, `builder`, `stack`.
- `labels.format`: `launch`, `build-log`, `project-signal`, `hiring`, `opinion`, `question`, `thread`, `has-link`.

## Sampling

Use `scripts/sample_corpus.py` rather than loading the whole JSONL.

Examples:

```bash
python3 scripts/sample_corpus.py --query "Claude Code" --limit 8
python3 scripts/sample_corpus.py --domain ai --format project-signal --limit 12
python3 scripts/sample_corpus.py --format launch --bucket small:1k-10k --limit 10
python3 scripts/sample_corpus.py --min-score 20 --limit 20
```

## Interpretation

The corpus is evidence, not a style bible. Use it to notice:

- how specific high-performing posts get in the first line
- how authors introduce a project without sounding like a press release
- how much context is enough before the result
- what kinds of personal detail make technical posts feel human

Do not copy exact hooks or phrasings from the corpus into user output.
