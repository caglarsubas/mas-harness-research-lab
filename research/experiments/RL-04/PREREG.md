# RL-04 preregistration: the scaling study (H-13) and H-19's second clause

Status: FROZEN v1 (2026-11-05; RL-03's H-19a, H-19b and H-19c PASS, RESULTS 213d27e6). Draft v0 (d4035108) is
superseded with no change except this status, the RL-03 digest in section 2 and the script name. Every run needs the
monitor's GO. An integrity check before this draft read, at the pin, the scaling
specification (parameters, point ids, families, worker counts, the one control's bypass set and counter) and the
committed scaling readings of `results.json` (the ten points' quantiles and the against-baseline ratios); no new
computation was made.

## 1. Hypotheses (falsifiable)

- H-13a (sign change between decomposable and sequential tasks): NOT RUNNABLE at this pin. The harness's scaling
  section has one task family (independent items, 5 per worker) in two topologies (CENTRAL, DECENTRALIZED); no
  sequential family exists. Declared UNRESOLVED-by-input; speedup and efficiency are reported descriptively.
- H-13b / H-19 second clause (leased claims reduce duplicated work relative to advisory claims; the breaches
  vanish under leased exclusivity at larger agent counts): at every scaling point with N in {2, 4, 8, 16} and in
  both families, the leased arm's duplicatedWorkRatioPpm is not above the advisory arm's, seed for seed.

Leased arm = the committed configuration (the HELD and VERSION claim checks on). Advisory arm = the same point
with `bypass=("HELD", "VERSION")`, which is the harness's own S-D16-EXCLUSIVE-OFF control extended to every point.

## 2. Inputs

| input | source | pin | state |
|---|---|---|---|
| E1 the RL-03 export (harness, classes.json f8286bc8, results.json 40ac8810) | MON-RL-M4 | tar sha256 90fdfe4d | PINNED; the scaling spec: workers [1, 2, 4, 8, 16], itemsPerWorker 5, deadline 400 + 50 per item, poisonPpm 50,000, stallPpm 20,000, maxLatency 3; points S-C1..S-C16 and S-D1..S-D16; baseline B-5..B-80 at one worker |
| RL-03 RESULTS.json (H-19a PASS) | the lab | 213d27e6 | PINNED |

Committed leased readings at the pin (duplicatedWorkRatioPpm p50 / p95 / max): S-C1 0 / 444,444 / 444,444;
S-C2 0 / 125,000 / 200,000; S-C4 0 / 64,516 / 125,000; S-C8 18,181 / 87,719 / 93,750; S-C16 27,272 / 86,538 /
100,000; S-D1 0 / 142,857 / 444,444; S-D2 0 / 83,333 / 142,857; S-D4 0 / 137,931 / 148,148; S-D8 18,518 / 66,666 /
76,923; S-D16 26,315 / 78,947 / 108,108. Duplicated work does not vanish under leasing at the committed points (the
p50 rises with N); the hypothesis as stated in the register is therefore tested as "lower than advisory", and the
register's wording "vanish" is reported against the data as a finding either way.

## 3. Design

- Runs: for each of the 8 points with N ≥ 2, both arms, the committed 32 seeds: 512 simulation runs, plus the two
  N = 1 points in both arms (128 runs) as a no-contention control where the arms should not differ. Readings per
  run: duplicatedWorkRatioPpm, completionPpm, lostWorkPpm, lastMergeTick, and the safety counters (claimOverlap in
  particular).
- Pairing: by (point, seed). Paired difference d = advisory − leased duplicatedWorkRatioPpm.
- Gate for H-13b: PASS when (a) at every N ≥ 2 point the median paired d is ≥ 0, and (b) the bootstrap 95 %
  interval (1,000 resamples by seed, seed 20261104) of the mean d pooled over the 8 points excludes zero from
  below; FAIL when at any point the leased p95 exceeds the advisory p95 and the pooled interval includes or is
  below zero; UNRESOLVED otherwise or when any run fails to finish. Safety: claimOverlap must be 0 in every leased
  run (the harness's own gate); its count under advisory is reported.
- Descriptive: speedup S(N) = baseline lastMergeTick p50 / point lastMergeTick p50 from the committed
  against-baseline ratios (reported, not reproduced unless GO allows the 160 baseline runs), efficiency S(N) / N,
  per family; completionPpm and lostWorkPpm per arm.
- Compute: `research/tools/rl04_scaling.py`; by RL-03's timing (4 ms per small run, scaling points are larger) the
  640 runs are expected within a few minutes; one job per GO; profile interpreter 3.12.14,
  `-I -B`, TMPDIR in scratch; never writes into the export.

## 4-6. Criteria, privacy

PASS / FAIL / UNRESOLVED as in section 3. Outputs are point ids, arm names, quantiles, counts and wall times; scanned
before reporting. A breach is a finding; no re-tune under RL-04.
