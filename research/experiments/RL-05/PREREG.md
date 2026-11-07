# RL-05 preregistration: the merge predicate (H-03)

Status: FROZEN v1 (2026-11-04). This file's sha256 goes into `research/hypotheses/REGISTER.md`. No draft preceded it;
an integrity check before the freeze read the field types and presence counts of the merge-decision records (which
keys exist, of which JSON type, how many head-bound booleans are false), never a value.

## 1. Hypothesis (falsifiable)

H-03: the merge predicate is a conjunction of independently produced records and holds for every merged packet.
Stated as: for every merge-decision record that names a merge commit, the predicate P below evaluates TRUE.

P = R ∧ V ∧ A ∧ I ∧ H ∧ T, where each conjunct reads one producer's record inside the merge-decision file:
- R (review): the record carries review evidence: `reviews` is a non-empty list or a reference string, or
  `packetReviews` / `contractReviews` is present.
- V (verifier): `verify.conclusion` is `success` and `verify.checkRun` is present (the verifier's check run).
- A (owner): `approver` is present.
- I (independence): `decidedBy` is present and differs from `approver` (compared in the script, never printed).
- H (head-bound): every boolean in `headBoundChecks` is true; MISSING when the object is absent.
- T (transport, hosted repositories only): `transportApproval` is present; TRUE by definition for the bridge
  repository (harness-onion), whose approvals are head-bound inside the record itself.

Each conjunct evaluates TRUE, FALSE or MISSING (the field needed is absent). A record is PASS when every conjunct
is TRUE, FAIL when any is FALSE, UNEVALUATED when none is FALSE and at least one is MISSING.

## 2. Inputs (sha256; source)

| input | source | pin | state |
|---|---|---|---|
| I1 merge-decision records, 53 files (`handoff/merge-decisions/*.json`) | bridge commit ee4f3a08 | set digest b3370227 (RL-01's pin) | PINNED; read only through `research/tools/rl05_predicate.py`, an allowlist script that emits booleans, counts and enums per record and never a string value |

Unit: a record with a `mergeCommit` (47 of 53 by the pre-freeze count). The 6 other records (errata, exceptions,
dry-run notes) are listed by kind flags and excluded from the predicate.

## 3. Design and gate

- Per-record evaluation of P as in section 1; per-conjunct counts of TRUE / FALSE / MISSING over the 47 merges;
  the same split by record form (`schema` = planeon.merge-decision/v1 or older) and by repository class (bridge
  repository or hosted), as enums derived in the script.
- Gate: H-03 PASS when every merged record is PASS; FAIL when at least one merged record is FAIL and no
  `exception` / `ownerException` / `erratumFor` field in that record or in a record naming the same PR explains it;
  UNRESOLVED when no record is FAIL and at least one is UNEVALUATED. A FAIL explained by an exception record is
  reported as such and does not change the verdict rule (an explained FAIL is still FAIL for H-03 as stated; the
  explanation is context).
- Deterministic; no seeds; no splits.

## 4. Compute plan

Light: `research/tools/rl05_predicate.py` (stdlib, `python3 -I -B`), seconds; no heavy slot.

## 5. PASS, FAIL, UNRESOLVED

As in section 3. A breach is a finding recorded in RESULTS.json; no re-tune under RL-05.

## 6. Privacy

The script's output holds only booleans, counts, enums, PR numbers and dates; scanned with `privacy_scan.py` before
it leaves the folder.
