# RL-18 report: the CONF-MAS arms study as MAS-RA-002 run manifests and distribution-gate comparisons (H-31)

**Asked.** Can the arms study of CONF-MAS-003 (three arm policies against the defended baseline over five classes and
32 seeds) be expressed as MAS-RA-002's split declaration, run manifests, evaluation records and distribution-gate
comparisons that validate against the contract's schemas (H-31b), and do the gate's non-inferiority verdicts agree
with the campaign's recorded bound verdicts per arm and metric (H-31c)? First, as an instrument check, does the lab's
own validator and integer gate reproduce the contract's 85 vectors (H-31a)? Preregistered as v2 (eca606be) after one
failed review on scope (v1 7807d764; `PREREG-REVIEW.md`). Scope: the arms study only; the other four campaigns'
class rows are absolute bound checks with no baseline to pair against and are out of scope (PREREG section 0).

**Measured.** Run-001 b9efff33; data bb3b5cc8; RESULTS 6756016b. H-31a: 18 of 18 SHAPE vectors refused, 25 of 25 valid vectors
accepted, 17 of 17 valid comparison vectors reproduced bit for bit (decision, nonInferior, statistics) and both
DECISION_MISMATCH vectors flagged. H-31b: the split declaration validates and all 9 comparisons validate, but 0 of 640
manifests and 0 of 12 evaluation records do: every one is refused at `configuration.budget.tokensPerTask` against the
schema's minimum ({"tokensPerTask": {"minimum": 1, "maximum": 9007199254740991}, "costMicrosPerTask": {"minimum": 0, "maximum": 9007199254740991}, "wallClockSecondsPerTask": {"minimum": 1, "maximum": 9007199254740991}}); the lab's mapping gave the simulation a token budget of 0 because the harness
has no model and no tokens. H-31c: 7 of 9 cells agree. The two disagreements are both on duplicated work: A1 is
non-inferior to the baseline in the pooled gate (mean +3,880 ppm, half width 9,104) while the campaign records its
bound broken in class C2 alone; A3 is non-inferior (mean +3,982, half width 12,676) while the campaign records its
bound broken in C5 and C7. A2's duplicated work is not non-inferior in the gate (mean -16,275, half width 21,204) and
breaks the campaign's bound in every class: agreement. Completion and lost work agree in every cell (no difference
at all; mean 0, half width 0).

**Verdict: FAIL as preregistered on H-31b; H-31a PASS; H-31c UNRESOLVED (7 of 9, the inconclusive band).** The
monitor's GO is the recorded start word (review 2 note 2).

**What it means.** The lab's reading of the contract is right: its gate reproduces every published vector bit for
bit, which is what the README promises any consumer. The arms study cannot be expressed as-is because the manifest
form requires a positive token budget per task: the contract assumes a model with tokens, and a deterministic
simulation has none. That is a finding about the record's form, not the lab's builder: the builder's other fields all
validate (the split, the comparisons, and the manifests and records on every other path). A sentinel budget (1 token)
or a declared "no model" configuration would express the study; either is a new id or a contract note. On agreement,
the two forms differ exactly where review 2's third note said they would: the campaign's verdict is a conjunction of
absolute per-class bound checks, the gate's is one pooled relative interval over five task clusters; a bound broken
in one class (A1 on C2) or two (A3 on C5 and C7) is averaged away by the pooled gate, which still finds the arm
non-inferior. A disagreement is a difference of forms, never an error in either record. Per-cell agreement is
reported above regardless of the verdict (note 1).

**What it does not show.** Nothing about the four other campaigns (out of scope by form); nothing about a real
model's manifests; the tolerance (10,000 ppm) and the agreement mapping are the lab's; five task clusters make the
gate's interval wide. The contract's semantic checks beyond the schema (the 17 refusal codes of the reference model)
were not run: the reference model script is not in the architecture export.

**Proposal.** RL-18-PROPOSAL, a design read for the visionary through the monitor, not a roadmap shift: (1) for
MAS-RA-002's consumers, note that the manifest form cannot carry a configuration without a token budget; a
`tokensPerTask` of 0 with a stated reason, or an explicit "no model" configuration, would let simulation campaigns
use the record; (2) for CONF-A3-001 and MAS-RA-005, note that a pooled task-clustered gate and per-task absolute
bounds answer different questions, and a campaign that keeps per-class bounds should keep them beside the gate, not
replace them with it; (3) the register's H-31 is narrowed to the arms study, with the other four campaigns'
bound-check form named as what a second record would need.
