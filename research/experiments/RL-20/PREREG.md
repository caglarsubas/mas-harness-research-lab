# RL-20 preregistration: a static checker over the TopologySpec vectors (H-25, the TopologySpec half)

Status: FROZEN v1 (2026-11-06, light; the monitor's standing word of 2026-11-05: "the c1b838be architecture export for H-25/H-26 may follow without a new word, each light with PREREG review first"). This file's sha256 goes into the register.

Integrity check before the freeze, by counts only: a fresh read-only git-archive export of harness-onion `architecture/` at main c1b838be (the archive pinned below; 1,999 members) was made into a new, empty scratch folder on 2026-11-06. Its `topology-coordination/` record (MAS-RA-004) holds a 299-line README with the TopologySpec rules (section A1: seven refusal codes checked as whole-record passes in order; A3: the selection rule with SELECTION_THRESHOLD 45/100), three closed schemas, and `vectors.json` with 95 cases (52 topology: 8 valid, 8 SHAPE, 3 DUPLICATE_ID, 5 UNKNOWN_REFERENCE, 1 CONFLICTING_OBJECTIVE, 13 MODE_STRUCTURE, 2 BUDGET, 12 SELECTION; 32 transcript; 11 binding) with stores (6 topologies, 11 records, 30 manifests, 12 splits, 19 ledgers). The reference model script is in `scripts/`, outside the architecture export, and is not read. No check was run before the freeze.

Researcher degrees of freedom, declared: the lab wrote its checker from the README's rules and the schemas (published, not oracles), blind to the reference model; it reuses its own schema-subset validator from RL-18 (pinned below) and implements the MAS-RA-002 record rules the topology vectors exercise (SHAPE, DUPLICATE_ID, UNKNOWN_REFERENCE, CONFIGURATION_MIXED, REPETITIONS, SEED_REUSED, TASK_SET, CACHE_EXCEEDS_TOKENS) for the baseline reference. The register's five graph classes were fixed before the record was read (RD-D1 (e)); which of them the TopologySpec form can express was decided after reading the README and before any check: cycle, unreachable node and budget escape are expressible; "two writers" and "unapproved effect path" are not (the form has no per-item writer and no effect marker), and are declared unexpressible, a finding for GRAPH-COMPILE-001, not a measurement. The record and its vectors were written by R00 for MAS-RA-004, independently of this hypothesis (R7).

## 1. Hypotheses (falsifiable)

H-25a (instrument check, evaluated first): the lab's checker returns, for every one of the 52 topology vectors, exactly the code the record expects (or acceptance). Gate: PASS when all 52 agree and at least 40 cases exist; otherwise UNRESOLVED (an instrument gap, fixed under a new version; never FAIL).

H-25b (the seeded classes the form can express): over the 8 valid topology vectors, three one-edit mutations each: a cycle (a DELEGATE back-edge from a non-coordinator node), an unreachable node (a node added with no edge), and a budget escape (the agent budget set below the node count). Expected refusals are the record's own codes: the cycle and the unreachable node are MODE_STRUCTURE in SINGLE_AGENT and CENTRAL (the record bounds delegation depth at 1 and requires the coordinator to delegate to every node), the budget escape is BUDGET in every mode; the unreachable node in DECENTRALIZED (2 vectors) has no rule in the record (peers may be isolated) and is reported descriptively, not gated. Gated edits: 8 + 6 + 8 = 22. A refusal counts when the lab's code equals the expected code and the checker names a witness (the offending node, edge or budget). Gate, in order: UNRESOLVED when H-25a is not PASS; FAIL when any gated edit is accepted or any valid vector is refused by the lab's checker; UNRESOLVED when a gated edit is refused with a different code or without a witness; else PASS. Expected outcome class: PASS on both (the record's rules cover the three expressible classes by construction); the finding of this id is the declared list of what the form cannot express.

Overall verdict: PASS when both PASS; FAIL when H-25b FAILs; UNRESOLVED otherwise. H-25's WorkPlan and strategy halves stay BLOCKED on GRAPH-COMPILE-001's schemas.

## 2. Inputs (pinned)

| input | sha256 | origin |
|---|---|---|
| `ho-architecture-c1b838be.tar`: git archive of harness-onion `architecture/` at main c1b838be18fff5081066817777bd8d4ed9c38694, 1,999 members | 79fb0d22e77544e9c8dc45494176d538d24b13078dea5639e2dc9936380fb531 | made read-only by the lab on 2026-11-06 under the monitor's word; extracted into a new, empty scratch folder |
| `architecture/topology-coordination/README.md` | 890af54aa39c6fbec35615bec8cadb5ffa62c33a5ccce0e21b7af5fcd3fb9c90 |
| `architecture/topology-coordination/vectors.json` | ad177f611d24862e390ddf55268ebd046036b31e176300dd1a2737456b384ec0 |
| `architecture/topology-coordination/topology-spec.schema.json` | a326f70fd56d4300aa1bfaa3838a888c90347a75fc84164188e4af42052e82d0 |
| `architecture/run-manifest/evaluation-record.schema.json` | 8b34740168f5a96f0186b69f9a1a43c544fdd971ed052f8e723c14dda1c3e625 |
| `architecture/run-manifest/run-manifest.schema.json` | ec62c1322179c44df40220a21806e1a0d17d25cc437a9a7e252cd4b1cf9d9636 |
| `architecture/run-manifest/split-declaration.schema.json` | f0247744e5f2e2c23db51ce63f7ed5a7a881f6986e2ee7d308ee5c65e6184a09 |

The lab's RL-18 validator `tools/rl18_manifest.py` (sha256 644a1462ef4cacbaec5c4424b3365155c312a8548990a0fac8d88ebd1ba8aa1f) is imported by path for the schema checks.

## 3. Design and compute (the lab's instruments, frozen)

- Checker `tools/rl20_topology.py`, sha256 57fd7b0c43d9898765869cee9ff08a3cbf6195add6e0bd90426da4bc4f0a2ed6: the topology check in the README's order, the baseline record check and eligibility, the selection rule with the vectors' threshold; the vector agreement; the 24 mutations (22 gated) and the 8 controls; writes `data/rl20_runs.json` (counts, ids, codes and witnesses; no document text).
- Evaluator `tools/rl20_eval.py`, sha256 56ba25ce3ead2ee39f56e7ad3db288d2b44bf81cb7430b61c8b95461b1e8fe7d: the two gates and `RESULTS.json`, naming its own digest. Both are the lab's instruments on the bridge working tree, no commit of their own, custody by these 64-character digests; a change after this freeze is a new PREREG version.
- Compute: light, this host, standard library, CPython 3.12.4, `python3 -I -B`, under a second; deterministic; no network; stream S2, queue class T; no ECU.
- Privacy: `privacy_scan.py` over every file of the folder before the report.

## 4. What is PASS, FAIL, UNRESOLVED

As the gates in section 1; a FAIL or UNRESOLVED is recorded as the finding; an instrument gap in H-25a is fixed under a new PREREG version.
