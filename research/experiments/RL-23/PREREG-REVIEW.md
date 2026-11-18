# RL-23 PREREG reviews (charter step 1a; blind, briefed by the Lane-Monitor from the frozen file, rule D)

## Review 1, of PREREG v1 (467c636c), 2026-11-12: FAIL

Verdict as written: CHANGES_REQUIRED (1 MAJOR, 11 MINOR, 7 NOTE); FAIL in the charter's two-valued form. Custody: the
Lane-Monitor briefed the reviewer from the frozen file; the lab did not brief it and has not seen the brief. Context: a
fresh pass holding the PREREG, the register rows and the bridge improvement file (its disclosures below). Model family:
as the monitor states for the record (asked in RL-M94). Review file RL23-REVIEW-R1-3ecd616c.md, sha256 3ecd616c393b8da610c49cc42d449195cd6abf9b73692dcc667f7dfd9e56f6c8,
31 lines, copied verbatim below; closure in PREREG v2 (969489d7) section 14.

---

# RL-23 PREREG v1 blind review r1 (subject sha256 467c636c..., verified; 215 lines)

verdict: CHANGES_REQUIRED (1 MAJOR, 11 MINOR, 7 NOTE)

## Findings

- RV1-1 MAJOR §2:45,49,53,54 + §7:156. H-37, H-39, H-41 and H-42 name no guard measure and region 5 lists guards for H-38/H-40/H-43/H-44 only, so H-41 (dry c2) and H-42 (pre-approved GO chains, which remove monitor checks) can read SUPPORTED while later-found defects rise. Fix: append to H-41 and H-42 "and later-found defects per post slot (median) do not exceed the pre median of slots 285 to 287 (section 4)"; append to H-37 and H-39 "Guard: none; the report states that no guard is tested"; region 5 list becomes "(H-38 overshoot, H-40, H-41 and H-42 defects, H-43 machinery MAJOR, H-44 slips)".
- RV1-2 MINOR §7:156 vs §2:47, §4:94. Region 5 tests a guard "rose above its pre value", but H-38's pre value is a single confounded overshoot on the excluded day 2026-11-12, the bridge baseline lists unclassified 5-hour stops at 97 % and 95 % on Nov 11-12, and §2 requires zero; the comparator is ambiguous. Fix: "Region 5 reads each guard against the comparator stated in section 2: H-38 zero unconfounded overshoots in post windows; H-40 to H-43 post median at most the pre median; H-44 post median at most 0. Pre-period overshoots are reported descriptively."
- RV1-3 MINOR §3:80 vs §2:45-47, §4:100, §8:171. Stopping "at the earlier of the minimum n reached for every hypothesis or 2026-11-26" can truncate the declared post windows (days to 11-19, slots to 292), and a post slot merging after Nov 19 cannot close its 7-day issue window by Nov 26. Fix: "The study stops at 2026-11-26 or, if earlier, when every declared post unit is complete (2026-11-19 ended, the last post slot at PACKET r1, every post slot's 7-day issue window closed); reaching the minimum n does not stop collection. A slot whose 7-day window is open at the stop has postMergeIssues7d missing."
- RV1-4 MINOR §3:76 + §4:99. Slot 288 is a post slot for H-40, yet its contract/source/reader rounds (2/2/2) were seen before the freeze and sit in the pre-constant column, and the cap reached R00 inside 288 (bridge step 4 "rule to R00 at 288"), so 288 is transitional. Fix: "H-40: pre slots 285 to 287; slot 288 excluded (transitional: the cap reached R00 inside it and its rounds were seen at the freeze); post slots 289 to 292" and drop "288: contract 2, source 2, reader 2" from the pre-constant column.
- RV1-5 MINOR §7:163 vs §4:107, §2:58. 22.2 is itself rounded (532/24 = 22.1667) and 18.87 = 0.85 x 22.2, not 0.85 x 22.1667 = 18.842; 365K vs 0.75 x 487K = 365.25K is undeclared; both conflict with "computed on the raw values, never on rounded ones". Fix: "The H-44 thresholds 365K tokens and 18.87 minutes are absolute constants fixed at this freeze from the rounded baselines 487K and 22.2; the raw-values rule applies to post values and to ratios of medians."
- RV1-6 MINOR §2:56, §3:77 vs REGISTER.md:53. PREREG H-43 guard is "the pre median" (288, plus 287 "where the monitor can reconstruct") while the register says "do not exceed 4 (slot 288's count)"; a post-freeze reconstruction of 287 would move the baseline. Fix (both files): "machinery MAJOR findings per post slot (median) do not exceed 4 (slot 288)"; §3:77 "slot 288 (single-slot baseline); 287's counts, if reconstructed, are descriptive only".
- RV1-7 MINOR §5:110-120. Missing material confounders: (a) intervention fidelity (no record that /autocompact 500k was typed, a GO chain issued, a dry c2 run, per unit); (b) other changes inside the post window (steps 5-8, new conventions, model or effort changes, monitor session restarts that reset context per call); (c) slot 288 baseline partly exposed to H1-H4, all landed during it on 11-12; (d) the bundle row covers H-37..H-39 only though H5-H8 all start at 289 (§9:175). Fix: add rows "| intervention fidelity | `fidelity` {h1..h8: true/false} per day and slot | a unit without its intervention is excluded from that hypothesis and counted |", "| other changes in the post window (steps 5 to 8, conventions, model or effort, monitor session restarts) | dated `changes[]` {date, kind} | later units flagged; all post units flagged gives U3 |", "| slot 288 partly exposed to H1 to H4 | none | H-41 to H-44 carry the tag 'baseline partly treated' |"; bundle row: "H-37 to H-39 cannot be separated, nor H-41 to H-44 (H5 to H8 all start at slot 289); each verdict names the bundle".
- RV1-8 MINOR §6:134,137 vs §4:95, §2:56. The confounded-overshoot test needs the usage percent at fan-out start, but `overshoots[]` has only `fanOutInWindow` (type undefined) nested under per-session days although windows are account-level; `slots[]` has no product/machinery kind for H-43's "post product slot". Fix: "top-level `windows[]` {`windowEnd`, `usageAtStop`, `fanOut3PlusStartUsage` (percent or null)}; `slots[]` gains `kind` (product or machinery); H-43's minimum is 3 post product slots."
- RV1-9 MINOR §6:143-144. Only `meterSha256` is held fixed across deliveries; the extractor can change silently. Fix: "the evaluator refuses a delivery whose `meterSha256` or `extractSha256` differs from the first delivery's, and the register row records both."
- RV1-10 MINOR §0:22 + §4:85. "Every baseline number below is copied from those two bridge files" and "pre values are constants pinned here at the freeze" conflict with the two MON-LAB-FACTORY-2 constants and with pre medians the evaluator computes from the pre delivery (H-37, H-39, H-40). Fix (line 22): "Every fixed baseline number below is copied from those two bridge files, except the two slot-288 constants pinned in section 4 from MON-LAB-FACTORY-2; the pre medians of H-37, H-39 and H-40 are computed by the evaluator from the pre-period delivery under the pinned producer digests."
- RV1-11 MINOR §4:101 + §2:53. "c2 builds" does not say whether C10's uncommitted dry c2 counts; H-41 flips on that choice. Fix: "c2 builds: committed c2 builds before PACKET r1; the dry c2 of C10 is not counted and is recorded as `dryC2Runs`."
- RV1-12 MINOR §2:49 + §3:75. H-39 does not say whether verify-start and post-push events share one pooled median or are tested per kind (a changed event mix moves a pooled median), and the pre load window has no start bound. Fix: "the pooled median of start load and post-push load over events without other-app load is at most 0.70 of the pooled pre median; each kind is also reported separately" and §3:75 "events from 2026-11-05 00:00 to 2026-11-12 11:05 local".
- RV1-13 NOTE §1:36. The H3 cost cell quotes "5.21 / 10.14 / 12.68 right after", a post-intervention load inside the excluded purge window, which reads like an early result (§12). Fix: append "(inside the excluded 11:05-12:00 purge window; not a result)".
- RV1-14 NOTE §4:103 vs §4:107. "about 8.5" hours scope to PACKET r1 vs the 532-minute (8.87 h) step span stated as the same window; "8.5" is not in FACTORY-IMPROVEMENTS.md. Gate unaffected (H-42 thresholds are absolute). Fix: "about 8.5 (brief; the step-report span is 8.87 h)".
- RV1-15 NOTE §2:47,51,58. The primaries of H-38 (hourly watch), H-40 (cap 2) and H-44 context (/autocompact 500k) are largely fixed by the intervention settings; H-40 also covers every series while bridge step 4 caps "contract series ... by default". Suggest labelling them "manipulation check" in the report.
- RV1-16 NOTE §2:58. The slip guard on the median with pre 0 tolerates slips in a minority of post slots; consider "total lost-detail slips over post slots at most 1". Accepted as registered.
- RV1-17 NOTE §7:155. Region 4 says "names as voiding" but §5 never uses that word; only account switches and limit resets (§5:115) lead to U3. Fix: "a confounder flag that section 5 sends to U3".
- RV1-18 NOTE §4:107-108 + §5. The producer is the intervening party: lost-detail slips, rulings waited on and other-app flags are monitor-labelled, and whether the scope message opens the first step interval is unstated. Suggest a lab spot-check against bridge lane step notes and "the first interval starts at the scope message".
- RV1-19 NOTE checks passed: digest 467c636c matches the register (4 places); draft 6c0e8f61 matches; the FACTORY-IMPROVEMENTS.md working copy hashes to 0bc476b1cfc8e633...; all five quoted digests are 64 hex; 532 min / 24 intervals and 18.87 = 0.85 x 22.2 hold; 144/872 = 16.5 %; register H-37..H-42, H-44, RL-23 match; §7:165 and §9 keep "consistent with", no causal promotion.

## Disclosures

- Read: research/experiments/RL-23/PREREG.md (shasum; sed 1-70, 71-140, 141-215; line-number greps); research/hypotheses/REGISTER.md (sed lines 47-54, 85 (table header, to read the RL-23 columns), 110; wc; a locating grep); handoff/FACTORY-IMPROVEMENTS.md (shasum; sed 1-67 cut at 260 chars; wc); ls -l of those two files; existence test of the PAUSE path (never PAUSED) and of this scratchpad folder.
- Slip: the locating grep over REGISTER.md printed 60-character prefixes of lines 46 (H-36 row) and 125 (rule J), outside the named rows. FACTORY-IMPROVEMENTS.md quotes a path under ~/.local/state as text; it was not opened.
- Not checked (outside read scope): the brief's 24-line count and digest, FACTORY-CONVENTIONS.md and README.md digests, the "differs from the draft only by" claim, the 4 MAJOR / 8.5 h sources. No network, environment, git config, transcripts or deliveries read.

## Review 2, of PREREG v2 (969489d7), 2026-11-12: FAIL

Verdict as written: CHANGES_REQUIRED (1 MAJOR, 4 MINOR, 3 NOTE); delta-scoped, the last round (C5). Custody: the Lane-Monitor
briefed a fresh reviewer from the frozen v2 (brief sha256 prefix cde3ed3934a5adb5, redacted copy in research/reviews/);
the lab did not brief it. Context: a fresh subagent context. Model family: Claude Opus (claude-opus-5-5), a different
family from the lab's author. Review file RL23-REVIEW-R2-83db5a01.md, sha256 83db5a011f5f8dadb7381f58641d203b9797d8beb8b7203cabb2a9f62ae838ae, 43 lines,
copied verbatim below; closure in PREREG v3 (0fa0d594) section 15, together with the monitor's correction of
the minutes-per-step constant (MON-LAB-FACTORY-6). No round 3: v3 closes by script-checked claims on the monitor's check.

---

# RL-23 PREREG v2 blind review r2 (delta-scoped, last round)

Digests verified with shasum -a 256: v2 969489d7 (270 lines), v1 467c636c (215 lines), r1 findings 3ecd616c (31 lines).

verdict: CHANGES_REQUIRED (1 MAJOR, 4 MINOR, 3 NOTE)

## Closure check (RV1 to v2 section 14, cited as v2 section:line)
- RV1-1 CLOSED: H-37 §2:49 and H-39 §2:54 state "Guard: none"; H-41 §2:57-58 and H-42 §2:59-61 carry the defect guard as worded; region 5 §7:179-182 lists the guards and names each comparator. A residual gap is filed as RV2-5.
- RV1-2 CLOSED: §7:179-182 (H-43 comparator 4, in line with RV1-6); pre overshoots descriptive.
- RV1-3 CLOSED: §3:92-95, as worded.
- RV1-4 CLOSED: §3:88 (288 transitional, post 289-292), §4:113 (the 288 rounds are dropped), §2:55.
- RV1-5 CLOSED: §2:64-67. The "(0.75 and 0.85 of them)" is approximate (0.75 x 487K = 365.25K); harmless because the constants are declared absolute.
- RV1-6 CLOSED: §2:62-63, §3:89; register H-43 reads "4 (slot 288's count)".
- RV1-7 PARTLY: the fidelity, 288 partly-treated and bundle rows (§5:133,135,137) are as worded; the changes row §5:134 and §6:154 add "compactions", which is not in the round-1 wording (RV2-1).
- RV1-8 CLOSED: §6:152-153, §6:156 `kind`, §3:89 H-43 minimum. The single-value field is filed as RV2-4.
- RV1-9 CLOSED: §6:163-165.
- RV1-10 CLOSED: §0:24-26 adds "or the brief" (accepted: the brief is a pinned input, §0:19); §4:99-101 also drops a clause (RV2-6).
- RV1-11 CLOSED: §2:57, §4:115, §6:157 `dryC2Runs`.
- RV1-12 CLOSED: §2:52-54, §3:87.
- RV1-13 CLOSED: §1:39.
- RV1-14 CLOSED: §4:117.
- RV1-15 CLOSED: §2:74-76.
- RV1-16 PARTLY: I ACCEPT the deviation. The median form matches the other guards, and round 1 itself said "Accepted as registered". But the descriptive total that §14:264 promises in "section 2 (H-44), section 9" appears in neither section (RV2-2).
- RV1-17 CLOSED: §7:178; §5:129 and §5:134 are the rows that send to U3.
- RV1-18 CLOSED: §4:121 first interval; §6:165-167 spot-check, kept outside the gate. The baseline consistency is filed as RV2-3.
- RV1-19 CLOSED: no action needed. The counts 1/11/7 and the 19 table rows match the round-1 file.

## New findings
- RV2-1 MAJOR §5:134 + §6:154. v2 adds routine compactions (four on 2026-11-12 alone, §4:122; and the compaction point is H8's own setting) to the dated `changes[]` rule "units after a change are flagged; all post units flagged gives U3". A compaction dated in the post window before slot 289, or on 2026-11-13, therefore sends H-40 to H-44 (and at least flags most post days) to U3 by construction, whatever the data show. Fix I accept: in §5:134 replace ", compactions" with ", a change to a compaction setting" and append to its handling "; routine compactions are not changes and flag no unit"; in §6:154 replace "compaction" with "compaction-setting change".
- RV2-2 MINOR §14:264 vs §2:64-67, §9:198-206. The RV1-16 closure cites a descriptive slip total that no section of v2 states. Fix I accept: append to H-44 (§2:67) "The total of lost-detail slips over post slots is reported descriptively." and change the §14:264 location cell to "section 2 (H-44)".
- RV2-3 MINOR §4:121. The new "the first interval starts at the scope message" rule gives N intervals for N step reports when the scope message comes before the first report. The pinned 288 baseline is 25 reports, 24 intervals from 09:58, and it does not say that 09:58 is the scope message, so post slots may be measured with one more interval than the baseline behind 18.87. Fix I accept: append to the 288 cell "(the 09:58 point is the scope message)" if the monitor confirms this; otherwise replace the clause with "the first interval starts at the first step report, as in 288's 24 intervals".
- RV2-4 MINOR §6:152-153 vs §4:109. `fanOut3PlusStartUsage` holds one percent per window, but a window can hold several fan-outs, and the H-38 guard (§7:180) flips on which one is recorded. Fix I accept: "(the highest percent at which a fan-out of 3 or more sessions started inside the window, or null)".
- RV2-5 MINOR §3:89 + §7:180-181. The new H-41/H-42 defect guards read H-40's pre slots 285-287, but section 3 sets no pre minimum for them. If those pre defects are missing, region 5 cannot be computed and SUPPORTED can be reached with the guard untested, which is the RV1-1 risk again. Fix I accept: §3:89 minimum "3 post slots, and for H-41 and H-42 also 2 pre slots (285 to 287) with later-found defects (H-43: 3 post product slots)".
- RV2-6 NOTE §4:99-101 (check 3). v2 drops v1's "named in the file, and this document is re-versioned if that figure is not available", which goes beyond RV1-10's wording. It is acceptable because the pre medians now come from the delivery. Fix I accept: append "a pre unit without the figure is not a unit (section 7, U1)".
- RV2-7 NOTE §7:189. The tag list omits "baseline partly treated" (§5:135). Fix: '("unmatched shape", "single baseline", "baseline partly treated")'.
- RV2-8 NOTE §11:215. "This text is frozen as `experiments/RL-23/PREREG.md` v1" is now stale. Fix: "This text was first frozen as `experiments/RL-23/PREREG.md` v1 (kept as `PREREG.v1.md`), with its digest in the register's RL-23 row".

Check 3: every other v1-to-v2 change is a closure, a pin, a digest, the registration record (§0:1,9-12; §11:221-222) or the self-check (§13:242-243). Check 4: the windows, slot ranges, IDs and register rows H-37..H-44 and RL-23 agree with v2; the gate order is unchanged, and exactly one region applies, except the defects in RV2-1 and RV2-5. Check 5: §12 holds. The only post-intervention numbers (§1:39) are labelled "not a result", and "consistent with" is kept (§1:32, §7:190).

## Disclosures
- Read: PREREG.md and PREREG.v1.md (shasum; wc; diff -u v1 v2 in full via sed ranges 1-239, cut at 400 chars; sed v2 14-26, 29-34, 124-138, 172-191, 192-212, 213-244; greps over v2 with -n); the r1 file (shasum; wc; cat -n); REGISTER.md (sed 47-54 and 110, cut at 700 chars). Each command first ran an existence test on the PAUSE path (never PAUSED); the scratchpad folder got one existence test.
- Slip: the locating grep over REGISTER.md printed 12-character prefixes of lines 46 (H-36), 85 (table header) and 125 (rule J), outside the named rows.
- Not checked (outside scope): FACTORY-IMPROVEMENTS.md and the brief digest; whether 09:58 was the 288 scope message (RV2-3); §13's script claims. No network, environment, git config, transcripts, deliveries or ~/.claude read.

## Review 3, of PREREG v3 (0fa0d594), 2026-11-12: PASS (closure by script-checked claims; not a reviewer round, C5)

The series closed at two reviewer rounds. The Lane-Monitor read the claims script (RL23-V3-CLAIMS.py, sha256 78c30a8a,
38 lines) and ran it from the bridge root with the isolated interpreter: "CLAIMS OK: 21 of 21", rc 0; its own path and
at-sign scans of the diff and of research/reviews read 0; relayed as MON-LAB-FACTORY-7 with the word PASS. The header
form is the charter's, so the checker reads v3's closing verdict; no third reviewer pass ran.

## Review 4, of PREREG v4 (2bbd9728), 2026-11-12: PASS (closure by the extended claims after preflight finding P1; not a reviewer round, C5)

v4 differs from v3 by the `scopeDate` field on slots[] and the slot rule in the changes row (PREFLIGHT.md, finding P1).
The Lane-Monitor read RL23-V4-CLAIMS.py (sha256 e4a6bd29, 43 lines; the v3 claims plus the P1 claims) and ran it from
the bridge root with the isolated interpreter: "CLAIMS OK: 26 of 26", rc 0; relayed as MON-LAB-FACTORY-8 with the word
PASS; bridge checkpoint e9cc04fb. The evaluator (9c08695c) runs on this digest only.

