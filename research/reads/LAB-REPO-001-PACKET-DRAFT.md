# LAB-REPO-001: R13's first task packet, drafted by the Research-Lab (draft 6.6, 2026-11-09; the YAML frozen at draft 6.1 before bundle v7's c2; paper only)

Draft 6.6 (MON-LAB-284-FINAL, 2026-11-09; outside the YAML, which stays draft 6.1's at sha256 8ae5c7fd, 20,123 B,
re-extracted and checked by script at this draft; the C1-6 channel, text only): section F's text gains the final-head
digests of R00's c8 a641e7bb (branch codex/met-registry-001-r13-registration; 300 changed paths against the base
e515f0b8, 16 A and 284 M by the monitor's count). Since c2 the head gained c3 the span fix (the placement record's
display lines 1598 to 1604), c4 the placement clause, c5 the D5a oracle and its identity, c6/c7 the ci/ weights and the
catalog reader list, and c8 a conftest gc.freeze(). The lab's final-head pass re-runs F5, F10, F14 and F15 against an
export of c8 and re-hashes every other F input; its records supersede the c2 pass in place (Q-LAB-9 (a), ruled standing
by the monitor in MON-LAB-284-YES2-OK, as is Q-LAB-10 (a), the VIS-284-ARGV reading). Nothing else changed; the route
key is untouched. Draft 6.5 was sha256 6974b279.
Draft 6.5 (MON-LAB-284-YES2, 2026-11-09; outside the YAML, which stays draft 6.1's at sha256 8ae5c7fd, 20,123 B,
re-extracted and checked by script at this draft; the C1-6 channel, text only): section F is amended for R00's rebuilt
chain of slot 284 (c2 e22e75a1, parent c1 7ad428ec, base e515f0b8; the monitor's values, read from disk), which
replaces the c1 212d6343 of the round-1 YES. (1) VIS-284-LPORACLE-2: `architecture/language-placement.json` and
`docs/adr/0010-language-placement.md` are byte-equal too; R13's placement row is in a successor placement record,
`architecture/repository-registration/language-placement.json`, with its schema beside it; C2's ADR line lands in
`docs/adr/0001-repository-boundaries.md`, which is modified. (2) `scripts/validate_reuse.py` is modified by one line
only, the task-packet count 293 to 295 from the chain cascade, with no reuse-logic edit: the check reads "no edit
except that count line" and is made by diff against the base. The successor registry record is named by path,
`architecture/repository-registration/repositories.json` with its schema beside it, and the composition reader is
`scripts/repository_registration.py` (registry_rows and placement_rows over the exported root, 14 each). Two further
readings at c2, each with the lab's recommended answer applied (section E): Q-LAB-9, the record form of the second YES
pass under the frozen file set; Q-LAB-10, the registry schema and readiness's EXPECTED_REPOSITORIES staying at
thirteen as MET-REGISTRY-001's contract 1 states. Nothing else changed; the route key is untouched. Draft 6.4 was sha256
7a48e79c.
Draft 6.4 (MON-LAB-284-ARGV, 2026-11-08; outside the YAML, which stays draft 6.1's at sha256 8ae5c7fd, 20,123 B,
re-extracted and checked by script at this draft; the C1-6 channel, text only): the visionary's VIS-284-ARGV changes
slot 284's registration design. The registry file `architecture/repositories.yaml` and the three release files
(`release/evidence-policy.yaml`, `release/fixture-release-set.yaml`, `release/repos.lock.json`) stay BYTE-EQUAL: eight
of the verifier's 64 inherited commands read them live and cannot change under v7. R13 is registered in a new SUCCESSOR
REGISTRY RECORD that 284 owns, read through one composition reader; releaseSet: EXCLUDED lives in that record. Section
C's items 2 and 5 are amended in place (the registry entry; "the 284 head's repositories.yaml (13 product names)"), and
every section F check that expected a registry or release-file edit now reads: the registry and release files are
byte-equal (absent from the PR's changed paths); the successor registry record holds R13's row with kind meta and
releaseSet EXCLUDED; the composition reader returns 14. Round 1 of the lab's YES (research/reads/LAB-REPO-001-YES.md on
c1 212d6343, accepted at checkpoint 6302bdc0) predates this ruling and stands as a record of c1; round 2 runs on R00's
rebuilt c2 against this section F, on the monitor's word. Nothing else changed; the route key is untouched. Draft 6.3
was sha256 f68f61a7.
Draft 6.3 (MON-LAB-62-OK, 2026-11-08; outside the YAML, which stays draft 6.1's at sha256 8ae5c7fd, 20,123 B,
re-extracted and checked by script at this draft): the visionary's VIS-284-CR1 (C1-3) adds a successor FUNCTION beside
the successor registration RECORD, a new file: it binds v2 by V2_SHA256 and reads the slot split from the record, and the
record's extends block names the function's digest. Section F gains that check (the function present as a new changed
path; the record names the function's digest; the function admits mas-harness-research-lab only from slot 284); v2, v3
and rule.json stay absent from the changed paths as at draft 6.2. The monitor verified draft 6.2 (07fa5d08) and keeps
section C's pointer. Nothing else changed; the route key is untouched. Draft 6.2 was sha256 07fa5d08.
Draft 6.2 (MON-LAB-284-F, 2026-11-08; outside the YAML, which stays byte for byte draft 6.1's at sha256 8ae5c7fd,
20,123 B, re-extracted and checked by script at this draft): section F is amended to the visionary's rulings on R00's
slot-284 contract (VIS-284, relayed by the monitor; slot 284 = MET-REGISTRY-001, the meta packet that registers R13
and publishes LAB-REPO-001 at K = 1). R00's contract review found section F expecting three things VIS-284 rules out:
the reuse edit in item C3 (validate_reuse.py's EXPECTED_REPOSITORIES), an in-place edit of
architecture/chain-product-packets/rule.json (item C5) and the YES's name check against rule.json's allowed names.
VIS-284 rules: the Phase-0 inventory stays frozen at 13, and reuse is unchanged; a SUCCESSOR registration rule record
allows mas-harness-research-lab from slot 284, with rule.json, v2 and v3 byte-equal; R13 is kind meta in the registry,
with releaseSet: EXCLUDED. Section C stays as drafted (R00's list at draft 6.1) under a pointer to these rulings;
section F names what the YES checks instead. Nothing else changed; the route key (LAB-REPO-001, 8ae5c7fd, the 53 A
and 8 M paths) is untouched. Draft 6.1 was sha256 f06fd72f.
Draft 6.1 (MON-LAB-Q8-RULED, 2026-11-08; a named delta over draft 6 with one change inside the YAML): the Privacy
contract's set reads "the manifest's file set plus README.md, LICENSE and the lab's own ci/ files; the four pinned
transport copies are fixed by digest in the Transport contract and not scanned", because ci/warm-source-isolation.sh,
pinned byte for byte to 4b2be353, matches the path shapes /private, /tmp, /Users and /home in its own isolation logic
(3 absolute-path hits by the contract's rule, found by the lab's section-D check runs; Q-LAB-8, ruled (a) by the
monitor). Nothing else in the YAML changed: a unified diff of the two extractions shows that one contract line removed
and added. The YAML's sha256 moves from 92a41264 to 8ae5c7fd and the v7 route keys on the new digest; the freeze
applies to 6.1. Outside the YAML this draft also records section D's state (the tools on the bridge and their check
runs) and the RL-01 register correction. Draft 6 was sha256 e603aa24.
Draft 6 (MON-283-MERGED-LAB, 2026-11-08; the freeze before v7's c2): 283 is MERGED (harness-onion main e515f0b8, PR 239,
verify 1009 s), so the runner pin ci/run_packet_argv.py sha256 c8ac40f0, 9084 B, 100755 is no longer provisional: the
monitor's word names it as main's runner now; the lab's platform checkout holds main 4b2be353 and no object e515f0b8 and
the lab has no fetch word, so the lab confirmed the pinned digest against the monitor's stated digest (equal, 64 hex) and
not against e515f0b8's bytes (a git-archive export of that commit's ci/ on the monitor's word would close that). The
head's file set widens from the packet's 12 files to the packet's 12 plus the bridge's research/** changes since the base
(research/reads/BRIDGE-CHANGES-SINCE-CC92594D.md at the freeze: 41 adds and 4 modifies, enumerated in the new
Bridge-changes contract; the manifest and the three page files M as before; 53 A and 8 M paths), since the head equals
the bridge's research/** at the checkpoint B'. Recommendation 2 of R13 issue 1 (R13-ISSUE-1-TRIAGE.md, PARTIAL) widens
rerun_table.json: every entry carries `level` (LEDGER_REDERIVED, RAW_REPRODUCED, INDEPENDENT_REPLICATION, RECORDED),
RECORDED entries carry `externalInputs`, and the PREREG argument is resolved by the ledger's prereg digest. The six
acceptance argv arrays, offlineExecution and the route clause's form are byte for byte draft 5's; the YAML's sha256
changes from 88159c5f to 92a41264 because the Tree contract, the deliverables and the evidence lines enumerate the
widened set: this is the named delta "freeze", and the v7 route keys on the new digest (Q-LAB-7, section E). From this
draft the bridge's research/** file set changes only by the packet's own files until B' is taken; any other add or
delete before the PR is a new named delta. Bridge HEAD at the draft: 8fdb94b5 (the monitor's checkpoint "283 MERGED
e515f0b8"; nothing uncommitted under research/). Draft 5 was sha256 de12ac97.
Draft 5 (MON-RL-R13-FREEZE; the owner "Freeze until v7", the visionary (a)): R13 main stays at cc92594d6daa, the lab's
push of 2026-11-07 on the owner's direct word (236 files: research/** from bridge a67b90a5, README.md, LICENSE,
.gitignore, research/tools/make_manifest.py and manifest_check.py, research/MANIFEST.json), recorded as the owner's
initial commit in place of the LICENSE-only one. The packet re-keys on that main as the PR's base: the head adds only the
packet's files and modifies research/MANIFEST.json (and, the lab's reading, the three page files; Q-LAB-6); rollback
"main returns to cc92594d"; work on branches only, a further push to main only on the owner's word through the monitor,
each re-keying the packet; the App install and the ruleset's main-verify go on together at v7's install, before 284's
PR. Draft 4 was sha256 5cfe26ab. Draft 4 (MON-RL-RUNNER): the runner pin is filled with 283's c1-frozen ci/run_packet_argv.py as relayed by the monitor
(sha256 c8ac40f0, 9084 B), provisional until 283's c2 (two reader probes may reopen c1; a new digest would be a new
named delta); the YAML's final freeze comes before v7's c2, after 283 merges. Draft 3 was sha256 4d738aa9.
Draft 3 (MON-RL-R13-284, the owner's change of plan): R13 moves to slot 284 at K = 1 under bundle v7; the YAML
freezes before v7's c2 and changes only by a named delta; ci/run_packet_argv.py pins to 283's fixed runner (digest
pending from the monitor). Draft 2 was sha256 d38c1324. Draft 2 folds the monitor's answers MON-RL-R13-ANSWERS (Q-LAB-1, 2, 4, 5) and the visionary's rulings MON-RL-R13-RULED
(Q-LAB-3; the owner's LICENSE-only first commit) and logs the RL-11 correction; draft 1 was sha256 b7f6421d.

Scope: the owner's word via the monitor, MON-RL-R13-PACKET ("Unpause for R13's packet only"). The lab drafts; R00
builds the packet at slot 284 (K = 1) under bundle v7 (the owner's word, MON-RL-R13-284; 283 stays at K = 3); the lab
says YES before 284's c2; the YAML freezes before v7's c2 and changes only by a named delta; R13 main stays at cc92594d
until v7 serves R13 and the lab works on branches only (MON-RL-R13-FREEZE). Everything else stays paused: no experiment, search, fetch, heavy run or commit.

Rulings this draft fits (the monitor's 283 design note, 2026-11-07; MON-RL-R13-FREEZE for the base): Q-283-1 as changed by the owner on 2026-11-07,
R13 at 284 at K = 1 (superseding the gated ride at 283); Q-283-5 (a) the hosted route for R13 in bundle v7: python-distribution profile
without the helm and cosign pins, no network, a standard-library workflow, a self-retiring first-packet route that
checks a PREREG plus its review record and the research/MANIFEST.json digest rule. Readiness's four needs: R13 in
`$defs.repositoryId`; EXPECTED_REPOSITORIES at 14; a docs/repositories plan whose fenced-tree roots equal the packet's
authorized roots; `repository` naming R13.

Inputs, by digest: `research/reads/REPO-MIGRATION-PLAN.md` draft 2 with its status note cf6eb2a1; the charter
`research/README.md` 6046110c (meta-review 001 additions); the register 57f55f4a (RL-15b row and the RL-11 correction);
`research/reads/BRIDGE-CHANGES-SINCE-CC92594D.md` (regenerated by script at this draft; the frozen set);
`research/reads/R13-ISSUE-1-TRIAGE.md` 100295c1 (recommendation 2); `handoff/SESSIONS.md` row Research-Lab and transition T12 (the packet id
LAB-REPO-001); the platform repository at main 4b2be353 through a git-archive export (tar sha256 b0aadaf9): the packet
schema, `scripts/validate_readiness.py` (the roots check at the docs/repositories plans, EXPECTED_REPOSITORIES,
EXPECTED_PACKET_COUNT), `architecture/chain-product-packets/rule.json`, `ci/run_packet_argv.py` (the argv rules),
`task-packets/CTRL-TRANSPORT-001.yaml` and `DIST-TRANSPORT-001.yaml` (the first-packet form); R13 main cc92594d6daa
(236 files, bridgeCommit a67b90a5; the monitor checked it by API, MON-RL-R13-MAIN); harness-onion main e515f0b8 (283
merged, PR 239) by the monitor's word only, no export. Bridge HEAD at draft 5: a67b90a5; at draft 6: 8fdb94b5.

## A. The packet (`task-packets/LAB-REPO-001.yaml` in the platform repository; R00 writes the file)

```yaml
id: LAB-REPO-001
repository: mas-harness-research-lab
branch: codex/lab-repo-001-repository-bootstrap
objective: "The bootstrap PR of R13 mas-harness-research-lab over its initial commit cc92594d (the bridge's research tree, README, LICENSE and manifest already on main): the shared offline transport, the remaining standard-library acceptance tools (preregistration and review records, evaluator re-derivation with reproduction levels and external-input provenance, privacy, page check, zero-bill), the bridge's research records added or modified since the base (41 added and 4 modified files: RL-15b, RL-15 run-002, the RL-11 coverage map, the claims table, the review-record data dictionary, meta-review 001, the R13 issue-1 triage and their tools), the manifest regenerated so every file stays listed, the page rebuilt, and the lab's YES record with its review record; no hosted workflow; research records only, no product code and no packets."
predecessors: []
allowedPaths: [".gitignore", "README.md", "LICENSE", "ci/verify-offline.sh", "ci/warm-source-isolation.sh", "ci/network_canary.py", "ci/run_packet_argv.py", "ci/zero_bill_scan.py", "research/"]
warmSourceAccess: PROHIBITED_DURING_IMPLEMENTATION
sourceReuse: []
contracts:
  - >-
    Tree: the PR's base is R13 main at cc92594d6daa, the owner's initial commit (MON-RL-R13-FREEZE: the lab's push of
    2026-11-07 on the owner's direct word, recorded in place of the LICENSE-only commit): research/** byte for byte from
    bridge commit a67b90a5, README.md (5827587a), LICENSE (Apache License 2.0, the canonical text, c71d239d), .gitignore
    (53f0c100), research/tools/make_manifest.py (bb536406), research/tools/manifest_check.py (5511aeec) and
    research/MANIFEST.json (235 files). Main stays at cc92594d until bundle v7 serves R13; the lab works on branches
    only; a further push to main happens only on the owner's word through the monitor and re-keys this packet by a new
    YAML digest. The head's name-status against the base: A for the packet's 12 files (the five ci/ files;
    research/tools/prereg_check.py, rerun_results.py, rerun_table.json, privacy_check.py, page_check.py;
    research/reads/LAB-REPO-001-YES.md; research/reviews/LAB-REPO-001-yes-r1.json) and for the 41 bridge research/**
    files added since the base, enumerated in the Bridge-changes contract (53 A paths); M for research/MANIFEST.json
    (regenerated so every file of the head stays listed; bridgeCommit = the checkpoint commit B' whose research/** the
    head carries), for the three page files research/research.json, research.html and history.json (rebuilt on the
    bridge, since the data record enumerates research/tools and research/reads; Q-LAB-6) and for the four bridge
    research/** files modified since the base, enumerated in the Bridge-changes contract (8 M paths), nothing else:
    README.md, LICENSE, .gitignore and every other base file unchanged. Under research/ the head equals the bridge's research/** at
    B' (which carries make_manifest.py and manifest_check.py byte for byte as on main) plus research/MANIFEST.json. No
    history rewriting: the bridge's git history of research/** stays on the bridge; the manifest is the
    bridge-to-repository link.
  - >-
    Bridge changes since the base (draft 6, the freeze; the rows of research/reads/BRIDGE-CHANGES-SINCE-CC92594D.md at
    the freeze, the bridge's research/** against R13 main cc92594d6daa): A, 41 paths:
    research/experiments/RL-11/data/coverage_map.json, research/experiments/RL-15/data/rl15_gate_002.json,
    research/experiments/RL-15/data/rl15_runs_002.json,
    research/experiments/RL-15/data/rl15_runs_002a_invalid_layout.json, research/experiments/RL-15/runs/run-002.md,
    research/experiments/RL-15b/PREFLIGHT.md, research/experiments/RL-15b/PREREG-REVIEW.md,
    research/experiments/RL-15b/PREREG.md, research/experiments/RL-15b/REPORT.md,
    research/experiments/RL-15b/RESULTS.json, research/experiments/RL-15b/data/preflight/preflight_addendum.json,
    research/experiments/RL-15b/data/preflight/preflight_results.json,
    research/experiments/RL-15b/data/preflight/synthetic-run-record.md,
    research/experiments/RL-15b/data/preflight/synthetic_fail_class_zero_refusals.json,
    research/experiments/RL-15b/data/preflight/synthetic_fail_class_zero_refusals_ledger.json,
    research/experiments/RL-15b/data/preflight/synthetic_fail_control.json,
    research/experiments/RL-15b/data/preflight/synthetic_fail_control_ledger.json,
    research/experiments/RL-15b/data/preflight/synthetic_fail_no_new_rule.json,
    research/experiments/RL-15b/data/preflight/synthetic_fail_no_new_rule_ledger.json,
    research/experiments/RL-15b/data/preflight/synthetic_pass.json,
    research/experiments/RL-15b/data/preflight/synthetic_pass_ledger.json,
    research/experiments/RL-15b/data/preflight/synthetic_unresolved_m4_one_new_rule.json,
    research/experiments/RL-15b/data/preflight/synthetic_unresolved_m4_one_new_rule_ledger.json,
    research/experiments/RL-15b/data/preflight/synthetic_unresolved_unattributed.json,
    research/experiments/RL-15b/data/preflight/synthetic_unresolved_unattributed_ledger.json,
    research/experiments/RL-15b/data/rl15b_runs.json, research/experiments/RL-15b/runs/run-001.md,
    research/hypotheses/CLAIMS.json, research/hypotheses/CLAIMS.md, research/reads/BRIDGE-CHANGES-SINCE-CC92594D.md,
    research/reads/PREREG-REVIEW-META-REVIEW-001-TABLES.md, research/reads/PREREG-REVIEW-META-REVIEW-001.json,
    research/reads/PREREG-REVIEW-META-REVIEW-001.md, research/reads/R13-ISSUE-1-TRIAGE.md,
    research/reads/REVIEW-RECORD-DATA-DICTIONARY.json, research/reads/REVIEW-RECORD-DATA-DICTIONARY.md,
    research/tools/claims_check.py, research/tools/prereg_review_meta.py,
    research/tools/review_record_dictionary_check.py, research/tools/rl15b_eval.py, research/tools/rl15b_mutate.py;
    M, 4 paths:
    research/README.md, research/hypotheses/REGISTER.md, research/reads/LAB-REPO-001-PACKET-DRAFT.md,
    research/reads/REPO-MIGRATION-PLAN.md;
    Each is byte for byte the bridge's research/** at B'; its digest is the manifest's at the head, not pinned here. The
    set is frozen at this YAML: from the freeze the bridge's research/** changes only by the packet's own files until B'
    is taken; any other add, delete or rename before the PR is a named delta with a new YAML digest. The two manifest
    tools are on the base and on the bridge byte for byte at B' (section D), so they are neither A nor M.
  - >-
    Transport: ci/verify-offline.sh, ci/warm-source-isolation.sh and ci/network_canary.py are byte-identical to
    harness-onion main 4b2be353 in sha256, size and git mode (unchanged since 64e5700d; the pins CTRL-TRANSPORT-001
    and DIST-TRANSPORT-001 cite at 57bb1033): ci/verify-offline.sh sha256
    778cb0faf59786dc31559e5d96a399d1e3bb26a4576e0ee9ff70e1f6546bd114, 3908 B, 100755; ci/warm-source-isolation.sh
    sha256 f717f62fb1c9fdaec9eb594c733f25b17394bae6b90a311b9ccc08d4eaf9233b, 4674 B, 100644; ci/network_canary.py
    sha256 1be4a837c4a5baee900db20007c4841361b8c823a1b5e521badcf28890d82099, 1459 B, 100755. ci/run_packet_argv.py is
    byte-identical to 283's fixed runner (MET-VERIFY-007's F head; the visionary's ruling, MON-RL-R13-284), which is
    harness-onion main e515f0b8's ci/run_packet_argv.py after 283's merge (PR 239; MON-283-MERGED-LAB): sha256
    c8ac40f0b85f327b75748cde7c8498a02fdf48c004dbf3259660b92cc289646f, 9084 B, 100755 (relayed by the monitor at 283's
    c1 freeze, MON-RL-RUNNER, and named as main's runner at the merge; no longer provisional); never c2ed0852 (the
    4b2be353 runner). A later change of any transport file on main is a named delta with a new YAML digest. No file under .github/,
    ever (the zero-bill rule; the owner's verifier refuses hosted workflows). ci/zero_bill_scan.py is the lab's own,
    standard library only: it walks the head, refuses WORKFLOW_PRESENT:<path> for any file under .github/,
    SYMLINK:<path> for any symbolic link, BYTECODE:<path> for any __pycache__ or .pyc entry, and HOSTED_RUNNER:<path>
    for the tokens runs-on, actions/ and uses: in any text file outside research/; exit 0 and no output when clean.
  - >-
    Manifest digest rule: research/MANIFEST.json is {"schemaVersion": "planeon.research.manifest/v1", "bridgeCommit":
    <40 hex>, "files": {<path>: <64 hex sha256>}} with sorted keys, paths relative to the repository root, one entry
    for every tracked file of the head except research/MANIFEST.json itself. research/tools/manifest_check.py walks the
    head (skipping .git), and refuses a path on one side only, a digest mismatch, a symbolic link, a bytecode entry, a
    .github directory or a bridgeCommit that is not 40 hex; it prints `MANIFEST OK: <n> files`, or the problem lines
    (repository paths and digest prefixes only) and `MANIFEST FAIL`. Both tools are on main at cc92594d
    (make_manifest.py bb536406, manifest_check.py 5511aeec). The move changes no file's bytes, so every digest already
    named in a register row, a results ledger, a report or a milestone message is an 8-hex prefix of a manifest value,
    checkable without the bridge.
  - >-
    Preregistration and review record (Q-283-5 (a)): research/tools/prereg_check.py requires, for every folder
    research/experiments/RL-nn/, PREREG.md or at least one PREREG.v*.md, RESULTS.json and REPORT.md; every 8-hex digest
    in that experiment's row of the register's "Experiments started" table (the sha256 (frozen) column) equal to the
    sha256 prefix of a PREREG*.md in the folder (frozen versions are kept byte for byte, never rewritten); for RL-14 and
    every later id (the charter's step 1a, adopted 2026-11-05) PREREG-REVIEW.md present, naming the PREREG digest it
    reviewed and ending in PASS for the run version; and the RESULTS.json ledger's evidenceRefs naming the run
    version's PREREG digest and the evaluator script's digest. From the first PR, every lab PR also carries a review
    record in harness-onion's planeon.review-record/v2 schema (schemas/review-record.schema.json at 4b2be353: the
    closed members schemaVersion, kind, series, round, subject {repository, commit, tree}, reviewDate, briefSha256,
    rulesSha256, wrapperSha256, reviewer {model, role} as strings, verdict, findings, checked, disclosures), stored as
    research/reviews/<series with / as ->-r<round>.json; its series is <packet or experiment id>/<brief slug>, its kind
    names the brief by path, and briefSha256 is that brief's sha256: PREREG-REVIEW.md for an experiment PR, the YES
    record research/reads/LAB-REPO-001-YES.md for this PR (Q-LAB-3, the visionary's ruling). prereg_check.py validates
    every research/reviews/*.json against those members and digests with the standard library. Counts only on stdout.
    The verifier reads presence, digests, shapes and the PASS line, never the judgement.
  - >-
    Evaluator re-derivation (widened in draft 6 by recommendation 2 of R13 issue 1): research/tools/rerun_results.py
    reads research/tools/rerun_table.json, which names every RL folder exactly once with a level: LEDGER_REDERIVED (the
    evaluator argv over the committed inputs and the committed RESULTS.json path; the driver runs it, writes under
    TMPDIR only, and requires byte equality with the committed ledger); RAW_REPRODUCED (LEDGER_REDERIVED plus a named
    argv that regenerates the committed inputs from a named raw source in the tree before the evaluator runs, byte
    equality on both); INDEPENDENT_REPLICATION (LEDGER_REDERIVED plus a second ledger from an independent run, named by
    path and sha256, whose verdict the driver compares with the committed one); RECORDED (a one-line reason: the
    verdict was computed over masked exports kept outside the repository, or the ledger predates the evaluator rule),
    which carries externalInputs, one object per input the verdict depended on: source (the repository or record by
    name, never a URL), commit (40 hex or the word none), sha256 (64 hex), availability (IN_TREE, OWNER_HELD or
    UNPUBLISHED) and retrieval (the procedure by which the lab obtained it, one line, no path). The PREREG argument of
    every argv is the PREREG*.md whose sha256 prefix equals the ledger's prereg digest among its evidenceRefs, never
    PREREG.md by name (RL-11's versioned case). At the first commit RL-14 to RL-22 and RL-15b are LEDGER_REDERIVED and
    RL-01 to RL-13 RECORDED; no RAW_REPRODUCED or INDEPENDENT_REPLICATION entry yet (the levels exist so a later PR can
    raise an entry without a schema change). A folder missing from the table, a duplicate, a level outside the four, a
    RECORDED entry without a reason or without externalInputs, or an argv whose PREREG digest is not the ledger's,
    fails. Counts per level on stdout.
  - >-
    Privacy: research/tools/privacy_check.py scans the manifest's file set plus README.md, LICENSE and the lab's own ci/ files; the four pinned transport copies are fixed by digest in the Transport contract and not scanned: it refuses
    absolute home-directory path shapes (the macOS and Linux user folders and the session temp folders), e-mail
    shapes and the legacy term by its
    published sha256 rule (BR-D1); NAME_TOKEN_SHA256 = {} with a loader for an unpublished digest file named by
    RESEARCH_NAME_DIGESTS (absent under the verifier, so the table stays empty; the lab's local pre-push scan sets it).
    Counts only; exit 1 on any hit.
  - >-
    Page check: research/build_research.py stays as on main (the bridge builds the page; its lane file and its links
    into other bridge folders are the bridge's, and README.md says those links do not resolve here).
    research/tools/page_check.py (new) imports build_research.py by path, replaces its lane reader with a fixed stub,
    regenerates the data record in memory, drops generatedAt, lane and bridgeCommit, compares it with the committed
    research/research.json minus the same keys, writes nothing, prints counts only and exits 1 on any difference. The
    bridge mirror copy drops the tree links: no repository URL goes in a bridge file (Q-LAB-4, ruled).
  - >-
    Standard-library workflow: every acceptance command is python3 -I -B over files of the head; no third-party
    import, no uv, make, pip or node, no network, writes only under TMPDIR; the six commands finish in seconds on the
    python-distribution profile without the helm and cosign pins (Q-283-5 (a)); the profile's pinned CPython 3.12.14.
  - >-
    Route: the self-retiring first-packet route of bundle v7, keyed by (LAB-REPO-001, this YAML's sha256) with the
    exact file set equal to the head's name-status against the base, which the route checks is R13's main at
    cc92594d6daa (MON-RL-R13-FREEZE): A for exactly the 53 paths and M for exactly the 8 paths named in the Tree and
    Bridge-changes contracts, nothing else; the manifest's keys equal the head's tracked set
    minus the manifest; single use bound to the first PR number, retired at that PR's merge. A push to main before the
    PR moves the base and re-keys the route by a new YAML digest. Later LAB packets are verified under the ordinary
    hosted route, inheriting this packet's six commands in order.
  - >-
    Verifiable only under bundle v7 (an owner install step, not a predecessor), which adds mas-harness-research-lab to
    the verifier's fixed repository list (the installed v6 refuses any product outside its twelve) and this packet's
    route keyed by the frozen YAML's sha256. The packet is a product at slot 284, K = 1 (the owner, MON-RL-R13-284);
    its YAML freezes before v7's c2, and any later change is a named delta with a new digest that re-keys the route.
    The App install and the ruleset's main-verify go on together at v7's install, before 284's PR (MON-RL-R13-FREEZE).
    R13 holds research records only: no product code, no packets, no roadmap writes.
deliverables:
  - "research/MANIFEST.json regenerated by research/tools/make_manifest.py (on main since cc92594d) with bridgeCommit B', listing every file of the head: the base's 235 plus the packet's 12 and the 41 bridge adds (288)."
  - "The 41 bridge research/** files added and the 4 modified since the base (Bridge-changes contract), byte for byte the bridge's research/** at B'."
  - "research/tools/prereg_check.py, rerun_results.py with rerun_table.json (every entry with level; RECORDED entries with externalInputs), privacy_check.py and page_check.py (new; written on the bridge first and carried in research/**); ci/zero_bill_scan.py; research/build_research.py, make_manifest.py and manifest_check.py as on main."
  - "The four exact transport copies (sha256, size and mode as pinned); no .github entry."
  - "README.md, LICENSE and .gitignore as on main cc92594d, unchanged and listed in the manifest (README.md: the layout, the manifest check, how to file an issue, the rules; the procedure and the PR flow are the charter's)."
  - "research/reads/LAB-REPO-001-YES.md (the lab's YES record, section F) and research/reviews/LAB-REPO-001-yes-r1.json (its review record v2 naming that brief by path and sha256); the three page files rebuilt on the bridge over the head's research/tools and research/reads."
excluded:
  - "Any experiment run, fetch, search, export or heavy job; network; .github; node, uv, make or pip; any bridge path; the lane file; any other repository; history rewriting; product code; packets; roadmap writes."
prefetchCommands: []
offlineAcceptanceCommands: [["python3","-I","-B","ci/zero_bill_scan.py"],["python3","-I","-B","research/tools/manifest_check.py","research/MANIFEST.json"],["python3","-I","-B","research/tools/privacy_check.py","research/MANIFEST.json"],["python3","-I","-B","research/tools/prereg_check.py","research/hypotheses/REGISTER.md","research/experiments"],["python3","-I","-B","research/tools/rerun_results.py","research/tools/rerun_table.json"],["python3","-I","-B","research/tools/page_check.py","research/MANIFEST.json"]]
offlineExecution: {"wrapperArgv":["./ci/verify-offline.sh"],"packetPathEnvironment":"HARNESS_TASK_PACKET","packetPathMode":"HASH_PINNED_READ_ONCE_NO_CHILD_PATH","commandTransport":"ARGV_ARRAY_V1","isolation":"OS_ENFORCED_DENY_ALL_OUTBOUND","sessionScope":"SINGLE_PROCESS_TREE","prefetchOutsideSession":false,"offlineEnvironment":{"UV_OFFLINE":"1","UV_FROZEN":"1","UV_NO_SYNC":"1"}}
expectedEvidence:
  - "Name-status of the head against the base cc92594d6daa: A for exactly the packet's 12 files (five ci/ files, five research/tools entries, the YES record and its review record) plus the 41 bridge adds of the Bridge-changes contract (53 paths), M for research/MANIFEST.json, the three page files and the four modified bridge files of that contract (8 paths), nothing else; the manifest's keys equal the head's tracked set minus the manifest; manifest_check PASS with 288 files (the base's 235 plus 53) and 0 problems."
  - "Three transport files equal harness-onion main 4b2be353 and ci/run_packet_argv.py equals 283's fixed runner, by sha256, size and mode; no .github entry; zero_bill_scan PASS."
  - "prereg_check PASS: 23 experiment folders (RL-01 to RL-22 and RL-15b); every frozen digest of the register present in its folder; PREREG-REVIEW.md present for RL-14 to RL-22 and RL-15b (10 of 23)."
  - "rerun_results PASS: 23 table entries, every level one of the four; RL-14 to RL-22 and RL-15b LEDGER_REDERIVED byte for byte (10); RL-01 to RL-13 RECORDED (13) with reasons and externalInputs; 0 RAW_REPRODUCED, 0 INDEPENDENT_REPLICATION."
  - "privacy_check 0 hits over the head; the lab's local pre-push scan over the same set with the unpublished digest file 0 hits, reported in the PR body as counts."
  - "page_check PASS (the data record reproduces minus generatedAt, lane and bridgeCommit); the six commands pass in one deny-all process tree under ./ci/verify-offline.sh in seconds; no heavy job."
rollback: Revert the PR; main returns to cc92594d6daa, the owner's initial commit, and the bridge stays the authoritative research tree, so nothing is lost.
```

Checks on the YAML against the published rules: `id` matches the schema's id pattern and rule.json's productId
(file stem = id); `branch` starts with codex/lab-repo-001; `repository` is one plain inline line (R12: safe_load reads
the same value); every `offlineAcceptanceCommands` argv avoids the forbidden tokens (curl, wget, npx, prefetch,
fetch, download, install, sync, add, pull), no shell executable, no uv; `offlineExecution` equals the runner's
EXPECTED_EXECUTION; `prefetchCommands` is []; `expectedEvidence` carries no legacy result token; no allowed path is
absolute, escapes, or is `.`, `*`, `**` or `/`; the authorized roots are {.gitignore, LICENSE, README.md, ci, research}.

## B. The repository plan (`docs/repositories/13-mas-harness-research-lab.md`; R00 writes the file)

```markdown
# Repository Plan: `mas-harness-research-lab`

## Purpose and boundaries

R13 is the programme's research repository (kind meta, no plane): the hypothesis register, preregistered experiments,
run records, verdict-form results ledgers, one-page reports, design reads and per-scope progress documents of the
Research-Lab session (`research/README.md`, the charter). It is public; another LLM provider's GitHub App reads it and
opens issues; it never writes. The repository is evidence and proposals, never authority: what should enter the product
goes to the roadmap visionary as a proposal and through the harness-admission gate as a candidate.

Non-goals:

- No product code, no task packets, no roadmap writes, no contracts; nothing another repository imports.
- No hosted workflow, runner, artifact, cache or package; verification is the owner-operated verifier only.
- No experiment runs under the verifier: acceptance re-derives committed ledgers from committed inputs and checks
  records; heavy runs stay on the lane monitor's queue.

## Repository structure and exact tree

This tree projects the current task-packet `allowedPaths`. Directory entries do not authorize edits beyond the packet
executed in a coding run.

```text
mas-harness-research-lab/
├── .gitignore
├── LICENSE
├── README.md
├── ci/
│   ├── verify-offline.sh
│   ├── warm-source-isolation.sh
│   ├── network_canary.py
│   ├── run_packet_argv.py
│   └── zero_bill_scan.py
└── research/
    ├── README.md
    ├── MANIFEST.json
    ├── build_research.py
    ├── research.html
    ├── research.json
    ├── history.json
    ├── hypotheses/REGISTER.md
    ├── experiments/RL-nn/{PREREG.md, PREREG-REVIEW.md, runs/, data/, RESULTS.json, REPORT.md}
    ├── reads/
    ├── reviews/
    ├── progress/
    └── tools/
```

## Dependencies

- Contract/source: none. The lab reads other repositories through git-archive exports at pinned commits (the
  platform's published contracts, the conformance-labs harness, never its oracle tests); nothing is imported.
- Build artifact: none; the acceptance set is the standard library on the verifier's python-distribution profile.
- Runtime integration: none. Downstream: the bridge mirrors `research/research.html`, `research.json`, `history.json`
  and `MANIFEST.json` at each merge; proposals reach the roadmap through the visionary, never by a dependency edge.

## Warm-source mapping

None. The repository holds no warm source and no reuse index entry.

## PR packets

1. `LAB-REPO-001-repository-bootstrap`: over the owner's initial commit cc92594d (the bridge's research tree byte for
   byte with `research/MANIFEST.json`, the root README, LICENSE and the manifest tools): the exact harness-onion
   transport copies (the runner at 283's fixed form, harness-onion main e515f0b8), a standard-library zero-bill scan,
   the remaining acceptance tools (preregistration and review records, evaluator re-derivation with reproduction
   levels, privacy, page check), the bridge's research records added or modified since the base (41 and 4 files, the
   packet's frozen set), the manifest regenerated, the page rebuilt and the lab's YES record with its review record;
   verifiable only once bundle v7 is installed, through its self-retiring first-packet route.

## Testing, verification, and acceptance

`LAB-REPO-001` declares `prefetchCommands: []` and ordered `offlineAcceptanceCommands` of six `python3 -I -B` argv
arrays: the zero-bill scan, the manifest check, the privacy check, the preregistration-and-review check, the evaluator
re-derivation and the page check. The executor supplies the hash-pinned packet through `HARNESS_TASK_PACKET` and
invokes only `offlineExecution.wrapperArgv: ["./ci/verify-offline.sh"]` for the complete ordered list. Later packets
add checks as direct argv arrays; each lab PR carries a PREREG, its review brief (PREREG-REVIEW.md) and a review
record in the platform's review-record v2 schema before any run, and the register's frozen digests are checked
against the folder's files at every head.

Acceptance: the head's tracked set equals the manifest; every digest named in a register row is present as a frozen
PREREG; every re-derived ledger is byte-identical; no privacy hit; the page's data record reproduces; no workflow file.

## Release and rollback

No release artifact. A merge is the publication; the bridge mirror follows. Rollback is the revert of the PR; frozen
preregistrations are never rewritten (a correction is a new version or a new experiment id).

## Zero-bill rules

No file under `.github/`; no hosted runner, Actions cache, artifact or package; no network in acceptance; the owner's
verifier is the only CI; `ci/zero_bill_scan.py` refuses any workflow file, symbolic link or bytecode entry.
```

Roots of the fenced tree: .gitignore, LICENSE, README.md, ci, research = the packet's authorized roots.

## C. Readiness edits that ride with the packet at 284 (R00's, listed so the lab's YES can check them)

VIS-284 (MON-LAB-284-F, 2026-11-08) supersedes two entries below: the reuse part of item 3 (validate_reuse.py keeps
the frozen Phase-0 inventory of 13; reuse is unchanged) and item 5 (rule.json is not edited in place; a SUCCESSOR
registration rule record allows mas-harness-research-lab from slot 284, with rule.json, v2 and v3 byte-equal). The items
stay as drafted for the record; section F lists what the lab's YES checks. VIS-284-ARGV (MON-LAB-284-ARGV, 2026-11-08)
amends items 2 and 5 in place: the registry file and the three release files stay byte-equal, and R13's row lives in a
SUCCESSOR REGISTRY RECORD that 284 owns. VIS-284-LPORACLE-2 and MON-LAB-284-YES2 (2026-11-09, draft 6.5): the
placement file and ADR 0010 stay byte-equal too and R13's placement row lives in the successor placement record
beside the registry record; item 3's `scripts/validate_reuse.py` carries one count line, 293 to 295, from the chain
cascade and no reuse-logic edit; item 1's schema stays byte-equal and readiness's EXPECTED_REPOSITORIES stays the
thirteen (Q-LAB-10, section E).

1. `schemas/repositories.schema.json` `$defs.repositoryId`: add `research-lab` (14 names).
2. `architecture/repositories.yaml` stays BYTE-EQUAL (VIS-284-ARGV, draft 6.4: eight of the verifier's 64 inherited
   commands read it and the three release files live; they cannot change under v7), and so do `release/evidence-policy.yaml`,
   `release/fixture-release-set.yaml` and `release/repos.lock.json`. R13's row (id research-lab, name
   mas-harness-research-lab, kind meta, releaseSet EXCLUDED; the record's exact shape is R00's) lives in a new SUCCESSOR
   REGISTRY RECORD that 284 owns, read through one composition reader that returns 14 (the file's 13 plus the record's
   R13); no graph edge (nothing consumes or provides at build time). Before draft 6.4 this item read as an entry
   `{id: research-lab, name: mas-harness-research-lab, kind: meta, dependsOn: []}` in the registry file.
   `docs/adr/0001-repository-boundaries.md`: the R13 boundary line (research records only; no other session writes
   there; the lab reads through exports).
3. `scripts/validate_readiness.py` EXPECTED_REPOSITORIES (+ mas-harness-research-lab, 14), the repository-plan count
   13 -> 14 and its message, EXPECTED_PACKET_COUNT from 283's count (293 at K = 3) to 284's (295: 284's meta packet +
   LAB-REPO-001; R00 states the counts); `scripts/validate_reuse.py`
   EXPECTED_REPOSITORIES; `scripts/validate_architecture.py` map (+ research-lab).
4. `docs/repositories/13-mas-harness-research-lab.md` as in section B (the title line exact; the fenced tree under
   "## Repository structure"; the "## PR packets" section declares LAB-REPO-001 once).
5. `architecture/chain-product-packets/rule.json` stays byte-equal (VIS-284), and so does `architecture/repositories.yaml`
   (VIS-284-ARGV, draft 6.4): no record revision over the registry file. The name mas-harness-research-lab is allowed
   from slot 284 by the SUCCESSOR registration rule record and its function (VIS-284, VIS-284-CR1; section F), which
   extend v2's R8 clause 2 (a `repository` outside the twelve names) for slot 284 onward as R00 builds them; the lab's
   YES checks the function's behaviour at slots 283 and 284 and no longer checks the product's `repository` line
   against rule.json. Before draft 6.4 this item read: the record revision moves from dd000fef (12 names) to the 284
   head's repositories.yaml (13 product names) with its sha256; the vectors follow.
6. `task-packets/README.md`: the 284 row names LAB-REPO-001 as its one product; the counts read 295 packets at slot
   284 (R00's count).
7. The session map, lanes.json and issue tracking entries are the monitor's; the verifier's R13 policy row is bundle
   v7 (the owner's install); the App install and the ruleset's main-verify go on together at v7's install, before
   284's PR (MON-RL-R13-FREEZE).

## D. The lab's work before the first commit (on the monitor's word; not under the pause)

- Done on main cc92594d (the owner's direct word, 2026-11-07; the monitor checked it by API, MON-RL-R13-MAIN):
  README.md, LICENSE, .gitignore, research/tools/make_manifest.py, research/tools/manifest_check.py and
  research/MANIFEST.json over research/** from bridge a67b90a5. Remaining, on the monitor's word, on the bridge first
  (research/tools/ and research/reads/ are the lab's) and then on a branch of R13 with no push to main:
  prereg_check.py, rerun_results.py with rerun_table.json, privacy_check.py and page_check.py; the two manifest tools
  copied onto the bridge byte for byte; the YES record and its review record; the page rebuilt on the bridge;
  ci/zero_bill_scan.py and the four transport copies on the branch; the manifest regenerated; the six commands run
  locally under the transport before the PR.
- RL-11 correction, done 2026-11-07 (MON-RL-R13-ANSWERS; a lab-internal record correction): the run version was v1.1
  (v1 plus the section-4 amendment, sha256 b06eabdb7d878795c268239c48541c8cf08dba156ebec3ba426d064e7c9c36d6, the
  ledger's scopeDigest and E6); after the run the MON-RL-M19 correction was appended in place as section 5, so
  PREREG.md read 7c6b64fc against the registered b06eabdb. Restored: PREREG.v1.md = 89d6ee61 (the original, from
  bridge commit 87bab8f7), PREREG.v1.1.md = b06eabdb (the run version, the current text cut before section 5; digest
  verified), PREREG.md = v1.2 7c6b64fc kept as the post-run amendment; the register row names all three. The rule in
  section A (every row digest present as a PREREG*.md) holds for 22 of 22 folders; RL-02 holds PREREG.v1.md bbb53d0b
  and PREREG.v2.md 1a927051 as its row names.
- rerun_table.json (schema widened in draft 6, recommendation 2): RL-14..RL-22 and RL-15b LEDGER_REDERIVED (the
  evaluators take RUNS_JSON PREREG_MD RUN_RECORD_MD OUT_PATH; inputs under data/ and runs/ are in the tree; RL-15b:
  rl15b_eval.py 2d6c349b over data/rl15b_runs.json f445e3c1, PREREG.md e5a75db2 and runs/run-001.md af1e9122, ledger
  d1810a57; RL-11: the PREREG argument is PREREG.v1.1.md b06eabdb, the ledger's prereg digest); RL-01..RL-13 RECORDED
  with the reason per folder (masked exports kept outside the repository, or a ledger written before the evaluator
  rule) and externalInputs per input (source, commit, sha256, availability, retrieval), filled from each PREREG's input
  list and run records when the table is written (section-D work, on the monitor's word).
- Section D done on the bridge (2026-11-08, MON-LAB-D6-OK GO): research/tools/make_manifest.py bb536406 and
  manifest_check.py 5511aeec copied from R13 main byte for byte (mode 755); research/tools/prereg_check.py 16001f66,
  rerun_results.py 284ca154, rerun_table.json 29dfb885 (23 entries: 10 LEDGER_REDERIVED, 13 RECORDED with reasons and
  externalInputs built from each ledger's evidence entries), privacy_check.py de3bd1b6 (the pinned transport copies
  excluded, Q-LAB-8), page_check.py 374a4c60; ci/zero_bill_scan.py c71c55a6 held in the lab's scratch for the branch.
  Check runs on a staging tree (a local clone of R13 at cc92594d with the bridge's research/** overlaid, the three
  transport copies from the 4b2be353 export and zero_bill_scan.py under ci/, the manifest regenerated; nothing
  committed): all six commands pass (MANIFEST OK 285 files; PRIVACY OK 283 files, 0 hits; PREREG OK 23 folders, 10
  reviewed; RERUN OK 23 entries; PAGE OK; zero-bill silent); name-status against the base A 50, M 8 (the frozen 53 A
  minus the runner, the YES record and its review record, which come later); negative controls refused as designed.
  RL-01 record correction (MON-LAB-Q8-RULED, accepted): the register's frozen column had named v1 f0bdb2f7, a digest
  with no file anywhere in the bridge history (PREREG.md was amended in place to v1.1 db893373 before the first commit,
  before the kept-versions rule); the row keeps v1.1 db893373 in the frozen column and records the lapse in the state
  column; no verdict, ledger or claim changed.
- The freeze (draft 6, 2026-11-08, MON-283-MERGED-LAB): the bridge's research/** changes since the base, as
  research/reads/BRIDGE-CHANGES-SINCE-CC92594D.md lists them at the freeze (41 A, 4 M, plus the three page files), are
  the Bridge-changes contract's set; the list file is regenerated at every milestone and must show the same A and M
  rows at B' (a new row would be a named delta). Nothing of section D is built by the freeze itself.

## E. Questions for the monitor, each with the lab's recommended answer (owner delegation of 2026-10-22)

- Q-LAB-1 LICENSE: ANSWERED (owner): Apache License 2.0.
- Q-LAB-2 the created repository's initial state: RULED, then SUPERSEDED 2026-11-07 (MON-RL-R13-FREEZE): main
  cc92594d6daa, the lab's push on the owner's direct word, is the owner's initial commit in place of the LICENSE-only
  one; the packet re-keys on it as the PR's base (section A); main stays there until v7 serves R13.
- (a)/(b) of RL-M46: RULED (a) by the visionary; the owner "Freeze until v7" (MON-RL-R13-FREEZE); folded into
  sections A, B, D and F.
- Q-LAB-6 the name-status form (the lab's reading of MON-RL-R13-FREEZE, applied with the recommended answer under
  the owner delegation): the ruling names A for the packet's files and M for research/MANIFEST.json; the data record
  of research/research.json enumerates research/tools and research/reads, which the packet extends, so the three page
  files are M as well (rebuilt on the bridge). Recommended (a), applied: the three M entries ride with the manifest
  update. (b) would freeze the page files and make page_check fail by design.
- Q-LAB-3 "review record v2": RULED (visionary): harness-onion's review-record v2 schema, one record per PR,
  reviewer identity as strings, the brief digest; PREREG-REVIEW.md is the brief, named by path and sha256; two files per
  review from the first PR. Folded into section A (the preregistration-and-review contract and the deliverables).
- Q-LAB-4 the bridge mirror's page links: ANSWERED: dropped; no repository URL goes in a bridge file.
- Q-LAB-5 the profile's interpreter: ANSWERED: the pinned CPython 3.12.14.
- Runner pin: RECEIVED (MON-RL-RUNNER): sha256 c8ac40f0b85f327b75748cde7c8498a02fdf48c004dbf3259660b92cc289646f,
  9084 B, 100755, filled into section A; CONFIRMED by the monitor's word at 283's merge (MON-283-MERGED-LAB:
  harness-onion main e515f0b8, PR 239; the c1 runner c8ac40f0 is main's). The lab's check: the 64-hex digest the
  monitor names equals the pinned one; the lab could not read e515f0b8's bytes (its platform checkout holds 4b2be353,
  no fetch word); an export of that commit's ci/ on the monitor's word would let the lab confirm size, mode and bytes
  itself. The freeze is draft 6.
- Q-LAB-7 the route key at the freeze (the lab's reading of "the six commands and the route key stay unchanged"):
  the key's form (LAB-REPO-001, the YAML's sha256, the exact file set) and the six argv arrays are unchanged byte for
  byte; the YAML's sha256 is new (92a41264, from 88159c5f) because the widened set is inside the YAML's contracts and
  evidence, as the route clause requires for any change. Recommended (a), applied: the new digest is the frozen key.
  (b), keeping 88159c5f, would leave the Tree contract naming 12 A paths against a head carrying 53, which the route
  would refuse.
- Q-LAB-8 the Privacy contract's set against the pinned transport copies: RULED (a) by the monitor (MON-LAB-Q8-RULED)
  and applied as draft 6.1, the one YAML change; privacy_check.py implements the same words.
- Q-LAB-9 the record form of the second YES pass (MON-LAB-284-YES2 "round 2 ... they supersede r1"; the lab's reading,
  applied with the recommended answer under the owner delegation): the YAML names the YES record
  research/reads/LAB-REPO-001-YES.md and one review record research/reviews/LAB-REPO-001-yes-r1.json among the 53 A
  paths, and its storage rule binds the file name to the round (-r<round>.json), so a -r2.json would be a 54th A path
  and a named delta inside the YAML (the Tree and Bridge-changes contracts and the evidence lines), re-keying the v7
  route. Recommended (a), applied: the second pass is written in place at the two frozen paths and supersedes round
  1's files; the review record's round reads 1 on its new subject c2 (the first review of the rebuilt chain), and the
  superseded pass on 212d6343 (accepted at checkpoint 6302bdc0) is recorded in the YES record's history and the
  record's disclosures. (b), a -r2.json beside -r1.json, needs a named delta through the monitor and leaves -r1.json's
  briefSha256 pointing at a YES text that no longer exists at that digest (prereg_check RECORD_BRIEF_MISMATCH) unless
  the round-1 brief is also kept as a new path.
- Q-LAB-10 the registry schema and readiness's EXPECTED_REPOSITORIES at c2 (the lab's reading, applied with the
  recommended answer under the owner delegation): MON-LAB-284-YES2 names the registry and release files byte-equal but
  not `schemas/repositories.schema.json` nor readiness's EXPECTED_REPOSITORIES; at c2 the schema is byte-equal (its
  repositoryId enum at 13) and the constant stays 13, and MET-REGISTRY-001's contract 1 (355b0bd3) states both under
  VIS-284-ARGV ("architecture/repositories.yaml, its schema, the three release files and tests/test_release_lock.py
  stay byte-equal"; "readiness's EXPECTED_REPOSITORIES stays the thirteen"). Recommended (a), applied: section F reads
  C1 and C3 as that contract states them (no enum edit; the successor record's own schema admits R13; EXPECTED_REPOSITORIES
  13 and the composed live rows 14), since the schema is the registry file's live-read companion and the ruling's logic
  covers it. (b), holding draft 6.4's words, would FAIL F3-C1 and F3-C3 against a packet built to the visionary's
  ruling. If the monitor or the visionary reads VIS-284-ARGV otherwise, the YES is withdrawn on those two checks.

## F. The lab's YES before 284's c2 (what it checks on R00's built packet; amended at drafts 6.2 to 6.6 to VIS-284, VIS-284-CR1, VIS-284-ARGV and VIS-284-LPORACLE-2, with the final-head digests at 6.6)

The YAML equals section A (draft 6.1, the freeze; Q-LAB-1..8, MON-RL-R13-FREEZE, MON-283-MERGED-LAB and
MON-LAB-Q8-RULED are folded in), byte for byte at sha256 8ae5c7fd, 20,123 B; the plan's fenced-tree roots equal the
YAML's authorized roots; the readiness edits present are C4 and C6, C2's ADR line (in `docs/adr/0001-repository-boundaries.md`,
which is modified and names the successor registry record), and C3 as the reader and the counts (draft 6.5: the schema
`schemas/repositories.schema.json` stays byte-equal with the registry file it validates, so C1's enum edit is not
expected and R13's id and name are admitted by the successor record's own schema beside it; readiness's
EXPECTED_REPOSITORIES stays the thirteen and the composed live rows are 14, as MET-REGISTRY-001's contract 1 states under
VIS-284-ARGV (Q-LAB-10); EXPECTED_PACKET_COUNT 295; `scripts/validate_architecture.py` maps the successor repository and
counts 14; `scripts/validate_reuse.py` carries no edit except its task-packet count line, 293 to 295 from the chain
cascade, which the YES checks by diff against the base (MON-LAB-284-YES2); VIS-284 "the Phase-0 inventory stays frozen
at 13, and reuse is unchanged" holds for the reuse logic); eleven files are byte-equal, read as their absence from the
PR's changed paths and by byte comparison with the base: the registry file `architecture/repositories.yaml` and its
schema, the three release files `release/evidence-policy.yaml`, `release/fixture-release-set.yaml` and
`release/repos.lock.json`, `tests/test_release_lock.py`, `architecture/chain-product-packets/rule.json`,
`scripts/chain_identity_v2.py`, `scripts/chain_identity_v3.py`, and the placement file
`architecture/language-placement.json` with `docs/adr/0010-language-placement.md` (VIS-284-ARGV: eight of the
verifier's 64 inherited commands read them live and they cannot change under v7; VIS-284-LPORACLE-2 for the placement
pair); the SUCCESSOR REGISTRY RECORD that 284 owns, `architecture/repository-registration/repositories.json` with its
schema beside it and pinned by digest in the record, is present among the changed paths and holds R13's row with kind
meta and releaseSet: EXCLUDED (VIS-284-ARGV; the YES reads the row from the record, not from the registry file); R13's
placement row is in the successor placement record `architecture/repository-registration/language-placement.json`
with its schema beside it, pinned the same way (VIS-284-LPORACLE-2); the composition reader
`scripts/repository_registration.py` returns 14 rows from registry_rows and 14 from placement_rows over the exported
root and 13 and 13 over the base's (the files' 13 plus the records' R13; the YES runs the reader from the exported tree
in scratch, no network, and a tampered schema pin makes it refuse); the name is allowed by a SUCCESSOR registration rule
record from slot 284 (VIS-284), and `architecture/chain-product-packets/rule.json`,
`scripts/chain_identity_v2.py` and `scripts/chain_identity_v3.py` are byte-equal, which the YES reads from the PR's changed
paths (none of the three among them; the lab holds their 4b2be353 digests 5e6e6821, 23fe723a and 29483ec3 and no
e515f0b8 export); the successor FUNCTION (VIS-284-CR1, C1-3) is present as a new changed path beside the record, binds v2
by V2_SHA256 and reads the slot split from the record, the record's extends block names the function's digest (the YES
reads the function's sha256 from the PR and finds it in the record), and the function admits mas-harness-research-lab
only from slot 284 (a slot below 284 refuses the name; the lab reads this from the function's text and its vectors as R00
states them): item C5's in-place edit of rule.json is not expected and the product's `repository` line is no longer
checked against rule.json's allowed names; the route clause names the base cc92594d6daa and the name-status form (A for
the 53 paths and M for the 8 paths of the Tree and Bridge-changes contracts; the bridge-changes list at B' shows the same
rows), and that base equals R13 main at the YES (a later push through the monitor would have re-keyed the packet); this
PR's review record v2 and its YES brief are among the deliverables; the runner pin equals harness-onion main e515f0b8's
runner c8ac40f0 as the monitor named it (byte-checked by the monitor at the merged tree); rerun_table.json's schema is
the Evaluator contract's (level on every entry, externalInputs on RECORDED entries, PREREG by the ledger's digest) with
the counts of the evidence line; the 284 row reads MET-REGISTRY-001 with LAB-REPO-001 as its one product at K = 1, with
the counts R00 states; the 284 meta YAML `task-packets/MET-REGISTRY-001.yaml` names LAB-REPO-001 as its one product
at K = 1 by the frozen digest, its authority's productPackets block registers it, its allowedPaths equal the PR's changed
paths and its counts read 295 packets at slot 284 (F10, at c2); the built YAML's sha256 is the one the v7 route keys
(frozen before v7's c2). At the final head c8 a641e7bb (draft 6.6, MON-LAB-284-FINAL) the F inputs read: unchanged since
c2, `task-packets/LAB-REPO-001.yaml` 8ae5c7fd, the plan bc19f6a5, the successor registry record 9c129674 with its schema
b2d07238 and the placement schema 26c4e874; changed since c2, `task-packets/MET-REGISTRY-001.yaml` 455cd736 (final prose,
300 allowedPaths), the successor rule record 4405e9da whose extends names the function e8635f23, the function
`scripts/repository_registration.py` e8635f23 (the clause parameter), the placement record 17fc67ef (its second source's
display lines 1604) and the authority b47b2309; byte-equal and absent from the changed paths as before, the eleven files
of F13 and the runner c8ac40f0.
