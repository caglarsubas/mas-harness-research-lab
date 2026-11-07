# Research-Lab design read of the two owner-supplied R&D roadmap documents (RD-D1), v2, 2026-11-05

Status: v2, written on resume (MON-RL-RESUME, owner "Resume now") after the owner supplied both files directly in
the lab session. v1 (same day, from the visionary's secondary records only) is superseded; what v1 got wrong is named
in section 9. The lab keeps no copy of either file (MON-RL-M21, "no second copy"); both are recorded by digest.

| source | title (as the file states it) | sha256 | size | lines, words | status |
|---|---|---|---|---|---|
| RS-1 | "R&D Roadmap for MAS-Harness / Planeon" | 61fa9041f2399f527fb8795cce00d5013cd5cfa3fa7e690e237aca1030e6cc47 | 42,792 B | 224, 5,270 | RS-MEMO-RDROADMAP (lock 29), OWNER_SUPPLIED; digest checked against the recorded value before reading |
| RS-2 | "MAS-Harness / Planeon R&D Roadmap: Academic Evidence, Prioritisation and Agent-Executable Research Programme" | 5b30977bfef178e097728c37618983b1f0d6273b99e5c2c6e2150d9a50b4441e | 60,459 B | 505, 7,191 | NEW, not yet recorded; proposed to the visionary as research source RS-MEMO-RDACADEMIC, OWNER_SUPPLIED, at the next lock |

Both are outside syntheses written over the programme's own R&D report (`visionary/RD-REPORT.md` a5557254) plus
external literature. RS-1's citation markers are unresolved rendering tokens; RS-2 carries resolvable identifiers
(DOIs, arXiv ids, venue pages) for about 35 works in a BibTeX block grouped by item. Every external figure below is
"as reported by the source", not reproduced; the dates, staffing and person-week figures of both are not copied.

Owner words that bind this read (LOCK29-RD-D1 section 0): "what research-lab said is more important than what
visionary said"; "Yes, on resume" to the lab's five points (a)-(e). Where the two reads differ, the lab's prevails,
and the visionary reconciles its held item notes to this read (section 8). Nothing here is a roadmap shift.

Compute figures below are from the lab's run records: every RL-01..RL-13 run took under 10 s of wall time (RL-04,
the largest, 640 simulation runs in 8 s); the cost of an experiment on this host is session work and the monitor's
GO, not compute. RS-2's own rule, "research from existing exhaust" in months 0-3, describes what the lab has done
since it opened.

## 1. What the two documents say, in brief

RS-1: four parallel streams (S1 qualification-critical B1, B2, C1, C2, E1; S2 differentiation A1, A2, B3, B7; S3
efficiency and scale D2, D3, B4, B5, B6; S4 publishability A3, A4, A5, C3, E2, F1); a Potential and Effort ranking of
the 22 lines on 1-5 scales (weights: maturity 20 %, novelty 25 %, applicability 25 %, impact 30 %; effort data 30 %,
compute 30 %, human 40 %), B2 first; four decision gates on the A2/A3/A4 path; an eight-lane agent operating model
("runner: no interpretation privileges"; "experiment designer: independent review before run"); the ECU unit and
the 60/25/15 compute split; for A1 the mitigation "never replace the production verifier initially; run checkpoint
mode as shadow verification and require disagreement analysis" and success bounds (at least 3x lower incremental
verification cost; miss and detection-delay curves at 5, 10 and 20 % sampling; no weakening of head-layer refusal
vectors).

RS-2: the same 22 lines scored 0-100 (potential = 25 % maturity + 30 % novelty + 30 % differentiation + 15 %
feasibility; effort = 30 % data + 30 % compute + 40 % human), with the rule that priority is not the ratio alone;
a literature map per item with identifiers; a two-speed programme (0-3 months from existing records, 3-6 months on
the first banking workloads, 6-12 native and fault campaigns, 12-18 generalisation and standards); a per-item
table of agent-executable tasks, success criteria and the human gate for each; a research DAG (B2 is the substrate
for B1, B3, B4, B5, B6, D2; B1 for B3, C2, E1; A2 for everything); a publication grouping into six to eight outputs;
and six success gates for any result (a formal property checked against production vectors; a preregistered
negative outcome still publishable; an external baseline reproduced faithfully; a dataset generated independently of
the hypothesis; replication on a held-out split or a second verifier; an artefact another group could run).

Where they differ: RS-1 ranks B2 first and A1 eighth (high potential, high effort, "start now, branch"); RS-2 ranks
A5, A4, F1, B7, A1, A2 and C3 first by ratio and says E1, C1, C2 outrank them by release-path position. Both agree
on the streams, the 60/25/15 split, shadow-first compaction, independent review before a run, and the model-harness
configuration as the unit of evaluation.

## 2. (a) Potential and effort per register hypothesis, recomputed from our records

Scales, defined from what the records show:

- Potential P (1-5): 5 = the result decides a pending owner question or a release-gate claim (A2/A3/A4, Q-CC2); 4 =
  it changes a contract or an item's design note; 3 = evidence for a campaign record or a design note; 2 =
  descriptive; 1 = method only.
- Effort E (1-5): 1 = light run on records the lab holds (seconds of compute, one session pass, as RL-01..13 ran);
  2 = light, but needs a new masked export or a day's paper artefact; 3 = one heavy GO on this host or a new script
  family with review; 4 = waits on a named roadmap item, then a heavy run; 5 = a lab run plan with owner-approved
  spend or a repository.
- Score = P / E. Stream: RS-1's S1-S4 by the hypothesis's lead section. Queue class for heavy GOs: Q =
  qualification-critical (S1; 60 %), T = topology, routing and memory (B3, B4, B5, B7, D2; 25 %), X = everything
  else (15 %). Light work is outside the split.
- Outside: advisory, never a score change (HO-D1): RS-1's rank and Potential/Effort of the lead section; RS-2's
  Potential/Effort/ratio of the same section.

| id | state from the records | next measurable step | P | E | score | stream | outside RS-1 (rank, P/E) | outside RS-2 (P/E, ratio) |
|---|---|---|---|---|---|---|---|---|
| H-01 | RL-07 PASS 116/116; live step rule not replayed | replay the live step rule on one head (needs an export) | 2 | 2 | 1.00 | S2 (X) | A1 #8, 4.9/4.3 | A1 97/72, 1.35 |
| H-02 | no run; Q-CC2-1..3 options in R00's DESIGN_CC2 rev 2; cost split at 280 measured | T(N) cost model from the 279/280 records (light); the detection-delay curves at 5, 10, 20 % from the shadow period (section 7); RS-1's bound "at least 3x lower incremental cost" as a candidate PASS bound | 5 | 2 | 2.50 | S2 (X) | A1 #8, 4.9/4.3 | A1 97/72, 1.35 |
| H-03 | RL-05 FAIL as stated; P_t proposed | P_t under a new id once DECISION-LEDGER-001's note lands | 3 | 2 | 1.50 | S2 (X) | A2 #7, 4.6/3.1 | A2 92/68, 1.35 |
| H-04 | RL-10 FAIL (clause), RL-12 PASS per claim | none open; a shared vector set is R00 material | 2 | 1 | 2.00 | S1 (Q) | B1 #2, 4.7/2.7 | B1 92/80, 1.15 |
| H-05 | BLOCKED on MAS-STRATEGY-001's design note | formalise the envelope invariant on paper now | 4 | 3 | 1.33 | S2 (T) | B3 #6, 4.8/3.7 | B3 89/92, 0.97 |
| H-06 | BLOCKED on RELEASE-EVIDENCE-001 | list the claims derivable from release-profile.json today (light, paper) | 5 | 3 | 1.67 | S1 (Q) | E1 #3, 4.7/3.5 | E1 89/94, 0.95 |
| H-07 | RL-01: a PASS by gate; b UNRESOLVED (one K 8 run) | b: 280's verify is a second K 8 head (1,162 s at load 8.03); re-fit at three K 8 heads | 3 | 2 | 1.50 | S4 (X) | A4 #17, 3.6/2.0 | A4 76/46, 1.65 |
| H-08 | RL-08 UNRESOLVED (no refusal history) | waits for a per-check refusal history (the review-record series) | 3 | 4 | 0.75 | S2 (X) | A1 #8, 4.9/4.3 | A1 97/72, 1.35 |
| H-09 | RL-02 UNRESOLVED (no oracle record; ids per round) | waits on REVIEW-RECORD-SERIES-001; report custody, context and model family separately (both documents say so) | 4 | 3 | 1.33 | S2 (X) | A2 #7, 4.6/3.1 | A2 92/68, 1.35 |
| H-10 | RL-06: a PASS; b FAIL (taxonomy over ids) | b v2 over rule text, counts only, on the monitor's permission; RS-2's A3 note (interrupted-time-series against team familiarity) as a design input | 2 | 2 | 1.00 | S4 (X) | A3 #19, 3.7/2.6 | A3 75/68, 1.10 |
| H-11 | BLOCKED on a live ledger consumer | define the measurement on the campaign ledgers (paper) | 3 | 4 | 0.75 | S1 (Q) | B1 #2, 4.7/2.7 | B1 92/80, 1.15 |
| H-12 | BLOCKED on PLANE-BOOTSTRAP-R06 and the read-only profile | the matrix design (paper); the substrate trial is H-31 | 5 | 5 | 1.00 | S1 (Q) | B2 #1, 4.8/3.0 | B2 86/84, 1.02 |
| H-13 | RL-04: b PASS; a UNRESOLVED-by-input | a sequential task family is R12's to add; not proposed | 2 | 3 | 0.67 | S2 (T) | B3 #6, 4.8/3.7 | B3 89/92, 0.97 |
| H-14 | BLOCKED on H-12's infrastructure | phase-plan design (paper) | 4 | 5 | 0.80 | S2 (T) | B3 #6, 4.8/3.7 | B3 89/92, 0.97 |
| H-15 | BLOCKED on MODEL-ROUTING-001 and SEM-QUAL-001 | the report's columns (paper); RS-2's D2 note: non-inferiority plus risk-coverage, not accuracy alone | 3 | 5 | 0.60 | S3 (T) | D2 #9, 4.4/2.8 | D2 86/92, 0.93 |
| H-16 | BLOCKED on the read-only profile | cohort design and metrics (paper) | 3 | 4 | 0.75 | S1 (Q) | E1 #3, 4.7/3.5 | E1 89/94, 0.95 |
| H-17 | BLOCKED on EVENT-TRIGGER-001's design note | vector design from the four monitor journeys (paper) | 4 | 3 | 1.33 | S1 (Q) | E1 #3, 4.7/3.5 | E1 89/94, 0.95 |
| H-18 | RL-09 FAIL (four families), RL-11 widened UNRESOLVED | paths 1-17 wait on a host-interface amendment that enumerates them | 4 | 3 | 1.33 | S1 (Q) | C1 #5, 4.8/4.6 | C1 88/82, 1.07 |
| H-19 | RL-03 PASS, RL-04 second clause PASS as bounded | closed | 2 | 1 | 2.00 | S1 (Q) | C2 #4, 4.7/3.2 | C2 86/94, 0.91 |
| H-20 | BLOCKED on CONF-LINUX-001 and UAT-CAMPAIGN-001 | template the case study (paper) | 3 | 4 | 0.75 | S1 (Q) | C1 #5, 4.8/4.6 | C1 88/82, 1.07 |
| H-21 | BLOCKED on an owner run plan and LINUX-HOST-AUTH-001 | define agreement; cost the plan (paper) | 4 | 5 | 0.80 | S2 (X) | A2 #7, 4.6/3.1 | A2 92/68, 1.35 |
| H-22 | RL-13 PASS; conventions unverified | verify the pinned conventions only after an approved fetch | 2 | 2 | 1.00 | S4 (X) | B2 #1, 4.8/3.0 | B2 86/84, 1.02 |
| H-23 | READY (paper) | clean-room sketch against the TopologySpec vectors | 3 | 2 | 1.50 | S4 (X) | B3 #6, 4.8/3.7 | B3 89/92, 0.97 |
| H-24 | READY (paper) | method note | 2 | 2 | 1.00 | S4 (X) | F1 #20, 3.3/2.1 | F1 82/54, 1.52 |
| H-25 | new, (e) static workflow checking (RS-1 B7) | reference checker over the published TopologySpec vectors; WorkPlan and strategy schemas not adopted (partial) | 4 | 2 | 2.00 | S2 (T) | B7 #11, 4.3/2.8 | B7 81/54, 1.50 |
| H-26 | new, (e) one authoritative writer per governed state (RS-1 C3) | contract-text half on the published contracts now; the trace half waits on MAS-RA-009's packet | 4 | 2 | 2.00 | S4 (X) | C3 #14, 4.1/2.8 | C3 80/62, 1.29 |
| H-27 | new, (e) concurrency and replay correctness (RS-1 D1, D3) | replay the run-event vectors through the exported harness (pin b4bbea79) | 4 | 2 | 2.00 | S3 (X) | D3 #10, 4.5/3.3 | D3 85/94, 0.90 |
| H-28 | new, (e) typed memory and handoff (RS-1 B5) | observational half on the programme's own handoff records now (light); the harness half waits on RELIABILITY-CAMPAIGN-001 | 4 | 1 | 4.00 | S3 (T) | B5 #13, 4.3/3.5 | B5 72/86, 0.84 |
| H-29 | new, (e) gate interleaving (RS-1 B4) | needs a masked export of R10's gate transcripts through the monitor | 4 | 3 | 1.33 | S3 (T) | B4 #12, 4.2/3.0 | B4 74/72, 1.03 |
| H-30 | new, (e) seeded-inconsistency benchmark for the roadmap build (RS-1 A5) | mutation seeding on a scratch copy of roadmap/ against build_roadmap's validators (light) | 3 | 1 | 3.00 | S4 (X) | A5 #21, 3.2/2.1 | A5 71/34, 2.09 |
| H-31 | new, the visionary's "H-25": MAS-RA-002's manifest and distribution gate on the CONF-MAS ledgers (RS-1 B2 "do now") | re-express the CONF-MAS-001..005 ledgers as run manifests on the b4bbea79 export; compare the gate's verdicts with the recorded ones | 4 | 2 | 2.00 | S1 (Q) | B2 #1, 4.8/3.0 | B2 86/84, 1.02 |

Reading of the table. By the lab's score the next light experiments are H-28's observational half (4.00), H-30
(3.00), H-02's cost model (2.50), then the 2.00 group (H-25, H-26, H-27, H-31). RS-2's ratio ordering (A5, A4, F1,
B7 first) agrees with ours on H-30 (A5), H-25 (B7) and H-07b (A4); RS-1's "B2 first" is H-31 now and H-12 when the
plane exists. Both documents' release-path rule (E1, C1, C2 outrank the ratio) is the lab's M-G1..M-G4 below, not a
score. The 60/25/15 split applies to heavy GOs only; every item marked light above needs no GO.

## 3. (b) The four decision gates as register milestones

RS-1's four gates become four register milestones with one lead hypothesis each (the ties the owner accepted:
H-12, H-02, H-06, H-17) and supporting hypotheses. The dates are not copied: a milestone closes when its lead
hypothesis has a verdict, not on a calendar.

| id | gate (RS-1) | release gate | lead | supporting | closes when |
|---|---|---|---|---|---|
| M-G1 | first gate: B2's substrate statistically usable; C1's coverage map closed enough for native qualification; E1's claims derivable without undocumented inference | A2 | H-12 | H-31 (substrate), H-18 (coverage), H-06's derivable-claims list | H-31 has a verdict and H-12's matrix is designed; RL-11's coverage map is current at the A2 head |
| M-G2 | second gate: keep full re-execution, checkpoint for development runs only, or a bounded compaction scheme, decided on measured cost against detection delay | none (owner decided G1, CC2-D1) | H-02 | H-07b | the shadow period of condition (v) ends clean and H-02's T(N) is fitted on measured layer seconds with the 5/10/20 % curves |
| M-G3 | third gate: which B3 strategy forms are admitted; default single agent plus independent verifier unless delegation shows a credible matched-budget advantage | A3 | H-06 | H-05, H-14, H-23 | H-06's derivable-claims list is checked against RELEASE-EVIDENCE-001's matrix; H-05's invariant is written |
| M-G4 | fourth gate: E1 + C2 + D1 + D3 + E2; replay safety, rollback, host qualification, unresolved-state handling, operator intervention | A4 | H-17 | H-20, H-11, H-16, H-27 | H-17's golden runs exist and H-20's case study is written from the evidence trail |

Reconciliation: the visionary's M-A2, M-A3, M-A4 are M-G1, M-G3, M-G4 here; M-G2 has no release-gate letter because
the owner already decided the gate (G1) and only its measurement remains.

## 4. (c) Independent review of every PREREG before its run

Rule, adopted into the charter's protocol (section 2, step 1a): no run starts until an independent pass that holds
only the PREREG, the register row and the charter (never the run script) writes `PREREG-REVIEW.md` in the
experiment's folder with a verdict. The checks:

- R1 falsifiable statement with PASS, FAIL and UNRESOLVED criteria that are exhaustive and exclusive;
- R2 clause scope: the unit named in the hypothesis is the unit the measurement counts (RL-10's slip: "per ledger"
  measured where the rule is "per claim"; it cost one FAIL and a restatement under a new id);
- R3 every input by sha256 and commit, each present in the lab's holdings;
- R4 bounds with units and a stated gate; seeds k >= 3 where stochastic; splits declared;
- R5 compute plan: light, or a heavy GO named, with the stream and the ECU count where it applies;
- R6 privacy: no path, handle or name token in the PREREG;
- R7 (from RS-2's success gates): the dataset's generation is independent of the hypothesis under test, or the
  dependence is declared.

A review FAIL returns the PREREG to a new version before it is frozen; the register records both digests. The
runner and evaluator separation of RS-1's operating model is adopted as the weaker half of the same rule: a verdict
is computed by the lab's evaluator script from the run records, and `RESULTS.json` names that script's digest; it is
never written by hand in the pass that ran the experiment. RL-01..RL-13 already followed this for the verdicts (each
has an `rl*_` script); the review step is new and applies from RL-14.

## 5. (d) The evaluation compute unit (ECU) and the 60/25/15 split in the run-plan form

RS-1 defines one ECU as "one complete four-use-case evaluation pass for one model-harness configuration at the
minimum statistical replication required by the platform". The lab adopts that definition as a count in the run-plan
form (v1 of this read had defined it as a single seeded run; corrected):

- one ECU = one pass over the four frozen banking use cases for one configuration tuple (model, harness, budget,
  agent count) at the platform's minimum replication, k >= 3 seeds (Q-MAS2-B); so one ECU is twelve seeded runs
  until the use-case count or k changes;
- a run plan states its ECU count (configurations x passes), the dated cost per ECU where the run is not on this
  host, the heavy-slot minutes it asks for, and its stream and queue class;
- the platform's measurement unit stays MAS-RA-002's run manifest and cost per success; ECU is a planning count,
  never a currency and never a reported result;
- the split 60 / 25 / 15 is the monitor's heavy-queue rule over a rolling window of twenty GOs (12 / 5 / 3), by the
  queue class the lab names in each GO request; platform verifies and R00 heavy steps always come first; light
  runs are outside the window. RS-1's own orders of magnitude for the product-coupled lines (B2 about 6-12 ECU,
  B3 12-20, B6 15-30) are as reported; no lab run plan exists yet.

## 6. (e) Six candidate hypotheses

Added to the register as H-25..H-30; each maps to one RS-1 line, which both documents score. H-31 is the visionary's
substrate trial, accepted as input and numbered after them.

- H-25 static workflow checking (B7): a static checker over TopologySpec, WorkPlan and strategy records refuses
  every seeded violation class (unbounded cycle, unreachable required end, two writers, unapproved effect path,
  budget escape), produces a witness trace per refusal, and refuses none of the published vectors. READY for the
  TopologySpec half; the rest waits on GRAPH-COMPILE-001's schemas. RS-2 names Agentproof (arXiv 2603.20356) and
  the EMNLP 2026 workflow survey as baselines, unread.
- H-26 one authoritative writer per governed state (C3): every governed state in the published contracts and the
  authority map has exactly one writer authority, every revoked authority refuses later writes in the vectors, and
  no board-mode trace shows two writers under adversarial seeds. READY (contract text); trace half waits on
  MAS-RA-009.
- H-27 concurrency and replay correctness (D1, D3): replaying a run-event log through the exported coordinator
  reproduces the claim and merge sequence exactly, and the replay vectors refuse reordered or duplicated events; no
  duplicated externally visible effect under the declared failure classes. READY on the b4bbea79 export for the
  replay half; the fault classes wait on DATA-CORRECTNESS-001.
- H-28 typed memory and handoff (B5): typed, digest-pinned handoff records are followed by fewer resume slips than
  free-text ones. Observational half READY on the programme's own handoff records (the dated MON rules of RL-06
  as the slip corpus); the harness half (state recovery after a forced compaction or restart; poisoning cannot grant
  a permission) waits on RELIABILITY-CAMPAIGN-001.
- H-29 gate interleaving (B4): a deterministic gate before every effectful phase never admits an effect without an
  approval record and adds bounded latency per phase; measured as cost per success and gate utility, not accuracy.
  Needs a masked export of R10's gate transcripts through the monitor.
- H-30 seeded-inconsistency benchmark for the roadmap build (A5): build_roadmap's validators catch every seeded
  inconsistency class (dangling dependency, status against evidence state, score drift, missing update entry, stale
  snapshot digest) on a scratch copy, with the false-positive rate on the frozen snapshot reported. READY, light;
  mutations only on a copy, never on roadmap/.

## 7. Condition (v) for CHAIN-COMPACTION-002

The lab's view is in `research/reads/CC2-CONDITION-V-LAB-READ.md`: adopt (v) as a bounded measurement period with a
reader-cost cap, N_shadow = one checkpoint cadence, and the shadow records as H-02's dataset. RS-1's A1 mitigation
says the same in one sentence; its success bounds (at least 3x lower incremental cost; 5/10/20 % curves; no weakened
head refusal vector) enter H-02's PREREG as candidate bounds, as reported.

## 8. Reconciliation of the visionary's held item notes (LOCK29-RD-D1 section 2) to this read

- CHAIN-COMPACTION-002 condition (v): confirmed, reworded per section 7 (bounded period, cost cap, disagreement
  classes, N_shadow options).
- MAS-RA-002 trial re-homed as a lab hypothesis: confirmed as H-31.
- GRAPH-COMPILE-001 named systems as unread references: dropped as an item note; H-25 carries the work; the names
  (now with identifiers from RS-2) enter the crosswalk only after an approved fetch and a read.
- RELIABILITY-CAMPAIGN-001 memory benchmarks and four case classes: the case classes are confirmed as an item note;
  the benchmark names are dropped until read; H-28 carries the hypothesis.
- DESIGN-UX-001 supervision-attention measures as E2 input: confirmed as an item note with RS-2's three measures
  (time to correct intervention, severity-weighted misses, workload), marked "named by an advisory source, not read".
- Register suggestions (LOCK29-RD-D1 section 3): stream column adopted (RS-1's S1-S4 plus the queue class); outside
  rank column adopted and filled from both documents; M-A2..A4 adopted as M-G1, M-G3, M-G4 with M-G2 added; the
  visionary's H-25 adopted as H-31; the H-09 note adopted; the runner/evaluator split adopted as the weaker half
  of (c).
- New for the visionary: RS-2 as research source RS-MEMO-RDACADEMIC (full sha256 above, OWNER_SUPPLIED, advisory);
  its per-item literature map is the fetch list's source of identifiers (section 10); its six success gates are
  adopted into the charter as the lab's standard for a reportable result.

## 9. What v1 got wrong, corrected here

- ECU: v1 defined it as one seeded run; RS-1 defines it as one four-use-case pass at minimum replication. v2 uses
  RS-1's definition.
- Stream letters: v1 used three ad hoc streams; v2 uses RS-1's four streams with the queue class beside them.
- The outside-rank columns are now filled from both documents.
- RS-2 was unknown to v1.

## 10. The fetch list, as the lab's own ask (no fetch before the owner's word, through the monitor)

`research/reads/FETCH-ASK-2026-11-05.md` restates the seven sources with the identifiers RS-2 gives, one line
each; the monitor holds the version it put to the owner, and this file is the lab's refinement of it, not a second
ask. Nothing is fetched until the owner approves each line.

## 11. What this read does not do

It does not rate roadmap items, change a status or a dependency, or copy a date. It quotes no external figure as
its own. It is the lab's design read to the visionary through the monitor; the visionary records what the owner
rules.
