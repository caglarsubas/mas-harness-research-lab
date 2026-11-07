# RL-21 PREREG reviews (charter step 1a; a fresh pass holding only the PREREG, the register row and the charter's protocol section)

## Review 1, of PREREG v1 (73c96e89), 2026-11-06: PASS

R1-R7 PASS. NOTES: (1) H-26c's "at most one root" admits a fork or a cycle; precedence unstated when a precondition
is unmet and a violation exists. (2) the register names the b4bbea79 export; the PREREG pins c1b838be without saying
why; "FROZEN" precedes the review. (3) a PASS is weaker than "exactly one writer": many later changers are allowed
if each names the creator; H-26a was known before its gate; the report must say "under this operationalisation".

Lab's disposition: after the review and before any run, the lab's own inventory showed that the meta authorities'
`metaBaseline` is a commit id, not a packet id, so H-26c's chain rule cannot be computed from the export (the chain
lives in git history outside it). A change to the operationalisation is a new version: v2 makes H-26c descriptive
(counts of multiply-owned paths and distinct baseline commits; no gate), states precedence (precondition first), says
why the export is c1b838be (the monitor's order: the published contracts are harness-onion's; the register's
b4bbea79 export is R12's harness for the trace half), and the report wording of note 3. v2 goes to a second review.

## Review 2, of PREREG v2 (9eb03897), 2026-11-06: PASS (run may start)

R1-R7 PASS (the uncomputable chain rule removed without an undefined outcome; the narrowing stated).
NOTES: (1) H-26a is a near-foregone PASS; the overall PASS rests on H-26b; the report says so. (2) "baseline" may be
direct or transitive; the report shows violating pairs by id if any. (3) the register records "contract-text half,
creator-linkage operationalisation", not H-26 PASS.

Lab's disposition: the run proceeds under v2; the notes are answered in the report and the register row.
