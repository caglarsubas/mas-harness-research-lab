# RL-22 preregistration: a clean-room board state machine from the README alone (H-23, coordinator half)

Status: v1, to be frozen after its review (2026-11-06, light; the monitor's GO: "H-23 on paper, under the standing word"). This file's sha256 goes into the register after the review.

Scope against the register's clause: H-23 names the TopologySpec, coordinator and strategy-envelope contracts. RL-20 already showed a second implementation of the TopologySpec check reproducing all 52 topology vectors from the README; the strategy envelope (MAS-STRATEGY-001) has no published record and is BLOCKED; this id takes the coordinator contract: a board state machine written from MAS-RA-004's README section A2 alone (the operation table, expiry, arbitration order, retries, the deadline; the transcript refusal codes), run on the record's 32 transcript and 11 binding vectors. One declared gap: VERIFY's ledger binding and verdict history are MAS-RA-001's model and are not re-implemented; the lab's machine takes a VERIFY's recorded answer and, when ACCEPTED, appends the stored ledger's status for the scope's work, so MERGE's verdict rules are modelled from that. A vector whose expectation depends on the un-modelled rules will disagree, and that is counted, not excused: the measurement is how far the README alone carries another runtime.

Integrity check before the freeze, by counts only: the record's vectors hold 32 transcript cases (3 valid, 9 SHAPE, 2 DUPLICATE_ID, 8 UNKNOWN_REFERENCE, 3 MODE, 3 RETRY, 4 REPLAY) and 11 binding cases (2 valid, 2 SHAPE, 5 UNKNOWN_REFERENCE, 2 BINDING); the valid central transcript has 62 operations with every answer recorded. No transcript was replayed before the freeze. The lab read section A2 (78 lines) and the two schemas; it did not read the reference model (outside the export).

Researcher degrees of freedom, declared: the state machine is the lab's reading of A2; where A2 is silent the lab chose (a retry whose original is unknown answers RETRY_MISMATCH; the ASSIGN target must be a WORKER the coordinator delegates to; a RELEASE by the coordinator in CENTRAL is allowed as the table says). The record and vectors were written by R00 for MAS-RA-004, independently of this hypothesis (R7). RL-20's checker (pinned) is reused for the topology reference check inside transcripts and bindings.

## 1. Hypothesis (falsifiable)

H-23 (coordinator half): the clean-room machine returns, for the 43 transcript and binding vectors, the code the record expects (or acceptance with every recorded answer reproduced) at a rate of at least 95 percent. Unit: one vector. Gate, in order: UNRESOLVED when fewer than 40 vectors are read; FAIL when at most 70 percent agree; PASS when at least 95 percent (41 of 43 or more); UNRESOLVED between. Minimum effect: at 95 percent another runtime could ship from the README with at most two points to ask the record's author; below 70 percent the README does not carry the contract. Expected outcome class, stated in advance: UNRESOLVED or PASS; the REPLAY and UNKNOWN_REFERENCE cases that turn on the ledger model are the likely disagreements (up to 4 of 43), and the report names each.

## 2. Inputs (pinned)

| input | sha256 | origin |
|---|---|---|
| `ho-architecture-c1b838be.tar` (harness-onion `architecture/` at main c1b838be18fff5081066817777bd8d4ed9c38694, 1,999 members) | 79fb0d22e77544e9c8dc45494176d538d24b13078dea5639e2dc9936380fb531 | the lab's read-only export of 2026-11-06 (RL-20's); `topology-coordination/README.md`, `vectors.json` and `topology-spec.schema.json` as pinned in RL-20's PREREG; `board-transcript.schema.json` 8a3cc5b87953e97a4b42362df382f9b101931be1d55de84f441b16020b405b7c; `topology-run-binding.schema.json` c7ac9539c82285d580ca605b1d8663029991b45c1b6cc4121a80450b8af69709; the run-manifest schemas as pinned in RL-18's PREREG |

The lab's instruments reused by path: `tools/rl18_manifest.py` 644a1462ef4cacbaec5c4424b3365155c312a8548990a0fac8d88ebd1ba8aa1f (the schema validator) and `tools/rl20_topology.py` 57fd7b0c43d9898765869cee9ff08a3cbf6195add6e0bd90426da4bc4f0a2ed6 (the topology check).

## 3. Design and compute (the lab's instruments, frozen after review)

- Machine and checker `tools/rl22_board.py`, sha256 1a56f824fe1777bf6a87d1183ef885168c6f224a4e1aecfee31e662e3955b2b1: the transcript check in A2's code order, the board, the arbitration order (t, agent, opId), retries, the deadline, the binding check; writes `data/rl22_runs.json` (per vector the expected and the lab's code, the count of mismatched answers and the first one; no document text).
- Evaluator `tools/rl22_eval.py`, sha256 07e6b0a6558269220964b1f882a2db84506fe628ffa5c36a449ada488222c358: the gate and `RESULTS.json` naming its own digest. Both on the bridge working tree, no commit of their own, custody by these digests; a change after the freeze is a new version.
- Compute: light, this host, standard library, CPython 3.12.4, `python3 -I -B`, under a second; deterministic; no network; stream S4, queue class X; no ECU.
- Privacy: `privacy_scan.py` over every file of the folder before the report.

## 4. What is PASS, FAIL, UNRESOLVED

As the gate in section 1; a FAIL or UNRESOLVED is recorded as the finding, with every disagreeing vector named and classed (the README silent, the ledger model, or the lab's reading); no re-tuning of the machine under this id.
