# Research-Lab read of Q-C286-2: the countEffect of an explained outcome change on a demoted layer, 2026-11-09

Asked by the monitor (MON-C286-Q2; light, paper only, rounds paused). Input: R00's CONTRACT_286 r1' (sha256 f23460f3,
408 lines), section 3.11 read whole, with its countEffect rows and vectors 17, 17b, 17c; the lab's adopted Q-048-1 read
(research/reads/DESIGN-048-Q1-LAB-READ.md, 9c795426, condition C2 "never neutral"). No run, no network. The lab's read
prevails; the owner decides.

## 1. Ruling: count, when the explanation is checked causally; restart otherwise

"Count" here means the verify is one of the ten clean verifies. The lab rules count for the explained case, on one
condition: the explanation must be shown causal, not only stated. Section 3.11's check as written (the authoring
packet's `outcomeStatements` names the layer, the path and every differing node, and the path's hunks include a
class-other hunk) is a statement check. It establishes that the author expected the change and edited the file; it
does not establish that the edit caused the change. The gap C2 was written for is exactly the case it lets through:
the packet also changes a file the demoted layer reads without declaring it, the author sees the nodes change in a
dry run, writes the statement to match, and the capture hook's miss is counted as a clean verify. A statement bound
by the record's digest is still written after the author's own runs, so it is a fit, not a prediction.

Restart as the alternative buys no evidence either: it only taxes content edits inside the period, which is what
(b) was adopted to avoid. So the choice is not count versus restart; it is whether the explained case is checked
in a way that separates the authored cause from an undeclared one. With that check, count. Without it, restart.

## 2. The isolation check (E1)

For a demoted layer whose live outcome differs from the record and whose statement matches:

1. Take the head tree into a scratch copy and restore every changed declared input of that layer to its base bytes
   (the merge base's blob for each path; the authority's beforeSha256 confirms it). Only declared inputs changed by
   authored, replay-verified edits exist at this point, or the layer would already be class A.
2. Run the differing nodes of that layer, and only those, on the scratch copy, under the same interpreter and
   environment as the shadow verify.
3. If every differing node returns its recorded outcome, the change is caused by the declared edits: kind
   "demoted-outcome-explained", countEffect count. If any node does not, the cause lies outside the declared inputs:
   unexplained, class A, restart (the analysis may reclassify it B when a repeat shows non-determinism, as the
   restart rule already allows).

The statement is still required (section 3.11's check stays, as the author's prior commitment); E1 is added to it.
The check is bounded: a copy of the tree and a handful of nodes; its seconds are verify time, not reader time, and
do not count against the 15 s cap. It runs inside the shadow verify when 286 carries it, or, until it does, as a
recorded light step on the monitor's word before the verify is credited: the shadow record then carries kind
"demoted-outcome-explained" with countEffect "pending isolation", and the period's count advances only when the
isolation record exists and reads PASS. An explained event at a merged head should be rare, since the suite passes
at merge and a differing outcome is a pass turned skip, a removed node or a renamed one, so the procedural form is
acceptable for 286; the reader form is preferred for MET-PERF-048, where sampled mode will depend on it.

## 3. What the record carries (C3, extended)

Per explained event: the statement's entry (layer, path, nodes), the isolation result per node (recorded outcome,
live outcome, outcome with declared inputs restored), the restored paths with their base digests, and the seconds.
The countEffect table gains the pending state above; C9's check that `COUNT_EFFECT` equals the README's rows covers
the new row. Vector 17c splits into 17c (statement matches, isolation PASS: count) and 17d (statement matches,
isolation FAIL: class A, restart).

## 4. Not claimed

No claim about how often the explained case occurs in 287-296, no verify-time figure for the isolation step, and
nothing on the rest of CONTRACT_286, which the lab did not read for this question.
