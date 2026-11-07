# RL-12 preregistration: the evidence algebra, ledger agreement restated per claim (H-04, new id; MON-RL-M18 GO)

Status: FROZEN v1 (2026-11-05, light). Disclosure, stated first: this experiment restates RL-10's check C2 clause 2
with the scope the ledger's rule has (per claim, not per ledger). RL-10's post-hoc check C5 already computed the
per-claim reading on the same seven vectors and found agreement 7 of 7; RL-12's value is to put that reading on the
record under a correctly scoped, preregistered clause, not to discover it. Nothing else changes: the same shared
order, the same two maps, the same inputs (RL-10's six files, digests in `data/inputs.txt`), the same C1 and C3.

## 1. Hypothesis and checks

H-04 as in RL-10. Checks C1 (totality) and C3 (native agreement) as in RL-10. C2 restated:
- C2a: every ledger vector whose expected code is CONSISTENCY_ONLY, CONSENSUS_ONLY or NOT_EVIDENCE carries an
  evidence item of the matching level (3, 2, 1).
- C2b (per claim): in each such vector, the claim whose checks cite that weak-level evidence has no deterministic
  check with outcome PASS on target DELIVERED whose cited evidence is all of level 5; a vector where the weak item
  is cited by no check (recorded as evidence only) satisfies C2b vacuously and is reported as such.
- Gate: H-04 PASS when C1, C2a, C2b and C3 hold; FAIL on any violation; UNRESOLVED when a vector's claims cannot
  be read.

## 2. Compute, privacy

Light: `research/tools/rl12_algebra.py` (RL-10's script with C2b per claim; stdlib; `python3 -I -B`), seconds.
Outputs as RL-10; scanned before reporting.
