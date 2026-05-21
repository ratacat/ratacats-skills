#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "references" / "corpus" / "tech-builder-tweets.jsonl"


def load_rows():
    with CORPUS.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                yield json.loads(line)


def has_label(row, kind, value):
    return value in row.get("labels", {}).get(kind, [])


def main():
    parser = argparse.ArgumentParser(description="Sample the human-tweet-editor corpus.")
    parser.add_argument("--query", help="Case-insensitive substring search over tweet text.")
    parser.add_argument("--domain", choices=["ai", "dev", "builder", "stack"])
    parser.add_argument("--format", dest="format_label")
    parser.add_argument("--bucket", help="Author follower bucket, e.g. small:1k-10k.")
    parser.add_argument("--min-score", type=float, default=0)
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of readable text.")
    args = parser.parse_args()

    query = args.query.lower() if args.query else None
    rows = []
    for row in load_rows():
        if query and query not in row.get("text", "").lower():
            continue
        if args.domain and not has_label(row, "domain", args.domain):
            continue
        if args.format_label and not has_label(row, "format", args.format_label):
            continue
        if args.bucket and row.get("author", {}).get("follower_bucket") != args.bucket:
            continue
        if row.get("metrics", {}).get("selection_score", 0) < args.min_score:
            continue
        rows.append(row)

    rows.sort(key=lambda r: r.get("metrics", {}).get("selection_score", 0), reverse=True)
    rows = rows[: args.limit]

    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
        return

    for i, row in enumerate(rows, 1):
        author = row["author"]
        metrics = row["metrics"]
        labels = row["labels"]
        print(f"{i}. @{author['handle']} ({author['follower_count']:,} followers, {author['follower_bucket']})")
        print(
            f"   score={metrics['selection_score']} rel={metrics['engagement_per_1k_followers']} "
            f"weighted={metrics['weighted_engagement']} labels={','.join(labels.get('domain', []))}/{','.join(labels.get('format', []))}"
        )
        print(f"   {row['text']}")
        print(f"   {row['url']}")
        print()


if __name__ == "__main__":
    main()
