#!/usr/bin/env python3
import json, os, sys, urllib.request
from datetime import datetime
from pathlib import Path

HOME = Path(os.environ.get("LEMMA_HOME", Path.home() / ".lemma"))
SETTLED = 0.2
SECONDHAND = {"secondary", "testimony"}

CREDENCE = {
    "type": "score",
    "instructions": "How probable `claim` is, judged only from `evidence` and `linked_claims` in state, not from outside knowledge. A source that asserts something is not proof of it unless the source had direct access to the fact. Thin or second-hand evidence cannot reach the ends of the scale.",
    "criteria": [
        "Established false: direct, independent evidence rules the claim out",
        "Probably false: good evidence against it and little for it, from direct observation or from several independent sources that report observations",
        "Leans false: some evidence against it, but thin, or one second-hand source",
        "No lean: no evidence, evidence that is balanced, or only bare assertion",
        "Leans true: some evidence for it, but thin, or one second-hand source",
        "Probably true: good evidence for it and little against it, from direct observation or from several independent sources that report observations",
        "Established true: direct, independent, repeated observation confirms the claim",
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
        headers={"Authorization": f"Bearer {os.environ['TYPESAFE_API_KEY']}", "Content-Type": "application/json", "User-Agent": "lemma"},
    )
    return json.load(urllib.request.urlopen(req))["answers"]


def judge(name, cid):
    g = load(name)
    c = g["claims"][cid]
    ev = {ref["id"]: g["evidence"][ref["id"]] for ref in c["evidence"]}
    questions = {"credence": CREDENCE, "atomic": ATOMIC}
    for eid in ev:
        questions[f"bears_{eid}"] = {"type": "score", "instructions": f"How `evidence.{eid}` bears on `claim`. Evidence that would be just as expected if the claim were false does not bear on it.", "criteria": BEARS}
    a = jev({"claim": c["text"], "evidence": ev, "linked_claims": linked_claims(g, cid)}, questions)
    for ref in c["evidence"]:
        ref["bears"] = round(a[f"bears_{ref['id']}"]["score"] / 2 - 1, 2)
    raw = round(a["credence"]["score"] / 6, 2)
    bound = lambda kind: [credence(g["claims"][e["from"]]) for e in g["edges"] if e["to"] == cid and e["type"] == kind and credence(g["claims"][e["from"]]) is not None]
    j = {
        "at": datetime.now().isoformat(timespec="milliseconds"),
        "credence": min([max([raw, *bound("sufficient_for")]), *bound("required_by")]),
        "jev": raw,
        "confidence": a["credence"]["confidence"],
        "atomic": a["atomic"]["noul"],
    }
    c.setdefault("history", []).append(j)
    c["judged"] = j
    save(name, g)
    print(json.dumps({"claim": cid, **j, "evidence": {r["id"]: r["bears"] for r in c["evidence"]}}))


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


RESEARCH = "Search for evidence against it, then for it. Add items to the ledger, link them, then judge."
EXPAND = "Add the missing claims: premises it rests on, or rivals that would undermine it. Link them with edges."
BREAK_DOWN = "Replace it with smaller claims under it, linked with `required_by` or `supports` edges."


def depths(g):
    d = {g["root"]: 0}
    queue = [g["root"]]
    for cid in queue:
        for e in g["edges"]:
            if e["to"] == cid and e["from"] not in d:
                d[e["from"]] = d[cid] + 1
                queue.append(e["from"])
    return d


def leverage(g):
    lev = {g["root"]: 1.0}
    changed = True
    while changed:
        changed = False
        for e in g["edges"]:
            if e["to"] in lev:
                weight = {"required_by": 1, "sufficient_for": 1 - (credence(g["claims"][e["to"]]) or 0)}.get(e["type"], 0.5)
                v = lev[e["to"]] * weight
                if v > lev.get(e["from"], 0):
                    lev[e["from"]] = v
                    changed = True
    return lev


def origin(e):
    return e.get("origin") or e["source"].split(",")[0]


def support_evidence(g, cid, seen=None):
    seen = seen if seen is not None else set()
    if cid in seen:
        return set()
    seen.add(cid)
    ids = {r["id"] for r in g["claims"][cid]["evidence"]}
    for e in g["edges"]:
        if e["to"] == cid and e["type"] != "undermines":
            ids |= support_evidence(g, e["from"], seen)
    return ids


def steps(g, name):
    claims, d, lev = g["claims"], depths(g), leverage(g)
    judge = lambda cid: f"Run `lemma.py judge {name} {cid}`."
    if not any(e["to"] == g["root"] and e["type"] == "undermines" for e in g["edges"]):
        yield 3, g["root"], "expand", "the root has no rival", "Add the strongest rival hypothesis with an `undermines` edge to the root."
    for cid, c in claims.items():
        if cid not in d:
            yield 3, cid, "expand", "not connected to the root", "Link it to the claim it bears on."
            continue
        j, cr = c.get("judged"), credence(c)
        kids = [e["from"] for e in g["edges"] if e["to"] == cid]
        ev = [g["evidence"][r["id"]] for r in c["evidence"]]
        reach = lev[cid]
        doubt = 1 if cr is None else 1 - abs(2 * cr - 1)
        if j and (any("bears" not in r for r in c["evidence"]) or any((claims[k].get("judged") or {}).get("at", "") > j["at"] for k in kids)):
            yield 2 + d[cid] / 100, cid, "judge", "evidence or linked claims changed after the last judgment", judge(cid)
        elif not j and (ev or any(credence(claims[k]) is not None for k in kids)):
            yield 2 + d[cid] / 100, cid, "judge", "has evidence or judged claims below it, but no credence", judge(cid)
        elif not ev and not kids:
            yield reach, cid, "research", "no evidence and no claims below it", RESEARCH
        elif j and SETTLED < cr < 1 - SETTLED:
            if kids and all(credence(claims[k]) is not None for k in kids):
                firm = all(not SETTLED < credence(claims[k]) < 1 - SETTLED for k in kids)
                yield reach * doubt * (1 if firm else 0.5), cid, "expand", f"credence {cr:.2f} is not settled; the claims below it may not be enough", EXPAND
            elif not kids:
                yield reach * doubt, cid, "research", f"credence {cr:.2f} is not settled", RESEARCH
        if j and j["atomic"] < 0.5 and not kids:
            yield reach * 0.8, cid, "break down", f"atomic {j['atomic']:.2f}: it may assert more than one thing", BREAK_DOWN
        if ev and all(e["kind"] in SECONDHAND for e in ev):
            yield reach * 0.6, cid, "research", "all linked evidence is second-hand", "Trace the sources back to a find, a primary document, or a measurement."
        under = [origin(g["evidence"][i]) for i in support_evidence(g, cid)]
        top = max(set(under), key=under.count) if under else None
        if kids and len(under) >= 4 and under.count(top) * 2 >= len(under):
            yield reach * 0.5, cid, "research", f"{under.count(top)} of {len(under)} evidence items under it trace to {top}", "Find sources independent of that origin."
        bears = [r.get("bears", 0) for r in c["evidence"]]
        if j and ev and (cr >= 1 - SETTLED and min(bears) >= 0 or cr <= SETTLED and max(bears) <= 0):
            yield reach * 0.3, cid, "research", f"credence {cr:.2f} rests on one-sided evidence", "Search for the strongest evidence the other way."


def next_steps(name, k="5"):
    g = load(name)
    crs = [credence(c) for c in g["claims"].values()]
    judged = [cr for cr in crs if cr is not None]
    settled = sum(cr <= SETTLED or cr >= 1 - SETTLED for cr in judged)
    print(f"{name}: {len(crs)} claims ({len(crs) - len(judged)} open, {len(judged) - settled} unsettled, {settled} settled), {len(g['evidence'])} evidence items, depth {max(depths(g).values())}")
    print(f"question: {g['question']}")
    print(f"root [{label(g['claims'][g['root']])}] {g['claims'][g['root']]['text']}")
    print("check: settling the root must answer the question, with no shift between intent and outcome, some and all, or possible and actual.")
    merged = {}
    for pri, cid, action, why, do in sorted(steps(g, name), key=lambda s: -s[0]):
        m = merged.setdefault((cid, action), [pri, [], []])
        m[1].append(why)
        m[2].append(do)
    ranked = sorted(merged.items(), key=lambda kv: -kv[1][0])[: int(k)]
    for i, ((cid, action), (_, whys, dos)) in enumerate(ranked, 1):
        print(f"{i}. {action} {cid}: {g['claims'][cid]['text']}\n   why: {'; '.join(whys)}\n   do: {' '.join(dos)}")


if __name__ == "__main__":
    cmd, *args = sys.argv[1:]
    {"judge": judge, "show": show, "next": next_steps}[cmd](*args)
