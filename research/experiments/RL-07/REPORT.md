# RL-07 report: the history chain's three properties (H-01), 2026-11-05

**Asked.** Do the records and published vectors establish that the history chain's accepted check set is monotone
(P1), that published bytes are immutable under projection (P2), and that a pinned-byte edit refuses at the oldest
layer that pinned it (P3)?

**Measured.** From harness-onion's `architecture/` at main afee03b9 (slot 278's merge; export sha256 948a20fa), the
three chain rules (identity rule, product-packet rule, inheritance rule, each pinning its predecessor by digest, both
pins verified) and their 116 published vectors, replayed through the pinned evaluator scripts at the same commit
(v1 1ec76480, v2 23fe723a, v3 29483ec3, the YAML reader 99c67356) in under a second. The three properties were mapped
to vector sections before the run (PREREG v1, amended twice only to record the scripts' digests).

| property | sections | vectors | matches |
|---|---|---|---|
| P1 monotone check set | inheritance (R13), steps (step rule) | 40 | 40 |
| P2 immutable published bytes | products, allowedPaths, classForms v2 and v3 | 52 | 52 |
| P3 pinned-byte edits refuse | bindings, counts, the v2 pin | 24 | 24 |

Record checks: the identity rule's step evidence is self-consistent (20 steps, 20 bridges checked and explained,
19 bump-clean with one recorded exception, no discrepancies, 66 of 66 layers on the allow-list); its bridged
classes equal the classes found.

**Verdict: PASS on the published vectors and records** (RESULTS.json), with two unresolved checks named. Every
refusal the rules promise is exercised by a vector and refuses with the promised clause: a product that drops or
reorders an inherited command, a non-plain binding of the product list, a count outside C = S + P, a changed or
re-identified published product, a class function that is not its K = 0 form after the P-forms are undone, a
missing, foreign or stale comparator pin, a moved or changed v2 model.

**What it does not show.** (1) The step rule over the live 66-layer chain and the 273-277 equivalence were not
replayed: the chain validators' sources are not in the export, and the 22 agreement rows, 5 bridge replays and 4
head-only checks name the mechanics replay and the head's own validate(). The identity rule's recorded evidence
stands in for them here. (2) P3's "oldest layer that pinned it" is not what the vectors fix: they fix the refusing
clause: all 17 inheritance refusals carry clause R13 with a detail message, 5 of them about a comparator pin, and
none names the refusing layer's slot. The claim
"refuses" is supported; "at the oldest layer" is unresolved and would need vectors that carry the layer.

**Proposal.** None as a roadmap read. One small input for the vectors' owner (Build-R00, through the monitor): add
the refusing layer's slot to the pin-refusal vectors' expectations, so that P3's attribution becomes replayable.
