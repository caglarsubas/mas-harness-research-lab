# Research-Lab read of Q-048-1 (an authored class-other edit to an attested file) under condition (v), 2026-11-09

Asked by the monitor (MON-048-LAB-READ; light, paper only, research rounds paused). Input: R00's DESIGN_048 rev 1
(sha256 715a4be8, 197 lines; it reads the 282 ledger's record only), read whole; the lab's own read of condition (v)
(research/reads/CC2-CONDITION-V-LAB-READ.md, 5ba84a50: the three mechanism checks, the classes A/B/C, the restart rule,
the 15 s reader cap, the 3/N bound, N_shadow = 10 with one rewrite inside the period). No run, no network. The lab's
read prevails over the visionary's on this question (RD-D1); the owner decides after both.

## 1. Ruling: (b), demote with countEffect neutral, under four conditions

(b) is right in substance: a layer whose declared input changed by an authored edit is never skipped, it is run in
full until the next rewrite, so the guarantee a skip would have rested on is replaced by execution. (a) spends
the period's count on edits that carry no information about the mechanism, and pushes every content edit to a rewrite
slot; (c) attests an outcome that was never observed on the new bytes and is rightly rejected.

The three checks, as R00 maps them:

1. Input-set completeness: unaffected for the layers that stay attested. Demotion is keyed on declared inputs, so a
   layer that reads the edited file without declaring it stays attested and its outcome change surfaces as a
   disagreement (class A). One attribution gap remains, named in condition C2 below.
2. Recorded equals live: for a demoted layer the check is void (the recorded outcome is about other bytes) and the
   layer runs instead. Its agreement with the record is not evidence; its disagreement still is (condition C2).
3. Reader cost: no added reader work, because the authority replay that decides "authored" is the identity rule's
   existing check. The suite cost of demoted layers is verify time, not reader time, and is observed, not capped.

The 3/N bound is unchanged in form. It bounds the per-verify disagreement rate over the layers that were compared;
demotions shrink that set for a verify, so the bound's coverage per layer falls with the demoted fraction. That is
why the period's composition needs the two requirements in C1, and why the demoted fraction is recorded (C3).

## 2. Conditions

- C1, the period's composition (the answer to R00's question): yes, and in both directions. The ten clean verifies
  must include at least one demotion-free verify (the full attested set compared, so the reader's cost under the
  15 s cap and the full-set agreement are measured where they are largest) and at least one verify with an authored
  demotion on a live head (vector 17 exercised where G1 will rely on it, not only in a fixture). If no packet in
  287-296 edits an attested file, one dry run on a live head with such an edit is the evidence, recorded as a dry run,
  as the lab's section 4 already allows for dry runs. Neither requirement restarts or extends the count by itself.
- C2, a demoted layer's outcome change is never neutral: countEffect neutral covers the demotion and an agreeing
  demoted layer, not a demoted layer whose live outcome differs from the record. That difference is classified like
  any other: explained by the authored hunks (the author's statement, checked against the hunks' classes) and
  recorded as "demoted, outcome changed, explained", or class A with restart when unexplained. Without this, an
  undeclared input that a demoted layer also reads is attributed to the authored edit and the capture hook's defect is
  not counted. (At a merged head such a change is a live failure and the verify fails anyway; the condition is about
  the record and the dry runs that precede merges.)
- C3, the record: the per-verify G1 record and the shadow record name the demoted layers, the authority entry that
  explains each, and their live seconds; the shadow record carries the attested fraction (layers compared over layers
  attested). RL-14's dataset (the lab's section 2) gains a demoted column; the lab reads it as it reads the rest.
- C4, bundle v8 recomputes the expected deselected set: under (b) the set is the attested layers minus the drawn
  sample minus the layers with any changed declared input, computed by v8 from the ledger's inputs and the live files,
  never taken from the G1 record. A deselected layer with a changed declared input is refused whether or not the
  record calls the edit authored (vector 19 amended; vector 18 unchanged). This is the one place where (b) adds a
  surface: the word "authored" must not be able to turn a changed input into a skip.

## 3. Does (b) keep G1's trust argument sound

Yes, with C4. The argument was: skipping an attested layer is safe because its declared inputs are unchanged, its
recorded outcome equals the live one, the reader is cheap, a 10 percent sample and the hard refusals catch the rest,
and a clean shadow period showed the three mechanism claims on live heads. Under (b) a layer with a changed declared
input is never skipped, so the argument's first premise holds by construction for every skipped layer; the undeclared
input case is the same as under (a) and (c) and is what the period and the sample are for. The cost is bounded by
the next rewrite, which re-attests the demoted layers on their new bytes.

## 4. A note on Q-048-4 (not asked; it touches the lab's own stipulation)

The lab's condition "one rewrite inside the period" was there so that condition (i)'s writer runs once on a live head
during the period and the verifies after it exercise the new ledger. A cadence rewrite at 296 followed by G1 at 297
leaves the new ledger with its own verify only. The lab recommends that the period end no earlier than three clean
shadow verifies after the rewrite that produces the ledger G1 will accept, without restarting the count; whether the
owner takes that as 297 moving to 299 or as the rewrite moving earlier is a planning choice, not the lab's.

## 5. Not claimed

No verify-time figure, no claim about which packets in 287-296 will edit attested files, and nothing about the
import bound (Q-048-2) or the hooks' placement (Q-048-3), which the lab did not read for this question.
