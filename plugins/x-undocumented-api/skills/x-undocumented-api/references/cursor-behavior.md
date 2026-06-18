# Cursor Behavior

Use this reference for X web timeline pagination, cursor stability, overlap, dedupe, and fan-out planning.

## Mental Model

Most X web timelines are cursor-led moving frontiers, not stable tables. A cursor is request state returned by X, useful for continuing a traversal. It is usually not a durable shard boundary.

Treat cursor behavior as operation-specific. `Followers`, `SearchTimeline`, `UserTweets`, lists, home timelines, and community timelines may all differ.

## Cursor Locations

Timeline instructions commonly include:

- `TimelineTimelineCursor` with `cursorType: "Top"` for newer/previous direction
- `TimelineTimelineCursor` with `cursorType: "Bottom"` for older/next direction
- occasional operation-specific cursor wrappers or nested cursor entries inside modules

Preserve:

- operation name
- variables
- request cursor
- returned `Top` cursor
- returned `Bottom` cursor
- emitted item IDs in order
- item count
- first and last `sortIndex`
- observation time

## Page Fingerprints

For comparing pages, fingerprint normalized emitted item IDs in emitted order:

- empty page: `empty:v1`
- non-empty page: `sha256:v1:<hex>`

Do not fingerprint raw response JSON, cursor text, or unstable object order.

## Stability Caveats

Observed timeline behavior can include:

- serial traversal works within one run
- top-of-list snapshots vary across time
- saved cursors decay or become invalid
- two different cursor strings can return identical item sequences
- the same starting point across accounts can overlap heavily
- cursor continuation can depend on the viewing account or session; a later-page cursor that works on one account can fail on another
- short bursts of `RUNNER_TERMINATED` / `runner_terminated` can be process-rollover artifacts from in-flight work rather than endpoint behavior; isolate restart windows before treating them as pagination evidence
- requested `count` can be ignored
- effective lane yield can diverge sharply from raw page count when local filtering sits above a broad timeline operation
- `sortIndex` is useful evidence but not a caller-controlled range boundary

## Fan-Out Guidance

Before using cursors for parallel collection:

1. Test whether derived starting cursors produce disjoint pages.
2. Measure overlap by item ID sequence, not by cursor text.
3. Keep global dedupe by item ID.
4. Keep one serial traversal as a correctness anchor for important crawls.
5. When probing search or user-corpus lanes, compare rotating-account continuation against one pinned-account traversal before concluding the cursor itself is bad.
6. Re-check behavior after endpoint or query-ID drift.
7. If stop reasons spike immediately after a worker restart, separate that rollover interval from the steady-state sample before drawing endpoint conclusions.

Avoid treating same-start cursor requests as partitions; they can spend requests on duplicate pages.

## Evidence Standard

Before documenting a cursor claim:

- capture repeated observations
- include exact operation, variables, auth mode, date/time, and result counts
- compare item IDs and sort boundaries
- distinguish one-off clues from repeated behavior
- document access scope and rate-limit context

Strong signal:

- raw versus emitted item counts tracked per page when local filtering is involved
- exact same item sequence when expected
- stable page fingerprint reuse
- preserved relative order
- consistent next cursor across repeated anchored probes

Weak signal:

- similar items with different ordering
- divergence after one or two pages
- behavior seen under only one access mode

No viable partition signal:

- low overlap where high overlap was expected
- high overlap where disjoint pages were expected
- cursor reuse failures after short delays
