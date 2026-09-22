#!/usr/bin/env python3
import json, os, sys, urllib.request
from datetime import datetime
from pathlib import Path

HOME = Path(os.environ.get("LEMMA_HOME", Path.home() / ".lemma"))
SETTLED, SURE = 0.2, 0.6
SECONDHAND = {"secondary", "testimony"}

CREDENCE = {
    "type": "score",
    "instructions": "How probable `claim` is, judged only from `evidence` and `linked_claims` in state, not from outside knowledge. A source that asserts something is not proof of it unless the source had direct access to the fact. Thin or second-hand evidence cannot reach the ends of the scale.",
    "criteria": [
        "Established false: direct, independent evidence rules the claim out",
        "Probably false: good evidence against it and little for it",
        "Leans false: some evidence against it, but thin or second-hand",
        "No lean: no evidence, evidence that is balanced, or only bare assertion",
        "Leans true: some evidence for it, but thin or second-hand",
        "Probably true: good evidence for it and little against it",
        "Established true: direct, independent evidence confirms the claim",
    ],
}
ATOMIC = {
    "type": "noul",
    "instructions": "`claim` asserts exactly one thing, so that one observation or one source could confirm or refute it.",
}
BEARS = [
    "Strongly undermines the claim",
    "Weakly undermines the claim",
    "Does not bear on the claim",
    "Weakly supports the claim",
    "Strongly supports the claim",
]


def path(name):
    return HOME / f"{name}.json"


def load(name):
    return json.loads(path(name).read_text())


def save(name, g):
    path(name).write_text(json.dumps(g, indent=2, ensure_ascii=False) + "\n")


def credence(c):
    return (c.get("judged") or {}).get("credence")


def linked_claims(g, cid):
    return [
        {"relation": e["type"], "claim": g["claims"][e["from"]]["text"], "credence": credence(g["claims"][e["from"]])}
        for e in g["edges"]
        if e["to"] == cid
    ]


def jev(state, questions):
    req = urllib.request.Request(
        "https://api.typesafe.ai/v1/systemone",
        data=json.dumps({"model": "jev-latest", "state": state, "questions": questions}).encode(),
        headers={"Authorization": f"Bearer {os.environ['TYPESAFE_API_KEY']}", "Content-Type": "application/json"},
    )
    return json.load(urllib.request.urlopen(req))["answers"]


def judge(name, cid):
    g = load(name)
    c = g["claims"][cid]
    ev = {ref["id"]: g["evidence"][ref["id"]] for ref in c["evidence"]}
    questions = {"credence": CREDENCE, "atomic": ATOMIC}
    for eid in ev:
        questions[f"bears_{eid}"] = {"type": "score", "instructions": f"How `evidence.{eid}` bears on `claim`.", "criteria": BEARS}
    a = jev({"claim": c["text"], "evidence": ev, "linked_claims": linked_claims(g, cid)}, questions)
    for ref in c["evidence"]:
        ref["bears"] = round(a[f"bears_{ref['id']}"]["score"] / 2 - 1, 2)
    j = {
        "at": datetime.now().isoformat(timespec="seconds"),
        "credence": round(a["credence"]["score"] / 6, 2),
        "confidence": a["credence"]["confidence"],
        "atomic": a["atomic"]["noul"],
    }
    c.setdefault("history", []).append(j)
    c["judged"] = j
    save(name, g)
    if SETTLED < j["credence"] < 1 - SETTLED or j["confidence"] < SURE:
        next_step = "investigate"
    elif ev and all(e["kind"] in SECONDHAND for e in ev.values()):
        next_step = "find primary evidence"
    else:
        next_step = "settled"
    print(json.dumps({"claim": cid, **j, "evidence": {r["id"]: r["bears"] for r in c["evidence"]}, "next": next_step}))


def label(c):
    cr = credence(c)
    return "open" if cr is None else f"{cr:.2f}"


def show(name, cid=None, depth=0, seen=None):
    g = load(name)
    cid = cid or g["root"]
    seen = seen if seen is not None else set()
    c = g["claims"][cid]
    print(f"{'  ' * depth}[{label(c)}] {cid}: {c['text']}  ({len(c['evidence'])} ev)")
    if cid in seen:
        return
    seen.add(cid)
    for e in g["edges"]:
        if e["to"] == cid:
            print(f"{'  ' * (depth + 1)}<{e['type']}>")
            show(name, e["from"], depth + 2, seen)


def frontier(name):
    g = load(name)
    for cid, c in g["claims"].items():
        cr = credence(c)
        if cr is None or SETTLED < cr < 1 - SETTLED:
            print(f"[{label(c)}] {cid}: {c['text']}  ({len(c['evidence'])} ev)")


if __name__ == "__main__":
    cmd, *args = sys.argv[1:]
    {"judge": judge, "show": show, "frontier": frontier}[cmd](*args)
