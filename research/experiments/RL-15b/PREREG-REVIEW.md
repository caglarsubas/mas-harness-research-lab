# RL-15b preregistration review (charter step 1a), 2026-11-07

Review 1 of PREREG v1 (e5a75db2) by an independent pass that held only the PREREG, the register row (given inline)
and the charter; it never saw the tools, the preflight or any run output. Verdict PASS; five non-blocking notes,
each with the lab's handling below. The review text as returned:

VERDICT: PASS

R1: PASS - The gate names three regions evaluated in a fixed order: PASS (17 of 17 catchable refused, 0 unattributed, new rules at least 2 M4 and 2 M6, 0 of 3 controls non-zero), FAIL (a class with no catchable refusal, any control non-zero, or neither new rule firing) and UNRESOLVED as the explicit remainder (a built or crashed catchable instance, an unattributed refusal, a new-rule count below expectation, or a failed precondition). PASS and FAIL cannot both hold, the order settles any FAIL/UNRESOLVED overlap, and the hypothesis is falsified by a concrete observable (a false positive, an uncaught class, inert new rules).

R2: PASS - The hypothesis names the catchable instance as its unit and the design counts builds after exactly one edit, with the third M6 instance declared uncatchable before the run for a stated structural reason (a secondary paper names no file), giving the denominator 17 in the hypothesis, the measures, the gate and the expectation alike. "Attributed" is operationalised as a lock-40 tag (NEW) or one of eight fixed older wordings (OLDER), which is a narrower proxy for "the older rule that ran first"; the mismatch resolves conservatively to UNATTRIBUTED and UNRESOLVED and is declared as the most-likely departure.

R3: PASS - Both tools, the builder and roadmap.json at commit ded99886, the 35-file base manifest, the RL-15 PREREG v5 and the run-002 output are pinned by sha256 in the inputs table, and every value the evaluator consumes (seed, tag strings, wording list, thresholds) is written into this frozen text. The erratum and run-001's messages are declared sources without a digest; see note 1.

R4: PASS - Every bound is a count over named units (instances of 17 or 3, controls of 3, unattributed of 17) with an explicit gate; the single seed 20261105 is declared with the reason it is kept; no split applies and the interval and non-inferiority rules do not apply to exact counts. The PREREG does not say in words that the build is deterministic, which is what makes k = 1 adequate; see note 4.

R5: PASS - Light run, 22 builds under 10 s, on the monitor's word, stream S2, 0 ECU, no network, python -I -B, TMPDIR in the lab scratch, no bytecode; the preflight adds 3 builds stated separately.

R6: PASS - No item text copied; the output carries ids, field names, exit codes, validator messages and wall times; privacy_scan.py over every file before reporting; the layout is given as a placeholder and no handle, name token or local path appears in the PREREG. Whole-message capture widens what the output carries, and the scan clause covers it.

R7: PASS - The dependence is declared in full: the seed and targets are those of run-002, whose draws, messages and counts the lab already knows; the expected counts are copied from the design authority's erratum; the older wordings were read from run-001 and run-002 refusal messages, never from the builder's source; the uncatchable declaration comes from run-002's finding. The named departure (UNRESOLVED by one unattributed refusal) is a real alternative with its consequence fixed (a wording-list finding, no re-tune under this id).

NOTES:
1. R3 lineage (non-blocking): the erratum MON-RL15-D1-RESTATED and RL-15 run-001's data are named as the sources of the two tag strings, the expected counts and part of the wording list, but carry no sha256. Because those strings and counts are transcribed into this frozen PREREG, the verdict does not depend on them; record both digests in the run record or the register row rather than reopening v1. The preflight check P4 ("match the erratum's exactly") should cite that digest when it runs.
2. R2 control asymmetry (non-blocking): a seeded instance is "refused" only with the roadmap.json: prefix (a bare non-zero is a crash), while a control counts as refused on any non-zero exit, so a crashing control is scored as a false positive and FAIL. This is declared and conservative; if it happens, the report should call it a crash, not a refusal, so the FAIL is read correctly.
3. Preflight boundaries (non-blocking, for the run pass): P2's four synthetic outputs exercise 17 of 17, controls 0, and new rules at the threshold, but not the M4 = 1 case (one new rule fires below expectation, which must read UNRESOLVED, not FAIL) nor a class with zero refusals (FAIL). Charter 1b (iv) asks for a value at each boundary; add those two fixtures to PREFLIGHT.md as checks beyond the four named. P4 covers message length; if the builder can emit more than one stderr line, confirm the tag sits on the last line, since "whole message" means the last line.
4. R4 wording (non-blocking): add one sentence that the builder is deterministic for a given input, so one seed is the design and the charter's k >= 3 does not apply; and the run record should count the preflight's 3 builds beside the 22 (25 light builds).
5. R7 framing (non-blocking): the expectation was written with knowledge of run-002's outcomes, so a PASS confirms the design authority's reading of run-002 on a corrected instrument rather than a fresh prediction; say so under "what it does not show" in the report. The expected arithmetic is consistent (4 new-rule refusals plus 13 older equals 17).

## The lab's handling of the notes (PREREG v1 stays frozen; nothing here changes a criterion)

1. The erratum reached the lab as the monitor's relayed message MON-RL15-D1-RESTATED (no file, so no digest); its
   tag strings and counts are transcribed in PREREG v1, and RL-15 run-001's data digest is ed7ce16d (its RESULTS
   050c553c), to be cited in the run record.
2. Accepted: a non-zero control exit without the `roadmap.json:` prefix will be reported as a crash under FAIL.
3. Done after the review (preflight addendum, two more synthetic inputs through the evaluator, no build): the
   M4 = 1 case reads UNRESOLVED and a class with zero refusals reads FAIL; `data/preflight/preflight_addendum.json`.
   The builder's refusals are single `fail()` lines and the tool reads the last stderr line, as RL-15 did.
4. Determinism: RL-15 run-001 recorded the build as deterministic (seed-independent given the input), which is why
   one seed is the design; the run record will count 25 light builds (3 preflight + 22).
5. Accepted for the report's "what it does not show".
