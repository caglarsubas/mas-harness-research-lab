# Research-Lab read of condition (v), shadow mode for CHAIN-COMPACTION-002 (G1), and Q-CC2-4 (N_shadow), 2026-11-05

Asked by the monitor on resume (MON-RL-RESUME): condition (v) is HELD pending the lab's read; R00's DESIGN_CC2 rev 2
(3b742672, read through a masking filter) carries it as a HELD candidate, with Q-CC2-4 held on the same read. Inputs:
DESIGN_CC2 rev 2 sections 1, 2, 5, 6, 7 and 8; the roadmap item CHAIN-COMPACTION-002 and decision CC2-D1; the lab's
RL-07 (slot attribution) and RL-08 (argv 63 concentration); the verify figures of slots 272-280 (956-1,162 s against
the 1,200 s cap, the owner's 1,000 s floor, the quiet-host commitment of Q-279-MARGIN (a)). Nothing here is a
roadmap shift; the numbers are options for the owner, recommendation first.

## 1. Verdict: adopt (v), bounded, as a measurement period with a cost cap

G1's correctness rests on three claims that the vectors of section 7 cannot establish on live heads:

1. The input set of an attested layer is complete (D3 (a), captured by an audit hook). A vector tests a declared
   input that changed; it cannot show that no undeclared input exists. Only live heads that edit files show a
   missed input, as a disagreement between the ledger's recorded outcome and the live outcome.
2. Recorded outcomes equal live outcomes for every attested node. The programme has had non-deterministic nodes
   (the R10 flock race carried as HE-002C-F). In sampled mode a flaky attested node is hidden for the verifies that
   do not sample it; in shadow mode it surfaces as a disagreement by slot.
3. The reader's own cost is small. Verifies at slots 276-280 ran 1,092 / 1,116 / 979 (re-verify) / 1,083 / 1,162 s
   against a 1,200 s cap: the margin is the thinnest number in the chain, and a reader that re-verifies about 34 MB
   of authority digests and 88 layers' input sets on every verify is not free until measured.

Shadow mode is the only step that measures all three before anything is skipped. It is therefore adopted, but as a
bounded period with an explicit cost cap and a stop rule, not as an open-ended guard.

## 2. What the shadow period records (the lab's H-02 dataset)

Per shadow verify, by slot: the reader's wall seconds; the attested set and the sampled set (sizes, and the sampled
slots); per layer the recorded and the live outcome and their agreement; per attested layer its measured seconds
from the writing run (section 4 of the design) and the live seconds. These replace the proportional bound of the
design's section 2 and fit H-02's T(N) with measured layer seconds; the sample's agreement rate is the detection-delay
model's first observation. The records are published with the packet (MET-PERF-047), so the lab reads them through
a masked export like any other record; RL-14 (H-02) is preregistered against them when the first shadow verify
exists.

## 3. Disagreement classes and the stop rule

Every disagreement stops the plan and returns the slot to G0 (as the design says); the analysis names its class:

- (A) undeclared input: the live outcome changed because a file the ledger does not list changed. The writer's
  capture is fixed and the checkpoint is rewritten; the count restarts.
- (B) non-deterministic node: outcomes differ with no input change. The node stays live (never attested) and is
  recorded as such; the checkpoint is rewritten without it; the count restarts.
- (C) reader defect: a digest or sample error. Fixed in `ci/`; the count restarts.

The count restarts in every class: a clean period is N consecutive shadow verifies with zero disagreements.

## 4. The cost cap

The shadow reader's added wall time per verify is measured on its first verify. Recommended cap: 15 s per verify
(about the A-A spread the K 6/8 A/B measured, 23.2 s, halved). Above the cap the reader runs inside the dry run
only, and dry runs count toward N_shadow, because a dry run executes the same suite on the same head; a verify then
adds nothing. This keeps the quiet-host floor rule untouched during the period.

## 5. Q-CC2-4, N_shadow: options, recommendation first

A clean period of N verifies bounds the per-verify disagreement rate at about 3/N (one-sided 95 %), so no practical
N proves a rate near zero; the purpose of the period is the three mechanism checks of section 1 over live edits,
not a rate estimate. The number should therefore cover one full checkpoint cycle so that condition (i)'s writer runs
once on a live head during the period.

- (a) Recommended: N_shadow = one checkpoint cadence, 10 slots at Q-CC2-1 (a), with at least one checkpoint
  rewrite inside the period. At about 1.7 slots a day this is about a week. Rate bound about 30 % per verify; the
  three mechanism checks run over ten heads of live edits and one rewrite.
- (b) N_shadow = 5 slots. Half a cadence; no rewrite inside the period unless the owner calls one; rate bound about
  60 %.
- (c) N_shadow = 20 slots, two cadences; about twelve days; rate bound about 15 %; two rewrites.

If Q-CC2-1 is answered (b) (every 5 slots), (a) reads as two cadences, 10 slots, unchanged in count.

## 6. Where it lands

- MET-PERF-047 carries the shadow reader (the design's section 6, "only if (v) is adopted") and the per-slot records
  of section 2.
- MET-PERF-048 states N_shadow, the cost cap, the disagreement classes and the restart rule, and merges only after a
  clean period and bundle v7.
- Vector 7 (a shadow disagreement fails, naming the slot) stays; one more vector: a reader over the cap refuses to
  run inside a verify and names the dry-run path.
- The lab's RL-14 (H-02) reads the records; its PREREG waits for the first shadow verify.

## 7. The owner-supplied documents on this point

RS-1 (61fa9041...) gives the same mitigation for A1 in one sentence: never replace the production verifier at first;
run checkpoint mode as shadow verification; require disagreement analysis. Its success bounds for A1 (at least 3x
lower incremental verification cost; miss and detection-delay curves at 5, 10 and 20 % sampling; no weakening of
head-layer refusal vectors) are candidate bounds for H-02's PREREG, as reported. RS-2 (5b30977b...) adds the
compaction agent's task "simulate checkpoint + 5/10/20 % sampling" and the human gate "owner approves any
interpretation that weakens fresh re-execution", which is condition (i) and the head-bound approval already.

## 8. Not claimed

The 15 s cap and the 3/N bound are the lab's figures, not measurements. Nothing here changes a standing rule before
the owner's numbers (Q-CC2-1..4), the review rounds and v7.
