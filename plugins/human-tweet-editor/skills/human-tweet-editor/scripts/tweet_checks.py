#!/usr/bin/env python3
import argparse
import json
import re
import sys


AI_TELLS = [
    "unlock",
    "elevate",
    "delve",
    "seamless",
    "robust",
    "game-changer",
    "game changer",
    "cutting-edge",
    "transformative",
    "in today's",
    "not just",
    "whether you're",
]


def checks(text):
    stripped = " ".join(text.split())
    lower = stripped.lower()
    urls = re.findall(r"https?://\S+", stripped)
    hashtags = re.findall(r"#\w+", stripped)
    mentions = re.findall(r"@\w+", stripped)
    tells = [tell for tell in AI_TELLS if tell in lower]
    sentences = [s for s in re.split(r"[.!?]+", stripped) if s.strip()]
    first_line = stripped.split("\n", 1)[0] if "\n" in text else stripped[:140]

    risk = 0
    risk += min(len(tells) * 12, 36)
    risk += 15 if len(stripped) > 280 else 0
    risk += 10 if len(stripped) > 560 else 0
    risk += 10 if len(hashtags) > 2 else 0
    risk += 8 if len(urls) > 1 else 0
    risk += 10 if len(sentences) > 5 and len(stripped) < 600 else 0
    risk += 12 if re.search(r"\b(excited|thrilled) to (announce|share)\b", lower) else 0

    return {
        "characters": len(stripped),
        "urls": len(urls),
        "hashtags": len(hashtags),
        "mentions": len(mentions),
        "sentences": len(sentences),
        "first_line": first_line,
        "ai_tells": tells,
        "ai_voice_risk_0_to_100": min(risk, 100),
        "mechanical_notes": [
            note
            for note in [
                "Over 280 chars; decide whether this should be a long-form post or a thread." if len(stripped) > 280 else "",
                "Multiple links can split attention." if len(urls) > 1 else "",
                "Too many hashtags for a natural builder voice." if len(hashtags) > 2 else "",
                "AI/marketing tells detected: " + ", ".join(tells) if tells else "",
            ]
            if note
        ],
    }


def main():
    parser = argparse.ArgumentParser(description="Mechanical checks for tweet drafts.")
    parser.add_argument("--text", help="Tweet text. If omitted, stdin is used.")
    args = parser.parse_args()
    text = args.text if args.text is not None else sys.stdin.read()
    print(json.dumps(checks(text), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
