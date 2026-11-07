# RL-02 preregistration: review independence (H-09)

Status: FROZEN v1 (2026-11-04, after the monitor's MON-RL-M2 delivered J1). Draft v0 (eaee90ba) is superseded; the
differences are in section 7. This file's sha256 goes into `research/hypotheses/REGISTER.md`. A v2 under a new
PREREG version (RESULTS v2 supersedes v1 by digest) is declared now for the day a finding-level export with oracle
verdicts exists; v2 reuses sections 1 and 3 of draft v0 unchanged.

## 1. Hypothesis (falsifiable)

H-09: review rounds and the independent oracle find different findings, and the verifier refuses a measurable
fraction of PASS_FOR_PUSH heads. Three tests as in draft v0:

- H-09a (independence, finding-level Jaccard overlap between review rounds and the oracle): NOT RUNNABLE on J1,
  which carries per-round counts and no oracle verdicts. Declared UNRESOLVED-by-input before any run.
- H-09b (verifier refusals): among distinct heads that received a PACKET-kind PASS_FOR_PUSH verdict, the fraction
  whose verify run in I2 concluded other than success; Wilson 95 % interval.
- H-09c (carried notes that became later findings): NOT RUNNABLE on J1 (note counts only, no identities). Declared
  UNRESOLVED-by-input; the per-round note counts are reported descriptively.

## 2. Inputs (sha256 per file; source)

| input | source | pin | state |
|---|---|---|---|
| J1 review rounds, 105 rows over 12 series groups from Build-R00's tools folders (packets, designs and contracts of MET-ADOPT-006, MET-ENFORCE-043, MET-PERF-043/044/045, MET-SECTOR-003/004/005, MET-VERIFY-005/006, VERIFIER-BUNDLE-V5, VERIFIER-EXT-R04-R11); columns packet, seriesKind, round, kind, verdict, form, subject8, findings, major, minor, note, disclosures, ruling, interruptions, duration_s | the monitor's masked export (MON-RL-M2) | sha256 a1a4b2373be0663089155962c5ff06927cfff18383d83e373874167c890456a4 | PINNED; copy at `inputs/J1_review_rounds_r00.tsv` |
| I2 verifier check-run summaries (head8, conclusion) | RL-01's input | sha256 808bf769 | PINNED (shared) |
| I1 rows (pr, slot) | RL-01's `data/I1_rows.tsv` | sha256 6c5a1c58 | PINNED (shared), context only |

Not in J1 (the monitor's note): oracle verdicts and oracle test counts; packets before about slot 268; the records
of the R10, R12, R03, R04 and R11 lanes. An integrity check before this freeze read J1's column types, the enum
value sets (seriesKind, kind, verdict, form, ruling) and the numeric ranges; no relationship between columns was
computed before the freeze.

## 3. Design

- Junk rows: a row is dropped when `kind` is not one of PACKET, DESIGN, CONTRACT, or `verdict` is not one of
  CHANGES_REQUIRED, PASS_FOR_PUSH, PASS_FOR_PRECHECK, PASS_FOR_ADOPTION, PASS_FOR_BUILD, or `round` is not an
  integer. The dropped count is reported (the monitor named 2 junk rows).
- H-09b unit: a distinct subject8 with at least one PACKET-kind PASS_FOR_PUSH row. Matched when I2 has a row with
  head8 equal to subject8. Refused = at least one matched I2 row with conclusion other than success. Heads with no
  I2 row are counted as unmatched and excluded from the fraction (I2 covers harness-onion PRs 207-232 only).
  Interval: Wilson 95 %. Gate (as drafted): PASS when the lower bound is above 0; FAIL when the observed fraction is
  0 with at least 40 matched heads; UNRESOLVED below 40 matched heads.
- Descriptive, not gated (no seeds; medians and Wilson intervals only): rounds per series by seriesKind; findings,
  major, minor, note and disclosures per round by round index (1, 2, 3, 4+) and by form (full, delta); the
  CHANGES_REQUIRED fraction by round index; the fraction of rounds at index 2 and above that still carry at least
  one finding (between-round independence, descriptive here, a candidate gated test for v2); duration_s and
  interruptions per round; rulings.
- Overall verdict rule: UNRESOLVED when any of H-09a, H-09b, H-09c is UNRESOLVED; FAIL when any is FAIL; PASS
  only when all three PASS. (With H-09a and H-09c UNRESOLVED-by-input, v1's overall verdict can only be UNRESOLVED;
  it is run for H-09b and the descriptive table, and to fix what v2 needs.)

## 4. Compute plan

Light: `research/tools/rl02_table.py` (stdlib, `python3 -I -B`), seconds; no heavy slot.

## 5. PASS, FAIL, UNRESOLVED

As in section 3. A breach is a finding recorded in RESULTS.json; no re-tune under RL-02 v1.

## 6. Privacy

Inputs arrive masked; every output file is scanned with `privacy_scan.py` (counts only) before it leaves the folder.
Packet names from J1 are item identifiers (MET-*, VERIFIER-*), which may appear in outputs; subject8 values are
8-character commit prefixes and may appear in outputs.

## 7. Changes from draft v0 (eaee90ba)

- Inputs pinned to J1 (count-level), I2 and I1 rows; the finding-level identity rule and the PR-clustered bootstrap
  of v0 are carried to v2, not used here.
- H-09a and H-09c declared UNRESOLVED-by-input; H-09b's unit refined (distinct heads, matched to I2, unmatched
  excluded).
- Descriptive table added (section 3); overall verdict rule stated.
