# S1: the history chain and the cost of re-proving everything

**Observe.** Every harness-onion packet re-executes the whole accepted history (92 layers at slot 280) on every verify.
Verify time reached the owner's 1,000 s floor and the 1,200 s cap (slots 272-280: 956 to 1,162 s); the owner adopted
eight workers (PERF-046) and chose the signed checkpoint with sampled re-execution (CHAIN-COMPACTION-002, G1) with
four conditions; a fifth, shadow mode, was the lab's to rule on. Why now: the cap is the programme's hardest number
and every contract packet pays it.

**Hypotheses.** H-07 (growth is load and test count, not layer count); H-08 (cost concentrates in few validators);
H-01 (the chain's monotonicity, immutability and refusal locality hold); H-02 (a checkpoint with sampling bounds T(N)
at a bounded detection delay).

**Data.** The verifier's masked run records (27 runs, PRs 207-232) and the merge-decision rows (RL-01); the cost split
at 280 (R00's cost_split280, 11 lines); the architecture export at afee03b9 (RL-07: identity rule, vectors);
DESIGN_CC2 rev 2 (R00, read masked).

**Experiments.** RL-01 (fit of verify time on load, test count and slot); RL-07 (116 of 116 chain vectors replayed
through the pinned evaluators); RL-08 (per-layer cost and refusal table); RL-16 (the G1 cost model: attested share,
equal-load growth per slot, the 5/10/20 percent table); the condition (v) read (shadow period, N_shadow 10, a 15 s
reader cap; adopted by the owner).

**Results and proof.** Load drives verify time (about 25-50 s per unit of run-mean load); growth at equal load is
9.3 s per slot (interval 5.7 to 13.5), reproducing the report's 13 s within the band; the attested share of argv 63
is 0.645 and a 10 percent sample keeps argv 63 near 220 s with an expected defect-detection delay of 6.5 verifies and
a hard bound of 10 at cadence 10; the chain vectors replay exactly; cost is spread, not concentrated (Gini about 0.5;
argv 63 is 0.86 of CPU). Verdicts: RL-01 PASS by gate (H-07a), RL-07 PASS, RL-08 UNRESOLVED (no refusal history),
RL-16 PASS.

**Next.** H-02's shadow half when MET-PERF-047's first shadow verify exists (the measured per-layer seconds and the
sample's agreement replace the proportional bound); an Ekstazi-style file-dependency arm as a comparison, named for R00.
