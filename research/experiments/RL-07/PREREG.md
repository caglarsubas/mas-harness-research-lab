# RL-07 preregistration: the history chain's three properties (H-01)

Status: FROZEN v1 (2026-11-05); amendment v1.1 (2026-11-05) records X2's digests; amendment v1.2 (2026-11-05) records X3's; nothing
else changes between amendments. Replay-script fix after run 001, disclosed: the clause parser strips the evaluators'
"identity " message prefix; run 001's outcomes were all correct in kind and are re-reported with the fix in run 002. Sections are replayed as their evaluators' inputs arrive (run 001: counts,
bindings, allowedPaths, pin; run 002: inheritance, steps, products, classForms). Integrity check before the freeze: the export's member listing (counts,
no oracle or closed-lane names), the 26 chain members' sizes, the rules' key structure, the vectors' section names,
sizes, key sets and expectation counts, and the evaluator strings; no vector was evaluated and no vector body read.

## 1. Hypothesis (falsifiable), as three properties over the records and vectors

H-01: the history chain's accepted check set is monotone (P1), published bytes are immutable under projection (P2),
and any pinned-byte edit refuses at the oldest layer that pinned it (P3).

- P1 monotone check set: (a) R13, the inheritance refusal (a product at slot 278 or later keeps every acceptance
  command of its repository's newest earlier packet): the 26 `inheritance` vectors replayed through
  `chain_identity_v3.check_inheritance_vector`; (b) the step rule (every non-head chain validator equals its
  previous-era bytes except the bump and bridge vocabularies): the 14 `steps` vectors through
  `chain_identity_v2.check_step_vector`, plus a record-consistency check of the identity rule's `evidence.steps`
  (20 steps; bumpClean, bumpExceptions, bridgesChecked, bridgesExplained and `discrepancies` must agree with the
  list). The step rule over the live chain's 66 layers is not replayed (the chain sources are not in the export).
- P2 immutable published bytes: the 14 `products` vectors (R6: a changed published product refuses), the 6
  `allowedPaths` vectors and both `classForms` sections (v2's cases on its bases; v3's on v2's bases by reference)
  through `check_products`, `check_allowed_paths` and `check_class_vector`; the identity rule's bridged classes
  (`d.bridgedClasses`, `evidence.dClassesFound`) must agree.
- P3 pinned-byte edits refuse at the pinning layer: the 14 `bindings` and 9 `counts` vectors through
  `layer_products` and `check_counts`, the inheritance vectors whose refusal is a pin refusal (missing, foreign,
  stale, digest), and the `pin` section (v2's file sha256 equals `V2_SHA256`). The "oldest layer" attribution is
  checked only where a vector's `detail` names the layer; otherwise that sub-claim is UNRESOLVED.

Not replayable here and excluded with their counts: `equivalence` (needs the live validators at slots 273-277),
`agreement` (22), `bridgeReplay` (5) and `headOnly` (4), which name the mechanics replay and the head's own
validate().

## 2. Inputs

| input | source | pin | state |
|---|---|---|---|
| X1 git archive of harness-onion `architecture/` at main afee03b9 (slot 278's merge); 1,404 files; 0 oracle or closed-lane members | the monitor (MON-RL-M10) | tar sha256 948a20fabc1353b9003999f4bb43c9a1c7b43276da6436f501d3c1a58dcadb81 | PINNED; only the 26 chain members extracted, listed with sha256 prefixes in `data/export_members.txt` |
| X1.rules `chain-inheritance/rule.json`, `chain-product-packets/rule.json` (pinned by the former at 5e6e6821), `chain-compaction/identity-rule.json` (pinned by the product rule at 4bfbcc03) | inside X1 | per-file prefixes in the members list | the `extends` digests are checked first |
| X1.vectors `chain-inheritance/vectors.json` (26 inheritance, 2 classForms, pin, equivalence), `chain-product-packets/vectors.json` (14 steps, 14 products, 9 counts, 14 bindings, 6 allowedPaths, classForms, 22 agreement, 5 bridgeReplay, 4 headOnly) | inside X1 | as above | the replay set |
| X2 `scripts/chain_identity_v2.py` 23fe723ae060b13727118b5808541d0b40bfee22ac5e803955e324f4dd6d9a55 (28,190 B; equals rule.json's pin) and `scripts/chain_identity_v3.py` 29483ec356f0d2b10f778fc5c4fe642df94795f8249daa088e7a06c995c67fb9 (20,490 B) at afee03b9 | the monitor (MON-RL-M10b) | PINNED (amendment v1.1, 2026-11-05) | staged in the lab scratch |
| X3 `scripts/chain_identity.py` (the v1 model) 1ec764808aaf4e7f2a9eea2da605d0c12d172c5a8e4c23bf3ac79bbb1d07e753 (62,675 B) and `scripts/safe_yaml.py` (the reader the live test passes as `safe_load`; it imports PyYAML) 99c673560e65e58cdc1abe86e53472feaf93e546dd76cb9f3ba051beef5c49d7 (566 B) at afee03b9 | the monitor (MON-RL-M10c) | PINNED (amendment v1.2, 2026-11-05) | staged in the lab scratch; run 002 uses an interpreter that has PyYAML, named in the run record |

## 3. Design and gate

- Replay: each vector section evaluated by the evaluator its `evaluators` entry names; outcome = OK or refuse with
  the clause; compared with the vector's `expect`, `refusal` and `clause`. Deterministic; no seeds.
- Gate: P1 PASS when the 26 inheritance and 14 steps vectors all match and the identity rule's step evidence is
  self-consistent; P2 PASS when the 14 products, 6 allowedPaths and all classForms cases match and the bridged
  classes agree; P3 PASS when the 14 bindings, 9 counts and the pin refusals match and v2's digest equals the pin.
  Any mismatch is FAIL for that property (a finding, never a re-tune); a section that cannot be evaluated (an
  evaluator missing or a signature the lab cannot call as the vectors describe) makes that property UNRESOLVED
  with the section named. H-01 overall: PASS only when P1, P2 and P3 all PASS; FAIL when any FAILs; else UNRESOLVED.
- Record-consistency checks are deterministic reads of the JSON; counts are reported.

## 4-6. Compute, criteria, privacy

Light: `research/tools/rl07_replay.py` (stdlib; `python3 -I -B`; the scripts imported by path from the lab's
scratch copy, never from a repository), seconds. Criteria as in section 3. Outputs hold vector ids, section names,
clauses, counts and booleans; scanned before reporting.
