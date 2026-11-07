# RL-01 report: the verify-time dataset (H-07), 2026-11-04, H-07b added 2026-11-05

**Asked.** Is verify-time growth since slot 255 explained by host load and the outer suite's test count rather than
by the layer count (H-07a)? Is worker wall time at K 8 non-inferior to K 6 (H-07b; amendment v1.1 of 2026-11-05)?

**Measured.** 27 verify runs of harness-onion PRs 207-232 (slots 253-278) from the verifier's published check-run
summaries (I2, sha256 808bf769), joined to the merge-decision records (I1, set digest b3370227) for the slot per PR.
23 rows entered the preregistered fits (PREREG v1 f0bdb2f7): 1 run has no test count (the capped, failed run of PR 232)
and 3 have no slot in their merge-decision record (PRs 214-216). Wall time ran from 726 s to 1,116 s (median 935 s)
on the rows used; load_run_mean from 4.6 to 11.9; tests_passed from 14,942 to 26,030.

| fit (standardised predictors) | load bL | test count bC | layer count bK | R² |
|---|---|---|---|---|
| T (s) | +49.5 [17.0, 85.1] | −25.9 [−194.3, 153.0] | +99.9 [−75.9, 265.1] | 0.63 |
| log T | +0.054 [0.018, 0.095] | −0.006 [−0.198, 0.199] | +0.088 [−0.111, 0.273] | 0.62 |

Intervals: PR-clustered percentile bootstrap, 1,000 resamples, seed 20261104 (run record `runs/run-001.md`).

**Verdict.** H-07a **PASS by the preregistered gate**: bK's interval includes zero in both fits and bL's excludes
zero with the same sign in both. One unresolved check is named in RESULTS.json: test count and layer count are
collinear at r = 0.98 over these 23 runs (both grow one slot at a time), so the gate cannot tell them apart. The
PASS supports "load is a driver on its own" (a one-standard-deviation rise in mean load adds about 50 s); it does
not support "test count rather than layer count". The growth component is one shared trend, worth about 0.64 in
correlation with T for either variable.

**What it does not show.** No causal separation of C from K; no per-worker balance (not in the check runs); no
cap-event analysis (the one capped run left the fit for a missing test count, a conflict between two PREREG rules,
recorded as a finding); nothing about K 8 (H-07b). 23 rows and 3 predictors is a sign test, not a cost model.

**Context, not gated.** 23 of 27 runs ran under OPERATOR_OVERRIDE of the quiet-host gate, 4 under QUIET; gate wait
(gate_after_s) ranged from 0 to 2,997 s. The outer suite's own time (suite_s, 417-678 s) is about half of wall time.

**H-07b (as relayed, not reproduced).** Build-R00's A/B (K 6, K 8, K 6; summary sha256 85ab23bf, kept in R00's
folder; figures relayed by the monitor): worker phase 517.5 s and 540.7 s at K 6 against 472.2 s at K 8 (−10.8 %,
beyond the A-A spread of 23.2 s); wall −10.2 %; summed worker time +18.2 % (3,620 s against 3,004 s and 3,122 s)
at a higher load mean (12.4 against 8.3 and 10.8). The K 8 run is marked non-comparable by R00 (the parent node failed
on the six-worker pins). Verdict **UNRESOLVED**: one run per arm against the preregistered three, and that one run
not comparable. Descriptively the direction is clear and consistent with H-07a: more workers finish sooner on the
wall and spend more summed time, part of it on efficiency cores.

**Proposal.** None from RL-01 alone. A follow-up under a new id (RL-01b) can separate C from K only with inputs that
vary them independently: the compaction cost report's per-layer timings (H-08, BLOCKED on an owner-approved export)
or the K 6 vs K 8 A/B (I3), which varies K at fixed C. The lab recommends reading I3 first (H-07b, amendment v1.1),
then asking the owner for the H-08 export through the monitor if the A/B leaves the question open. This is not a
roadmap shift: PERF-045 / VERIFY-HEADROOM-263 keep their state; the quiet-host rule is consistent with bL.
