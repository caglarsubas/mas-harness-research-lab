# RL-21 preregistration v2: one writer per governed state, as the published authority records express it (H-26, contract-text half)

Status: v2, to be frozen after its review (2026-11-06, light; the monitor's GO of 2026-11-06: "H-26 (one writer per governed state, contract-text half), on the c1b838be export, light, with PREREG review first"). v1 (73c96e89, `PREREG.v1.md`) passed review 1, but before any run the lab's inventory showed that the meta authorities' `metaBaseline` is a commit id, not a packet id, so v1's H-26c chain rule cannot be computed from the export; v2 makes H-26c descriptive, states precedence, and says why the export is c1b838be. Both digests go to the register. The export is harness-onion's at c1b838be, the monitor's order for H-25/H-26, because the published contracts are harness-onion's; the register row's b4bbea79 export is R12's simulation harness, the input of the trace half, not of this one.

Scope against the register's clause: H-26 names every governed state in the published contracts and the authority map, revocation vectors, and board-mode traces. The authority map (AUTHORITY-MAP-001) is not yet published and MAS-RA-009's board traces are a later id (BLOCKED), so this id tests the contract-text half on the one form the published contracts give "writer of a state": harness-onion's authority records. Each packet authority names the files it creates (`newFiles`), the files it changes (`changedFiles`) and the packets it builds on (`baselinePackets`); each meta authority names the files it owns (`ownedPaths`) and the meta authority it builds on (`metaBaseline`). A governed state here is a published path; its writer is the authority that created or owns it; "one writer" is: one creator, every later change explicitly built on the creator, and ownership handed down one chain. Revocation ("a revoked authority refuses later writes") is the identity rule's pinned-byte refusals, shown by RL-07, and not re-measured here.

Integrity check before the freeze, by counts only (the inventory of 2026-11-06 on the export): 114 authority records in the export, 92 of the packet form and 22 of the meta form; the packet authorities create 1,547 paths under `architecture/` and list 16,415 changed-file entries, of which the inventory counted 4,335 to paths created inside the export (the rest change files outside `architecture/`, which the export does not hold) and found 0 paths created twice; the meta authorities own 275 distinct paths, 139 owned by more than one of them. The inventory counted; it did not evaluate H-26b's linkage or H-26c's chains beyond the raw totals, which the run computes.

Researcher degrees of freedom, declared: the operationalisation (authorities as writers; paths as states; the three checks) is the lab's, fixed after the inventory's counts and before the run; the inventory saw that no path is created twice, so H-26a's PASS was expected when its gate was written. The authority records were written by the programme's packets for the verifier, independently of this hypothesis (R7).

## 1. Hypotheses (falsifiable)

H-26a: every path under `architecture/` created by a packet authority is created by exactly one. Gate: PASS when 0 paths are created twice; FAIL otherwise.

H-26b: every change a packet authority records to a path created in the export names that path's creator among its own baseline packets (or is the creator itself). Gate: PASS when every such change is linked; FAIL when any is not (the changer and creator named). Changes to paths outside the export are counted and not gated.

H-26c (descriptive, never gated): the paths owned by more than one meta authority, the number of meta authorities, and the form of `metaBaseline` (a commit id). The ownership chain between meta generations runs through git history, which the export (one commit) does not hold; a later id with a git-history export could check it.

Precedence, per claim: the precondition first (at least 50 packet authorities, 5 meta authorities and 500 created paths read; otherwise UNRESOLVED), then H-26b's count (fewer than 100 in-scope changes: UNRESOLVED), then FAIL, then PASS. Overall: PASS when H-26a and H-26b PASS; FAIL when either FAILs; UNRESOLVED otherwise. A PASS means "one creator per path and every change explicitly built on it", the contract-text half under this operationalisation, not the register's whole clause; many later changers are allowed when each names the creator. Expected outcome class, stated in advance: PASS on H-26a (seen in the inventory); H-26b and H-26c unknown; a FAIL on either is a finding about the published records' writer discipline, which the chain's identity rule may or may not enforce (RL-07 checked pinned bytes, not baseline naming).

## 2. Inputs (pinned)

| input | sha256 | origin |
|---|---|---|
| `ho-architecture-c1b838be.tar`: git archive of harness-onion `architecture/` at main c1b838be18fff5081066817777bd8d4ed9c38694, 1,999 members | 79fb0d22e77544e9c8dc45494176d538d24b13078dea5639e2dc9936380fb531 | made read-only by the lab on 2026-11-06 under the monitor's word (RL-20's export, unchanged); the 114 authority records are read from its extracted tree, by name pattern `*-authority.json` and `*/authority.json` |

## 3. Design and compute (the lab's instruments, frozen)

- Checker `tools/rl21_writers.py`, sha256 444493cee0e025be6e1e52e0863b64790683f34d19cd0cd766ca1d871e30829b: reads the authority records, computes the three checks and writes `data/rl21_runs.json` (counts, packet ids and paths of any violation; no file content).
- Evaluator `tools/rl21_eval.py`, sha256 091bad8289062c7d2f4f90cff1449331ab9440251187d3b7f5824654e0c0d181: the gates and `RESULTS.json`, naming its own digest. Both are the lab's instruments on the bridge working tree, no commit of their own, custody by these 64-character digests; a change after this freeze is a new PREREG version.
- Compute: light, this host, standard library, CPython 3.12.4, `python3 -I -B`, under a second; deterministic; no network; stream S4, queue class X; no ECU.
- Privacy: `privacy_scan.py` over every file of the folder before the report; the outputs hold packet ids and repository-relative paths only.

## 4. What is PASS, FAIL, UNRESOLVED

As the gates in section 1; a FAIL or UNRESOLVED is recorded as the finding; no re-tuning of the operationalisation under this id.
