# LAB-REPO-001: R13's first task packet, drafted by the Research-Lab (draft 4, 2026-11-07; paper only)

Draft 4 (MON-RL-RUNNER): the runner pin is filled with 283's c1-frozen ci/run_packet_argv.py as relayed by the monitor
(sha256 c8ac40f0, 9084 B), provisional until 283's c2 (two reader probes may reopen c1; a new digest would be a new
named delta); the YAML's final freeze comes before v7's c2, after 283 merges. Draft 3 was sha256 4d738aa9.
Draft 3 (MON-RL-R13-284, the owner's change of plan): R13 moves to slot 284 at K = 1 under bundle v7; the YAML
freezes before v7's c2 and changes only by a named delta; ci/run_packet_argv.py pins to 283's fixed runner (digest
pending from the monitor). Draft 2 was sha256 d38c1324. Draft 2 folds the monitor's answers MON-RL-R13-ANSWERS (Q-LAB-1, 2, 4, 5) and the visionary's rulings MON-RL-R13-RULED
(Q-LAB-3; the owner's LICENSE-only first commit) and logs the RL-11 correction; draft 1 was sha256 b7f6421d.

Scope: the owner's word via the monitor, MON-RL-R13-PACKET ("Unpause for R13's packet only"). The lab drafts; R00
builds the packet at slot 284 (K = 1) under bundle v7 (the owner's word, MON-RL-R13-284; 283 stays at K = 3); the lab
says YES before 284's c2; the YAML freezes before v7's c2 and changes only by a named delta. Everything else stays paused: no experiment, search, fetch, heavy run or commit.

Rulings this draft fits (the monitor's 283 design note, 2026-11-07): Q-283-1 as changed by the owner on 2026-11-07,
R13 at 284 at K = 1 (superseding the gated ride at 283); Q-283-5 (a) the hosted route for R13 in bundle v7: python-distribution profile
without the helm and cosign pins, no network, a standard-library workflow, a self-retiring first-packet route that
checks a PREREG plus its review record and the research/MANIFEST.json digest rule. Readiness's four needs: R13 in
`$defs.repositoryId`; EXPECTED_REPOSITORIES at 14; a docs/repositories plan whose fenced-tree roots equal the packet's
authorized roots; `repository` naming R13.

Inputs, by digest: `research/reads/REPO-MIGRATION-PLAN.md` draft 2 cf48e682; the charter `research/README.md`
207cb431; the register f3d883f4; `handoff/SESSIONS.md` row Research-Lab and transition T12 (the packet id
LAB-REPO-001); the platform repository at main 4b2be353 through a git-archive export (tar sha256 b0aadaf9): the packet
schema, `scripts/validate_readiness.py` (the roots check at the docs/repositories plans, EXPECTED_REPOSITORIES,
EXPECTED_PACKET_COUNT), `architecture/chain-product-packets/rule.json`, `ci/run_packet_argv.py` (the argv rules),
`task-packets/CTRL-TRANSPORT-001.yaml` and `DIST-TRANSPORT-001.yaml` (the first-packet form). Bridge HEAD at the
draft: ca2bfac7.

## A. The packet (`task-packets/LAB-REPO-001.yaml` in the platform repository; R00 writes the file)

```yaml
id: LAB-REPO-001
repository: mas-harness-research-lab
branch: codex/lab-repo-001-repository-bootstrap
objective: "The first commit of R13 mas-harness-research-lab: the bridge's research tree moved byte for byte with a manifest that keeps every published digest checkable, the shared offline transport, a standard-library acceptance set (manifest, preregistration and review records, evaluator re-derivation, privacy, page build, zero-bill), and no hosted workflow; research records only, no product code and no packets."
predecessors: []
allowedPaths: ["README.md", "LICENSE", "ci/verify-offline.sh", "ci/warm-source-isolation.sh", "ci/network_canary.py", "ci/run_packet_argv.py", "ci/zero_bill_scan.py", "research/"]
warmSourceAccess: PROHIBITED_DURING_IMPLEMENTATION
sourceReuse: []
contracts:
  - >-
    Tree: the first commit of mas-harness-research-lab. Under research/ it is the bridge's research/** at the monitor's
    checkpoint commit B (the last bridge copy before the move; B is recorded as bridgeCommit in research/MANIFEST.json),
    byte for byte and path for path, plus the lab tools this packet names under research/tools/ and the manifest
    itself; outside research/ only README.md and the five ci/ files. Main before this PR holds exactly one owner-made
    commit with one file, LICENSE (Apache License 2.0, byte for byte; MON-RL-R13-RULED); the PR leaves it unchanged
    and lists it in the manifest by sha256. No other path. No history rewriting: the bridge's git history of research/** stays on the bridge; the repository
    starts at this commit with the manifest as the bridge-to-repository link.
  - >-
    Transport: ci/verify-offline.sh, ci/warm-source-isolation.sh and ci/network_canary.py are byte-identical to
    harness-onion main 4b2be353 in sha256, size and git mode (unchanged since 64e5700d; the pins CTRL-TRANSPORT-001
    and DIST-TRANSPORT-001 cite at 57bb1033): ci/verify-offline.sh sha256
    778cb0faf59786dc31559e5d96a399d1e3bb26a4576e0ee9ff70e1f6546bd114, 3908 B, 100755; ci/warm-source-isolation.sh
    sha256 f717f62fb1c9fdaec9eb594c733f25b17394bae6b90a311b9ccc08d4eaf9233b, 4674 B, 100644; ci/network_canary.py
    sha256 1be4a837c4a5baee900db20007c4841361b8c823a1b5e521badcf28890d82099, 1459 B, 100755. ci/run_packet_argv.py is
    byte-identical to 283's fixed runner (MET-VERIFY-007's F head; the visionary's ruling, MON-RL-R13-284): sha256
    c8ac40f0b85f327b75748cde7c8498a02fdf48c004dbf3259660b92cc289646f, 9084 B, 100755 (283's c1 freeze, as relayed by
    the monitor, MON-RL-RUNNER; provisional until 283's c2); never c2ed0852 (the 4b2be353 runner). If 283's c1 changes any other transport file, its pin follows by the same
    named delta. No file under .github/,
    ever (the zero-bill rule; the owner's verifier refuses hosted workflows). ci/zero_bill_scan.py is the lab's own,
    standard library only: it walks the head, refuses WORKFLOW_PRESENT:<path> for any file under .github/,
    SYMLINK:<path> for any symbolic link, BYTECODE:<path> for any __pycache__ or .pyc entry, and HOSTED_RUNNER:<path>
    for the tokens runs-on, actions/ and uses: in any text file outside research/; exit 0 and no output when clean.
  - >-
    Manifest digest rule: research/MANIFEST.json is {"schemaVersion": "planeon.research.manifest/v1", "bridgeCommit":
    <40 hex>, "files": {<path>: <64 hex sha256>}} with sorted keys, paths relative to the repository root, one entry
    for every tracked file of the head except research/MANIFEST.json itself. research/tools/manifest_check.py walks the
    head (skipping .git), and refuses a path on one side only, a digest mismatch, a symbolic link, a bytecode entry or
    a bridgeCommit that is not 40 hex; it prints counts only. The move changes no file's bytes, so every digest already
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
    Evaluator re-derivation: research/tools/rerun_results.py reads research/tools/rerun_table.json, which names every
    RL folder exactly once as RE-DERIVED (the evaluator argv over the committed inputs and the committed RESULTS.json
    path) or RECORDED (a one-line reason: the verdict was computed over masked exports kept outside the repository, or
    the ledger predates the evaluator rule). For RE-DERIVED entries the driver runs the evaluator with the committed
    inputs, writes under TMPDIR only, and requires byte equality with the committed ledger. RL-14 to RL-22 are
    RE-DERIVED at the first commit. A folder missing from the table, a duplicate, or a RECORDED entry without a reason
    fails.
  - >-
    Privacy: research/tools/privacy_check.py scans the manifest's file set plus README.md, LICENSE and ci/: it refuses
    absolute home-directory path shapes (the macOS and Linux user folders and the session temp folders), e-mail
    shapes and the legacy term by its
    published sha256 rule (BR-D1); NAME_TOKEN_SHA256 = {} with a loader for an unpublished digest file named by
    RESEARCH_NAME_DIGESTS (absent under the verifier, so the table stays empty; the lab's local pre-push scan sets it).
    Counts only; exit 1 on any hit.
  - >-
    Page build: research/build_research.py runs from the repository root; the bridge lane file is optional (absent:
    lane status "ON THE BRIDGE", no resume block); --check regenerates the data record in memory, drops generatedAt and
    lane, compares it with the committed research/research.json minus the same keys, writes nothing and exits 1 on any
    difference; the page's links into experiments/, reads/, progress/ and tools/ are repository-relative. The bridge
    mirror copy drops the tree links: no repository URL goes in a bridge file (Q-LAB-4, ruled).
  - >-
    Standard-library workflow: every acceptance command is python3 -I -B over files of the head; no third-party
    import, no uv, make, pip or node, no network, writes only under TMPDIR; the six commands finish in seconds on the
    python-distribution profile without the helm and cosign pins (Q-283-5 (a)); the profile's pinned CPython 3.12.14.
  - >-
    Route: the self-retiring first-packet route of bundle v7, keyed by (LAB-REPO-001, this YAML's sha256) with the
    exact file set equal to the head's name-status against main's pre-PR tree, which the route checks is exactly
    LICENSE (the owner's initial commit): LICENSE unchanged, every other path A, the set equal to the manifest's keys
    plus research/MANIFEST.json; single use bound to the first PR number, retired at that PR's merge.
    Later LAB packets are verified under the ordinary hosted route, inheriting this packet's six commands in order.
  - >-
    Verifiable only under bundle v7 (an owner install step, not a predecessor), which adds mas-harness-research-lab to
    the verifier's fixed repository list (the installed v6 refuses any product outside its twelve) and this packet's
    route keyed by the frozen YAML's sha256. The packet is a product at slot 284, K = 1 (the owner, MON-RL-R13-284);
    its YAML freezes before v7's c2, and any later change is a named delta with a new digest that re-keys the route.
    R13 holds research records only: no product code, no packets, no roadmap writes.
deliverables:
  - "Under research/: the bridge tree at B, byte for byte, with research/MANIFEST.json (the generator research/tools/make_manifest.py runs once at the first commit and is committed)."
  - "research/tools/manifest_check.py, prereg_check.py, rerun_results.py with rerun_table.json, privacy_check.py; research/build_research.py with the optional lane file, repository-relative links and --check; ci/zero_bill_scan.py."
  - "The four exact transport copies (sha256, size and mode as pinned); no .github entry."
  - "README.md at the root: what the repository is, the procedure (charter section 1a), the PR flow (one PR per unit of work, PREREG and its review record first), the issue triage rule (FIX / DECLINE / ROUTE within the next lab turn), and that the bridge's page is a mirror. LICENSE: the owner's initial commit (Apache License 2.0), unchanged and listed in the manifest."
  - "research/reads/LAB-REPO-001-YES.md (the lab's YES record, section F) and research/reviews/LAB-REPO-001-yes-r1.json (its review record v2 naming that brief by path and sha256)."
excluded:
  - "Any experiment run, fetch, search, export or heavy job; network; .github; node, uv, make or pip; any bridge path; the lane file; any other repository; history rewriting; product code; packets; roadmap writes."
prefetchCommands: []
offlineAcceptanceCommands: [["python3","-I","-B","ci/zero_bill_scan.py"],["python3","-I","-B","research/tools/manifest_check.py","research/MANIFEST.json"],["python3","-I","-B","research/tools/privacy_check.py","research/MANIFEST.json"],["python3","-I","-B","research/tools/prereg_check.py","research/hypotheses/REGISTER.md","research/experiments"],["python3","-I","-B","research/tools/rerun_results.py","research/tools/rerun_table.json"],["python3","-I","-B","research/build_research.py","--check"]]
offlineExecution: {"wrapperArgv":["./ci/verify-offline.sh"],"packetPathEnvironment":"HARNESS_TASK_PACKET","packetPathMode":"HASH_PINNED_READ_ONCE_NO_CHILD_PATH","commandTransport":"ARGV_ARRAY_V1","isolation":"OS_ENFORCED_DENY_ALL_OUTBOUND","sessionScope":"SINGLE_PROCESS_TREE","prefetchOutsideSession":false,"offlineEnvironment":{"UV_OFFLINE":"1","UV_FROZEN":"1","UV_NO_SYNC":"1"}}
expectedEvidence:
  - "Name-status of the head against main's LICENSE-only tree: LICENSE unchanged, every other path A; the set equals research/MANIFEST.json's keys plus the manifest itself; manifest_check PASS with the file count of the checkpoint commit (227 under research/ at bridge ca2bfac7, plus the packet's files) and 0 mismatches."
  - "Three transport files equal harness-onion main 4b2be353 and ci/run_packet_argv.py equals 283's fixed runner, by sha256, size and mode; no .github entry; zero_bill_scan PASS."
  - "prereg_check PASS: 22 experiment folders; every frozen digest of the register present in its folder; PREREG-REVIEW.md present for RL-14 to RL-22 (9 of 22)."
  - "rerun_results PASS: 22 table entries; RL-14 to RL-22 re-derived byte for byte; RL-01 to RL-13 RECORDED with reasons."
  - "privacy_check 0 hits over the head; the lab's local pre-push scan over the same set with the unpublished digest file 0 hits, reported in the PR body as counts."
  - "build_research.py --check PASS; the six commands pass in one deny-all process tree under ./ci/verify-offline.sh in seconds; no heavy job."
rollback: Revert the PR; main returns to the owner's LICENSE-only commit and the bridge stays the authoritative research tree until the mirror form is adopted, so nothing is lost.
```

Checks on the YAML against the published rules: `id` matches the schema's id pattern and rule.json's productId
(file stem = id); `branch` starts with codex/lab-repo-001; `repository` is one plain inline line (R12: safe_load reads
the same value); every `offlineAcceptanceCommands` argv avoids the forbidden tokens (curl, wget, npx, prefetch,
fetch, download, install, sync, add, pull), no shell executable, no uv; `offlineExecution` equals the runner's
EXPECTED_EXECUTION; `prefetchCommands` is []; `expectedEvidence` carries no legacy result token; no allowed path is
absolute, escapes, or is `.`, `*`, `**` or `/`; the authorized roots are {LICENSE, README.md, ci, research}.

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

1. `LAB-REPO-001-repository-bootstrap`: the first commit: the bridge's research tree byte for byte with
   `research/MANIFEST.json` (every path and sha256 plus the bridge commit), the exact harness-onion transport copies
   (the runner at 283's fixed form), a standard-library zero-bill scan, the lab's acceptance tools (manifest, preregistration and review records,
   evaluator re-derivation, privacy, page build) and the root README over the owner's LICENSE-only initial commit;
   verifiable only once bundle v7 is installed, through its self-retiring first-packet route.

## Testing, verification, and acceptance

`LAB-REPO-001` declares `prefetchCommands: []` and ordered `offlineAcceptanceCommands` of six `python3 -I -B` argv
arrays: the zero-bill scan, the manifest check, the privacy check, the preregistration-and-review check, the evaluator
re-derivation and the page build check. The executor supplies the hash-pinned packet through `HARNESS_TASK_PACKET` and
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

Roots of the fenced tree: LICENSE, README.md, ci, research = the packet's authorized roots.

## C. Readiness edits that ride with the packet at 284 (R00's, listed so the lab's YES can check them)

1. `schemas/repositories.schema.json` `$defs.repositoryId`: add `research-lab` (14 names).
2. `architecture/repositories.yaml`: entry `{id: research-lab, name: mas-harness-research-lab, kind: meta, dependsOn: []}`;
   no graph edge (nothing consumes or provides at build time). `docs/adr/0001-repository-boundaries.md`: the R13
   boundary line (research records only; no other session writes there; the lab reads through exports).
3. `scripts/validate_readiness.py` EXPECTED_REPOSITORIES (+ mas-harness-research-lab, 14), the repository-plan count
   13 -> 14 and its message, EXPECTED_PACKET_COUNT from 283's count (293 at K = 3) to 284's (295: 284's meta packet +
   LAB-REPO-001; R00 states the counts); `scripts/validate_reuse.py`
   EXPECTED_REPOSITORIES; `scripts/validate_architecture.py` map (+ research-lab).
4. `docs/repositories/13-mas-harness-research-lab.md` as in section B (the title line exact; the fenced tree under
   "## Repository structure"; the "## PR packets" section declares LAB-REPO-001 once).
5. `architecture/chain-product-packets/rule.json` `productRepository.allowedNames`: the record revision moves from
   dd000fef (12 names) to the 284 head's repositories.yaml (13 product names) with its sha256; the vectors that
   enumerate the allowed names follow. Without this the v2 live identity test refuses LAB-REPO-001 under R8 clause 2
   (a `repository` outside the twelve names), and so does the verifier's part 2.
6. `task-packets/README.md`: the 284 row names LAB-REPO-001 as its one product; the counts read 295 packets at slot
   284 (R00's count).
7. The session map, lanes.json and issue tracking entries are the monitor's; the verifier's R13 policy row is bundle
   v7 (the owner's install).

## D. The lab's work before the first commit (on the monitor's word; not under the pause)

- Write the five tools and the manifest generator named in section A; the build_research.py changes (optional lane
  file, repository-relative links, --check); README.md; LICENSE per Q-LAB-1; run the six commands locally under the
  transport before the PR.
- RL-11 correction, done 2026-11-07 (MON-RL-R13-ANSWERS; a lab-internal record correction): the run version was v1.1
  (v1 plus the section-4 amendment, sha256 b06eabdb7d878795c268239c48541c8cf08dba156ebec3ba426d064e7c9c36d6, the
  ledger's scopeDigest and E6); after the run the MON-RL-M19 correction was appended in place as section 5, so
  PREREG.md read 7c6b64fc against the registered b06eabdb. Restored: PREREG.v1.md = 89d6ee61 (the original, from
  bridge commit 87bab8f7), PREREG.v1.1.md = b06eabdb (the run version, the current text cut before section 5; digest
  verified), PREREG.md = v1.2 7c6b64fc kept as the post-run amendment; the register row names all three. The rule in
  section A (every row digest present as a PREREG*.md) holds for 22 of 22 folders; RL-02 holds PREREG.v1.md bbb53d0b
  and PREREG.v2.md 1a927051 as its row names.
- rerun_table.json: RL-14..RL-22 RE-DERIVED (the evaluators take RUNS_JSON PREREG_MD RUN_RECORD_MD OUT_PATH; inputs
  under data/ and runs/ are in the tree); RL-01..RL-13 RECORDED with the reason per folder (masked exports kept outside
  the repository, or a ledger written before the evaluator rule).

## E. Questions for the monitor, each with the lab's recommended answer (owner delegation of 2026-10-22)

- Q-LAB-1 LICENSE: ANSWERED (owner): Apache License 2.0.
- Q-LAB-2 the created repository's initial state: RULED: the repository was created empty; the owner makes the first
  commit on main holding LICENSE only (Apache-2.0, byte for byte); the lab's PR lists it in the manifest; the route
  checks main's pre-PR tree is exactly that file.
- Q-LAB-3 "review record v2": RULED (visionary): harness-onion's review-record v2 schema, one record per PR,
  reviewer identity as strings, the brief digest; PREREG-REVIEW.md is the brief, named by path and sha256; two files per
  review from the first PR. Folded into section A (the preregistration-and-review contract and the deliverables).
- Q-LAB-4 the bridge mirror's page links: ANSWERED: dropped; no repository URL goes in a bridge file.
- Q-LAB-5 the profile's interpreter: ANSWERED: the pinned CPython 3.12.14.
- Runner pin: RECEIVED (MON-RL-RUNNER): sha256 c8ac40f0b85f327b75748cde7c8498a02fdf48c004dbf3259660b92cc289646f,
  9084 B, 100755, filled into section A; provisional until 283's c2 (if a reader probe reopens c1, the new digest is a
  new named delta). The YAML's final freeze comes before v7's c2, after 283 merges.

## F. The lab's YES before 284's c2 (what it checks on R00's built packet)

The YAML equals section A (draft 2; Q-LAB-1..5 are folded in); the plan's fenced-tree roots equal the YAML's
authorized roots; items C1-C6 present; the route clause names main's pre-PR tree as LICENSE only; this PR's review
record v2 and its YES brief are among the deliverables; the runner pin equals the 283 F runner digest the monitor
sent; the 284 row reads K = 1 with the counts R00 states; the product's `repository` line is among rule.json's
allowed names at the 284 head; the built YAML's sha256 is the one the v7 route keys (frozen before v7's c2).
