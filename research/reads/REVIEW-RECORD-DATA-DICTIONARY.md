# Review-record data dictionary (R13 issue 1, recommendation 4)

Research-Lab, 2026-11-07. A design input to REVIEW-RECORD-SERIES-001's "decide accept or forbid" step, as the
visionary disposed it (VIS-R13-I1-RL item 3): the fields a review-record series needs so that review independence,
error detection and later refutation become measurable (H-09, H-32), with every denominator defined before any
collection. The machine form is `REVIEW-RECORD-DATA-DICTIONARY.json`; the completeness check is
`research/tools/review_record_dictionary_check.py`, which reads the dictionary and a record schema (or a folder of
records) and prints, per field, whether a candidate path exists in the schema (or is filled in the records). It
prints field names and counts only, never record values.

## Fields

| field | unit | definition (short) | candidate paths in the v2 forms | denominator | feeds |
|---|---|---|---|---|---|
| findingId | identity | a stable identity across rounds: an id that does not embed the raising round, or an id plus a `supersedes` reference | findings[].id, findings[].supersedes (new) | findings | H-09c, H-09d, H-32 |
| reviewedHead | commit | the exact head the round reviewed | subject, base | rounds | H-32 |
| round | integer | the round number inside the series | round | rounds | H-09c, H-09d |
| firstDetectionRound | integer | derived: the first round the identity appeared | derived | findings | H-09d, H-32 |
| recurrence | count | derived: later rounds raising the same identity | derived | findings | H-09c |
| severity | enum | the record form's severity | findings[].severity | findings | H-09-descriptive, H-32 |
| blocks | boolean | whether the finding blocks the verdict | findings[].blocks | findings | H-32 |
| disposition | enum | the author's disposition in the next round, with a note | dispositions[].status, dispositions[].note | findings | H-09-descriptive, H-32 |
| laterAdjudication | enum + reference | confirmed, refuted or untested by a later round, the verifier or the oracle, with the record | none in v2 (new) | disputed or unanimous findings | H-32 |
| unanimity | boolean | derived: every reviewer of the round accepted the claim | derived across reviewer records of one round | claims per round | H-32 |
| verifierOutcome | enum + reference | the verifier's conclusion after PASS_FOR_PUSH, with the check-run reference | merge-decision record, verifier block | PASS_FOR_PUSH heads | H-09b, H-32 |
| oracleContribution | verdict + count | the oracle's per-packet verdict and test count from the merge-decision record's oracle block (RL-02-PROPOSAL part 2) | merge-decision record, oracle block | packets | H-09a |
| reviewEffort | minutes or runs | the reviewer's runs and limits, launched and finished, the author's minutes to address | identity.runs[].used, identity.launched, identity.finished | rounds | H-10a, effort columns |
| custodySeparation | boolean | the reviewer ran under a custodian separate from the author | identity.operator, identity.author.agentIds, identity.reviewer.agentId | rounds | H-09, H-32 |
| contextSeparation | boolean | the reviewer held only the brief, the rules and the export | briefSha256, rulesSha256, wrapperSha256 | rounds | H-32 |
| modelFamily | string | the reviewer's model, apart from custody and context | reviewer.model, identity.reviewer.model | rounds | H-32 |
| interruptions | list | identity interruptions as strings | identity.interruptions | rounds | reviewEffort |

Denominators: rounds = review-record documents of one series; findings = findings[] entries across the series'
rounds, de-duplicated by findingId; packets = merge-decision records with a merge commit; PASS_FOR_PUSH heads =
heads a round marked PASS_FOR_PUSH, matched to a verifier run; claims per round = claims the round's verdict
accepted or disputed.

## What the v2 forms already carry and what is new

Checked by script against the published schemas at harness-onion main 4b2be353 (the check's output is in the
lane file entry of 2026-11-07): the review-record form carries round, subject, severity, blocks, dispositions,
the brief, rules and wrapper digests and the reviewer's model; the review-identity form carries operator, author
agent ids, reviewer agent id and model, launched, finished, runs and interruptions. New fields: `findingId` as a
cross-round identity (or `supersedes`), which RL-02-PROPOSAL part 1 made a clause of REVIEW-RECORD-SERIES-001's
packet (381 of 381 current ids embed the raising round); `laterAdjudication`; the oracle block and the verifier
block live in the merge-decision record (DECISION-LEDGER-001), not in the review record. Derived fields
(firstDetectionRound, recurrence, unanimity) need no new form field once findingId is stable.

## Rules

- The oracle side is read only through the custodian's summary (the oracle block); the lab never reads protected
  tests.
- Every field is recorded, never inferred from prose, before the series' first collection.
- Custody, context and model family are three fields, never one.
