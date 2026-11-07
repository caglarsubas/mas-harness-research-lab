# RL-13 preregistration: the interchange mapping (H-22)

Status: FROZEN v1 (2026-11-05, light; MON-RL-M20 "fine as paper plus one lab-written emitter vector, no network").
Integrity check before the freeze, disclosed: the three contracts' schema shapes (required sets, property names,
enums), the vectors' section names and sizes, the run-event log's operation enum (11 operations), the names of the
OTel mapping sections and the dotted attribute names they carry, and the run-events README's mapping section (it
pins the GenAI conventions at a commit of the conventions repository and states a per-operation table that the
contract's builder checks against seven pinned files). No instance was written or validated before the freeze.

## 1. Hypotheses (falsifiable)

- H-22a (interchange): the verdict-ledger, run-manifest and run-event-log contracts can be emitted by another
  platform from their published schemas alone. Test: the lab writes one minimal instance per contract from the
  schema's required set and type constraints (no contract vector copied), and validates it with the lab's own
  stdlib schema checker (the checker used for the lab's ledgers, extended with local $ref resolution). PASS when all
  three instances validate; a refusal is a finding, and at most two logged repairs per instance are allowed
  (fixture building, not re-tuning); FAIL when an instance cannot be made to validate within two repairs or the
  schema needs information outside its text; the checker is also run over each contract's own positive vectors
  as its sanity check (every positive must pass).
- H-22b (coherent extension of the GenAI conventions): the run-event log's operations map onto the conventions
  without gaps, and the attribute names used are convention names or declared local extensions. Test: (i)
  coverage: every operation in the log's enum has a row in otelSpans or otelPointEvents; (ii) every dotted name in
  the mapping is either a gen_ai.* name the lab knows from the conventions as of its knowledge (a list fixed in
  the script, marked "from the lab's knowledge, not fetched, version unverified"), a gen_ai.* name the lab does not
  know (reported, not failed: the contract pins a later commit), or a planeon.* local extension; (iii) the README's
  never-emitted list and the mapping's used set are disjoint. PASS when (i) and (iii) hold and (ii) reports no
  name outside the three classes; FAIL on a gap in (i) or an overlap in (iii); UNRESOLVED when the pinned
  conventions cannot be checked (they cannot; (ii)'s unknown names stay unverified by design).

## 2. Inputs (prefixes in `data/inputs.txt`; inside the architecture export 948a20fa at afee03b9)

verdict-ledger/ledger.schema.json + vectors.json; run-manifest/run-manifest.schema.json + vectors.json + README.md;
run-events/run-event-log.schema.json + mas-metrics.schema.json + vectors.json + README.md.

## 3. Deliverables, compute, privacy

`MAPPING.md` (the three contracts' interchange surfaces and the convention mapping with each name's class);
`data/emitter_*.json` (the three lab-written instances); `data/interchange_results.json`. Light:
`research/tools/rl13_interchange.py` (stdlib, `python3 -I -B`), seconds. No network. Scanned before reporting.
