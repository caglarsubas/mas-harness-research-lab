# RL-10 report: the evidence algebra (H-04), 2026-11-05

**Asked.** Do the verdict ledger's evidence rule and the native qualification record's evidence classes compose
into one evidence algebra?

**Measured.** From harness-onion's published records at main afee03b9: the ledger's check-kind registry (15
evidence kinds; the not-evidence, not-confirmation and consistency-only lists; 27 refusal codes) and its 112
vectors; native profile v4's six closed evidence classes, its by-role table and its 444 negative vectors. Before
the run the lab fixed one shared order of five levels (ESTABLISHING, PROOF_BOUND, CONSISTENCY_ONLY,
NOT_CONFIRMATION, NOT_EVIDENCE, with OUT_OF_SCOPE outside it) and the two maps into it, then checked totality and
whether each record's refusals agree with the order.

| check | result |
|---|---|
| C1 totality of both maps; the ledger's three lists equal the map's levels 3, 2, 1 | PASS |
| C2 the 7 ledger vectors refused as consistency-only, consensus-only or not-evidence carry an item of that level | PASS, 7 of 7 |
| C3 clause 2 as frozen: no such vector holds an establishing deterministic check | FAIL, 7 of 7 |
| C4 the 13 native refusals that name a class respect the order (strictly below, missing, or above the role's ceiling) | PASS, 13 of 13 |

**Verdict: FAIL as preregistered** (RESULTS.json), on clause 2 of C2. The clause said "no such vector carries an
establishing deterministic check on the delivered target"; every one of the seven ledgers holds two claims, and
the establishing check belongs to the claim that is not refused. The rule the ledger applies is per claim, and the
lab's clause was per ledger. A post-hoc per-claim reading (recorded as check C5, not gated) shows the composition
holding: in each vector the refused claim has no establishing deciding check and carries exactly the weak level
its code names; the two vectors that record model confidence or a self-report as evidence are refused on sight,
without any check citing them. The protocol records the mis-scoped clause as a finding; a restatement per claim is
a new id, which the lab expects to PASS and does not run without the monitor's word.

**What it means.** The two vocabularies do map onto one order without remainder, and both records refuse exactly
where the order says support is too weak: consistency-only and consensus-only support cannot decide a claim in the
ledger, and a capture cannot claim a class above its role's ceiling or below a field's requirement in the native
record. The asymmetries are real and small: the native record has an out-of-scope class the ledger lacks; three
native classes (label-bound, entry-bound, declared with a T04 proof) share one level; the ledger's
not-confirmation level has no native counterpart.

**What it does not show.** No semantic equivalence of the two records' refusal procedures; only agreement of their
vectors with one order; the ledger's per-claim rule was read from its vectors, not from a proof; one aggregate
(evidence kinds grouped by code) was seen before the freeze, as disclosed in the PREREG.

**Proposal.** None as a roadmap read. A note for the contract owners, through the monitor if wanted: if both records
emitted the shared level with each evidence item, a single shared vector set could test both.
