# RL-17 PREREG reviews (charter step 1a; a fresh pass holding only the PREREG, the register row and the charter's protocol section)

## Review 1, of PREREG v1 (15939132), 2026-11-05: FAIL

R1 FAIL: the PASS, FAIL and UNRESOLVED regions overlap (fewer than 39 pairs with all identical; an accepted stale
replay together with a driver exception) and no precedence beyond the precondition is stated. R2 FAIL: the register
names replaying a run-event log through the coordinator and reproducing the claim and merge sequence; the PREREG
measured re-simulation pairs, one committed class row and single post-run replays, without declaring the
substitution; "reordered" was only a fresh-id operation with an old expectedVersion. R3 PASS. R4 PASS. R5 PASS.
R6 PASS. R7 PASS.
VERDICT: FAIL.
NOTES: (1) H-27c counts any non-ACCEPTED answer as a refusal, so a refusal for an unrelated reason would pass, and a
replay whose expectedVersion still equals the current version would be legitimately ACCEPTED (a false FAIL) unless
acceptance always advances the version. (2) the precondition checks the archive's internal consistency, not its
provenance. (3) the register names "the run-event contract and vectors"; the PREREG pins no such contract.

Lab's disposition: v1 kept as `PREREG.v1.md`. v2 adds the register's clause as its own claim H-27d (the recorded
operation sequence replayed in order, at its ticks, through a fresh simulation's board; the claim and merge answers
compared), keeps determinism (H-27a) as a separately named claim, states the precedence (precondition, then FAIL,
then UNRESOLVED, then PASS, per claim), requires STALE_VERSION itself for a stale replay and excludes attempts the
version rule cannot refuse (the board advances the version on every acceptance; the driver checks it), says the
precondition is internal consistency and provenance is the archive digest and commit, and names the effect-log form
inside the archive as the run-event vectors. The driver and evaluator change and are re-frozen. v2 goes to a second
review before any run.

## Review 2, of PREREG v2 (77015690), 2026-11-05: PASS (run may start)

R1 PASS (precedence stated; overall rule exhaustive; review 1 answered). R2 PASS (H-27d is the register's clause;
determinism named separately; the effect-log form declared as the vectors). R3 PASS. R4 PASS. R5 PASS. R6 PASS.
R7 PASS.
VERDICT: PASS.
NOTES: (1) H-27a's UNRESOLVED threshold (39 pairs) is looser than its unit (416 pairs), and H-27a/H-27b have no
exception branch; treat any shortfall against 416 as UNRESOLVED. (2) the replay runs through Board.apply, which
stands for "the coordinator"; "reordered" is the stale-version late arrival, not a permuted log; label both as
proxies in the report. (3) say beforehand how an exception in H-27d is classed: the driver counts it as a
divergence, so FAIL takes precedence, which is the same D1 finding.

Lab's disposition: the run proceeds under v2 with all 32 seeds (416 pairs; a shortfall is reported as UNRESOLVED
per note 1); notes 2 and 3 are answered in the report.
