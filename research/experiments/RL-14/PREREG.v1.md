# RL-14 preregistration: typed resume blocks and the rule lines that follow them (H-28, observational half)

Status: FROZEN v1 (2026-11-05, light; MON-RL-RESUME "RL-14 may start now, light, with PREREG-REVIEW first"). This
file's sha256 goes into the register. First experiment under charter step 1a: an independent PREREG review
(`PREREG-REVIEW.md`) precedes the run. Integrity check before the freeze, by script and counts only (no line of
any handoff file printed): 9 files match the sample rule (the lanes' own files `LANE-*.md` and the monitor's
`STATE.md`; the lab's own lane file excluded; prompts, templates and the monitor's other records excluded); 51
resume blocks; 43 consecutive-block windows, 33 with at least one day between the two dates; 47 of 51 blocks
carry at least one digest prefix or line pin, so the exposure is continuous (density), not binary. No outcome
value was computed before the freeze.

Disclosure: the lab read several of the sampled files earlier on 2026-11-05 (its own resume, the lane file and
STATE.md's hand-written section); the handoff records were written by the programme's sessions for their own
resumes, independently of this hypothesis (R7). The slip proxy below is the same dated MON-line unit RL-06 used.

## 1. Hypothesis (falsifiable)

H-28 (observational half): resume blocks that pin their referents by digest and line number are followed by fewer
monitor rule lines per day than blocks that do not.

- Unit: a window = two consecutive dated resume blocks in one file (heading `Resume here`, `HANDOVER n` or
  `RESUME`, with a date in the heading), ordered by date; the window opens at the first block's date and closes
  at the second's. Windows of zero days are excluded (both blocks on one day: no following period).
- Exposure X: the opening block's typedness = (distinct 8-hex digest prefixes + line pins of the form "line(s)
  n" or "lines n-m") per 100 words of the block.
- Outcome Y: dated MON lines per day = the number of lines anywhere in the same file that carry a MON identifier
  and a date inside (opened, closed], divided by the window's days. A dated MON line is the lab's proxy for a
  monitor rule or correction recorded for that lane; it over-counts relays that are not slips and under-counts
  slips that got no MON id (disclosed; RL-06 found 70 percent of rule ids incident-specific).
- Statistic: Spearman rank correlation rho(X, Y) over the windows with days >= 1; a 95 percent percentile
  bootstrap interval over windows (1,000 resamples, seed 20261105); secondary, descriptive: median Y for windows
  with X above the median X against those at or below it.
- Gate: PASS when n >= 20, rho <= -0.30 and the interval's upper bound is below 0. FAIL when n >= 20 and either
  rho > 0 with the interval's lower bound above 0 (the opposite association) or |rho| < 0.10 with the whole
  interval inside (-0.30, 0.30) (an association too small to matter). UNRESOLVED otherwise, or when n < 20.
- Confounds, named: a lane's activity level drives both the detail of its resume blocks and the number of
  rules it receives; the monitor's own STATE.md blocks are resumes of a different role; window length varies
  (1 to about 10 days). None is adjusted for; a PASS here is an association, not a cause, and the report says so.

## 2. Inputs

| input | source | pin | state |
|---|---|---|---|
| K1 `handoff/LANE-*.md` and `handoff/STATE.md` at the bridge's working tree of 2026-11-05 (9 files; `LANE-RESEARCH-LAB.md` excluded) | the bridge | per-file sha256 recorded in the output and the run record | read by script for headings, dates, digest prefixes, line pins and MON ids only; no line printed or copied |

## 3. Design and compute

- Extractor `tools/rl14_handoff.py` (c42d0e6a at the freeze; its digest at the run is in the run record): blocks,
  windows, X and Y per window, written to `data/rl14_windows.json` (counts and per-window numbers only, file
  names and dates, no text).
- Evaluator `tools/rl14_eval.py` (written before the run, digest in the run record): rho, bootstrap, the secondary
  medians, the gate, `RESULTS.json` in the verdict-ledger form; it names its own digest in the ledger. The run
  pass writes no verdict by hand.
- Compute: light, this host, standard library, `python3 -I -B`, deterministic apart from the seeded bootstrap;
  no GO needed; stream S3, queue class T; no ECU (not a product-coupled run).
- Privacy: `privacy_scan.py` over every file of the folder before the report.

## 4. What is PASS, FAIL, UNRESOLVED

As the gate in section 1. A FAIL or UNRESOLVED is recorded as the finding; no re-tuning of the proxy, the
threshold or the sample under this id. A different proxy (for example slips classified from rule text, which
needs the monitor's permission) is a new id that names this one.
