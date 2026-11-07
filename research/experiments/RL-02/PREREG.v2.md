# RL-02 preregistration v2: review independence (H-09), finding level

Status: FROZEN v2 (2026-11-04, after MON-RL-M3 delivered J2). RESULTS v2 supersedes RESULTS v1 (2a6648f3) by digest.
Sections 1-3 of v1 (bbb53d0b) stay in force where not changed here. An integrity check before this freeze read J2's
column types, the enum value sets (seriesKind, kind, form, severity, blocks, latestStatus), the round ranges, the
shape of findingId (381 lane tokens, 16 masked) and the count of distinct findingId values (322 of 397 rows); no
relationship between columns was computed before the freeze.

## 1. Hypotheses (falsifiable)

- H-09a (rounds vs oracle): still NOT RUNNABLE. J2 carries no oracle verdicts; the merge-decision records carry only
  a check_pr_oracles PASS string. UNRESOLVED-by-input, declared before the run.
- H-09b (verifier refusals): unchanged from v1 (same inputs J1 and I2; the result is carried, not recomputed).
- H-09c (carried findings): among findings whose latest disposition is PARTLY, NOT or RECORDED (carried), the
  fraction re-raised, i.e. the same findingId appears in a row with a higher roundRaised in the same series.
  Descriptive as in v0 (no bound): the fraction and its Wilson 95 % interval are reported.
- H-09d (between-round independence, new in v2, derived from v1's descriptive result): among findings raised in
  round 2 or later, the fraction whose findingId was not raised in any earlier round of the same series. Gate: PASS
  when the Wilson 95 % lower bound is above 0.5; FAIL when the upper bound is below 0.5; UNRESOLVED otherwise or
  below 40 such findings.

## 2. Inputs

| input | source | pin | state |
|---|---|---|---|
| J2 findings, 397 rows over 25 series of the same 12 R00 groups; columns packet, seriesKind, roundRaised, kind, form, severity, blocks, findingId, latestStatus, statusRound | the monitor's masked export (MON-RL-M3) | sha256 d7e4ff31c02280b31f2cc7c9b463202e1b6a739c1458b6c84ce3fd2ce20fd3d5 | PINNED; copy at `inputs/J2_findings_r00.tsv` |
| J1, I2 | as v1 | a1a4b237, 808bf769 | PINNED (H-09b carried from v1) |

## 3. Design

- Identity: (packet, seriesKind, findingId). Rows whose findingId is not a lane token (shape LETTERS/DIGITS-LETTERS/DIGITS-number)
  are excluded from H-09c and H-09d and counted; a masked id could be shared by distinct findings.
- H-09c unit: a carried finding (latestStatus in PARTLY, NOT, RECORDED). Re-raised = another row with the same
  identity and a strictly higher roundRaised. Findings with no disposition (91 rows) are not carried by this rule;
  their count is reported.
- H-09d unit: a row with roundRaised ≥ 2 and a lane-token id. New = no row with the same identity and a lower
  roundRaised. Wilson 95 % interval. Clustering by series is reported descriptively (per-series new fractions) but
  the gate uses the pooled Wilson interval as stated above.
- Descriptive, not gated: severity mix by round index (1, 2, 3, 4+); blocks fraction by severity; ADDRESSED fraction
  by severity among dispositioned findings; rounds from raise to disposition (statusRound − roundRaised) median.
- Overall verdict rule as v1: UNRESOLVED when any of H-09a, H-09b, H-09c-with-no-bound, H-09d is UNRESOLVED; the
  overall verdict for v2 can therefore only be UNRESOLVED (H-09a); H-09d carries its own PASS/FAIL.

## 4-6. Compute, criteria, privacy

Light: `research/tools/rl02_v2.py` (stdlib, `python3 -I -B`), seconds. Criteria as in section 1 and 3. Outputs hold
counts, fractions, enums and round numbers; lane-token ids never leave the script. Scanned before reporting.
