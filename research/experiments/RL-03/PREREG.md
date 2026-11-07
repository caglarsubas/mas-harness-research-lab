# RL-03 preregistration: the adversarial campaign's breaches reproduced on a pinned export (H-19, first clause)

Status: FROZEN v1 (2026-11-04). No run has taken place; every run below needs the monitor's GO (heavy queue). This
file's sha256 goes into `research/hypotheses/REGISTER.md`. An integrity check before the freeze read the export's
member list, the ledger's structure (keys, the four classes' committed result, gates and quantiles, the arms'
policy ids and one arms row, the scaling parameters) and the ledger module's function signatures; nothing was run.

## 1. Hypothesis (falsifiable)

H-19 first clause: the adversarial campaign's duplicated-work breaches (C2, C5, C7, C9) reproduce on a git-archive
export of the conformance-labs simulation harness at a pinned commit. Stated as:

- H-19a (class rows): for each of C2, C5, C7 and C9, `class_row(config, cls)` recomputed from the export over the
  committed 32 seeds equals the committed row in `results.json` (same `result`, same `gates`, same defended
  quantiles; the whole row compared and the differing top-level keys listed if any).
- H-19b (arms): `arms_section(config)` recomputed equals the committed arms results for every (arm, class) pair
  (A1-A3 over C2, C3, C4, C5, C7): same quantiles and totals.
- H-19c (the breach itself): in the recomputed rows, the only ratio-bound gate that fails for C2, C5, C7 and C9 is
  duplicatedWorkRatioPpm (p95 above 100,000 or max above 250,000 under the committed bounds), with
  completionPpm and lostWorkPpm holding, as the committed ledger states.

H-19's second clause ("vanish under leased exclusivity at larger agent counts") is RL-04's (H-13) with the
harness's scaling section (workers 1, 2, 4, 8, 16) and its claim policies; it is not tested here.

## 2. Inputs (sha256; source)

| input | source | pin | state |
|---|---|---|---|
| E1 `r12-tests-mas-b4bbea79.tar`: git archive of conformance-labs `tests/mas` at main b4bbea795e5a61d4ddc1815ddb8b0b58c2fe23b3 (the tree of CONF-MAS-005's merge c17bcfe3); 23 files, 0 oracle or README members (`test_oracle*.py`, TOOLS/masra010*/** excluded by the exporter and checked by the monitor and the lab) | R12 through the monitor (MON-RL-M4) | sha256 90fdfe4d75a8ade4a8d9652d3dbfbe0093afd4343d52dc72962a1135393e1000, 563,200 B | PINNED; extracted into the lab's scratch only, never into a repository; no bytecode left |
| E1.results `tests/mas/results.json` (ledger v5, C1-C13, 32 seeds) | inside E1 | 40ac8810 | committed rows to reproduce |
| E1.campaign `tests/mas/campaign-record.json` (arms A1-A3) | inside E1 | 0d06ee3d | context |
| E1.classes `tests/mas/classes.json` (preregistered parameters; the ledger's classesSha256) | inside E1 | f8286bc8 | config; its sha256 must equal the ledger's classesSha256 (checked first) |
| E1.modules `_ledger.py` 370d48a2, `_sim.py` f5df8ae2, `_classes.py` bd1be2f5 | inside E1 | as listed | the harness |

Committed breach rows (the monitor's relay, to be confirmed from E1.results in the run): defended
duplicatedWorkRatioPpm p50 / p95 / max: C2 0 / 133,333 / 142,857; C5 40,000 / 178,571 / 281,250; C7 0 / 142,857 /
148,148; C9 200,000 / 285,714 / 303,030; each FAILs only on duplicatedWorkRatioPpm (RECORDED_FAILS).

## 3. Design

- Deterministic: the harness seeds every run from `config["seeds"]` (32 seeds); no lab seeds. k >= 3 is met by the
  32 committed seeds.
- Runs, in this order, each on its own GO: (1) `--timing`: one run of C2 at the first seed, wall time only, to size
  the next two; (2) `--classes`: the four class rows, with wall time per class; (3) `--arms`: the arms section.
- Comparison: JSON deep equality after sorting keys (`strip`); a row that differs lists its differing top-level keys.
- Gate: H-19a PASS when all four rows equal their committed rows; FAIL when any `result`, `gates` or defended
  quantiles differ; UNRESOLVED when the rows agree on those but differ elsewhere (listed), or when a run cannot
  complete. H-19b PASS when every (arm, class) pair agrees on quantiles and totals; FAIL otherwise; UNRESOLVED when
  not run. H-19c PASS when the recomputed four rows fail only the duplicatedWorkRatioPpm bound; FAIL otherwise.
- A difference is a finding about the export, the pin or the harness's determinism, never a reason to re-run under
  RL-03 with other parameters.

## 4. Compute plan

Heavy, on this host: the monitor's relay sizes the full suite at 61-73 s; the four class rows and the arms section
are 128 and 480 simulation runs. Command shape: `python3 -I -B research/tools/rl03_repro.py <scratch export>/tests/mas
<out.json> --timing|--classes|--arms` with TMPDIR in the lab's scratch; the script puts the export on sys.path and
imports `_ledger`; it never writes into the export. No sampler word on the command line. One job at a time; never
during a harness-onion verify or a heavy R00 step; on the monitor's GO only.

## 5. PASS, FAIL, UNRESOLVED

As in section 3. Any breach of a preregistered expectation is a finding recorded in RESULTS.json.

## 6. Privacy

Outputs hold class ids, arm ids, booleans, quantiles and wall times; scanned with `privacy_scan.py` before reporting.
The export stays in the scratch directory and is removed when RL-03 and RL-04 close (moved to the Trash, not rm).
