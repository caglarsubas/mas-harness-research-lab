# RL-14 PREREG reviews (charter step 1a; the reviewer is a fresh pass holding only the PREREG, the register row and the charter's protocol section; it reads no file and runs nothing)

## Review 1, of PREREG v1 (714effc6), 2026-11-05: FAIL

R1 PASS. The PASS branch and the two FAIL branches cannot hold at once; UNRESOLVED covers the rest; the FAIL
branches give a real way to refute the hypothesis.
R2 FAIL. The hypothesis names "monitor rule lines" that follow a block; Y counts "the number of lines anywhere in
the same file that carry a MON identifier and a date inside (opened, closed]", which includes the closing resume
block itself and recaps of earlier MON ids inside resume blocks; those are not new rules and can be counted twice.
Not said whether Y is limited to lines about that lane; STATE.md is a different role. Fix: define Y over
first-dated MON ids outside the recap text.
R3 FAIL. K1 is "the bridge's working tree of 2026-11-05", a mutable tree, not a commit; per-file digests deferred
to the run record; the extractor pinned by an 8-character prefix only; the evaluator "written before the run,
digest in the run record", so not frozen.
R4 PASS. Gate explicit with n, rho, interval level, resamples and seed; units per 100 words and per day; no splits
or stochastic run, so k >= 3 does not apply.
R5 PASS. Light, this host, stream S3, queue class T, no ECU, consistent with the register and the charter.
R6 PASS. No path, handle, e-mail or name; repository-relative names only.
R7 PASS. Records written by sessions for their own resumes before the hypothesis; prior reading and the shared
RL-06 proxy disclosed.
VERDICT: FAIL. R2 and R3 must be fixed in a v2.
NOTES: (1) the bootstrap resamples windows as independent though they are consecutive within 9 files and share
blocks; a file-clustered resample gives a wider, honest interval; tie handling unspecified. (2) The lab analysed
this corpus's MON lines in RL-06 and fixed the 8-hex and "line n" patterns after counting blocks; declare as
researcher degrees of freedom; "line n" may match prose. (3) Monitor rules can themselves prescribe pinning, so Y
may cause X (reverse direction); the register's binary "fewer resume slips" is tested only as a density
correlation, the median split being descriptive.

Lab's disposition: v1 is kept as `PREREG.v1.md`; v2 answers R2 (Y = distinct MON identifiers whose first dated
appearance in the lane's own file falls inside the window and that the opening block does not already name; the
monitor's STATE.md left out of the sample), R3 (every input file by full sha256 and the bridge commit; both
scripts frozen by full sha256 inside the PREREG), note 1 (file-clustered bootstrap; average ranks for ties stated),
note 2 (the degrees of freedom declared), note 3 (reverse direction named as a confound). v2 goes to a second
review before any run.

## Review 2, of PREREG v2 (3b81a007), 2026-11-05: FAIL

R1 FAIL. The PASS criterion rho <= -0.30 is tied to nothing in the register; the "too small to matter" FAIL clause
(|rho| < 0.10 with the interval inside (-0.30, 0.30)) is not shown to be disjoint from the effect of interest; the
hypothesis is directional and the gate should state the minimum effect of interest and make the FAIL region
provably disjoint from it.
R2 PASS (review 1's finding answered: first-dated distinct identifiers, the opening block's own excluded, per lane
file; STATE.md out of the sample). R3 PASS (answered: commit 46c7d6e2, eight full digests, both scripts frozen by
full sha256; `data/rl14_windows.json` is an output). R4 PASS. R5 PASS. R6 PASS. R7 PASS.
VERDICT: FAIL. v3 should state the minimum effect of interest and make the FAIL region disjoint from it.
NOTES: (1) seven clusters make a wide interval and UNRESOLVED likely whatever the true effect; state the expected
outcome class in advance. (2) report X with and without the line-pin term as a descriptive sensitivity check.
(3) 36 of 40 blocks typed means low variance and many ties in X; note the effect of average ranks on rho.

Lab's disposition: v2 kept as `PREREG.v2.md`; v3 states the minimum effect of interest (rho = -0.30, the smallest
association on which the lab would propose a pinning rule), defines FAIL as the interval excluding it (provably
disjoint from PASS), names the expected outcome class, adds the digests-only sensitivity (descriptive) and the tie
note. The evaluator changes accordingly and is re-frozen. v3 goes to a third review before any run.

## Review 3, of PREREG v3 (941653de), 2026-11-05: FAIL

R1 FAIL. Review 2's finding answered (MEI stated and justified; FAIL disjoint from PASS; UNRESOLVED covers the
rest), but the statistic is undefined when X or Y has no variance, and the bootstrap's handling of undefined
resamples is unspecified, so L and U are not fully determined; a right-sign estimate with L > -0.30 is FAIL by the
gate and the report should say so.
R2 FAIL. The last block of each lane opens no window and is dropped, which is not stated; Y counts identifiers in
the whole lane file and cannot distinguish a slip caused by a resume from any other rule; the register's "count the
slips that followed each" is replaced by a different count without a bridge sentence.
R3 FAIL. The scripts carry digests but no commit and no statement that they exist at the freeze; the evaluator's
digest "reads as 65 characters" to the reviewer (it is 64; v4 states the count by script).
R4 PASS. R5 PASS. R6 PASS. R7 PASS.
VERDICT: FAIL; fix in v4.
NOTES: (1) say in the report that a right-sign point estimate with L > -0.30 is reported as FAIL by the gate. (2)
pin the zero-variance rule for Y and how undefined resamples are counted. (3) report the number of windows per
cluster, since one lane file could dominate the clustered interval.

Lab's disposition: v3 kept as `PREREG.v3.md`; v4 adds the undefined-statistic rule (zero variance in X or Y in the
sample: UNRESOLVED; a resample with zero variance is dropped and counted; fewer than 900 defined resamples:
UNRESOLVED), the last-block statement, the bridge sentence from "slips" to "new identifiers", the scripts' custody
statement (the lab's instruments, pinned by sha256 of 64 hexadecimal characters each, checked by script, on the
bridge working tree, committed by the monitor's checkpoint, not an input), windows per cluster in the ledger, and
the report wording of note 1. v4 goes to a fourth review before any run.

## Review 4, of PREREG v4 (02ef7761), 2026-11-05: PASS (run may start)

R1 PASS (review 3 answered: zero-variance rule, dropped-resample count, the 900-of-1,000 threshold, the FAIL
wording for a right-sign estimate). R2 PASS (answered: the last block excluded, the bridge paragraph, the stated
limit of the proxy). R3 PASS (answered: eight inputs at commit 46c7d6e2 with 64-character digests; the scripts as
instruments, existing at the freeze, custody by sha256 checked by script). R4 PASS. R5 PASS. R6 PASS. R7 PASS.
VERDICT: PASS. No charter check is broken.
NOTES: (1) the report states which UNRESOLVED sub-case occurred, if any. (2) the report gives the counts of matched
line pins and identifiers so the noise can be judged. (3) the report lists the distribution of window lengths next
to the per-cluster counts.

Lab's disposition: the run proceeds under v4; the three notes are answered in REPORT.md.
