# RL-08 preregistration: inherited checks and the chain's cost per layer (H-08)

Status: FROZEN v1 (2026-11-05, light; MON-RL-M10b unblocked H-08, MON-RL-M11 "go ahead"). Integrity check before the
freeze, disclosed: the cost report's key structure and sample value shapes were read, and in doing so four figures
were seen: argv 63's cpuSeconds (2,580.8 of the argv total 3,282.0), its genericScaffoldCpu (927.6), layer 02's
bytes:read:authority (256.4 GB of about 496 GB), and tests 16,560. Those four quantities are therefore descriptive
only and carry no gate below; the gated measures (per-file CPU shares and the per-layer shares over all 60 layers
with counters) were not computed before the freeze.

## 1. Hypotheses (falsifiable)

- H-08a (refusal history): some inherited checks never refused anything and some refused real drift. NOT RUNNABLE:
  the cost report records cost, not refusals, and no export of per-check refusal counts exists. UNRESOLVED-by-input,
  declared before the run.
- H-08b (concentration): the chain's cost per layer is concentrated in a small set of validators. Two gated
  measures: (B2) within argv 63 (the chain identity test), the top 10 percent of test files by CPU (14 of 141)
  hold at least 50 percent of argv 63's per-file CPU; (B3) across the 60 bridged scaffold layers with counters
  (passC, slots 192-254), the top 10 percent of layers (6) hold at least 50 percent of bytes:read:authority. Gate:
  PASS when both hold; FAIL when either top decile holds under 30 percent; UNRESOLVED otherwise. Gini coefficients
  and the top-5 shares are reported for both; the four seen figures and the per-argv distribution (B1) and the
  generic-scaffold share (B4) are descriptive.

## 2. Inputs

| input | source | pin | state |
|---|---|---|---|
| Y1 `architecture/chain-compaction/cost-report.json` (M1's cost report, run 20261021T1041) from the RL-07 export (harness-onion main afee03b9) | the monitor (MON-RL-M10b ruling: a published record) | sha256 ea50f1d56df9fac17eacfc5c04271e540d18676f15d3d6c811e1e4076f4dde44 | PINNED |
| Y2 `architecture/chain-compaction/ab.json` and README.md, same export | as Y1 | prefixes in RL-07's members list | descriptive context (keys and counts only) |

## 3. Design

- Per-file CPU: argv63.perFile[file] = [cpu seconds, tests]; share of the top 14 files; Gini over 141 files.
- Per-layer bytes: passC[layer]["bytes:read:authority"] over the layers that carry counters; share of the top 6;
  Gini. Secondary, descriptive: reads:authority and call:_checked_own_authority_raw per layer; authorityReadsPerVerify
  perPath top-5 share (88 authority files).
- Per-argv: argv[].cpu over 64 commands, top-1 and top-3 shares (descriptive; argv 63 seen).
- Deterministic; no seeds. Light: `research/tools/rl08_cost.py` (stdlib, `python3 -I -B`), seconds.

## 4-6. Criteria, privacy

As in section 1. Outputs hold shares, Gini values, counts, layer indices and test-file paths of the repository (public
paths), no local paths; scanned before reporting.
