# RL-15b companion validation (R13 issue 3), 2026-11-09

A companion record, written after the run on the owner's issue 3 and the monitor's light GO (MON-R13-3-4-GO). The frozen
evaluator `tools/rl15b_eval.py` (2d6c349b), the ledger `RESULTS.json` (RL-15b-RESULTS-v1), the run record and the report
are not edited; this note and the three data files beside it carry their own provenance. Nothing here is a verdict.

## What the issue found, confirmed by reading the evaluator

The frozen evaluator takes the catchable denominator, the control count and every aggregate from the run record's
`counts` block, accepts `refused_any == n` without requiring the frozen case set (17 catchable, 3 controls), drops
zero-sized classes from the FAIL test and never reconciles the rows with the counts it gates on. The preflight (P2)
exercised the four gate regions on complete synthetic records only. The gap is the instrument's acceptance boundary;
the committed record is complete, so the recorded PASS describes the data.

## Frozen case set

`data/rl15b_case_set.json` (35525dd9), derived by `tools/rl15b_validate.py derive` from RL-15 run-002's record
(`experiments/RL-15/data/rl15_runs_002.json`, a60da422), whose targets the PREREG pins by seed 20261105: 21 (class,
target, field) identities, 18 seeded (M1 to M6, three each; the secondary-paper digest instance declared uncatchable,
as the PREREG states) and 3 controls; expected rows per class and catchable per class.

## Validator and its checks

`tools/rl15b_validate.py` (31ae73e4), standard library, outcomes VALID, INCOMPLETE or INVALID, never PASS or FAIL:
V5 row types; V1 identities equal the case set (missing and extra listed); V2 no duplicate identity; V3 rows per class;
V4 catchable flags and the one declared exclusion; V6 field consistency (a refusal has a non-zero exit and no crash,
attribution implies refusal and exactly one source, message length equals the message); V7 every supplied count equals
the recount from rows; V8 (with the ledger) the ledger's scores equal the gate quantities re-derived from the rows and
its evidence E1 names this record. A missing class, control or case reads INCOMPLETE; an extra, duplicate, malformed or
inconsistent row, or a summary that disagrees with its rows, reads INVALID.

## Result on the committed record

`data/rl15b_validation.json` (05276597): VALID, 8 of 8 checks PASS on `data/rl15b_runs.json` (f445e3c1) against the
case set and `RESULTS.json`; the re-derived gate quantities (catchable 17, refused 17, attributed 17, new rules M4 2
and M6 2, older rules 13, unattributed 0, controls 3 with 0 refused, crashed 0, classes uncaught 0) equal the ledger's
scores. The H-30b verdict is unchanged by construction: this record only establishes that the data it rests on is
the complete frozen case set.

## Acceptance boundary (charter step 1b (vii), applied here after the fact)

`tools/rl15b_boundary.py` (4e86669a) derives five mutated copies of the record deterministically, runs the frozen
evaluator and the validator on the original and on each copy, and writes `data/rl15b_boundary.json` (1f722721); the
copies and the evaluator's outputs on them stay in the lab scratch (each copy's sha256 is in the table).

| input | counts recomputed | frozen evaluator | validator |
|---|---|---|---|
| original (f445e3c1) | not applicable | PASS | VALID |
| every M1 row removed (denominator 14) | yes | PASS | INCOMPLETE (V1 3 missing, V3 one class short) |
| every control removed (controls 0 of 0) | yes | PASS | INCOMPLETE (V1 3 missing, V3 one class short) |
| first seeded row set to built and unattributed, counts kept | no | PASS | INVALID (V7 5 of 16 count keys differ) |
| the second seeded row appended again (denominator 18) | yes | PASS | INVALID (V2 one duplicate, V3 one class over) |
| one M3 row removed (denominator 16) | yes | PASS | INCOMPLETE (V1 1 missing, V3 one class short) |

Completion as the issue states it: the original record is VALID and yields the recorded result; every incomplete or
inconsistent case is rejected; the frozen evaluator passes all five, which is the boundary the issue reported (its
fourth table row included). Interpreter CPython 3.12.14 (the profile interpreter), `-I -B`; sub-second.

## What this does not show

The validator and the record share an author; the case set is derived from a record that shares the seed with the
run, so it enforces "the same 21 cases" and not an independent choice of cases; no build was re-run; a refusal
message's wording is not re-attributed here (V6 checks the attribution fields' consistency, not their truth). From
RL-23 on the acceptance-boundary step runs in the preflight before the gated run (README section 2, step 1b (vii)).
