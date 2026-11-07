# RL-22 report: a clean-room board state machine from the README alone (H-23, coordinator half)

**Asked.** How far does MAS-RA-004's README section A2 alone carry another runtime: does a board state machine
written from it, with VERIFY's ledger rules declared un-modelled, reproduce the record's 32 transcript and 11 binding
vectors at a rate of at least 95 percent? Preregistered as v1 (511c8b66), reviewed once (PASS). Scope: the
coordinator half of H-23; the TopologySpec half is RL-20's (52 of 52); the strategy envelope has no record yet.

**Measured.** Run-001 9c0c21bf; data 1113270e; RESULTS 16915493. 38 of 43 vectors reproduced (88.4 percent): 28 of 32
transcript vectors (every SHAPE, DUPLICATE_ID, MODE and RETRY case, all 4 REPLAY cases and 7 of 8 UNKNOWN_REFERENCE
cases), 10 of 11 binding vectors. The five disagreements, each named and classed: B01, B02, B03 (the three valid
transcripts) and B17 (an UNKNOWN_REFERENCE case) all diverge at the same point: the lab's machine answers ACCEPTED where
the record answers CONCURRENCY_LIMIT. The lab read A2's "fewer than `concurrency` items held" as held by the
acquiring agent; A1 defines `concurrency` as "the most items held at once", board-wide, which the record applies.
One reading of one word; it accounts for 4 of the 5. R05 (binding, expected UNKNOWN_REFERENCE, the lab said BINDING)
turns on MAS-RA-002's record model refusing the manifest, which the lab's binding check validates by schema only: the
declared un-modelled dependency.

**Verdict: UNRESOLVED as preregistered** (between the 70 percent FAIL line and the 95 percent PASS line).

**What it means.** The README carries the coordinator contract to another runtime up to two points to ask its
author: the scope of `concurrency` (A2's wording against A1's definition) and the dependence of the binding and
VERIFY checks on MAS-RA-002's and MAS-RA-001's models, which a runtime must also implement or import. Everything
else in A2 (the operation table, expiry, the arbitration order, retries, the deadline, the transcript codes) replayed
as written, including the reversed-order vector. With the concurrency reading corrected the lab's machine would
reproduce 42 of 43, which would be a PASS; that is a new id, not a re-tune, and the report says so.

**What it does not show.** Nothing about the strategy envelope; the VERIFY binding and history rules were not
re-implemented; one implementation by one reader; the lab knew the vector categories and counts before writing.

**Proposal.** None as a roadmap read. For R00 and the visionary (through the monitor), two documentation inputs to
MAS-RA-004: say in A2's ACQUIRE and ASSIGN rows that the count is board-wide, as A1 defines it; and name, in the
transcript and binding sections, the two outside models a consumer must implement. For H-23: the TopologySpec and
coordinator halves are now measured (52 of 52 and 38 of 43 from the records alone); the strategy half waits for its
record.
