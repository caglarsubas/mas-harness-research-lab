# RL-16 PREREG reviews (charter step 1a; a fresh pass holding only the PREREG, the register row and the charter's protocol section)

## Review 1, of PREREG v1 (1a34ec9b), 2026-11-05: FAIL

R1 PASS. R2 PASS. R3 FAIL: input I2 has a sha256 but neither a commit nor a statement that none exists; the
constants 13 s per slot (RD-REPORT) and 0.645 / 0.4195 (DESIGN_CC2 rev 2) carry a revision tag or nothing, not a
digest. R4 PASS. R5 PASS. R6 PASS. R7 PASS.
VERDICT: FAIL; pin I2's origin and the constants' sources.
NOTES: (1) H-02b can PASS with an uninformative wide interval; a width cap would make PASS discriminating. (2) the
UNRESOLVED triggers (fewer than 15 runs; fewer than 900 resamples) can coincide with FAIL; a precedence line is
needed; the instrument stop maps to no verdict. (3) the 13 s figure comes from dry runs and is tested on verifies;
say whether they measure the same thing, and whether RL-01's published fit was seen when the band was chosen.

Lab's disposition: v1 kept as `PREREG.v1.md`. v2 states I2's origin (the monitor's masked export of the verifier's
check-run summaries; no commit exists because the verifier's directories are never read; the lab holds it by
sha256 only), pins the two source documents by full sha256, adds a width cap of 20 s to PASS, orders the gate
(precondition and UNRESOLVED triggers first, then FAIL, then PASS), says an instrument stop writes no ledger,
declares that the 13 s figure is a dry-run figure tested on verifies of the same suite on the same host (the verify
adds the verifier's own steps; declared as an approximation), and that RL-01's slot coefficient (unidentified,
interval -76 to 265) was seen but the band was taken from the report's figure. The evaluator changes for the width
cap and the precedence and is re-frozen. v2 goes to a second review before any run.

## Review 2, of PREREG v2 (8788236b), 2026-11-05: PASS (run may start)

R1 PASS (ordered gate; width cap; total overall rule). R2 PASS (the dry-run against verify distinction declared).
R3 PASS (review 1 answered: I2 "no commit exists"; the constants tied to pinned documents). R4 PASS. R5 PASS. R6
PASS. R7 PASS.
VERDICT: PASS.
NOTES: (1) say "no commit pinned, digest only" for RD-REPORT as plainly as for I2. (2) report two further bootstrap
seeds as a non-gating sensitivity; say what an instrument stop does to the overall verdict. (3) say that H-02b's
verdict concerns verifies, not the dry-run figure, and that RL-16's overall verdict does not settle the register's
bounded-T(N) clause, since H-02c is never gated.

Lab's disposition: the run proceeds under v2; notes 1 and 3 are answered in the report; note 2's seeds are
reported descriptively in the report from a separate, non-gating run of the model script (seeds named).
