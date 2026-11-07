# RL-04 report: the scaling study, leased versus advisory claims (H-13, H-19 second clause), 2026-11-05

**Asked.** Do leased claims reduce duplicated work relative to advisory claims as agent count grows (H-13b), and do
the campaign's breaches vanish under leased exclusivity at larger counts (H-19's second clause)? Does speedup change
sign between decomposable and sequential tasks (H-13a)?

**Measured.** On the pinned conformance-labs export (RL-03 reproduced it exactly), the harness's ten scaling points
(CENTRAL and DECENTRALIZED topologies at 1, 2, 4, 8 and 16 workers, 5 items per worker) were run under two arms
over the committed 32 seeds: leased (the committed configuration) and advisory (the HELD and VERSION claim checks
bypassed, the harness's own S-D16 control extended to every point). 640 simulation runs, 8 s in all, one GO.
Readings: duplicated-work ratio, completion, lost work, makespan (last merge tick), the safety counters.

| point | workers | leased dup p50 / p95 (ppm) | advisory dup p50 / p95 (ppm) | median paired d | advisory claim overlap (seeds) |
|---|---|---|---|---|---|
| S-C2 | 2 | 0 / 125,000 | 0 / 90,909 | 0 | 0 |
| S-C4 | 4 | 0 / 64,516 | 0 / 47,619 | 0 | 0 |
| S-C8 | 8 | 18,518 / 87,719 | 23,255 / 69,767 | 4,365 | 0 |
| S-C16 | 16 | 28,037 / 86,538 | 21,739 / 44,444 | 1,663 | 0 |
| S-D2 | 2 | 0 / 83,333 | 230,769 / 444,444 | 202,381 | 32 |
| S-D4 | 4 | 0 / 137,931 | 400,000 / 500,000 | 373,303 | 32 |
| S-D8 | 8 | 18,518 / 66,666 | 511,904 / 581,632 | 498,417 | 32 |
| S-D16 | 16 | 26,548 / 78,947 | 629,629 / 653,679 | 600,748 | 32 |

Pooled over the 256 pairs at N ≥ 2: mean difference +206,288 ppm, bootstrap 95 % 176,200 to 234,760. By family:
DECENTRALIZED +415,741 (387,763 to 443,445); CENTRAL −3,166 (−8,332 to +1,621). Leased claim overlap: 0 in all 640
leased runs. Completion stayed at 1,000,000 ppm and lost work at 0 under both arms at every point.

**Verdict.** H-13b **PASS by the preregistered gate** (median paired difference non-negative at every N ≥ 2 point;
pooled interval above zero), with the family split as the finding that matters: the whole effect is the
decentralized topology's, where advisory claims duplicate 23 to 63 percent of work and overlap claims in every
seed, growing with N; in the central topology the two arms are indistinguishable (the coordinator assigns, so the
claim checks have nothing to resolve) and advisory is even slightly lower at p95. H-19's second clause as
preregistered ("lower than advisory") **PASS**; its register wording "vanish" is **false**: under leasing the
decentralized family still duplicates 18,518 to 26,548 ppm at the median at 8 and 16 workers, bounded, not zero.
H-13a is **UNRESOLVED-by-input**: the harness has one task family and no sequential one. Overall UNRESOLVED on
that account; the two runnable claims are supported.

**Makespan, descriptive.** Leasing costs ticks where there is no contention: CENTRAL last-merge p50 139 to 187
leased against 118 to 139 advisory. Where there is contention it pays: DECENTRALIZED 153 to 231 leased against 157
to 298 advisory from N 2 up. Speedup from the committed against-baseline ratios (as reported in the ledger, not
reproduced): CENTRAL 1.1, 2.0, 3.6, 6.8, 13.5 at N 1 to 16, efficiency falling from 1.1 to 0.84.

**What it does not show.** No sequential task family (H-13a); one harness and one host; the advisory arm is a
bypass of two checks, not a designed advisory protocol; the lab's median convention differs from the harness's by
one rank at three points (p95 and max agree), with no effect on the gate's signs.

**Proposal.** RL-04-PROPOSAL, a design read for the visionary through the monitor, not a roadmap shift: a dated
note on MAS-STRATEGY-001 (and for Build-R12's campaign record) that leased exclusivity is a decentralized-topology
requirement and a central-topology cost: the strategy envelope should require leases exactly where claims are
peer-to-peer and may omit them under a single coordinator, where they add about 30 percent to the makespan for no
duplicated-work gain. Evidence state: simulation at pin b4bbea79, 640 runs, seed-paired.
