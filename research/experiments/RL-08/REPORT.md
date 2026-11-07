# RL-08 report: inherited checks and the chain's cost per layer (H-08), 2026-11-05

**Asked.** Do some inherited checks never refuse while others refuse real drift (H-08a)? Is the chain's cost per
layer concentrated in a small set of validators (H-08b)?

**Measured.** The published compaction cost report (M1's run of 2026-10-21, in harness-onion's `architecture/` at
main afee03b9): CPU per argv command of the verify (64), per test file (141) and per test (1,594) inside argv 63 (the
chain identity test), per-layer counters for 60 bridged scaffold layers (slots 192-254), and authority reads per
path (88 files). Concentration was measured as the top-decile share and the Gini coefficient, with the bounds fixed
before the run (top decile at or above 50 percent for PASS, below 30 percent for FAIL).

| dimension | units | top decile share | Gini | largest |
|---|---|---|---|---|
| CPU per test file in argv 63 | 141 | 0.34 | 0.48 | one native-profile test file at 0.06 |
| authority bytes read per layer | 60 | 0.31 | 0.53 | layer 02 at 0.12 |
| authority reads per layer | 60 | descriptive | see ledger | |
| authority reads per path | 88 | top 5: see ledger | 0.43 | one backend-profile authority at 0.06 |
| CPU per argv command (seen before the freeze) | 64 | top 1: 0.86 | 0.91 | argv 63 |

**Verdict: UNRESOLVED** (RESULTS.json). H-08a cannot be run: the report records cost, not refusals, and no
per-check refusal history exists in any record the lab can read. H-08b falls between its bounds on both gated
measures: within the chain identity test the cost is moderately spread across files and layers (Gini about 0.5,
top decile a third), not held by a small set. The one sharp concentration is one level up: the chain identity test
is 86 percent of the whole verify's CPU (2,581 of 3,282 s), and a third of that is the generic scaffold; both were
seen while reading the report's structure and are reported, not gated.

**What it means.** Cutting the chain's cost by removing a few validators would not work: the long tail of layers
and test files carries most of it. The levers are the ones M1 already named (the generic scaffold, the argv-63
share), which is consistent with PERF-045's cuts targeting the outer suite rather than single layers.

**What it does not show.** Which checks ever refused (H-08a); any cost after the compaction (this is M1's report
of the pre-compaction run; the A/B record's keys were read, not its values); wall time, which the argv totals
give at 1,131 s for the whole verify but which is not per layer.

**Proposal.** None. For H-08a the lab would need a per-check refusal history: an input to DECISION-LEDGER-001's
note stream only if the owner wants refusals recorded per check, which the lab does not propose now.
