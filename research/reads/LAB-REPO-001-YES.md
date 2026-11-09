# LAB-REPO-001: the Research-Lab's YES on R00's built packet (final-head pass, at c8 of slot 284)

Research-Lab, 2026-11-09, on the Lane-Monitor's word (MON-LAB-284-FINAL). Subject: Harness-Engineering commit
a641e7bb82085cd49e1863c241d5f0ebb84e33d0 (tree 323c61bce61418fb2179d54866ca21800b6ca0d5; parent 608a225d02c0d0a2f442e3f7c939eaae3de3274f; base e515f0b83ca4b3cda9dca02acb6ac0db623b66df, main after 283; branch
codex/met-registry-001-r13-registration), R00's final head c8 of slot 284 (MET-REGISTRY-001, the meta packet that
registers R13 mas-harness-research-lab in the successor registry record and publishes LAB-REPO-001 at K = 1). Changed
paths against the base: 16 added and 284 modified by the monitor's count; the lab's pruned walk sees 16 and 282 and the
meta YAML's 300 allowedPaths cover them plus 2 closed paths the lab does not read. Since the accepted c2 pass the head
gained c3 (the placement record's display lines), c4 (the placement clause), c5 (the D5a oracle and its identity), c6/c7
(the ci/ weights and the catalog reader list) and c8 (a conftest gc.freeze()); the D5a oracle test is counted by the
walk and never read.

Rules: section F of `research/reads/LAB-REPO-001-PACKET-DRAFT.md` at draft 6.6 (sha256 3037ea86129f73838567666be4503f254923888d926c42f9db73c4e2cc4d77cb), which names the
final-head digests. Read route: `git archive` of a641e7bb into a fresh scratch directory, compared with the base's and
the c2 export through the kit's pruned walk, never in place; no network; `python3 -I -B`; TMPDIR in the scratch; no
bytecode left. As agreed in MON-LAB-284-YES2-OK, F5, F10, F14 and F15 were re-run against c8 and every other F input
re-hashed; the check script (scratch, unpublished; counts and digests only) has sha256 4c90ddd650d931b29518ff894416c43ae471e217ff676b28947153ef50251e47 and runs all twenty
checks, so every check was in fact re-run. The composition reader and the successor function were imported from the
export and run in scratch with tampered-pin negative controls; the bridge tools of F9 and of the review-record check
are the packet's own `research/tools/rerun_results.py` and `prereg_check.py`.

## Verdict

**YES at the final head c8.** Every section F check passes: 20 PASS, 0 PENDING, 0 FAIL. This pass supersedes the
accepted c2 pass (MON-LAB-284-YES2-OK) in place; Q-LAB-9 (a) and Q-LAB-10 (a) were ruled standing by the monitor. The c2
pass's one NOTE (the placement record's stale display lines) is resolved at c3. No finding.

## Checks

| id | section F check | result | what was read |
| --- | --- | --- | --- |
| F0 | c8's changed paths against the base e515f0b8 (two git-archive exports compared through the kit's pruned walk) against the meta YAML's allowedPaths | PASS | pruned walk (head: 2477 files kept, 1 dirs pruned, 5 closed files dropped; base: 2461 kept): A 16, M 282, D 0 seen; the meta YAML's 300 allowedPaths = the seen paths plus 2 closed paths the lab does not read (the monitor's A + M count) |
| F1 | task-packets/LAB-REPO-001.yaml equals section A byte for byte at 8ae5c7fd | PASS | task-packets/LAB-REPO-001.yaml 8ae5c7fd, 20123 B, a new path; equals section A's extraction by the fence rule |
| F2 | docs/repositories/13-mas-harness-research-lab.md: section B's text, fenced-tree roots = the YAML's authorized roots, title, PR packets | PASS | plan 13 bc19f6a5 (new path) equals section B's fenced block byte for byte; roots ['.gitignore', 'LICENSE', 'README.md', 'ci', 'research'] = the YAML's; title exact; PR packets names LAB-REPO-001 once; 14 plans |
| F3-C1 | schemas/repositories.schema.json stays byte-equal; no C1 enum edit (Q-LAB-10, ruled (a)) | PASS | schemas/repositories.schema.json 8b1841a7 byte-equal (repositoryId enum 13, no research-lab): no C1 enum edit, as MET-REGISTRY-001's contract 1 states; R13 is admitted by the successor record's schema (F14) |
| F3-C2 | C2's ADR line in docs/adr/0001-repository-boundaries.md; the registry file byte-equal | PASS | ADR 0001 baccff68 modified: the R13 kind-meta boundary line, no other session writes there, names the successor registry record, fourteen repositories; architecture/repositories.yaml byte-equal |
| F3-C3 | C3 as the reader and the counts: validate_readiness.py, validate_architecture.py, validate_reuse.py by diff (one count line) | PASS | validate_readiness f60e7fdb: EXPECTED_REPOSITORIES 13 without R13 (contract 1), no Phase-0 constant, EXPECTED_PACKET_COUNT 295, composed rows asserted 14 via registry_rows; validate_architecture 161c6628: successor map + 14; validate_reuse 8e21f01e: the diff against the base is one line pair, 293 to 295, nothing else (2 diff lines) |
| F3-C5 | rule.json, chain_identity_v2.py, chain_identity_v3.py byte-equal; no in-place rule.json edit; no name check against rule.json | PASS | rule.json 5e6e6821, chain_identity_v2.py 23fe723a, chain_identity_v3.py 29483ec3 byte-equal to the base and absent from the changed paths; no in-place rule.json edit |
| F3-C6 | task-packets/README.md: the 284 rows | PASS | task-packets/README.md 428e82d9: row 294 MET-REGISTRY-001 (K = 1, 295 packets at slot 284, the successor registry record, publishes LAB-REPO-001); row 295 LAB-REPO-001 in mas-harness-research-lab, the one LAB-REPO-001 row |
| F4 | the registration: R13 kind meta with releaseSet: EXCLUDED, and the release lock's conditions | PASS | R13 kind meta with releaseSet EXCLUDED in the composed rows; check_release_lock.py d6138729 reads the composed rows, refuses EXCLUDED on a non-meta repository and takes the release set minus EXCLUDED |
| F5 | the SUCCESSOR registration rule record and function (VIS-284, VIS-284-CR1 C1-3), re-run at c8 | PASS | function e8635f23 and record 4405e9da are new paths; V2_SHA256 = chain_identity_v2.py's sha256; the record's extends names rule.json 5e6e6821 and the function e8635f23 with their clauses; allowedNames [{fromSlot 284, add [mas-harness-research-lab]}]; load() accepts the real bytes; allowed_names at 283 = 12 names without R13, at 284 = 13 with it; a one-byte change to the function: refused (registration extends) |
| F6 | the route clause's base equals R13 main at the YES | PASS | the route clause (inside the byte-equal YAML) names the base cc92594d6daa; the lab's local clone's main is cc92594d6daa (no fetch) |
| F7 | this PR's review record v2 and its YES brief are among the deliverables | PASS | the YAML's deliverables name research/reads/LAB-REPO-001-YES.md and research/reviews/LAB-REPO-001-yes-r1.json |
| F8 | the runner pin equals harness-onion main e515f0b8's runner c8ac40f0 | PASS | ci/run_packet_argv.py c8ac40f0, 9084 B, mode 755 in the head, byte-equal to the base e515f0b8's |
| F9 | rerun_table.json's schema and counts, by the packet's own command | PASS | the YAML's rerun command on the bridge: rc 0, RERUN OK: 23 entries; LEDGER_REDERIVED 10, RAW_REPRODUCED 0, INDEPENDENT_REPLICATION 0, RECORDED 13; table 29dfb885 |
| F10 | the 284 meta YAML task-packets/MET-REGISTRY-001.yaml and its authority's productPackets block, re-run at c8 | PASS | task-packets/MET-REGISTRY-001.yaml 455cd736 (new path): id, repository Harness-Engineering, branch, predecessors [MET-VERIFY-007]; objective K = 1, 295 packets at slot 284, publishes task-packets/LAB-REPO-001.yaml; contract 3 names the product by path and the frozen digest; evidence 14 repositories and 295 packets; excluded names the registry, its schema and the release files; the authority b47b2309 productPackets block holds one entry naming LAB-REPO-001 and the frozen digest (keys ['LAB-REPO-001']) |
| F11 | the built YAML's sha256 is the one the v7 route keys | PASS | 8ae5c7fd at c2, the digest the v7 route keys |
| F12 | section A's rule checks on the YAML against c8's task-packet schema and runner | PASS | id matches the schema's pattern and the file stem; branch codex/lab-repo-001-repository-bootstrap matches and starts with codex/lab-repo-001; repository one inline line; 6 argv arrays free of the runner's 10 forbidden tokens, no shell executable, no uv; offlineExecution = EXPECTED_EXECUTION; prefetchCommands []; 9 allowedPaths none absolute/escaping/wild |
| F13 | the eleven byte-equal files (VIS-284-ARGV, VIS-284-LPORACLE-2, MET-REGISTRY-001 contract 1), re-hashed | PASS | byte-equal to the base and absent from the changed paths: repositories.yaml 02190a66, repositories.schema.json 8b1841a7, evidence-policy.yaml ead30b57, fixture-release-set.yaml 7597ebe4, repos.lock.json 6067ca5e, test_release_lock.py 41f1e773, rule.json 5e6e6821, chain_identity_v2.py 23fe723a, chain_identity_v3.py 29483ec3, language-placement.json 5e4c76bd, 0010-language-placement.md e4c7504b |
| F14 | the SUCCESSOR REGISTRY RECORD with its schema pin, and the composition reader registry_rows, re-run at c8 | PASS | successor registry record 9c129674 (new path) pins its schema b2d07238 by digest and holds one row {research-lab, mas-harness-research-lab, kind meta, dependsOn [], releaseSet EXCLUDED}; registry_rows(head) = 14 rows = the base's 13 names + R13, ids unique; registry_rows(base) = 13; a tampered schema pin: refused (registration registry) |
| F15 | the successor placement record with its schema pin and source spans, and placement_rows, re-run at c8 | PASS | successor placement record 17fc67ef (new path) pins its schema 26c4e874 by digest; one row research-lab/mas-harness-research-lab, R13, PYTHON, Python 3.12.14, decision for LAB-REPO-001; its 2 source spans are located once by digest inside their sections with their evidence tokens present (13-mas-harness-research-lab.md 1-line span at line 73 of ## Testing, verification, and acceptance (display lines [73, 73]); 00-harness-engineering.md 1-line span at line 1604 of ## PR packets (display lines [1604, 1604])); placement_rows(head) = 14 = the base's 13 + R13, placement_rows(base) = 13; a tampered schema pin: refused (registration placement) |

## c8's changed paths (the exports compared through the pruned walk)

Added (16): the 14 of c2 (`architecture/chain-checkpoint/hunk-classes/284.json`,
`architecture/repository-registration-authority.json`, the five files under `architecture/repository-registration/`,
`docs/repositories/13-mas-harness-research-lab.md`, `scripts/repository_registration.py`,
`scripts/validate_met_registry_001.py`, `task-packets/LAB-REPO-001.yaml`, `task-packets/MET-REGISTRY-001.yaml`,
`tests/test_met_registry_001.py`, `tests/test_release_lock_registration.py`) plus `architecture/oracle-identity-met-registry-001.json`
and the D5a oracle test under `tests/` (counted, not read).

Modified (282 seen): the cascade files under `scripts/validate_*.py` and `tests/test_*.py`, `architecture/review-record/briefs.json`,
`ci/parallel_suite_weights.json`, `docs/MASTER_DEVELOPMENT_PLAN.md`, `docs/adr/0001-repository-boundaries.md`,
`docs/repositories/00-harness-engineering.md`, `scripts/check_release_lock.py`, `scripts/language_placement.py`,
`task-packets/README.md`, `tests/conftest.py`; 2 further modified paths lie under names the lab's walk prunes and are
counted, not read.

Final-head digests of the F inputs: unchanged since c2, `task-packets/LAB-REPO-001.yaml` 8ae5c7fd, the plan bc19f6a5, the
successor registry record 9c129674 with its schema b2d07238, the placement schema 26c4e874; changed since c2,
`task-packets/MET-REGISTRY-001.yaml` 455cd736, the successor rule record 4405e9da (extends naming the function e8635f23),
the function e8635f23, the placement record 17fc67ef, the authority b47b2309.

## Not checked by the lab

- c8's edits outside section F, beyond their presence in the changed paths: the cascade edits, the review-record rider,
  the master plan and plan 00 lines, `tests/conftest.py` (the bounded recursion raise and the gc.freeze()),
  `ci/parallel_suite_weights.json`, the D5a oracle test and its identity record `architecture/oracle-identity-met-registry-001.json`,
  the hunk-class record, `scripts/language_placement.py` beyond its call of the composition reader, and
  `scripts/validate_met_registry_001.py` with its tests and the authority beyond F10's read of the productPackets block.
- R00's validators, tests and the 64 inherited commands were not run by the lab; the lab read their constants and
  conditions and ran only the composition reader and the successor function from the export.
- The YAML's full JSON-schema validation: the lab checked section A's enumerated rules against c8's schema and runner.
- The 2 modified paths under pruned names, and the content of the D5a oracle test.

## History

- Round 1 (2026-11-08, MON-LAB-284-YES): YES at c1 212d6343 (13 PASS, F10 pending at c2), accepted at bridge checkpoint
  6302bdc0 (YES 3af085ec, review record 8dd36ef1). R00 then rebuilt the chain to VIS-284-ARGV and VIS-284-LPORACLE-2,
  so that subject left the branch.
- Second pass (2026-11-09, MON-LAB-284-YES2): YES at the rebuilt c2 e22e75a1 (20 PASS; YES 835be39e, review record
  9f582542), accepted in MON-LAB-284-YES2-OK with Q-LAB-9 (a) and Q-LAB-10 (a) standing; one NOTE on the placement
  record's display lines, fixed by R00 as c3.
- Final-head pass (this file): c8 a641e7bb, supersedes the c2 pass in place at the two frozen paths (Q-LAB-9: the
  frozen YAML names this file and `research/reviews/LAB-REPO-001-yes-r1.json` and binds the review record's file name
  to its round; the record's round reads 1 on its subject c8).

## Disclosures

- The lab drafted the packet; this YES is the author's check of R00's build against the author's own section F, not an
  independent review. The subject's identity (commit, tree, parent, base, counts, file digests) was relayed by the
  Lane-Monitor from disk and confirmed by `git rev-parse` on the archive source and by the lab's own digests.
- Q-LAB-9 and Q-LAB-10 were answered by the lab with its recommended option under the owner delegation of 2026-10-22
  and ruled standing by the monitor (MON-LAB-284-YES2-OK); Q-LAB-10 is noted to the visionary at lock 46.
- The D5a oracle test added at c5 is a closed path for the lab (hash and count only); its identity record was not read
  beyond its presence.
- R13 main's position (cc92594d) is the monitor's word plus the lab's local clone; the lab holds no fetch word.
