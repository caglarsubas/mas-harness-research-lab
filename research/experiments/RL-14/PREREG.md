# RL-14 preregistration v4: typed resume blocks and the new rule identifiers that follow them (H-28, observational half)

Status: FROZEN v4 (2026-11-05, light; MON-RL-RESUME "RL-14 may start now, light, with PREREG-REVIEW first"). v1 (714effc6) FAILED review 1 on R2 and R3; v2 (3b81a007) FAILED review 2 on R1; v3 (941653de) FAILED review 3 on R1 (undefined statistic), R2 (last block, bridge sentence) and R3 (scripts' custody); each is kept as `PREREG.vN.md`. v4 answers review 3 and goes to a fourth review before any run (`PREREG-REVIEW.md`). All digests go to the register.

Integrity check before the freeze, by script and counts only (no line of any handoff file printed): the sample rule selects the lanes' own files `handoff/LANE-*.md` (8 files; the lab's own `LANE-RESEARCH-LAB.md` excluded; the monitor's `STATE.md`, prompts, templates and other records excluded because they are not a lane's resume); 40 resume blocks in 7 of them (`LANE-TEMPLATE.md` has none); 33 consecutive-block windows, 23 with at least one day between the two dates; 36 of 40 blocks carry at least one digest prefix or line pin, so the exposure is a density, not a binary. The last block of each lane opens no window and is therefore not in the analysis (7 blocks). No outcome value was computed before the freeze.

Researcher degrees of freedom, declared: the lab analysed this corpus's MON identifiers in RL-06 (its "70 percent OTHER" finding) and has read several sampled files on 2026-11-05; the heading, digest-prefix, line-pin and MON-id patterns were fixed after the inventory counts above, not after any outcome; the "line n" pattern can match ordinary prose and is kept as written. The records themselves were written by the programme's sessions for their own resumes, independently of this hypothesis (R7).

## 1. Hypothesis (falsifiable)

H-28 (observational half): resume blocks that pin their referents by digest and line number are followed by fewer new monitor rule identifiers per day than blocks that do not.

Bridge from the register's wording: the register says "count the slips that followed each" resume block. No record marks a rule as a resume slip, and classifying rule text needs the monitor's permission, so this observational half operationalises "slips that followed" as "new monitor rule identifiers whose first date falls in the window the block opens". The count cannot distinguish a rule caused by the resume from any other rule addressed to the lane in that window; that is the limit of this half, stated here and in the report, and a text-level proxy is a new id.

- Unit: a window = two consecutive dated resume blocks in one lane file (heading `Resume here`, `HANDOVER n` or `RESUME` with a date in the heading), ordered by date; it opens at the first block's date and closes at the second's. One block opens one window; the last block of each lane opens none and is excluded; windows of zero days are excluded.
- Exposure X: the opening block's typedness = (distinct 8-hex digest prefixes + line pins "line(s) n" or "lines n-m") per 100 words of the block (the block runs from its heading to the next heading).
- Outcome Y: new MON identifiers per day = the number of distinct identifiers of the form MON-<segments> whose first dated appearance anywhere in the same lane file (the earliest date on a line that carries the identifier) falls inside (opened, closed] and that the opening block does not already name, divided by the window's days. Recaps, repeats and the opening block's own identifiers count zero; an identifier counts once, in the window of its first date. The proxy over-counts relays that are not slips and under-counts slips that got no identifier (RL-06 found the identifiers incident-specific). The median split below is descriptive only.
- Statistic: Spearman rank correlation rho(X, Y) over the windows with days >= 1, ties by average ranks; a 95 percent percentile bootstrap interval [L, U] that resamples lane files (clusters) with replacement, keeping every window of a drawn file, 1,000 resamples, seed 20261105; secondary, descriptive: median Y for windows with X above the median X against those at or below it; the number of windows per cluster is reported.
- Undefined statistic, rule: rho is undefined when X or Y has no variance. In the sample that is UNRESOLVED. A resample in which X or Y has no variance is dropped and counted; the interval is the percentile interval of the defined resamples; when fewer than 900 of the 1,000 resamples are defined the result is UNRESOLVED.
- Minimum effect of interest (MEI): rho = -0.30. It is the smallest association on which the lab would propose a rule (digest and line pins required in every resume block, a cost paid by every session at every handover): at rho = -0.30 typedness accounts for about a tenth of the rank variance of the rule rate (rho squared 0.09); below that the rule's cost is not justified by this evidence. The register's row carries no number; this is the lab's stated threshold, fixed before the run.
- Gate (three regions, disjoint by construction):
  PASS when n >= 20, rho <= -0.30 and U < 0 (the association reaches the MEI and the interval excludes zero).
  FAIL when n >= 20 and L > -0.30 (the interval excludes the MEI; the association, if any, is smaller than the lab would act on; the sub-case L > 0 is the opposite direction and is named as such). A point estimate with the hypothesised sign but L > -0.30 is FAIL by this rule and the report says so in those words. PASS and FAIL cannot both hold: PASS needs rho <= -0.30 and rho lies inside [L, U], so L <= -0.30.
  UNRESOLVED otherwise (the interval reaches the MEI but PASS is not met), when n < 20, or under the undefined-statistic rule.
- Expected outcome class, stated in advance: with 23 windows in 7 clusters the clustered interval will be wide; UNRESOLVED is the most likely class whatever the true effect, and the report says so if it happens. A PASS or a FAIL is then a stronger statement than the sample size suggests and is reported with the interval.
- Sensitivity, descriptive and never gated: rho recomputed with X' = digest prefixes only (no line-pin term), and the counts of tied X and tied Y values. Ties: average ranks; with 36 of 40 blocks typed and many zero Y windows, ties pull rho toward zero rather than away from it, which makes a PASS harder, not easier.
- Confounds, named and not adjusted for: a lane's activity level drives both the detail of its resume blocks and the number of rules it receives; the monitor's rules can themselves prescribe pinning, so Y may drive X (the reverse direction); window length varies (1 to about 10 days); seven lane files are few clusters and one file could hold most windows (hence the per-cluster count). A PASS is an association, not a cause, and the report says so.

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

The files are read by script for headings, dates, digest prefixes, line pins and MON identifiers only; no line is printed or copied; the output holds file names, dates and numbers.

## 3. Design and compute (the lab's instruments, frozen)

The two scripts are the lab's instruments, not inputs: they live in `research/tools/` on the bridge working tree, exist at the freeze, carry no commit of their own (the monitor's checkpoint commits `research/**`), and are held in custody by their sha256, each 64 hexadecimal characters, checked by script at the freeze. A change to either after this freeze is a new PREREG version.

- Extractor `tools/rl14_handoff.py`, sha256 a7a80e560465429abadbd51fa2163a7406d3c3784a957d873b2c22865848bd2c: blocks, windows, X, X' and Y per window, to `data/rl14_windows.json` (an output).
- Evaluator `tools/rl14_eval.py`, sha256 ac639ff85852f60a10071aec1acbb898eac5757ef4afbe46c68c8b1798cb616a: rho, the clustered bootstrap with the undefined-resample rule, the secondary medians, the sensitivity, the windows per cluster, the three-region gate, `RESULTS.json` in the verdict-ledger form naming its own digest. The run pass writes no verdict by hand.
- Compute: light, this host, standard library, `python3 -I -B`, deterministic apart from the seeded bootstrap; no GO needed; stream S3, queue class T; no ECU (not a product-coupled run).
- Privacy: `privacy_scan.py` over every file of the folder before the report.

## 4. What is PASS, FAIL, UNRESOLVED

As the gate in section 1. A FAIL or UNRESOLVED is recorded as the finding; no re-tuning of the proxy, the threshold or the sample under this id. A different proxy (for example slips classified from rule text, which needs the monitor's permission) is a new id that names this one.
