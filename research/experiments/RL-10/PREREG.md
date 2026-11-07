# RL-10 preregistration: the evidence algebra (H-04)

Status: FROZEN v1 (2026-11-05, light; MON-RL-M14 "go ahead"). Integrity check before the freeze, disclosed: the two
records' evidence vocabularies (the ledger's 15 evidence kinds, its not-evidence, not-confirmation and
consistency-only lists, its 27 refusal codes; the native profile's six closed evidence classes and its by-role
table), the vector sections' sizes and key sets, the native negatives' refusal-code distribution (170 distinct), and
one aggregate seen while sizing the check: the evidence kinds present in the ledger vectors grouped by expected code
(e.g. the CONSISTENCY_ONLY vectors carry REGRESSION_RUN). That aggregate makes check C2 confirmatory in form only;
it is kept because the vector-level rule (every such vector, not the aggregate) was not computed.

## 1. Hypothesis (falsifiable)

H-04: the verdict ledger's evidence rule and the host record's evidence classes compose into one evidence algebra.
Stated as: there is one ordered set of evidence levels into which both vocabularies map totally, such that each
record's refusals agree with the order.

The shared order L, fixed here: ESTABLISHING (5) > PROOF_BOUND (4) > CONSISTENCY_ONLY (3) > NOT_CONFIRMATION (2) >
NOT_EVIDENCE (1); OUT_OF_SCOPE (0) is outside the order (neither supports nor refutes).

Ledger map (from check-kinds.json): TEST_RESULT, REPRODUCER, SCHEMA_RESULT, POLICY_RESULT, ARTIFACT, TRACE, DIFF,
ENVIRONMENT_STATE, DOCUMENT_EXTRACT → ESTABLISHING; RESOLVER_REPORT, CHALLENGER_REPORT, VERIFIER_REPORT → PROOF_BOUND
(a named role's report with evidence); REGRESSION_RUN → CONSISTENCY_ONLY (the consistencyOnly list); ROLLOUT_AGREEMENT,
POOL_RECOMPUTATION → NOT_CONFIRMATION (the notConfirmation list); MODEL_CONFIDENCE, SELF_REPORTED_STATUS → NOT_EVIDENCE
(the notEvidence list).

Native map (from the v4 README and schema): OBSERVED → ESTABLISHING; LABEL_BOUND, ENTRY_BOUND, DECLARED_T04 →
PROOF_BOUND (observation or declaration bound by a named T04 proof); CONSISTENCY_ONLY → CONSISTENCY_ONLY; a self-report
→ NOT_EVIDENCE ("No self-report counts as evidence"); OUT_OF_SCOPE_HOST → OUT_OF_SCOPE.

## 2. Inputs (sha256 prefixes in `data/inputs.txt`; inside the architecture export 948a20fa at afee03b9)

verdict-ledger/check-kinds.json, vectors.json (112 ledgers, 27 codes), README.md; native-profile-v4/qualification.schema.json
(the evidenceClasses const), vectors.json (5 positive, 444 negative, 18 accepted), README.md.

## 3. Checks and gate

- C1 totality: the vocabularies read from the records (15 ledger kinds + 2 not-evidence names; 6 native classes)
  equal the PREREG's lists and each element has exactly one level. FAIL on any element outside the map.
- C2 ledger agreement: every ledger vector whose expected code is CONSISTENCY_ONLY, CONSENSUS_ONLY or NOT_EVIDENCE
  carries at least one evidence item whose kind maps to level 3, 2 or 1 respectively; and no vector whose expected
  code is one of those carries a deterministic check that establishes a value from a level-5 kind on the delivered
  target alone (the lab reads the ledger's `checks` and `evidence`). FAIL on any vector violating either clause.
- C3 native agreement: every negative vector whose refusal names an evidence class ("LABEL_BOUND capture where
  OBSERVED is required", "OBSERVED field missing from the capture", "field forbidden in a LABEL_BOUND capture") is
  consistent with the order: the offered or missing class is strictly below the required class, or the field's
  class ceiling for the role is below the field's required class (the by-role table). FAIL when any such vector
  pairs classes of the same level or inverts the order.
- Gate: H-04 PASS when C1, C2 and C3 all hold; FAIL when any fails; UNRESOLVED when a vector's classes cannot be
  read from its text. Reported, not gated: the asymmetries (OUT_OF_SCOPE has no ledger counterpart; three native
  classes share PROOF_BOUND; NOT_CONFIRMATION has no native counterpart) and a shared vector set proposal.

## 4-6. Compute, criteria, privacy

Light: `research/tools/rl10_algebra.py` (stdlib, `python3 -I -B`), seconds. Outputs hold vocabulary names, levels,
vector ids, codes and counts; scanned before reporting.
