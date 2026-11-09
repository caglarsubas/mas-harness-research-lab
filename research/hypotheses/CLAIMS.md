# Claims table (generated from CLAIMS.json by research/tools/claims_check.py --render; do not edit by hand)

One row per claim of every verdict ledger (RESULTS.json) in research/experiments, added 2026-11-07 for R13 issue 1 (recommendation 1). The ledgers are the record; this table separates, for each claim, the protocol verdict (copied), the instrument's validity, the scope the verdict supports, the clauses it leaves open, the evidence type and the replication state, and names the decision the verdict justifies. Invalid test cases are recorded beside the historical verdict, never by changing it. RECORDED means the ledger was computed over inputs kept outside the repository or before the evaluator rule; LEDGER_REDERIVED means the committed evaluator reproduces the committed ledger byte for byte from committed inputs (RL-14 to RL-22; also reproduced by the R13 issue 1 reviewer); no claim has a raw-output reproduction or an independent replication yet. Checked by research/tools/claims_check.py, which also renders CLAIMS.md.

Columns: the ledger's claim and verdict (copied, never changed); what was operationally measured; whether the
instrument could answer the clause (VALID, VALID_WITH_LIMITS, UNDERPOWERED, INVALID, NONE, DESCRIPTIVE); the
scope the verdict supports; the clauses it leaves open; evidence type (simulation, documentary, empirical,
formal) and method; replication state (RECORDED, LEDGER_REDERIVED, RAW_REPRODUCED, INDEPENDENT_REPLICATION);
invalid cases recorded beside the verdict; the decision the verdict justifies.

Rows: 46 claims over 23 experiments; verdicts CONTRADICTED 8, NEW_VALUE_ESTABLISHED 1, SUPPORTED 23, UNRESOLVED 14; replication LEDGER_REDERIVED 19, RECORDED 27.

## RL-01 (RL-01-RESULTS-v2, ledger status PASS, H-07)

### H-07a: SUPPORTED

- Tested clause: H-07a: verify-time growth since slot 255 is explained by host load and the outer suite's test count, not by layer count
- Measured: PASS by the preregistered gate with one unresolved check (C4) and one finding (C5)
- Operational definition: OLS of verify wall time on run-mean host load, outer-suite test count and layer count over 23 of 27 verify runs (slots 253-278); gate: load's interval excludes zero in both fits, layer count's includes zero
- Instrument: VALID_WITH_LIMITS. valid for the load clause; test count and layer count are collinear (r 0.98), so the instrument cannot separate them (C4); 23 rows and 3 predictors is a sign test
- Supported scope: host load is a verify-time driver on its own (about 50 s per one-SD rise), K 6 era, one host
- Unresolved clauses: 'test count rather than layer count'; cap events (the capped run left the fit); per-worker balance (ledger checks C4)
- Evidence: empirical; observational regression over published check-run summaries joined to merge-decision records
- Replication: RECORDED
- Decision justified: treat load as a cost driver (the quiet-host verify floor); claim nothing about the per-layer cost

### H-07b: UNRESOLVED

- Tested clause: H-07b: worker wall time at K 8 is non-inferior to K 6 on this host
- Measured: below 3 runs per arm and the K 8 run non-comparable; the direction (K 8 faster in wall, costlier in summed time) is recorded descriptively
- Operational definition: worker wall time K 8 against K 6 from relayed figures: one K 8 run, two K 6 runs
- Instrument: INVALID. below three runs per arm and the K 8 run non-comparable (failed pins); figures relayed, not measured by the lab
- Supported scope: none; direction recorded descriptively (wall -10.2 percent, summed +18.2 percent)
- Unresolved clauses: the non-inferiority clause (ledger checks C6)
- Evidence: empirical; relayed verify figures, descriptive
- Replication: RECORDED
- Decision justified: none from this claim; the K 8 adoption rests on the owner's measurement at 279, recorded in the roadmap

## RL-02 (RL-02-RESULTS-v2, ledger status UNRESOLVED, H-09)

### H-09a: UNRESOLVED

- Tested clause: H-09a: review rounds and the independent oracle find different findings
- Measured: UNRESOLVED-by-input
- Operational definition: oracle findings against review-round findings per packet
- Instrument: NONE. no oracle verdict exists in any record the monitor can export, so there is no instrument
- Supported scope: none
- Unresolved clauses: the whole clause (UNRESOLVED-by-input) (ledger checks C1)
- Evidence: empirical; review records at count and finding level
- Replication: RECORDED
- Decision justified: input: DECISION-LEDGER-001's oracle block (RL-02-PROPOSAL part 2, disposed at lock 29); re-run when it lands

### H-09b: UNRESOLVED

- Tested clause: H-09b: the verifier refuses a measurable fraction of PASS_FOR_PUSH heads
- Measured: below the head bound
- Operational definition: fraction of matched PASS_FOR_PUSH heads the verifier refused; bound 40 heads
- Instrument: UNDERPOWERED. valid measure on 9 heads: 1 refused (0.11, Wilson 0.02 to 0.44), below the preregistered head count
- Supported scope: a descriptive rate on 9 heads
- Unresolved clauses: the measurable-fraction clause until 40 matched heads exist (ledger checks C2)
- Evidence: empirical; verifier refusals after PASS_FOR_PUSH joined by head
- Replication: RECORDED
- Decision justified: none yet; re-run at 40 heads

### H-09c: UNRESOLVED

- Tested clause: H-09c: carried findings re-raised in later rounds, descriptive fraction
- Measured: measure vacuous under the id scheme (C5)
- Operational definition: re-raise fraction of carried findings across rounds under the identity (packet, series, finding id)
- Instrument: INVALID. the identity embeds the raising round (381 of 381 lane-token ids), so no cross-round identity exists (C5); 0 of 57 is vacuous
- Supported scope: none
- Unresolved clauses: the whole clause (ledger checks C5)
- Evidence: empirical; finding-level review records (397 findings, 25 series)
- Replication: RECORDED
- Decision justified: stable finding identity: a clause of REVIEW-RECORD-SERIES-001's packet (RL-02-PROPOSAL part 1, disposed at lock 29)

### H-09d: UNRESOLVED

- Tested clause: H-09d: findings raised in round 2 or later are new identities in at least half the cases
- Measured: gate met vacuously; the identity rule encodes the round (C5), so the claim is not established
- Operational definition: share of round-2-or-later findings that are new identities; bound one half
- Instrument: INVALID. gate met vacuously (227 of 227) for the same reason as H-09c (C5): the id scheme makes every finding new
- Supported scope: none
- Unresolved clauses: the whole clause (ledger checks C5)
- Evidence: empirical; finding-level review records
- Replication: RECORDED
- Decision justified: as H-09c; the series packet's identity clause

### H-09-descriptive: NEW_VALUE_ESTABLISHED

- Tested clause: descriptive finding table, not gated
- Measured: later rounds raise MINOR and NOTE findings, MAJOR only in rounds 1-2; MAJOR findings are addressed least often (0.68)
- Operational definition: severity by round and addressed rate by severity over 397 findings
- Instrument: DESCRIPTIVE. descriptive table, no gate
- Supported scope: later rounds raise MINOR and NOTE findings, MAJOR only in rounds 1-2; MAJOR findings are addressed least often (0.68)
- Unresolved clauses: none (descriptive) (ledger checks none)
- Evidence: empirical; finding-level review records
- Replication: RECORDED
- Decision justified: informs the series design: severity and disposition fields, round of first detection

## RL-03 (RL-03-RESULTS-v1, ledger status PASS, H-19)

### H-19a: SUPPORTED

- Tested clause: H-19a: the four breach class rows recomputed from the pinned export equal the committed rows
- Measured: the export at b4bbea79 reproduces the breach rows exactly
- Operational definition: the four duplicated-work class rows (C2, C5, C7, C9) recomputed over the committed 32 seeds equal the committed ledger rows
- Instrument: VALID. deterministic recomputation through the harness's own ledger module; compared key by key
- Supported scope: the committed breach rows reproduce exactly on the pinned export, one host
- Unresolved clauses: nothing about the other nine classes or larger agent counts (ledger checks none)
- Evidence: simulation; git-archive export at b4bbea79 driven in memory; 5 s
- Replication: RECORDED
- Decision justified: the campaign ledger is trustworthy as an input to later simulation work (RL-04, RL-17, RL-18)

### H-19b: SUPPORTED

- Tested clause: H-19b: the arms section recomputed equals the committed arms results
- Measured: the arms reproduce exactly
- Operational definition: the arms section (three claim policies over five classes) recomputed equals the committed arms results
- Instrument: VALID. deterministic recomputation; 15 arm pairs equal
- Supported scope: the arms results reproduce; the shape of the fix space is as recorded (A3 removes C2, A1 removes C7, A2 worsens every class, C5 stays above p95)
- Unresolved clauses: no independent implementation; one host (ledger checks none)
- Evidence: simulation; export at b4bbea79; 3 s
- Replication: RECORDED
- Decision justified: admissible as a baseline for the arms successor (R13 issue 1, rec 5)

### H-19c: SUPPORTED

- Tested clause: H-19c: the recomputed rows fail only the duplicatedWorkRatioPpm bound
- Measured: the breach is duplicated work only, as the ledger states
- Operational definition: the recomputed rows fail only the duplicatedWorkRatioPpm bound
- Instrument: VALID. bound-by-bound comparison of the recomputed rows
- Supported scope: the breach is the duplicated-work bound alone on the pinned export
- Unresolved clauses: leased versus advisory (RL-04's question) (ledger checks none)
- Evidence: simulation; export at b4bbea79
- Replication: RECORDED
- Decision justified: the duplicated-work bound is the one to study under topology and contention

## RL-04 (RL-04-RESULTS-v1, ledger status UNRESOLVED, H-13, H-19)

### H-13a: UNRESOLVED

- Tested clause: H-13a: speedup and efficiency change sign between decomposable and sequential tasks
- Measured: UNRESOLVED-by-input
- Operational definition: sign change of speedup and efficiency between decomposable and sequential task families
- Instrument: NONE. the harness holds one decomposable task family; no sequential family exists to compare (C1)
- Supported scope: none
- Unresolved clauses: the whole clause (UNRESOLVED-by-input; the sequential family is R12's) (ledger checks C1)
- Evidence: simulation; export at b4bbea79
- Replication: RECORDED
- Decision justified: input request; no topology recommendation rests on this clause

### H-13b: SUPPORTED

- Tested clause: H-13b: leased claims reduce duplicated work relative to advisory claims at N >= 2, seed for seed
- Measured: PASS by gate; the effect is the DECENTRALIZED family's (mean +415,741 ppm) and absent in CENTRAL (mean -3,166 ppm, interval includes zero)
- Operational definition: duplicated-work ratio, leased minus advisory, paired by seed at each of ten scaling points (two topologies x 1-16 workers, 5 items per worker, 32 seeds); gate: median paired difference non-negative at every N >= 2 and pooled interval above zero
- Instrument: VALID_WITH_LIMITS. the advisory arm bypasses two checks (HELD, VERSION), not a designed advisory protocol; one task family; fixed items per worker, not fixed total work
- Supported scope: leased claims reduce duplicated work, and the whole effect is the decentralized topology's (advisory duplicates 23 to 63 percent there); central shows no difference and pays about 30 percent makespan for leases
- Unresolved clauses: generalisation beyond one task family, one harness, one host; failover and stale coordinators (not covered) (ledger checks C8)
- Evidence: simulation; 640 simulation runs, seed-paired; 8 s
- Replication: RECORDED
- Decision justified: the dated note on MAS-STRATEGY-001 (leases required where claims are peer-to-peer, optional under one coordinator), ruled at lock 29 as not gate material; the successor design (rec 5) is the admission-grade test

### H-19-second: SUPPORTED

- Tested clause: H-19 second clause: the breaches vanish under leased exclusivity at larger agent counts (tested as: lower than advisory)
- Measured: lower than advisory; the register's word 'vanish' is contradicted and recorded as a finding
- Operational definition: breach rate under leasing lower than under advisory at larger counts (tested as 'lower than', not 'vanish')
- Instrument: VALID_WITH_LIMITS. the register wording 'vanish' is false by the same data: leased decentralized runs still duplicate 18 percent at N 16
- Supported scope: leasing lowers duplicated work in the decentralized family; it does not remove it
- Unresolved clauses: the 'vanish' wording (false) stays unresolved as a hypothesis statement (ledger checks none)
- Evidence: simulation; as H-13b
- Replication: RECORDED
- Decision justified: register wording of H-19 to be read as 'lower than advisory'

## RL-05 (RL-05-RESULTS-v1, ledger status FAIL, H-03)

### H-03: CONTRADICTED

- Tested clause: H-03: the merge predicate P = R and V and A and I and H and T holds for every merged packet (every merge-decision record with a merge commit)
- Measured: FAIL as stated; holds for every record decided on or after 2026-10-24 that can be evaluated
- Operational definition: P = R and V and A and I and H and T evaluated by an allowlist script over the 47 merge-decision records that name a merge commit (set digest b3370227)
- Instrument: VALID_WITH_LIMITS. independence of the records is not tested, only that the fields come from distinct producers; approval files' bytes unreadable to the lab (C5)
- Supported scope: six records of 2026-10-21/22 predate a mechanism their form lacks (check-run reference, transport approval); every record decided on or after 2026-10-24 satisfies P or is UNEVALUATED
- Unresolved clauses: independence in fact; the five earliest decisions without a merge commit; the approval files' bytes (ledger checks C5)
- Evidence: documentary; predicate check over published merge-decision records
- Replication: RECORDED
- Decision justified: record the early-form gap as a finding; no change to the merge predicate; a form-version field would make the gap explicit (DECISION-LEDGER-001)

## RL-06 (RL-06-RESULTS-v1, ledger status FAIL, H-10)

### H-10a: SUPPORTED

- Tested clause: H-10a: throughput and cost per packet are measurable from the handoff and merge-decision records
- Measured: measurable; 3.13 merges per day over 15 days, median verify 743 s per merge, median 2 review rounds
- Operational definition: coverage of date, verify time and review count over 47 merged records; throughput per day; medians
- Instrument: VALID_WITH_LIMITS. no token or wall cost per packet build exists in readable records; throughput mixes packets, errata and contract merges
- Supported scope: cadence is measurable from the programme's own records: 3.13 merges per day over 15 days, median verify 743 s, median 2 review rounds
- Unresolved clauses: cost per packet build in tokens or wall time (ledger checks none)
- Evidence: empirical; allowlist extraction over merge-decision records and check runs
- Replication: RECORDED
- Decision justified: use the records for cadence reporting; effort columns (rec 7) add what the records lack

### H-10b: CONTRADICTED

- Tested clause: H-10b: the incident-to-rule corpus forms a stable taxonomy (keyword categories over MON identifiers)
- Measured: the preregistered keyword taxonomy over identifiers fails (OTHER 0.70); the identifiers are not a taxonomy
- Operational definition: keyword categories fixed in PREREG v1 applied to the 111 rule identifiers; FAIL when OTHER exceeds 0.40
- Instrument: VALID_WITH_LIMITS. the rule subset (a line with the word 'rule') is coarse; the lab's prior exposure shaped the keyword lists (disclosed)
- Supported scope: the identifier-level keyword taxonomy is not stable (OTHER 0.70)
- Unresolved clauses: a text-level classification (the lab's own v2 follow-up) (ledger checks none)
- Evidence: empirical; keyword classification over 17 handoff files (1,012 identifiers)
- Replication: RECORDED
- Decision justified: do not build a taxonomy from identifiers; a text-level v2 is a new id

## RL-07 (RL-07-RESULTS-v1, ledger status PASS, H-01)

### P1: SUPPORTED

- Tested clause: H-01 P1: the history chain's accepted check set is monotone (R13 inheritance; the step rule)
- Measured: on the published vectors and the identity rule's recorded evidence; the live chain is not replayed here
- Operational definition: the three chain rules' 116 published vectors replayed through the pinned evaluator scripts; monotonicity read from the inheritance refusals (R13 clause)
- Instrument: VALID_WITH_LIMITS. the step rule over the live 66-layer chain and the 273-277 equivalence were not replayed (sources not in the export); the identity rule's recorded evidence stands in (C7)
- Supported scope: every refusal the rules promise is exercised by a vector and refuses with the promised clause
- Unresolved clauses: the live-chain step rule; the 273-277 equivalence (ledger checks C7)
- Evidence: documentary; vector replay of published chain rules at main afee03b9
- Replication: RECORDED
- Decision justified: the chain rules' vectors are complete for the refusals they promise; a live-chain replay needs the validators' sources

### P2: SUPPORTED

- Tested clause: H-01 P2: published bytes are immutable under projection
- Measured: on the published vectors
- Operational definition: published bytes immutable under projection: vectors for changed or re-identified published products refuse
- Instrument: VALID. the vectors fix the refusing clause for each case
- Supported scope: immutability under projection holds on the published vectors
- Unresolved clauses: none beyond the vectors' scope (ledger checks none)
- Evidence: documentary; vector replay
- Replication: RECORDED
- Decision justified: no action

### P3: SUPPORTED

- Tested clause: H-01 P3: a pinned-byte edit refuses at the oldest layer that pinned it
- Measured: refusal supported; the 'oldest layer' attribution unresolved (C6)
- Operational definition: a pinned-byte edit refuses; 'at the oldest layer that pinned it' read from the refusal detail
- Instrument: VALID_WITH_LIMITS. all 17 inheritance refusals carry clause R13 with a detail message, none names the refusing layer's slot (C6)
- Supported scope: 'refuses' is supported
- Unresolved clauses: 'at the oldest layer' (the vectors do not carry the layer) (ledger checks C6)
- Evidence: documentary; vector replay
- Replication: RECORDED
- Decision justified: input for the vectors' owner: vectors that carry the refusing layer (RL-07's small input through the monitor)

## RL-08 (RL-08-RESULTS-v1, ledger status UNRESOLVED, H-08)

### H-08a: UNRESOLVED

- Tested clause: H-08a: some inherited checks never refused anything and some refused real drift
- Measured: UNRESOLVED-by-input
- Operational definition: per-check refusal history: which inherited checks never refused and which refused real drift
- Instrument: NONE. the compaction cost report records cost, not refusals; no per-check refusal history exists in any readable record (C1)
- Supported scope: none
- Unresolved clauses: the whole clause (UNRESOLVED-by-input) (ledger checks C1)
- Evidence: documentary; published compaction cost report (M1's run)
- Replication: RECORDED
- Decision justified: input request: a per-check refusal history from the verifier's records

### H-08b: UNRESOLVED

- Tested clause: H-08b: the chain's cost per layer is concentrated in a small set of validators (top decile holds at least half)
- Measured: between the bounds: moderately concentrated (Gini about 0.5), not held by a small set; the one concentration that is sharp is at the argv level (argv 63), seen before the freeze and descriptive
- Operational definition: top-decile share and Gini of CPU per test file (141) and per layer (60) inside argv 63; bounds fixed before the run
- Instrument: VALID_WITH_LIMITS. pre-compaction run only; wall time not per layer; the A/B record's keys read, not its values
- Supported scope: cost inside the chain identity test is moderately spread (Gini about 0.5, top decile a third); the sharp concentration is one level up (argv 63 is 86 percent of the verify's CPU), reported not gated
- Unresolved clauses: post-compaction cost; refusal value per check (ledger checks C2)
- Evidence: documentary; descriptive concentration measures over a published cost report
- Replication: RECORDED
- Decision justified: PERF-045/046 cuts target argv 63 as a whole, not a small validator set

## RL-09 (RL-09-RESULTS-v1, ledger status FAIL, H-18)

### H-18: CONTRADICTED

- Tested clause: H-18: the union of seccomp rows, SELinux matrix rows, descriptor sets and T04 proofs covers every effect path the threat model names, with a finite residual list
- Measured: FAIL as preregistered on paths 18-28: the four record families do not reach the paths whose required mechanism is a gate rule; a v2 with the gate-channel and admission records as a fifth family is a new design
- Operational definition: join by citation and clause token of counterexamples 18-28 to the seccomp duties (v5), SELinux assertions (v4), descriptor amendments (HS53, HE5) and T04 rows; gate: every path covered or residual
- Instrument: VALID_WITH_LIMITS. a citing row may not enforce what is required (nothing semantic); two paths yield no token; path 27's coverage rests on a generic token
- Supported scope: the four kernel-level families do not cover four gate-rule paths (A3, C4, C6, cgroup directory search): the threat model's effect paths are not all kernel paths
- Unresolved clauses: paths 1-17 (not enumerated); semantics; older record versions (ledger checks C3, C4)
- Evidence: documentary; token join over published host-interface records at main afee03b9
- Replication: RECORDED
- Decision justified: the coverage claim needs the gate-channel family (RL-11); H-18 stays open

## RL-10 (RL-10-RESULTS-v1, ledger status FAIL, H-04)

### H-04: CONTRADICTED

- Tested clause: H-04: the verdict ledger's evidence rule and the host record's evidence classes compose into one evidence algebra (one five-level order, both maps total, both records' refusals agree with the order)
- Measured: FAIL as preregistered on clause 2 (C3); the per-claim reading (C5) shows the composition holding; a per-claim restatement is a new id
- Operational definition: one five-level evidence order fixed before the run; totality of both maps; agreement of the ledger's 112 vectors and the native profile's 444 negatives with the order; clause 2 of C2 stated per ledger
- Instrument: INVALID. clause 2 was per ledger while the ledger's rule is per claim (every vector holds two claims), so the clause was mis-scoped; a post-hoc per-claim reading (C5, not gated) shows composition holding
- Supported scope: the order and both totality checks; the FAIL is the record of the mis-scoped clause, not of the records
- Unresolved clauses: semantic equivalence of the two refusal procedures (never tested) (ledger checks C6)
- Evidence: documentary; vector agreement check over published records
- Replication: RECORDED
- Decision justified: RL-12 is the corrected statement; RL-10's ledger stands as the finding about clause scoping (R2 of the review step)

## RL-11 (RL-11-RESULTS-v1, ledger status UNRESOLVED, H-18)

### H-18-widened: UNRESOLVED

- Tested clause: H-18 widened: the union of the kernel-level records and the gate-channel contracts covers every effect path the threat model names, with a finite residual list
- Measured: no path uncovered; one path not joinable by token (24); 18-28 otherwise closed by join, with 28 documentary only and the open cells of MON-RL-M17 recorded
- Operational definition: RL-09's join plus the gate-channel family (1,541 vector rows, READMEs and authorities as text rows, R10's cited transcript ids); gate: every path of 18-28 covered or residual; UNRESOLVED when a path yields no token
- Instrument: VALID_WITH_LIMITS. nothing semantic; G counts for 18 and 27 come from generic tokens (weak); 28's coverage is a README sentence (documentary); 24 yields no token
- Supported scope: no enumerated path is uncovered: the four paths RL-09 could not cover are the four the gate-channel vectors do cover; the join agrees with the visionary's expected cells
- Unresolved clauses: path 24 (no join token); paths 1-17; evidence levels differ by path (see data/coverage_map.json) (ledger checks C3, C4, C5)
- Evidence: documentary; token join over the architecture export 948a20fa with the fifth family
- Replication: RECORDED
- Decision justified: the coverage map with evidence levels is the committed residual list; paths 1-17 and 24 are input requests to the threat model's owner

## RL-12 (RL-12-RESULTS-v1, ledger status PASS, H-04)

### H-04: SUPPORTED

- Tested clause: H-04: one five-level evidence order into which both vocabularies map totally, with each record's refusals agreeing with the order (ledger agreement per claim)
- Measured: the composition holds on the published vectors under the per-claim clause; RL-10's FAIL stands as the record of the mis-scoped clause
- Operational definition: RL-10's design with the ledger-agreement clause scoped per claim: in each weak-evidence vector the claim whose checks cite the weak item has no establishing deterministic PASS on the delivered target
- Instrument: VALID_WITH_LIMITS. agreement of vectors with one order, not a proof of the refusal procedures' equivalence; one aggregate seen before the freeze (disclosed in RL-10)
- Supported scope: the two evidence vocabularies compose into one five-level order without remainder; each record refuses where the order says support is too weak
- Unresolved clauses: semantic equivalence; the asymmetries (an out-of-scope native class, three native classes on one level, a not-confirmation level with no native counterpart) (ledger checks C4)
- Evidence: documentary; vector agreement check (restatement of RL-10 under a new id)
- Replication: RECORDED
- Decision justified: the shared order can be cited by the evidence-matrix design; RL-10 stays the record of the first statement

## RL-13 (RL-13-RESULTS-v1, ledger status PASS, H-22)

### H-22a: SUPPORTED

- Tested clause: H-22a: the verdict-ledger, run-manifest and run-event-log contracts can be emitted by another platform from their published schemas alone
- Measured: interchange from the schema text alone holds for the three contracts; the lab's checker has one unexplained refusal on a contract positive (C2)
- Operational definition: one minimal instance per contract written from each schema's required set and types, validated by the lab's standard-library checker; operation coverage of the OpenTelemetry mapping
- Instrument: VALID_WITH_LIMITS. emission only, by one reader; the lab's checker is not the contract's validator and refuses one contract positive it cannot explain (C2)
- Supported scope: the three contracts can be emitted from their schemas alone; four non-obvious points documented in MAPPING.md
- Unresolved clauses: consumption by another platform (never tested); the unexplained rejected positive (ledger checks C2)
- Evidence: documentary; schema instantiation at main afee03b9
- Replication: RECORDED
- Decision justified: MAPPING.md is the emitter's guide; the consumption test is the obligation-level successor (R13 issue 1, rec 3)

### H-22b: SUPPORTED

- Tested clause: H-22b: the multi-agent span and metric set is a coherent extension of the GenAI semantic conventions
- Measured: coherent on coverage and naming; the pinned conventions are unverified by the lab (C5)
- Operational definition: every dotted attribute name of the mapping classified against the GenAI semantic conventions as known by the lab
- Instrument: VALID_WITH_LIMITS. the pinned conventions were not verified by the lab (C5): names from the lab's knowledge, no fetch
- Supported scope: the span and metric set is a coherent extension as far as the lab's knowledge of the conventions goes
- Unresolved clauses: the pinned convention versions (ledger checks C5)
- Evidence: documentary; name classification
- Replication: RECORDED
- Decision justified: none until the conventions are fetched on the owner's word

## RL-14 (RL-14-RESULTS-v1, ledger status UNRESOLVED, H-28)

### H-28-obs: UNRESOLVED

- Tested clause: H-28 (observational half): typed resume blocks are followed by fewer dated MON lines per day
- Measured: n 23; rho 0.124; 95 percent clustered bootstrap [-0.413, 0.358] (1000 of 1,000 resamples defined); digests-only rho 0.117 (descriptive); tied X values 0, tied Y values 16; windows per cluster {"LANE-DESIGN-UX.md": 1, "LANE-PARALLEL.md": 10, "LANE-R00-HARNESS-ONION.md": 5, "LANE-R03.md": 3, "LANE-R04.md": 2, "LANE-R11.md": 2}; median rate above-median typedness 1.000 vs at-or-below 0.000 (n 11 / 12)
- Operational definition: Spearman rho between a resume block's pin density (digests and line pins per 100 words) and new monitor identifiers per day in the window it opens; 23 windows in 6 clusters; file-clustered bootstrap interval; MEI -0.30
- Instrument: VALID_WITH_LIMITS. the proxy counts every new monitor identifier addressed to the lane, not slips; windows are 1-2 days; no adjustment for lane activity or the reverse direction; PREREG v4 after three failed independent reviews
- Supported scope: nothing: rho +0.124 with interval [-0.413, +0.358] (the preregistered most-likely class); descriptive numbers point the other way
- Unresolved clauses: the slip clause (a text-level proxy is a new id on the monitor's permission); the harness half (state recovery, poisoned observation) is untouched and BLOCKED (ledger checks C2)
- Evidence: empirical; observational correlation over the programme's own lane files
- Replication: LEDGER_REDERIVED
- Decision justified: no change to the handoff form on this evidence; the controlled recovery design (rec 4) is the test that could

## RL-15 (RL-15-RESULTS-v1, ledger status FAIL, H-30)

### H-30: CONTRADICTED

- Tested clause: H-30: the roadmap build's validators refuse every seeded inconsistency class and no benign control edit
- Measured: attributed recall 10/18 (any refusal 14/18); false positives 0/3; precision 0.714; per class [attributed, refused, n] {"M1": [3, 3, 3], "M2": [3, 3, 3], "M3": [2, 3, 3], "M4": [0, 2, 3], "M5": [2, 3, 3], "M6": [0, 0, 3]}; baseline exit 0 in 0.81 s
- Operational definition: 18 seeded edits (six classes x three) and 3 benign controls on a scratch copy of the roadmap builder at a pinned digest; attributed refusal = a refusal naming the seeded edit; FAIL when any class has 0 of 3 attributed
- Instrument: VALID_WITH_LIMITS. three edits per class; one record; the validators and the record share an author; the digest class seeded on research-source digests only
- Supported scope: the validators cover the shape rules (dangling dependency, status against evidence, score drift, stale reference) and not the process rule (status change without an update entry) or the digest rule; 0 false alarms on 3 controls
- Unresolved clauses: validators the lab did not seed (ledger checks none)
- Evidence: empirical; seeded-mutation benchmark on a scratch copy; 22 builds, 7.7 s
- Replication: LEDGER_REDERIVED
- Decision justified: RL-15-PROPOSAL (two validators) ACCEPTED by the visionary (VIS-RL15, 2026-11-05), one reviewed builder change staged as its own lock before lock 40; the lab re-runs 18 + 3 on the patched builder on the monitor's word (expected 18 of 18, 0 of 3; RL15-D1); run-002 (2026-11-07, builder 690cff6a, frozen gate): refused 17 of 18, attributed 13 of 18, one control refused by the new date rule (FAIL region); both new validators catch what a file comparison can; RL-15b is the clean restatement

## RL-15b (RL-15b-RESULTS-v1, ledger status PASS, H-30 (restated))

### H-30b: SUPPORTED

- Tested clause: H-30 restated (RL-15b, ERRATUM to RL15-D1): on the lock-40 builder every catchable seeded inconsistency instance is refused, each refusal is attributed to a named rule (a new rule by its tag, or the older rule that runs first), the new rules refuse at least 2 of 3 M4 and both catchable M6 instances, and no benign control edit is refused
- Measured: catchable refused 17/17 (attributed 17: new rules 4 [M4 2, M6 2], older rules 13, unattributed 0); uncatchable instance ['built']; false positives 0/3; precision 1.000; per class [attributed, refused, n] {"M1": [3, 3, 3], "M2": [3, 3, 3], "M3": [3, 3, 3], "M4": [3, 3, 3], "M5": [3, 3, 3], "M6": [2, 2, 2]}; baseline exit 0 in 3.64 s
- Operational definition: 18 seeded edits (6 classes x 3, seed 20261105, the same instances as RL-15 run-002) and 3 offset-bearing benign controls, one build each on a fresh export of roadmap/ at bridge HEAD with builder 690cff6a; refused = non-zero exit with the validators' prefix; attributed = the lock-40 tag in the whole message, or one of eight fixed older-rule wordings; the secondary-paper digest instance declared uncatchable and excluded (denominator 17); gate PASS = 17 of 17 refused and attributed, new rules M4 >= 2 and M6 >= 2, 0 controls non-zero
- Instrument: VALID. preflight (charter 1b) PASS: layout, 21 edits all change bytes, evaluator known answers at every gate region, positive and negative controls, tag beyond 120 characters; blind review PASS; the older-rule wording list is fixed, so a differently worded refusal would read as unattributed (none did)
- Supported scope: on this roadmap.json and builder, both lock-40 validators refuse what a file comparison can catch (the process rule 2 of 3 M4, the third refused first by an older rule; the digest rule 2 of 2), every catchable seeded instance is refused with a named rule, and no benign control is refused
- Unresolved clauses: none for the restated claim; the secondary-paper digest class stays uncaught by design (no file to compare); validators the lab did not seed (ledger checks none)
- Evidence: empirical; seeded-mutation benchmark on a scratch export; 22 builds, 15.2 s; 25 light builds with the preflight
- Replication: LEDGER_REDERIVED
- Decision justified: RL15-D1's restated expectation (ERRATUM, lock 41) is met instance by instance; the RL-15b report enters as a research source by digest when the visionary records it; a PASS here confirms the design authority's reading of run-002 on a corrected instrument, not a fresh prediction

## RL-16 (RL-16-RESULTS-v1, ledger status PASS, H-02)

### H-02a: SUPPORTED

- Tested clause: H-02a: the attested share of argv 63 and the kept fraction at a 10 percent sample re-derive from the published cost split to R00's figures
- Measured: bands sum 1453.4 vs reported 1453.3 (within 1 percent: True); attested 0.6448 vs 0.645 (within 0.005: True); kept at 0.10 0.4196 vs 0.4195 (within 0.005: True)
- Operational definition: five slot bands of the published cost split summed; attested share of argv 63's serial time; kept fraction at a 10 percent sample; tolerances preregistered
- Instrument: VALID. arithmetic re-derivation from the published split to R00's figures (0.6448 against 0.645; 0.4196 against 0.4195)
- Supported scope: the cost split's figures re-derive
- Unresolved clauses: none for this clause (ledger checks none)
- Evidence: documentary; re-derivation from a published cost report
- Replication: LEDGER_REDERIVED
- Decision justified: the attested share and kept fraction are usable inputs to the checkpoint cost model

### H-02b: SUPPORTED

- Tested clause: H-02b: the equal-load growth of verify time per slot in the K 6 era reproduces the report's about 13 s per slot within 5 s
- Measured: g 9.34 s per slot at equal load, 95 percent pairs bootstrap [5.73, 13.50] (1000 defined resamples), n 23 runs over slots 253-278, load coefficient 24.8 s per unit, R2 0.624; univariate slope 8.35
- Operational definition: OLS of verify wall time on slot and run-mean load over the 23 successful verifies of slots 253-278; g = growth per slot at equal load; band 8 to 18 s, width cap 20 s
- Instrument: VALID_WITH_LIMITS. slot and test count are collinear, so g is the whole suite's growth per slot, not the per-layer cost; one host, one era; the 13 s figure came from dry runs
- Supported scope: at equal load the verifies grew about 9.34 s per slot [5.73, 13.50], within the band; the report's 13 s is reproduced within the band with the point estimate below it
- Unresolved clauses: the register's bounded-T(N) clause (H-02c is a model, not a measurement): the reader's cost, the sample's agreement and the checkpoint's writing-run seconds come from the shadow period (ledger checks none)
- Evidence: empirical; observational regression over published verify records
- Replication: LEDGER_REDERIVED
- Decision justified: supports the cost half of the checkpoint design; the sampling and cadence choice waits for the shadow-period measurement (condition (v), N_shadow 10)

## RL-17 (RL-17-RESULTS-v1, ledger status FAIL, H-27)

### H-27a: SUPPORTED

- Tested clause: H-27a: two runs of the same class and seed produce identical effect logs
- Measured: classes.json digest matches the committed results: True; 416 of 416 run pairs identical (whole effect log)
- Operational definition: two runs per (class, seed) over 13 classes x 32 seeds compared byte for byte
- Instrument: VALID. deterministic comparison; 416 of 416 identical
- Supported scope: the simulation harness is deterministic on this host
- Unresolved clauses: nothing about the production coordinator (ledger checks none)
- Evidence: simulation; export at b4bbea79
- Replication: LEDGER_REDERIVED
- Decision justified: the harness is a valid instrument for replay and fault work

### H-27b: SUPPORTED

- Tested clause: H-27b: the committed REPLAY_STALE class row reproduces exactly on the pin
- Measured: REPLAY_STALE class C3: result PASS (committed PASS); whole row equal: True; differing keys: []
- Operational definition: the committed REPLAY_STALE class row (C3) recomputed and compared key by key
- Instrument: VALID. deterministic recomputation
- Supported scope: the committed row reproduces
- Unresolved clauses: none (ledger checks none)
- Evidence: simulation; export at b4bbea79
- Replication: LEDGER_REDERIVED
- Decision justified: as H-27a

### H-27c: UNRESOLVED

- Tested clause: H-27c: duplicated and stale (reordered) board operations replayed after a run are refused and change nothing
- Measured: duplicates: 70169 of 70169 answered DUPLICATE_ID, 0 changed state; stale replays: 0 of 39795 answered STALE_VERSION, 39795 refused otherwise, 0 accepted, 0 changed state, 0 not posable (version unchanged); exceptions 0
- Operational definition: 70,169 duplicate replays and 39,795 stale replays (fresh id, original expectedVersion, posed at the deadline tick) answered by Board.apply; expected DUPLICATE_ID and STALE_VERSION
- Instrument: VALID_WITH_LIMITS. stale vectors were posed after lease expiry, so the holder and state checks fired before the version check; 'reordered' is a late stale arrival, not a permuted log (declared proxies)
- Supported scope: every duplicate was refused DUPLICATE_ID and changed nothing; every stale replay was refused and changed nothing
- Unresolved clauses: the version rule itself (no STALE_VERSION observed); a vector posed mid-run, before expiry, is the new id (rec 3) (ledger checks C3)
- Evidence: simulation; replay through the harness's coordinator board
- Replication: LEDGER_REDERIVED
- Decision justified: the mid-run stale-version vector goes into the obligation-level successor PREREG

### H-27d: CONTRADICTED

- Tested clause: H-27d: the recorded operation sequence replayed in order through a fresh board reproduces the claim and merge answers exactly
- Measured: log replay through a fresh board: claim and merge sequence identical in 0 of 416 runs; agreement by operation kind (agree, total): {"ACQUIRE": [6149, 8095], "ASSIGN": [2045, 3349], "MERGE": [817, 9461], "MESSAGE": [32, 20388], "RELEASE": [109, 113], "RENEW": [17686, 25223], "VERIFY": [0, 10082]}; exceptions 10082
- Operational definition: the recorded operation sequence replayed in order through a fresh board; expected identical claim and merge answers
- Instrument: VALID_WITH_LIMITS. an exception in the fresh-board replay counted as a divergence (review 2 note 3); the board consults durable state (VERIFY, MESSAGE)
- Supported scope: the board is not a pure function of its operation stream: event-only replay diverges in every run
- Unresolved clauses: replay over a declared durable-state snapshot (the distinction the successor must make); the fault classes (BLOCKED on DATA-CORRECTNESS-001) (ledger checks none)
- Evidence: simulation; replay through a fresh board, 416 runs
- Replication: LEDGER_REDERIVED
- Decision justified: replay semantics must declare the durable-state snapshot; event-only replay is not a correctness claim of the harness

## RL-18 (RL-18-RESULTS-v1, ledger status FAIL, H-31)

### H-31a: SUPPORTED

- Tested clause: H-31a (instrument): the lab's validator and integer gate reproduce the contract's vectors
- Measured: SHAPE vectors refused 18 of 18; valid vectors accepted 25 of 25; valid comparison vectors reproduced bit for bit 17 of 17; DECISION_MISMATCH vectors flagged 2 of 2
- Operational definition: the lab's validator and integer gate against the contract's vectors: 18 SHAPE refusals, 25 valid acceptances, 17 comparison vectors reproduced, 2 DECISION_MISMATCH flagged
- Instrument: VALID. instrument check, all vectors reproduced bit for bit
- Supported scope: the lab's gate implementation agrees with the contract's vectors
- Unresolved clauses: none (ledger checks none)
- Evidence: documentary; vector replay of MAS-RA-002
- Replication: LEDGER_REDERIVED
- Decision justified: the lab's gate is a valid instrument for the arms study and its successor

### H-31b: CONTRADICTED

- Tested clause: H-31b: the CONF-MAS arms study is expressible as valid run manifests, evaluation records and comparisons
- Measured: split valid True; manifests 0 of 640 valid; records 0 of 12; comparisons 9 of 9; refusals: [{"runId": "DEFENDED-C2-s1", "where": "$.configuration.budget.tokensPerTask minimum"}, {"runId": "DEFENDED-C2-s2", "where": "$.configuration.budget.tokensPerTask minimum"}, {"runId": "DEFENDED-C2-s3", "where": "$.configuration.budget.tokensPerTask minimum"}, {"digest": "sha256:7a38e35a496f0af6", "recordId": "DEFENDED-completionPpm", "valid": false, "where": "$.configuration.budget.tokensPerTask minimum"}, {"digest": "sha256:ca423f9c2f991025", "recordId": "DEFENDED-duplicatedWorkRatioPpm", "valid": false, "where": "$.configuration.budget.tokensPerTask minimum"}, {"digest": "sha256:47063b46e27dc516", "recordId": "DEFENDED-lostWorkPpm", "valid": false, "where": "$.configuration.budget.tokensPerTask minimum"}]
- Operational definition: the arms study expressed as a split declaration, 640 run manifests, 12 evaluation records and 9 comparisons validated against the contract's schemas
- Instrument: VALID. deterministic schema validation; the refusal point is one field (configuration.budget.tokensPerTask minimum)
- Supported scope: the simulation's manifests are inexpressible as published: the form requires a positive token budget per task and a simulation has none; the split and the comparisons validate
- Unresolved clauses: the contract's semantic checks beyond the schema (the reference model's 17 refusal codes) were not run (ledger checks none)
- Evidence: documentary; schema validation of generated records
- Replication: LEDGER_REDERIVED
- Decision justified: a sentinel or 'no model' budget is a contract note or a new id (RL-18-PROPOSAL); M-G1's 'substrate usable' is not shown by this verdict, which closes only the expressibility question

### H-31c: UNRESOLVED

- Tested clause: H-31c: the distribution gate's non-inferiority verdicts agree with the campaign's recorded bound verdicts per arm and metric
- Measured: cells (arm, metric): A1/completionPpm: gate WITHIN_NOISE nonInferior True mean 0 half 0, campaign bounds hold in all classes True -> agree; A1/duplicatedWorkRatioPpm: gate WITHIN_NOISE nonInferior True mean 3880 half 9104, campaign bounds hold in all classes False -> DISAGREE; A1/lostWorkPpm: gate WITHIN_NOISE nonInferior True mean 0 half 0, campaign bounds hold in all classes True -> agree; A2/completionPpm: gate WITHIN_NOISE nonInferior True mean 0 half 0, campaign bounds hold in all classes True -> agree; A2/duplicatedWorkRatioPpm: gate WITHIN_NOISE nonInferior False mean -16275 half 21204, campaign bounds hold in all classes False -> agree; A2/lostWorkPpm: gate WITHIN_NOISE nonInferior True mean 0 half 0, campaign bounds hold in all classes True -> agree; A3/completionPpm: gate WITHIN_NOISE nonInferior True mean 0 half 0, campaign bounds hold in all classes True -> agree; A3/duplicatedWorkRatioPpm: gate WITHIN_NOISE nonInferior True mean 3982 half 12676, campaign bounds hold in all classes False -> DISAGREE; A3/lostWorkPpm: gate WITHIN_NOISE nonInferior True mean 0 half 0, campaign bounds hold in all classes True -> agree
- Operational definition: the distribution gate's non-inferiority verdict against the campaign's recorded bound verdict per (arm, metric) cell: 7 of 9 agree; inconclusive band
- Instrument: VALID_WITH_LIMITS. the tolerance (10,000 ppm) and the agreement mapping are the lab's; five task clusters make the interval wide
- Supported scope: a pooled non-inferiority gate can agree with a campaign while per-class absolute bounds are breached: the two disagreeing cells are where pooling averages away broken classes
- Unresolved clauses: agreement under a per-class bound beside the pooled interval (the successor keeps both, rec 5) (ledger checks C3)
- Evidence: simulation; the lab's gate over the campaign's simulation ledgers
- Replication: LEDGER_REDERIVED
- Decision justified: per-class correctness bounds must stand beside pooled efficiency intervals in any admission gate

## RL-19 (RL-19-RESULTS-v1, ledger status UNRESOLVED, H-24)

### H-24-fig: UNRESOLVED

- Tested clause: H-24 (figure grounding): the figures the three syntheses attribute to the five held papers are found in the papers' own text at a rate of at least 90 percent
- Measured: found 24 of 29 claims (0.828); by source {"RS-1": {"claims": 1, "found": 0}, "RS-2": {"claims": 11, "found": 9}, "RS-3": {"claims": 29, "found": 24}}; by paper {"F2": {"claims": 6, "found": 6}, "F4a": {"claims": 5, "found": 3}, "F4b": {"claims": 5, "found": 4}, "F5": {"claims": 6, "found": 6}, "F6": {"claims": 7, "found": 5}}; not found: ['F4a-4', 'F4a-5', 'F4b-5', 'F6-5', 'F6-6']
- Operational definition: 29 figures attributed by RS-1/RS-2/RS-3 to five held papers searched in the papers' own text by a pattern extractor plus a first-page hand pass; PASS at 0.90, FAIL below 0.70
- Instrument: VALID_WITH_LIMITS. pattern matches and first-page readings, not claim-level context, definitions and conditions; nothing about papers the lab does not hold
- Supported scope: 24 of 29 attributed figures are found in the papers (0.828)
- Unresolved clauses: the five figures not found; the syntheses' interpretations; claim-level context before a borrowed figure becomes a local gate (rec 7) (ledger checks C1)
- Evidence: documentary; literature grounding over five owner-approved papers
- Replication: LEDGER_REDERIVED
- Decision justified: a borrowed figure (the 45 percent threshold among them) is a candidate to test locally, never a gate on its own; source lineage is kept per claim in data/claims.json

## RL-20 (RL-20-RESULTS-v1, ledger status FAIL, H-25)

### H-25a: SUPPORTED

- Tested clause: H-25a (instrument): the lab's checker reproduces the record's topology vectors
- Measured: the lab's checker agrees with 52 of 52 topology vectors; disagreements: []
- Operational definition: a static checker written from MAS-RA-004's README against the record's 52 topology vectors
- Instrument: VALID. instrument check; 52 of 52 agree
- Supported scope: the lab's checker reproduces the record's topology vectors
- Unresolved clauses: none (ledger checks none)
- Evidence: documentary; vector replay
- Replication: LEDGER_REDERIVED
- Decision justified: the checker is a valid instrument for the seeded-edit test

### H-25b: CONTRADICTED

- Tested clause: H-25b: the seeded graph classes the TopologySpec can express (cycle, unreachable node, budget escape) are refused with the record's code and a witness, and no valid vector is refused
- Measured: gated seeded edits refused as expected 21 of 22 (accepted 1); valid vectors accepted 8 of 8; descriptive (decentralized isolated peer): [{"base": "T02", "class": "unreachable", "lab": null}, {"base": "T05", "class": "unreachable", "lab": null}]
- Operational definition: 22 gated seeded edits (cycle, unreachable node, budget escape, one per class on the 8 valid vectors) expected refused with the record's code and a witness; 8 valid vectors expected accepted
- Instrument: VALID_WITH_LIMITS. the edits and the checker share an author; one edit per class per vector; 'witness' is the refusing rule's named object; one edit was not a refusable case (see invalid cases), which the preregistration review foresaw
- Supported scope: 21 of 22 gated edits refused with the expected code and a witness; all 8 valid vectors accepted; the record's rules are not contradicted
- Unresolved clauses: a clean count with the invalid case excluded is a new id (never a re-tune under this id); the WorkPlan and strategy halves (ledger checks none)
- Evidence: documentary; seeded edits on published vectors
- Replication: LEDGER_REDERIVED
- Invalid cases: budget-escape edit on the one-node SINGLE_AGENT vector: INVALID_CASE: the edit could not express a budget below the node count (the minimum is 1 and the edit keeps at least 1), so the 'accepted' outcome is the record behaving correctly; counted as a FAIL by the preregistered gate and left as recorded
- Decision justified: the TopologySpec form refuses the expressible classes by construction; the FAIL records the instrument's invalid case beside the verdict, not a defect of the record; input to GRAPH-COMPILE-001's design note

## RL-21 (RL-21-RESULTS-v1, ledger status PASS, H-26)

### H-26a: SUPPORTED

- Tested clause: H-26a: every path under architecture/ is created by exactly one packet authority
- Measured: 1547 paths created by 92 packet authorities; created twice: 0 []
- Operational definition: over 114 authority records at c1b838be: paths under architecture/ created, by how many packet authorities each
- Instrument: VALID. deterministic count; 1,547 created, none twice
- Supported scope: one creator per published path
- Unresolved clauses: revocation; runtime writers; files outside architecture/ (ledger checks none)
- Evidence: documentary; authority records join
- Replication: LEDGER_REDERIVED
- Decision justified: supports AUTHORITY-MAP-001's creator rule as input

### H-26b: SUPPORTED

- Tested clause: H-26b: every change to a created path names its creator among the changer's baseline packets
- Measured: changes to created paths 4335 of 16415 entries (12080 outside the export's scope); creator named among the changer's baseline packets 4335; unlinked 0 []
- Operational definition: every changed-file entry for a created path names the creator among the changer's direct baseline packets (4,335 of 4,335 in scope)
- Instrument: VALID_WITH_LIMITS. 12,080 entries change paths outside architecture/ and are not gated; the chain between meta generations needs git history
- Supported scope: every published change explicitly builds on the creator (creator linkage)
- Unresolved clauses: 'exactly one writer over time' in the register's sense is not what was measured: many later packets change a path, each naming the creator (ledger checks none)
- Evidence: documentary; authority records join
- Replication: LEDGER_REDERIVED
- Decision justified: read H-26 as creator linkage, not single-writer; the register wording to say so

### H-26c: SUPPORTED

- Tested clause: H-26c (descriptive, not gated): ownership of paths by meta authorities
- Measured: descriptive: paths owned by more than one meta authority 139 of 275; meta authorities 22; metaBaseline is a commit id (form str), so the ownership chain is git history outside the export and is not checked here
- Operational definition: descriptive layout of ownership by the 22 meta authorities
- Instrument: DESCRIPTIVE. not gated
- Supported scope: descriptive table in the report
- Unresolved clauses: none (descriptive) (ledger checks none)
- Evidence: documentary; authority records
- Replication: LEDGER_REDERIVED
- Decision justified: informs AUTHORITY-MAP-001 (input through the monitor)

## RL-22 (RL-22-RESULTS-v1, ledger status UNRESOLVED, H-23)

### H-23-coord: UNRESOLVED

- Tested clause: H-23 (coordinator half): a board state machine written from the README alone reproduces at least 95 percent of the record's transcript and binding vectors
- Measured: transcript vectors 28 of 32; binding vectors 10 of 11; rate 0.884; disagreements: [["B01", null, "REPLAY", ["a3", ["ACCEPTED", "CONCURRENCY_LIMIT"]]], ["B02", null, "REPLAY", ["q6", ["ACCEPTED", "CONCURRENCY_LIMIT"]]], ["B03", null, "REPLAY", ["q6", ["ACCEPTED", "CONCURRENCY_LIMIT"]]], ["B17", "UNKNOWN_REFERENCE", "REPLAY", ["a3", ["ACCEPTED", "CONCURRENCY_LIMIT"]]], ["R05", "UNKNOWN_REFERENCE", "BINDING", null]]
- Operational definition: a board state machine written from README section A2 alone, VERIFY's ledger rules declared un-modelled, against 32 transcript and 11 binding vectors; PASS at 0.95, FAIL below 0.70
- Instrument: VALID_WITH_LIMITS. one implementation by one reader who knew the vector categories and counts; VERIFY binding and history rules not re-implemented; VERIFY consumed the recorded answer for the un-modelled rules
- Supported scope: 38 of 43 vectors reproduce (0.884); the five disagreements are one point (board-wide count read as per-task at ACQUIRE/ASSIGN) plus the un-modelled manifest dependency
- Unresolved clauses: runtime interchangeability (an aggregate rate cannot show it); the three valid transcripts B01-B03 disagree, which an obligation-level gate would surface (ledger checks C1)
- Evidence: documentary; re-implementation from documentation against published vectors
- Replication: LEDGER_REDERIVED
- Decision justified: MAS-RA-004 README inputs (board-wide count; the two outside models) ruled at lock 36, owed by R00's next packet; the obligation-level successor (rec 3) is the interoperability test
