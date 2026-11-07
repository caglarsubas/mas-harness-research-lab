# RL-15 PREREG reviews (charter step 1a; a fresh pass holding only the PREREG, the register row and the charter's protocol section)

## Review 1, of PREREG v1 (56b2829f), 2026-11-05: FAIL

R1 PASS (the gate covers every count; refusal defined mechanically). R2 FAIL: the register's fifth class is "stale
snapshot digest"; the PREREG renamed it "a stale reference" and measured unknown keys and a duplicate id, none of
which touches a snapshot digest, without declaring the substitution. R3 PASS (ten files by full sha256 at commit
fce8245b; the mutation tool pinned). R4 PASS. R5 PASS. R6 PASS. R7 PASS.
VERDICT: FAIL; v2 restores the class or declares the narrowing and renames the clause.
NOTES: (1) if the baseline fails, every build fails and both FAIL and UNRESOLVED rules fire; state that the
precondition is evaluated first. (2) a refusal counts on any `roadmap.json:` message, even one unrelated to the
seeded class; the evaluator should report whether the message names the edited field or item. (3) the register
promises precision and recall; the PREREG reports recall and control false positives only; the evaluator's digest is
promised in the run record, not pinned.

Lab's disposition: v1 kept as `PREREG.v1.md`. v2 restores "stale snapshot digest" as class M6 (three edits of the
record's own digest fields), keeps M5 declared as the lab's added "stale reference" class, counts a seeded edit as
caught only when the refusal message names the edited item or field (attributed refusal), reports precision, states
that the precondition decides first, and pins the evaluator by sha256. v2 goes to a second review before any run.

## Review 2, of PREREG v2 (532b08a3), 2026-11-05: FAIL

R1 PASS (ordered gate, disjoint and exhaustive; prediction stated). R2 PASS (review 1 answered: M6 restored, M5
declared as the lab's class; the attributed-refusal unit matches the clause). R3 FAIL: M6 relies on the copied
`research/papers/` files, which are not pinned, against "the builds read these files from the copy only"; the
interpreter is not pinned. R4 PASS. R5 PASS. R6 PASS. R7 PASS.
VERDICT: FAIL; pin every file the build may read and the interpreter.
NOTES: (1) attribution is loose: substring matches on short field names let another class's check score an edit
(M4 on an item whose evidenceState is PLANNED would be caught by M2's rule); qualify M4's targets and require
whole-token matches. (2) a non-zero exit without the `roadmap.json:` prefix is neither refused nor accepted; a
crashing control could still permit PASS; classify crashes and count any non-zero control exit as a false positive.
(3) M6's third instance (a secondary paper's digest; no file in the bridge) cannot be detected by a file comparison,
so an all-18 PASS is probably unreachable; say so in the expected outcome.

Lab's disposition: v2 kept as `PREREG.v2.md`. v3 pins the whole copied directory by a manifest (every file by
sha256, the manifest itself by sha256 in the PREREG) at the same commit, pins the interpreter, qualifies M4's targets
(READY items whose evidence state is consistent with DONE), uses whole-token attribution, classifies crashes (a
control's non-zero exit of any kind is a false positive; a seeded crash is not caught), and states M6c's expected
outcome. v3 goes to a third review before any run.

## Review 3, of PREREG v3 (cda3e838), 2026-11-05: PASS (run may start)

R1 PASS (ordered gate, disjoint and exhaustive; the crash case closed). R2 PASS. R3 PASS (review 2 answered: all 37
files of the copied directory pinned through the manifest; the ten script-named inputs by sha256 at commit
fce8245b; both instruments by 64-character digests; the interpreter pinned). R4 PASS. R5 PASS. R6 PASS. R7 PASS.
VERDICT: PASS.
NOTES: (1) M6's third instance is undetectable by design, so only FAIL or UNRESOLVED can come out; the report must
not present UNRESOLVED as a near-miss of PASS. (2) state the qualifying count per class in the run record. (3) keep
the full last-line classification in the record so a multi-line refusal read as a crash can be audited.

Lab's disposition: the run proceeds under v3; the three notes are answered in the run record and the report.

## Instrument stop before any seeded build, under v3, 2026-11-05

The mutation tool stopped while drawing M4's targets: no READY item has an evidence state of IMPLEMENTED or
CONTRACT_ADOPTED (all 51 READY items are PLANNED); the only open items with such a state are 3 IN_PROGRESS items.
The baseline build had run; no seeded build ran; no outcome exists. This is review 3's note 2 made real, and a
change to the tool is a new PREREG version: v4 draws M4 from open items (READY or IN_PROGRESS) with an evidence state
consistent with DONE (exactly 3 qualify, so the draw is fixed), records the qualifying count per class, and makes
attribution field-specific (the edited field's name or the seeded value, never the item id alone) so that another
class's check cannot be credited to the seeded one. v4 goes to a fourth review before any run.

## Review 4, of PREREG v4 (cf9fe7a9), 2026-11-05: FAIL

R1 PASS. R2 FAIL: the hypothesis clause still reads "with the refusal naming the edited item or field" while the
unit counts only a class-specific token ("never the item id alone"); the clause and the counted unit must say the
same thing. R3 PASS (manifest, ten files, both instruments, interpreter). R4 PASS. R5 PASS. R6 PASS. R7 PASS.
VERDICT: FAIL; align the hypothesis sentence with the unit.
NOTES: (1) M5's duplicate instance and M6 accept an id as the token; say these are the seeded values for those
classes. (2) the gate has no region for a run stopped by the qualifying-target rule; say what is written then.
(3) say that M4's qualification and the "exactly 3 qualify" count were read from the record after the v3 stop.

Lab's disposition: v4 kept as `PREREG.v4.md`. v5 is a text-only version: the hypothesis sentence, the status line
and the minimum-effect paragraph say "a token specific to the seeded edit (the field's name or the seeded value)";
the id rule is stated per class; a stop before any build writes no ledger and is recorded as an instrument stop; the
origin of M4's count is stated. The instruments are unchanged. v5 goes to a fifth review before any run.

## Review 5, of PREREG v5 (1e8dfc4a), 2026-11-05: PASS (run may start)

R1 PASS (the stop case now writes no ledger and is recorded). R2 PASS (review 4 answered: the hypothesis, the
unit, the minimum-effect lead-in and the status paragraph say the same thing; the id exceptions are labelled seeded
values). R3 PASS. R4 PASS. R5 PASS. R6 PASS. R7 PASS (M4's rule's post-hoc, counts-only origin declared).
VERDICT: PASS.
NOTES: (1) M4's tokens `updates`/`update` are the missing entry, not the edited field; reword the parenthetical in
a next version. (2) recall is capped at 17 of 18 by M6's third instance, so the gate can only end in FAIL or
UNRESOLVED; say so in the report. (3) the draw procedure and the token `B2` (a benefit-factor key) should be spelled
out in a next version.

Lab's disposition: the run proceeds under v5; notes 1 and 3 go to the next PREREG that reuses the form; note 2 is
answered in the report.

Post-run note (2026-11-05): the privacy scan flagged one absolute-path shape in the frozen mutation tool (a literal
system temp directory in an environment default, unused); the published copy removes it (sha256 b35e6009109729fc73e3c7c190351dff3ba317e4d0b6baad657aabec34ea0e84); the run
record carries both digests.
