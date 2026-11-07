# RL-05 report: the merge predicate (H-03), 2026-11-04

**Asked.** Is the merge predicate a conjunction of independently produced records, and does it hold for every
merged packet (H-03)?

**Measured.** The predicate was written before the run (PREREG v1 462f9cc1) as P = R ∧ V ∧ A ∧ I ∧ H ∧ T: review
evidence present; the verifier's conclusion success with a check-run reference; an approver; a decider distinct from
the approver; every head-bound boolean true; a transport approval for hosted repositories. It was evaluated by an
allowlist script over the 53 merge-decision records on the bridge (set digest b3370227), on the 47 records that name
a merge commit. Run 001 had a script defect (two bare-named bridge records classed as hosted); run 002 is the run of
record and the defect is disclosed in the ledger.

| conjunct | TRUE | FALSE | MISSING |
|---|---|---|---|
| R review evidence | 45 | 0 | 2 |
| V verifier success with check run | 43 | 4 | 0 |
| A approver present | 47 | 0 | 0 |
| I decider differs from approver | 47 | 0 | 0 |
| H head-bound booleans all true | 47 | 0 | 0 |
| T transport approval (hosted) | 43 | 4 | 0 |

Records: PASS 39, FAIL 6, UNEVALUATED 2.

**Verdict: FAIL as stated** (RESULTS.json). Six merged records do not satisfy P. All six were decided on
2026-10-21 or 2026-10-22, in the older record form or on the first day of the v1 form, and each lacks a mechanism
its form predates: four carry no check-run reference (the verifier's summary came later), four hosted-repository
records carry no transport approval (the head-bound approval file came later). No exception, erratum or slip field
explains them. Every record decided on or after 2026-10-24 satisfies P or is UNEVALUATED (two hosted records with
no reviews field; PRs 25 and 8).

**What it means.** The conjunction is real: four independent producers (reviewers, the verifier, the owner as
approver, the monitor as decider) each leave a record, and the head-bound booleans are never false. But the
predicate is not stationary: its conjuncts entered the record one at a time through October, so "holds for every
merged packet" is false over the whole history and true over the history since the record form stabilised. The
right formal statement is a time-indexed predicate P_t whose conjunct set is the record form in force at t.

**What it does not show.** Nothing about whether the records are independent in fact (only that they are distinct
fields from distinct producers); nothing about the five earliest decisions (2026-10-20/21), which record a clean
merge state without a merge commit and fall outside the unit (descriptively 3 FAIL, 2 UNEVALUATED, for the same
reasons as above); nothing about the approval files' bytes, which the lab cannot read.

**Proposal.** A design read for the visionary, RL-05-PROPOSAL, is justified but small and not a roadmap shift: when
the merge-decision schema is next amended, state the merge predicate as P_t in the schema's README with the date
each conjunct became mandatory, and add `reviews` to the required set so R cannot be MISSING. The lab sends it
through the monitor after RL-02 v2 reports.
