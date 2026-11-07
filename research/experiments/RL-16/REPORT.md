# RL-16 report: the cost model of the signed checkpoint (H-02, cost-model half)

**Asked.** Do the published records support the cost side of H-02: does the attested share of argv 63 re-derive from
R00's cost split at 280, does verify time in the K 6 era grow by about 13 s per slot at equal load as the programme's
report says, and what do the checkpoint's sample fractions buy at cadence 10, in time and in detection delay?
Preregistered as v2 (8788236b) after one failed review (v1 1a34ec9b; `PREREG-REVIEW.md`). The shadow-period half of
H-02 (live heads) is a later id; this one uses records only.

**Measured.** Run-001 68b1e636; data 1192173c; RESULTS 839c1c6f. H-02a: the five slot bands of the cost split sum to
1,453.4 s against the reported 1,453.3 s; the attested share of argv 63's serial time is 0.6448 (R00: 0.645); the kept
fraction at a 10 percent sample is 0.4196 (R00: 0.4195). H-02b: over the 23 successful verifies of slots 253-278, verify
wall time = -1,732 + 9.34 s x slot + 24.8 s x run-mean load (R2 0.62); g = 9.34 s per slot at equal load, 95 percent pairs
bootstrap [5.73, 13.50] (1,000 of 1,000 resamples defined; width 7.8 s); the univariate slope without the load term is
8.35 s per slot. Sensitivity, non-gating: seeds 20261106 and 20261107 give [5.66, 13.39] and [5.67, 13.27].

**Verdict: PASS.** H-02a PASS (all three agreements inside the preregistered tolerances). H-02b PASS: the interval
contains 13, the estimate 9.34 lies in [8, 18], and the interval is 7.8 s wide, under the 20 s cap. The verdict concerns
verifies; the report's 13 s figure came from dry runs of the same suite on the same host and is reproduced here within
the band, with the point estimate below it: at equal load the verifies grew by about 9 s per slot, not 13.

**H-02c, descriptive, never gated.** With cadence 10 and R00's proportional scaling of argv 63's K 8 wall (524.6 s): at a
5 percent sample the kept fraction is 0.387, argv 63 about 203 s (saving 321 s), projected dry-run total about 629 s;
at 10 percent 0.420, about 220 s (saving 305 s; R00's own estimate: about 220 s), total about 645 s; at 20 percent
0.484, about 254 s (saving 271 s), total about 679 s. The reader's own seconds are excluded (unmeasured; the
condition (v) read caps them at 15 s). Growth bound per cadence: 10 x 9.34 = 93 s before each checkpoint resets the
live tail. Detection delay for a defect in an attested layer (sampled with probability f per verify, certain at the
cadence rewrite): expected 8.0 verifies at 5 percent, 6.5 at 10 percent, 4.5 at 20 percent; P(detected within 5
verifies) 0.23, 0.41, 0.67; maximum 10 in every case.

**What it means.** The cost side of the G1 design is consistent with the records: the attested share is what R00
published, the growth per slot at equal load is about 9 s (the report's 13 s was a dry-run figure under load), and a
10 percent sample at cadence 10 keeps argv 63 near 220 s with an expected detection delay of about six verifies and
a hard bound of ten. Growth is bounded by the cadence: about 93 s of live tail accumulates before a checkpoint, which
is the figure Q-CC2-1 (a) trades against the cost of a writing run. The load coefficient, 25 s per unit of run-mean
load, says once more (RL-01, RL-04's makespan note) that the host matters as much as the chain.

**What it does not show.** A PASS here does not settle the register's bounded-T(N) clause, because H-02c is a model,
not a measurement: the reader's cost, the sample's real agreement and the first checkpoint's writing-run seconds come
from the shadow period (the condition (v) read, N_shadow). 23 runs over 26 slots, one host, one era (K 6); slot and
test count are collinear, so g is the growth of the whole suite per slot, not the per-layer cost. The 13 s figure is
reproduced within a band the lab chose (8 to 18 s).

**Proposal.** None as a roadmap read. For R00 and the visionary, as input to MET-PERF-047/048 and Q-CC2-1..3: the
lab's independent figures agree with DESIGN_CC2 rev 2 section 2 to the third decimal; the equal-load growth of
about 9 s per slot and the 93 s per-cadence bound are the lab's numbers for the owner's cadence question; the
detection-delay table is the lab's for Q-CC2-2's sample fraction.
