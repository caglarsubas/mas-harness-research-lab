# RL-15b instrument preflight (charter step 1b), 2026-11-07

Run by the lab after PREREG v1 (e5a75db2) was frozen and before the blind review and the gated run; results in
`data/preflight/preflight_results.json` (02132735) with the four synthetic evaluator inputs and their ledgers and
the synthetic run record under `data/preflight/`. Base: the git-archive export of `roadmap/` at ded99886 in the
lab scratch (builder 690cff6a); work copy `<parent>/roadmap/`; CPython 3.12.4, `python3 -I -B`, TMPDIR in the
scratch; no bytecode left; no network. Three builds in all (the baseline and the two known controls); the gated
run did not start.

| check | result | detail |
|---|---|---|
| P0 layout and precondition | PASS | the tool refuses a work copy not named `roadmap` (assertion); the unmodified copy builds, exit 0 in 3.33 s |
| P1 expressibility | PASS | 21 edits applied to fresh copies, every one changes `roadmap.json`'s bytes; the one uncatchable instance is the secondary-paper digest (M6, third instance), as declared; qualifying targets M1 214, M2 85, M3 214, M4 4, M5 642, M6 68 (sources, papers and secondary papers), C 214; the 21 targets are run-002's (seed 20261105) |
| P2 units and denominators | PASS | evaluator on four synthetic outputs: PASS (17 of 17, new rules M4 2 and M6 2, controls 0), FAIL (one control refused), FAIL (neither new rule fires), UNRESOLVED (one unattributed refusal); the catchable denominator reads 17 in each |
| P3 known controls | PASS | positive: a dangling dependency on ADR-AMEND-0001-0002 (outside the drawn targets) refused, "unknown dependency", attributed to that older rule; negative: the offset-bearing update entry builds, exit 0 |
| P4 boundaries | PASS | a 148-character message with the tag at its end is read as NEW over the whole message and not over its first 120 characters; the tag strings equal the erratum's "(RL-15 v1)" and "(RL-15 v2)" |

Overall: PASS. The instrument is valid for the gated run; nothing returns the PREREG to v2.

Addendum after review 1 (note 3; evaluator only, no build; `data/preflight/preflight_addendum.json`): the M4 = 1
case (one new-rule refusal below the expectation, the other M4 instance refused by an older rule) reads
UNRESOLVED, and a class with zero refusals reads FAIL. Both as the gate states.
