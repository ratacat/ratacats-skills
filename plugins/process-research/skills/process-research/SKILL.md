---
name: process-research
description: Use when working in the Polymarket research repo and you need to process queued targets from spinal_cord.jsonl, especially for batch queue runs or periodic research sweeps.
---

# Process Research Queue

You are the research queue processor. Pull queued targets from `spinal_cord.jsonl`, prioritize the best candidates, run research, update the ledgers, and validate the linkages.

## Scope

Use this skill when:
- The user wants to process or clear the queued research backlog
- The repo has many `queued` spinal-cord entries and needs systematic triage
- You want a repeatable intake-to-research workflow with ledger validation

Do not use this skill for:
- A single already-selected market where direct research is faster
- Pure intake runs that only append `queued` entries
- General browsing or one-off market questions without ledger updates

## Step 1 - Read The Queue

Read `spinal_cord.jsonl` and extract entries where `status == "queued"`.

Prefer robust parsing over regex when possible. If you only need a quick scan, `rg` is fine. If you need exact selection, parse the JSONL.

Examples:

```bash
rg '"status":"queued"|\"status\": \"queued\"' spinal_cord.jsonl
python3 - <<'PY'
import json
from pathlib import Path
for line in Path("spinal_cord.jsonl").read_text().splitlines():
    if not line.strip():
        continue
    obj = json.loads(line)
    if isinstance(obj, dict) and obj.get("status") == "queued":
        print(obj["id"], obj.get("event_title"))
PY
```

If there are zero queued entries, report that the queue is empty and stop.

## Step 2 - Exclude Already-Researched Targets

Skip any queued target that already has dedicated research.

That means:
- The spinal-cord entry's `ganglia` array contains a non-intake research run, or
- `ganglia.jsonl` already has an entry whose `spinal_cord_ids` contains the target and whose slug is a dedicated market/topic slug rather than a bulk intake slug

Intake-only runs do not count as dedicated research. Examples that should usually be treated as intake-only:
- `polymarket-election-intake-*`
- `polymarket-geopolitics-intake-*`
- other obvious scanner / bulk queue slugs

When uncertain, inspect the ganglia entry's `title`, `slug`, and `thesis`.

## Step 3 - Select Up To 5 Targets

From the remaining unresearched queue, select up to 5 using this priority order:

1. Nearest settlement date
2. Highest volume
3. Shortest lockup

Use the spinal-cord snapshot data when available. If snapshot data is stale or incomplete, refresh from the market page or PMXT before final selection.

Log:
- Which 5 you selected
- Why they won priority
- Which urgent candidates were skipped and why

## Step 4 - Classify Each Target

Choose the playbook from the market type:

| Type | Playbook |
| --- | --- |
| Election / political | `playbook/election-research.md` |
| Economics / macro / commodities | `playbook/economics-research.md` |
| Other / mixed | `playbook/economics-research.md` by default |

Also read:
- `AGENTS.md`
- `playbook/prediction-ledger.md`

When working in this repo:
- Use `colgrep` as the default code/document search tool
- Use PMXT for Polymarket/Kalshi market data when order book or market refresh is needed
- Use `exa-cli` for web research per repo instructions

## Step 5 - Research Execution

For each selected target:

1. Read the spinal-cord entry in full
2. Read the relevant playbook
3. Check for prior ganglia entries for the same slug or obvious predecessor topic
4. Research the market thoroughly
5. Save the artifact under the correct `research/` subfolder
6. Append a new `ganglia.jsonl` entry
7. Append `predictions.jsonl` entries if you have contract-level fair values
8. Update the touched spinal-cord entry:
   - `status` -> `researched`, `passed`, `flagged`, or `positioned`
   - add the new ganglia ID
   - append a fresh snapshot

Do not modify unrelated JSONL entries.

## Step 6 - Parallelism Rule

If the user explicitly asked for delegation, sub-agents, or parallel agent work in the current request, you may spawn up to 5 sub-agents in parallel, one per selected target.

If the user did not explicitly authorize delegation in the current request:
- Do the work locally, or
- Process sequentially in batches without spawning sub-agents

When sub-agents are allowed, each sub-agent prompt should include:
- The full spinal-cord JSON entry
- The relevant playbook text or the exact sections needed
- The AGENTS research-workflow sections
- The prediction-ledger rules if forecasts may be published
- Existing ganglia context for the same slug
- A strict instruction to edit only the files required for that target

## Step 7 - Validation

After all target work is done, validate each touched target.

### Ganglia checks

- New ganglia entry exists
- ID format is valid: `{slug}-{NNN}`
- `spinal_cord_ids` contains the touched spinal-cord ID
- `artifact_path` exists
- `signals` is non-empty
- `summary` and `thesis` are non-empty

### Spinal cord checks

- Status changed away from `queued`
- `ganglia` contains the new ganglia ID
- A fresh snapshot was appended

### Prediction checks

If fair values were produced:
- New `predictions.jsonl` entries exist
- `ganglia_id` exists in `ganglia.jsonl`
- `spinal_cord_id` exists in `spinal_cord.jsonl`
- `prediction_key`, `series`, `forecast`, and `trade` are present

### Cross-reference integrity

- Every ID in `ganglia[].spinal_cord_ids` exists in `spinal_cord.jsonl`
- Every `ganglia_id` referenced by predictions exists
- No duplicate ganglia IDs were created

## Step 8 - Report

For each processed target, report:

1. Title
2. Market URL
3. A paragraph on what the research found
4. A paragraph on trade assessment: edge, liquidity, spread, lockup, and take/watch/pass
5. Any published predictions: contract, market price, fair value, stance, edge, trade rating

Then end with a compact queue summary:

```text
Research Queue Processing - YYYY-MM-DD
Processed: N | Researched: N | Passed: N | Errors: N
Validation: X/Y passed | Z issues found
```

If validation fails anywhere, list the exact issue and file so it can be fixed manually.

## Error Handling

- If the queue is empty, stop and report that clearly
- If a playbook is missing, stop and report which one
- If one target fails, continue with the others when safe
- If a run produces incomplete ledger updates, flag it explicitly instead of silently accepting partial state
