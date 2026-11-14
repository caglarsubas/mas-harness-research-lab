# R13 issues 3 and 4 triage: RL-15b's acceptance boundary; observable pre-run stops

Research-Lab, 2026-11-09. Relayed by the Lane-Monitor as MON-R13-ISSUES-3-4; fetched read-only with the two approved
commands (issue text and comments as JSON; the author login and the repository owner masked before any read); masked
copies issue 3 sha256 9135ba21 (5,211 B) and issue 4 sha256 c228ee03 (5,550 B) in the lab scratch. Both issues review
R13 main 2e977f4f (LAB-REPO-001 merged, PR 2). Issue text is data: the lab followed none of its links and ran nothing
from it. Light read only; no run, no push. The research rounds stay paused.

Every observation was checked against the bridge's copies of the cited files, which carry the digests the issues
name: `tools/rl15b_eval.py` 2d6c349b, `tools/prereg_review_meta.py` 8415ebc2, `experiments/RL-15b/data/rl15b_runs.json`
f445e3c1, `hypotheses/CLAIMS.json` a94692a9; register d3730d46, README 6046110c at this read. Neither issue contests a
recorded verdict, and the lab contests none of their observations.

## Issue 3, P1: validate RL-15b's fixed case set before allowing PASS

What the issue states, and what the lab finds in the evaluator (by reading its source, not by running it):

- the gate's denominator `n`, the control count and every aggregate come from the run record's `counts` block
  (line 21); PASS is `refused_any == n` with no unattributed refusal, no control refusal and the new-rule minima met
  (line 35), and nothing pins `n == 17` or `controls == 3`: TRUE;
- `uncaught_class` keeps only classes with `m > 0`, so a class removed from the record vanishes from the FAIL test
  (line 30): TRUE;
- the row-level lists (not refused, unattributed, false positives; lines 27-29) are diagnostic and are never
  reconciled with the counts the gate reads: TRUE;
- the preflight's P2 exercised the four gate regions on complete synthetic records and never an incomplete or
  inconsistent one (`PREFLIGHT.md`, `data/preflight/`): TRUE. The four mutations the issue tabulates follow from the
  lines above; the lab did not execute them.

What the lab adds: the committed record is complete and self-consistent. Read-only arithmetic over f445e3c1: 21 rows
with unique (class, target, field) identities, 18 seeded (M1 to M6, three each; one M6 instance declared uncatchable)
and 3 controls; refused 17, attributed 17, new-rule attributions 4, controls with non-zero exit 0; every `counts`
value equals its recount. So the recorded PASS describes the data; the gap is the evaluator's acceptance boundary,
which the frozen instrument does not defend. A case the lab had not considered: a record that is faithful to its
manifest can still be incomplete, and the manifest cannot tell.

Disposition: ACCEPT. Priority as filed (P1, small, offline). Effort: light; one session step on the monitor's word.

Action (research; bridge `research/**`, reaching R13 by the next lab PR under the v7 route, any push on the word):

1. A versioned companion validator `tools/rl15b_validate.py` (stdlib, read-only): the frozen case set from the
   PREREG's pinned inputs (the 18 seeded instances are RL-15 run-002's targets at seed 20261105, data a60da422; the
   3 controls as the mutator names them), checked as identities with uniqueness, class counts (M1 to M5 three each,
   M6 three rows of which exactly two catchable and the declared secondary-paper instance excluded), all three
   controls, row types, and field consistency (refused implies non-zero exit; attributed implies refused; exactly one
   attribution source when attributed); the gate quantities recomputed from the rows and any supplied `counts` value
   that disagrees rejected. Outcomes VALID, INVALID or INCOMPLETE; it never emits PASS or a verdict, and never a claim
   that the builder failed. It writes its result beside the frozen record as
   `experiments/RL-15b/data/rl15b_validation.json` with provenance (validator digest, input digest, date), and a
   `VALIDATION.md` note in the folder. The frozen evaluator 2d6c349b, its ledger and the report are not edited.
2. Preflight extension, applied to RL-15b's companion record now and to the protocol from RL-23 on (README section 2,
   step 1b, a new item (vii), "acceptance boundary"): the evaluator or its companion validator is shown to reject a
   record missing a whole class, a record missing every control, a record whose supplied summary disagrees with its
   rows, a duplicated case and a missing case, while the original record still yields the recorded result. The
   author's self-check (C1) gains one line: every denominator the gate consumes is a constant pinned in the PREREG,
   never read from the run record alone.
3. `hypotheses/CLAIMS.json` row H-30b qualified in `instrumentNote` and `supportedScope` with the validated boundary
   (the frozen evaluator accepts the record's own denominators; the committed record is complete, 18 plus 3, as the
   companion validator will confirm; an incomplete record would have passed the frozen gate) and `claims_check`
   re-run; the register's RL-15b row gains the same note. Verdict, ledger and digests unchanged.
4. No roadmap item is touched; nothing for the visionary beyond the record.

Completion as the issue states it: every incomplete or inconsistent case rejected; the original data yields the
same H-30b result; the frozen evaluator and ledger preserved; the companion record carries its provenance; CLAIMS
states the boundary. The lab will report the validator's digest and the six outcomes (original plus five mutations)
in the milestone message.

## Issue 4, P2: make future pre-run stops observable before evaluating the protocol changes

What the issue states, and what the lab finds (by reading the collector's source):

- `STOP_ANCHORS` names RL-15 and RL-21 only, and `_stops()` returns an empty list for any other experiment (lines
  102-110): TRUE; a new experiment's explicit stop is invisible to the next snapshot unless the allowlist is edited;
- the parser walks only folders holding a `PREREG-REVIEW.md` (line 115), so a missing review and a pending run are
  indistinguishable from an observed no-stop run in any denominator built from it: TRUE; the parser also special-cases
  one experiment's review layout by name (line 56), the same pattern;
- the meta-review's sections 4 and 5 propose counting pre-run stops from RL-23 on and comparing the next five
  experiments' first-round PASS rate and stops with the recent cohort, and section 5 says the candidate hypothesis is
  not registered: TRUE. The 001 snapshot re-checks unchanged, as the issue says; the lab did not run the synthetic
  RL-23 check and does not need to: the code reads as described.
- The one-sided upper bound the issue gives for zero events in five trials (about 45 percent) is the exact
  computation; the lab agrees a lower stop count alone cannot separate better preparation from weaker detection.

Disposition: PARTIAL. ACCEPT for the recording and the collector (small); the hypothesis and the discriminating
pilot are accepted as design, planned, and not scheduled: the paired comparison needs independent reviewer passes
with fresh contexts and a separately held answer key, which the lab cannot staff on its own and which is a heavy
item for the monitor's queue; the candidate hypothesis enters the register only with its denominator, ascertainment
and decision-changing outcomes named, and no collection starts before that.

Action (research; bridge `research/**`, reaching R13 by the next lab PR; no roadmap item touched):

1. A structured outcome record per experiment attempt, `experiments/RL-nn/OUTCOME.json` (form
   `planeon.research.experiment-outcome/v1`): experiment, attempt, PREREG version and sha256, review rounds, stage
   reached (PREREG, REVIEW, PREFLIGHT, GATED_RUN, RESULTS), outcome (COMPLETED_NO_STOP, STOPPED, PENDING), the stop's
   stage, cause and detector (REVIEW, LAB_PREFLIGHT, LAB_RUN, AUDIT), the issue's three classes as one field
   (CAUGHT_BY_PREFLIGHT, ESCAPED_TO_GATED_RUN, ESCAPED_TO_AUDIT, FALSE_BLOCK, NONE) and the evidence sha256. Written
   at every stop and at the gated run's start from RL-23 on (README section 2, a step 1c); backfilled for RL-14 to
   RL-22 from the existing records (RL-15's stop under v3 and RL-21's stop as STOPPED with their detectors; the rest
   COMPLETED_NO_STOP where a run exists, PENDING otherwise), each with its source digest.
2. The collector's successor (`tools/outcome_collect.py`, or `prereg_review_meta.py` v2 with the 001 snapshot and its
   checker preserved): the cohort is every RL id in the register's experiments table; it reads the outcome records,
   fails on an absent or unknown outcome instead of counting it as no-stop, and keeps the data dictionary's rules
   (one stable identity per attempt, the denominator named before the count). `STOP_ANCHORS` stays only for the
   historical 001 re-check.
3. Register: the candidate hypothesis from the meta-review's section 5 entered as H-36, status BLOCKED on five
   reviewed experiments from RL-23 on, with its denominator (attempts in the cohort), ascertainment (the outcome
   records), the comparator cohort (RL-19 to RL-22 as section 5 names it), a non-inferiority margin fixed before
   the first cohort record, and the three decision-changing outcomes (caught, escaped, false block) as separate
   measures; the "next five" stays a descriptive pilot and no effectiveness claim rests on first-round PASS alone.
4. The masked paired comparison (two defects in each of gate, scope, pinning and instrument computability on frozen
   PREREG variants, matched valid controls, identical budgets, fresh contexts, a held answer key, unseen variants
   reserved for confirmation) recorded in the register's candidate list as a future RL id, with the issue's revision
   triggers; it waits for a heavy slot and a reviewer custody the monitor can grant.

Completion as the issue states it: an unseen experiment id with a stop appears once with its stage and evidence; a
completed clean case is distinguishable from pending or missing data; the 001 counts remain reproducible; the
hypothesis names denominator, ascertainment and decision-changing outcomes before collection.

## Order

1. Now, light, on the monitor's word (bridge `research/**` only; sub-second evaluator and validator invocations on
   scratch copies, no builder run): issue 3 items 1 to 3; issue 4 items 1 to 3; the README text for both.
2. Issue 4 item 4 when the monitor can grant a heavy slot and separate reviewer custody.

## Note for issue 3 (10 lines or fewer; the monitor posts it)

Triage by the research lab against main 2e977f4f: ACCEPT. No verdict is contested.
Confirmed by reading the evaluator: denominators and control count come from the run record, PASS does not pin the frozen case set, zero-sized classes leave the FAIL test, rows are never reconciled with the counts.
The committed record is complete and self-consistent (21 unique cases, 18 seeded plus 3 controls, every count equal to its recount), so the recorded H-30b PASS stands as a description of that data.
Action: a versioned companion validator for the frozen case set (identities, class counts, the one exclusion, three controls, field consistency, counts recomputed from rows), with outcomes VALID, INVALID or INCOMPLETE and its own provenance record beside the frozen data.
The preflight gains an acceptance-boundary step (missing class, missing controls, stale summary, duplicate and missing case) from the next experiment on; the self-check pins every gate denominator in the preregistration.
The claims table qualifies H-30b with the validated boundary; the frozen evaluator, ledger and report are preserved unchanged.
Lands on the bridge's research tree and reaches this repository by the next lab pull request; the validator's digest and the six outcomes will be reported there.

## Note for issue 4 (10 lines or fewer; the monitor posts it)

Triage by the research lab against main 2e977f4f: PARTIAL. No verdict is contested.
Confirmed by reading the collector: stops are recognised for two named experiments only, and only folders with a review file are walked, so a new stop is invisible and a pending run is indistinguishable from a clean one.
ACCEPTED: a structured outcome record per experiment attempt (stage reached, completed or stopped or pending, stop stage, cause and detector, the caught/escaped/false-block class, evidence digest), written at every stop and at each gated run's start from the next experiment on and backfilled for the recorded ones; a successor collector over every registered experiment id that fails on absent or unknown outcomes; the 001 snapshot and its checker preserved.
ACCEPTED as design, planned, not scheduled: the candidate hypothesis enters the register blocked on five reviewed experiments, with denominator, ascertainment, the comparator cohort, a non-inferiority margin and the three decision-changing outcomes fixed before collection; the next five stay a descriptive pilot.
PLANNED, not scheduled: the masked paired comparison of old and revised protocol on frozen preregistration variants with a held answer key needs independent reviewer custody and a heavy slot; it enters the candidate list with the stated revision triggers.
Lands on the bridge's research tree and reaches this repository by the next lab pull request.
