# RL-02 report: review independence (H-09), v2, 2026-11-04

**Asked.** Do review rounds and the independent oracle find different findings (H-09a)? Does the verifier refuse a
measurable fraction of PASS_FOR_PUSH heads (H-09b)? Are carried findings re-raised (H-09c)? Are later rounds'
findings new rather than repeats (H-09d, added in v2 from v1's descriptive result)?

**Measured.** v1 (REPORT.v1.md, RESULTS.v1.json 2a6648f3): 104 review rounds over 25 Build-R00 series at count
level. v2 adds J2 (sha256 d7e4ff31): 397 findings of the same series with kind, severity, blocking flag, a lane
finding id, the round that raised it and its latest disposition; no oracle verdicts exist in any record the monitor
can export. Both runs are light, deterministic and recorded (runs/run-001.md, runs/run-002.md).

**Verdict: UNRESOLVED** (RESULTS.json, superseding v1 by digest).
- H-09a: not measurable; the oracle's verdicts are not recorded anywhere the lab can read. UNRESOLVED-by-input.
- H-09b: 1 of 9 matched PASS_FOR_PUSH heads refused (0.11, Wilson 0.02 to 0.44), below the 40-head bound.
- H-09c and H-09d: the preregistered identity (packet, series, finding id) cannot span rounds, because every one
  of the 381 lane-token ids ends its middle segment with the digits of the round that raised it (381 of 381; the 69
  repeated identities are same-round full-form pairs). H-09d's gate was met with 227 of 227 "new" findings and
  H-09c's re-raise fraction is 0 of 57, and both numbers are vacuous. The lab records the gate result and sets the
  claim verdicts UNRESOLVED with the validity check named, rather than report a PASS the design cannot support.

**What the findings show (descriptive, not gated).** Round 1 raises the MAJOR findings (16 of 19; 3 more in round 2;
none later); rounds 3 and later raise MINOR and NOTE findings only. MAJOR findings always block, MINOR block in 0.90,
NOTE never. Among dispositioned findings, MAJOR are ADDRESSED least often (0.68 of 19), MINOR 0.82, NOTE 0.81; the
median disposition comes one round after the raise. 91 findings carry no disposition (raised in a final round or
never dispositioned).

**What it means.** Later rounds are not empty (v1) and their findings are of lower severity (v2): the review
chain's second and later rounds mostly refine. Whether a later round repeats an earlier finding under a new id is
exactly what the record cannot say, because the id scheme is per round. The oracle's independence (H-09's main
claim) is unmeasured.

**Proposal.** RL-02-PROPOSAL, a design read for the visionary through the monitor, small and not a roadmap shift:
(1) give review findings a cross-round identity in the review-record form (a stable id, or a "supersedes" field
naming the earlier id) so re-raises and carried findings become measurable; (2) record the oracle's per-packet
verdict and test count in the merge-decision record (its `oracle` block exists in a few records) so H-09a can be
run. Until then H-09a, H-09c and H-09d stay UNRESOLVED-by-input.
