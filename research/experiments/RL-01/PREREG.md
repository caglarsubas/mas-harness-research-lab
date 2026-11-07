# RL-01 preregistration: the verify-time dataset (H-07)

Status: FROZEN v1 (2026-11-04, after the monitor's MON-RL-M1: GO for the extractor, I2 delivered). H-07a runs under
this version. H-07b runs only after amendment v1.1 records I3's digest; the amendment changes nothing else. The
draft v0 (f03faedf) is superseded; its differences are listed in section 7. This file's sha256 goes into
`research/hypotheses/REGISTER.md`.

## 1. Hypothesis (falsifiable)

H-07: verify-time growth since slot 255 is explained by host load and the outer suite's test count, not by layer
count. Stated as two tests over the verifier's run records:

- H-07a: in a linear fit of wall time T on (load L, test count C, layer count K), the K coefficient's paired,
  task-clustered 95 % interval includes zero, while at least one of L or C has an interval that excludes zero.
- H-07b (reads Build-R00's K 6 vs K 8 A/B; the lab runs nothing): worker wall time at K 8 is non-inferior to K 6
  under the run-manifest contract's non-inferiority rule, on the same host and comparable load.

## 2. Inputs (sha256 per file; commit each came from)

| input | source | pin | state |
|---|---|---|---|
| I1 merge-decision records, 53 files (`handoff/merge-decisions/*.json`), PR 207 onward | bridge commit ee4f3a08 | set digest b3370227 (sha256 over sorted name + content) | PINNED; read only through the allowlist extractor `research/tools/rl01_extract.py` (section 4), never printed raw; gives the merge date and the slot per PR |
| I2 verifier check-run summaries, 27 verify runs, harness-onion PRs 207-232 (slots 255-279), columns pr, head8, checkRun, conclusion, commandsDone, commandsTotal, elapsed_s, load_start_1/5/15, load_run_max, load_run_mean, load_samples, tests_passed, tests_skipped, suite_s, gate, gate_after_s, activation | the monitor's masked export (MON-RL-M1), from the published check-run summaries; no repository names, handles or free text | sha256 808bf769ab2bbc1e45a768816bc1bbf28ccbea052ff20a281b5b4c003532fb4b | PINNED; primary series |
| I3 the K 6 vs K 8 A/B result (K6, K8, K6 on a quieter host) | Build-R00, through the monitor | sha256 TBD in amendment v1.1 | WAITS; H-07b only |
| I4 layer count K and test count C per run | derived: K = slot (the catalog count is slot plus a constant number of product layers, so the K coefficient is unchanged); C = tests_passed from I2 | derived from I1 and I2 | PINNED rule |

I2 is the primary series (every run carries elapsed_s and load_run_mean; 26 of 27 carry tests_passed). I1 supplies
the slot per PR and the merge date. There is no run-record export beyond I2: the verifier's own directories are never
readable. Per-worker balance is not in I2 and is out of RL-01's scope.

An integrity check before this freeze read I2's column ranges (min and max per column, the conclusion and gate
counts); no relationship between columns was computed before the freeze.

## 3. Design

- Unit: one verify run (one head, one verifier run). Clusters: one PR (a PR verified twice forms a cluster).
- Factors: L = load_run_mean, C = tests_passed, K = slot. The draft's date covariate is dropped: K is itself
  monotone in time, and a date term would be collinear with it in 27 rows. Repository is constant (harness-onion).
- Fit 1: ordinary least squares T = b0 + bL L + bC C + bK K. Fit 2: the same on log T. Intervals: PR-clustered
  percentile bootstrap, 1000 resamples, seed 20261104, 95 %. The two fits are the whole confirmatory analysis; no
  model selection after seeing the data. Predictors are standardised (z-scores) for the report; the bounds below
  are on the sign of the interval and do not depend on the scale.
- Rows: a run without tests_passed is dropped from both fits and counted. The one failed run (the cap) is kept: a
  cap event is part of verify time, not an outlier.
- Bounds and gate: H-07a PASS when bK's 95 % interval includes zero AND at least one of bL, bC has an interval
  excluding zero (same sign in both fits); FAIL when bK's interval excludes zero with a positive coefficient in both
  fits; UNRESOLVED when fewer than 20 rows carry L, C and K, when the two fits disagree on the sign of bK's interval,
  or when neither bL nor bC excludes zero. (The draft said 40 rows; 20 is set here because the export holds 27
  runs, a number known from the monitor's description of I2 before any value was read; with 3 predictors it is the
  smallest count the lab accepts for a sign test.)
- Descriptive, not gated: the distribution of gate_after_s (the quiet-host gate's wait) and of suite_s against
  tests_passed, as context in the REPORT.
- H-07b (after amendment v1.1): worker wall time at K 8 non-inferior to K 6 under the run-manifest contract's
  non-inferiority rule, paired by position (K6, K8, K6); UNRESOLVED below 3 runs per arm.

## 4. Compute plan

Light: one stdlib Python script (`research/tools/rl01_extract.py`, allowlist extractor; `python3 -I -B`), seconds
on this host; no heavy slot needed. The extractor emits only numeric and enum columns from an allowlist (elapsed
seconds, load, test count, layer count, conclusion, date, PR number, slot) and never a string field that could carry
a handle, a path or a URL.

## 5. PASS, FAIL, UNRESOLVED

As in section 3. Any breach of a bound is recorded in RESULTS.json as a finding; no re-tune under RL-01.

## 6. Privacy

Every output file is scanned with `privacy_scan.py` (counts only) before it leaves the folder.

## 7. Changes from draft v0 (f03faedf)

- Inputs I2 and I4 pinned (section 2); I3 moved to amendment v1.1.
- Row threshold 40 to 20, with the reason given in section 3; date covariate dropped; clusters are PRs, not packets.
- Intervals fixed as PR-clustered percentile bootstrap (1000 resamples, seed 20261104).

## 8. Amendment v1.1 (2026-11-05): I3 recorded; H-07b runs

- I3: Build-R00's K 6 / K 8 / K 6 A/B at head bd882493, summary file in R00's tools folder, sha256
  85ab23bff6d46f109b9ddc0e987690905d1abb558b2a6207281565e82d51e14f (152 lines). The lab does not read the file (it
  stays in R00's folder); the figures below are as relayed by the monitor (MON message of 2026-11-05) and are marked
  "as relayed" in RESULTS and REPORT.
- Figures as relayed: A1 (K 6) wall 542.98 s, worker phase 517.5 s, summed 3,003.8 s, imbalance 16.9 s, tail 11.9 s,
  load mean 8.32. B (K 8) wall 498.44 s, worker phase 472.2 s, summed 3,620.1 s, imbalance 19.6 s, tail 9.6 s, load
  mean 12.42, with a non-comparability note: the parent node failed on the six-worker pins (131 FAILED lines).
  A2 (K 6) wall 566.73 s, worker phase 540.7 s, summed 3,122.3 s, imbalance 20.3 s, tail 11.8 s, load mean 10.78.
  Deltas B minus mean(A): worker phase −56.9 s (−10.8 %), A-A spread 23.2 s; wall −56.4 s (−10.2 %), spread
  23.8 s; summed +557.1 s (+18.2 %), spread 118.5 s. Host: 18 cores (6 performance, 12 efficiency); workers 7 and 8
  run on efficiency cores.
- Nothing else changes: H-07b's rule (section 3) stands: non-inferiority of K 8 worker wall time under the
  run-manifest contract's rule, paired by position; UNRESOLVED below 3 runs per arm.
