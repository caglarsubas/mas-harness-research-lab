# RL-13 report: the interchange mapping (H-22), 2026-11-05

**Asked.** Can the verdict-ledger, run-manifest and run-event-log contracts be emitted by another platform from
their published schemas alone (H-22a)? Is the multi-agent span and metric set a coherent extension of the GenAI
semantic conventions (H-22b)?

**Measured.** From the published contracts at harness-onion main afee03b9: the three schemas and their vectors,
the run-events README's mapping section. The lab wrote one minimal instance per contract from each schema's required
set and types (no vector copied) and validated it with its own standard-library checker; it also checked the
operation coverage of the contract's OpenTelemetry mapping and classified every dotted attribute name it uses.
Every convention name is from the lab's knowledge, not fetched, version unverified; the contract pins the
conventions repository at a commit the lab cannot reach.

| check | result |
|---|---|
| three emitter instances validate | PASS: ledger at once; manifest and event log after two logged repairs each |
| checker sanity on the contracts' positives | 15 of 16 ledger positives pass; one (L13) refused by the lab's checker, unexplained; manifest positives not run (kind labels unmapped) |
| every run-event operation has a span or point-event mapping | PASS, 11 of 11 |
| names: known convention names / unconfirmable span-type ids / local extensions / unknown | 9 / 3 / 6 / 0; no overlap with the 16 never-emitted names |

**Verdict: PASS** (RESULTS.json) with two unresolved checks named: the lab's checker refuses one contract positive
it cannot explain, and the pinned conventions are unverified by the lab. The interchange surfaces are documented
in MAPPING.md: what an emitter must produce, including the four things the schema text alone did not make obvious
to the lab on first writing (object-valued model and harness, non-empty lock arrays, the seed object, the
per-branch attribute sets), all of which the schema does state.

**What it means.** The three contracts are emittable from their text, and the event log's conventions mapping is
complete over the operation set with its local extensions declared. What the lab cannot say is whether the three
span-type identifiers match the pinned conventions commit; the contract's own builder checks that against seven
pinned files, which is the contract's evidence rather than the lab's.

**What it does not show.** No consumption test (another platform reading the records); no check of the pinned
conventions; the MAS metrics and MAST annotation schemas were not instantiated; the lab's checker is not the
contract's validator.

**Proposal.** None. H-23 (the topology and coordination contracts implementable by another runtime) and H-24 (the
crosswalk method repeatable) remain as paper items for a later session.
