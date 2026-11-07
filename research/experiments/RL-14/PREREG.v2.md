# RL-14 preregistration v2: typed resume blocks and the new rule identifiers that follow them (H-28, observational half)

Status: FROZEN v2 (2026-11-05, light; MON-RL-RESUME "RL-14 may start now, light, with PREREG-REVIEW first"). v1
(714effc6, kept as `PREREG.v1.md`) FAILED review 1 on R2 and R3 (`PREREG-REVIEW.md`); v2 answers it and goes to a
second review before any run. This file's sha256 goes into the register beside v1's.

Integrity check before the freeze, by script and counts only (no line of any handoff file printed): the sample rule
selects the lanes' own files `handoff/LANE-*.md` (8 files; the lab's own `LANE-RESEARCH-LAB.md` excluded; the
monitor's `STATE.md`, prompts, templates and other records excluded because they are not a lane's resume); 40
resume blocks in 7 of them (`LANE-TEMPLATE.md` has none); 33 consecutive-block windows, 23 with at least one day
between the two dates; 36 of 40 blocks carry at least one digest prefix or line pin, so the exposure is a density,
not a binary. No outcome value was computed before the freeze.

Researcher degrees of freedom, declared: the lab analysed this corpus's MON identifiers in RL-06 (its "70 percent
OTHER" finding) and has read several sampled files on 2026-11-05; the heading, digest-prefix, line-pin and MON-id
patterns were fixed after the inventory counts above, not after any outcome; the "line n" pattern can match
ordinary prose and is kept as written. The records themselves were written by the programme's sessions for their
own resumes, independently of this hypothesis (R7).

## 1. Hypothesis (falsifiable)

H-28 (observational half): resume blocks that pin their referents by digest and line number are followed by fewer
new monitor rule identifiers per day than blocks that do not.

- Unit: a window = two consecutive dated resume blocks in one lane file (heading `Resume here`, `HANDOVER n` or
  `RESUME` with a date in the heading), ordered by date; it opens at the first block's date and closes at the
  second's. Windows of zero days are excluded.
- Exposure X: the opening block's typedness = (distinct 8-hex digest prefixes + line pins "line(s) n" or "lines
  n-m") per 100 words of the block (the block runs from its heading to the next heading).
- Outcome Y: new MON identifiers per day = the number of distinct identifiers of the form MON-<segments> whose
  first dated appearance anywhere in the same lane file (the earliest date on a line that carries the identifier)
  falls inside (opened, closed] and that the opening block does not already name, divided by the window's days.
  Recaps, repeats and the opening block's own identifiers therefore count zero; an identifier counts once, in the
  window of its first date. A new MON identifier is the lab's proxy for a monitor rule or correction addressed to
  that lane; it over-counts relays that are not slips and under-counts slips that got no identifier (RL-06 found
  the identifiers incident-specific). The register's binary wording ("fewer resume slips") is tested as this density
  association; the median split below is descriptive only.
- Statistic: Spearman rank correlation rho(X, Y) over the windows with days >= 1, ties by average ranks; a 95
  percent percentile bootstrap interval that resamples lane files (clusters) with replacement, keeping every window
  of a drawn file, 1,000 resamples, seed 20261105; secondary, descriptive: median Y for windows with X above the
  median X against those at or below it.
- Gate: PASS when n >= 20, rho <= -0.30 and the interval's upper bound is below 0. FAIL when n >= 20 and either
  rho > 0 with the interval's lower bound above 0 (the opposite association) or |rho| < 0.10 with the whole interval
  inside (-0.30, 0.30) (too small to matter). UNRESOLVED otherwise, or when n < 20.
- Confounds, named and not adjusted for: a lane's activity level drives both the detail of its resume blocks and
  the number of rules it receives; the monitor's rules can themselves prescribe pinning, so Y may drive X (the
  reverse direction); window length varies (1 to about 10 days); seven lane files are few clusters. A PASS is an
  association, not a cause, and the report says so.

## 2. Inputs (pinned)

Bridge commit 46c7d6e2; every file below is unmodified at that commit (clean in the working tree at the freeze).

| input | sha256 |
|---|---|
| `handoff/LANE-DESIGN-UX.md` | 051a23aa2b04233a3e3ee72c41a04090ac0eb4a1852989bb2d96dc901da1ecf3 |
| `handoff/LANE-PARALLEL.md` | 868271117f0a4737f3bafb0bc599002960b944e926fbc10b43dfd0f4322567e4 |
| `handoff/LANE-PRIMARY.md` | 4b7fd1f236c36ecb2f7fb1eef2c74288e08e66708362be7e89f55e7778d33470 |
| `handoff/LANE-R00-HARNESS-ONION.md` | 14995d97bf3c8ccd6dc0292f96d3c7f733b2194e52fe27cde27cae41b5412e3d |
| `handoff/LANE-R03.md` | b085d152695af6c7362475fae75885440c9425d1f3553f4f25ef675d583d6421 |
| `handoff/LANE-R04.md` | 9d9718e26815a32ca5aebe6763d0faacb47c4932fcd3b27c81d6422654ef8929 |
| `handoff/LANE-R11.md` | bc6d05d564d12ee75f66f358b3bde6926087acf173ff4ea42342cc972272b483 |
| `handoff/LANE-TEMPLATE.md` | aa4c8b26401e09927917ddc1c9d1677a347d4ee0cc0169527f17414897590274 |

The files are read by script for headings, dates, digest prefixes, line pins and MON identifiers only; no line is
printed or copied; the output holds file names, dates and numbers.

## 3. Design and compute (scripts frozen)

- Extractor `tools/rl14_handoff.py`, sha256 6f678ba33da2fa211dfb55cec6e9efd5fe065f23c944500192be8d6e293084aa:
  blocks, windows, X and Y per window, to `data/rl14_windows.json`.
- Evaluator `tools/rl14_eval.py`, sha256 0fe97a9fc463c9dda40481fc0247ec72dec7fab456962ff6fc406f7bbeb0710e: rho,
  the clustered bootstrap, the secondary medians, the gate, `RESULTS.json` in the verdict-ledger form naming its own
  digest. The run pass writes no verdict by hand. A change to either script after this freeze is a new PREREG
  version.
- Compute: light, this host, standard library, `python3 -I -B`, deterministic apart from the seeded bootstrap; no
  GO needed; stream S3, queue class T; no ECU (not a product-coupled run).
- Privacy: `privacy_scan.py` over every file of the folder before the report.

## 4. What is PASS, FAIL, UNRESOLVED

As the gate in section 1. A FAIL or UNRESOLVED is recorded as the finding; no re-tuning of the proxy, the
threshold or the sample under this id. A different proxy (for example slips classified from rule text, which needs
the monitor's permission) is a new id that names this one.
