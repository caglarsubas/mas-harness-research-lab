# Research-Lab lane log archive (rule I, 2026-11-17: the lane file keeps its resume block and the last ten entries; older text lives here, unchanged)

Moved from handoff/LANE-RESEARCH-LAB.md on 2026-11-17 (the file as it stood: sha256 prefix a575214e). Three parts, each unchanged in wording: the Resume here
note as it stood, the superseded status notes, and the dated entries older than the last ten (40 moved on 2026-11-17, one more with
each later lane entry, appended at the end in the order they leave the lane file). The resume log page research/resume-log.html
shows them beside the lane file's entries.

## The Resume here note as it stood on 2026-11-17

2026-11-10, PAUSED; LAB-REPO-001 MERGED: R13 main 2e977f4f5a3162bd2ec3e939b9c2c16c8956a994 (tree ff349d61 = the approved head 080513a0's tree, parent cc92594d; PR 2, verify 6/6 in 3 s, check run 128945583698; issue 1 CLOSED by the monitor's note); the local clone's main fast-forwarded; later R13 packets go on branches from 2e977f4f; every push, heavy run or fetch still on the monitor's word; the paused research rounds resume only on the word; later 2026-11-09: R13 issues 3 and 4 triaged (RL-M77) and remediated on the bridge (RL-M78); the R13 PR waits for the owner's word; later 2026-11-09: E1 tool read delivered with findings (RL-M81), v2 re-read PASS (RL-M82); 2026-11-10: SC-D1 correction F adopted, the lab's heavy share (RD-D1's 60/25/15 split) paused until one deployable runs end to end, nothing changes under the standing pause (RL-M83); owner-requested self-criticism of the lab's R&D decisions written, research/reads/LAB-SELF-CRITIQUE.md 8cf22653, corrections A-K proposed as SC-D2 (RL-M84); owner (a) adopted A-K (MON-SC-D2), applied in the charter, the register and this file; D and K in force, I and J on resume (RL-M85); 2026-11-12: owner-approved single fetch of the Agent Laboratory repository page (AL-1, sha256 6b76db5f, head d9017d90) and the lab read research/reads/AGENT-LABORATORY-LAB-READ.md 6d86b6af: a method reference for rules D, I and J and a later tenant workload, no roadmap item recommended (RL-M86); MON-RL-M86: owner "Method reference only" + "Prepare the R13 PR", GO to prepare: branch codex/lab-sync-a2482753 in the local R13 clone, head 9992d175 (tree 2112241e, parent 2e977f4f), research/** = bridge a2482753 byte for byte + MANIFEST 62c8725e (325 files), 37 A / 9 M / 0 D, six commands PASS, scans 0; NOT PUSHED, head/tree/claims reported as RL-M87; MON-RL-R13-PUSH-GO: owner "Approve push 9992d175 (Recommended)": pushed exactly 9992d175 to codex/lab-sync-a2482753, PR <owner>/mas-harness-research-lab#5 OPEN (refs/pull/5/head = 9992d175), body 8e8f3c89 (12/12 claims), transport-approval file 4694ddcb unplaced in the session-neutral tmp folder, reported as RL-M88; file installed by the owner (MON-RL-R13-VERIFY-GO); MON-RL-R13-ROUTE: the verify was REFUSED before launch (check run 2 s: harness-onion main has 0 packets naming R13 with the head branch; exactly one required), SLIP recorded (every lab PR needs its own harness-onion packet naming the repository and head branch, inheriting the six commands); owner "Ride slot 288 (Recommended)": R00 adds a lab-sync packet to slot 288; PR 5 stays OPEN at 9992d175, no push or rebase, the transport file stays valid; packet inputs sent as RL-M89 and written for R00 as LAB-SYNC-288-inputs.json (sha256 e4125198, 0444, in the session-neutral tmp folder; RL-M90); the verify after 288 merges, on the monitor's word; the merge is the owner's; MON-LAB-FACTORY-2: owner "Adopt all eight (Recommended)"; RL-23 PREREG v1 FROZEN research/experiments/RL-23/PREREG.md 467c636c, H-37..H-44 registered, outcome attempt 1 PENDING; prereg_check PENDING rule patched 54ddffc7 with 3 self-test vectors (RL-M93; ships in LAB-SYNC-002); review r1 FAIL closed by PREREG v2 969489d7 (RL-M94); r1/r2 records ec70ead7/82447e60 with redacted brief copies; review r2 FAIL closed by PREREG v3 0fa0d594 + the monitor's 18.90 constant correction; claims 21/21 PASS (MON-LAB-FACTORY-7); evaluator rl23_factory.py 9c08695c, preflight finding P1 -> PREREG v4 2bbd9728, preflight PASS 14 fixtures, v4 claims 26/26 (RL23-V4-CLAIMS.py e4a6bd29), v4 closed PASS by claims (MON-LAB-FACTORY-8, checkpoint e9cc04fb); the pre-period delivery expected 2026-11-13 ~12:00, checked by `rl23_factory.py check` and held until the stop date; night window open on LAB-NIGHT-GO, tonight's queue EMPTY 7706a55b; 2026-11-13 MON-ISSUE6: bridge issue 6 ACCEPT, evaluator a2aeed82 with 20 fixtures, PREFLIGHT.json a1ce2b3d, PREFLIGHT.md 91ce7222, attempt 2 stays PENDING, note file ISSUE6-NOTE.md sent as RL-M98; 2026-11-14 MON-R13-PR5-MERGED: R13 PR 5 (LAB-SYNC-001) MERGED, squash 25b11c5d (parent 2e977f4f, tree 2112241e = head 9992d175), R13 main now 25b11c5d; local clone main stays 2e977f4f until the monitor's fetch word; LAB-SYNC-002 branches from 25b11c5d; 2026-11-14 MON-R13-ISSUE6: R13 issue 6 ACCEPT, successor read CONTRACT-286-QC2-LAB-READ-V2.md 817e1e2b + tools/e1_control.py 374ece1b (selftest PASS) for LAB-SYNC-002, no PREREG or outcome touched, note R13-ISSUE6-NOTE.md 478e07ba sent as RL-M99; 2026-11-15 MON-C15-R13: RL-23 attempt 2 collection OPEN under v4 (tier LIGHT, C14-C16), run record runs/run-001.md 900a8a32, OUTCOME.json e118c066, spot-check slot 289 pre-registered, no delivery opened yet, reply held for the pre-period delivery; MON-PACE-HOLD 2026-11-15: HOLD attempt 2 until 19:45 +08:00 and the monitor's RESUME (C15 pacing, 5-hour window 74 %), no new agents, no reply needed; MON-RL23-PRE 2026-11-15: the pre-period delivery is announced, NOT opened (hold): research/experiments/RL-23/deliveries/pre-period-2026-11-05_11.json sha256 11445fda9dd7a977, 23,479 B, checkpoint fe3bce99, days 63 / windows 8 / changes 0 / slots 3 (285-287), fidelity h1-h8 all false, omissions listed in a provenance member; the monitor's points for the report: (1) 287 stepMinutesMean 21.60 by the slot-id rule vs the extractor's 19.80 (287 is descriptive only per section 3), (2) Nov 11 stops 3 in STATE.md vs 2 in FACTORY-IMPROVEMENTS.md, STATE.md used, (3) a Lane-Monitor session first appears Nov 11 with no restart record (not in changes[]; pre period), (4) FACTORY-IMPROVEMENTS.md now d4111fa4 vs the pinned 0bc476b1 (constants read from the PREREG), (5) the producer reads included a few argument-handling source lines (data-rule point to check at intake); intake after the RESUME = digest check + `check` + delivery-log row + today's one message; MON-RL23-PRE-V2 2026-11-16: INGEST v2, not v1: research/experiments/RL-23/deliveries/pre-period-2026-11-05_11.v2.json sha256 0a720805cb2b3740, 0444, checkpoint 3404e53f, the monitor's own check ACCEPTED (days 63, windows 6, loadEvents 0, slots 0, changes 0); v1 (11445fda) failed check per bridge issue 11 and stays for provenance; v2 changes: windowEnd host-local, 2 windows without a recorded windowEnd excluded, slots 285-287 excluded (no recorded kind), loadEvents [] documented NOT COLLECTED (empty = unavailable, never zero; issue-6 rule applies); for the analysis: this pre delivery carries no slot and no load-event units, so H-39's pre events and H-40's pre slots (285-287) must come from a later delivery or read U1/U2 at the stop; still on pace hold, intake only after the RESUME; 2026-11-16 MON-PAGES-RL-1: research.html REDESIGNED on the shared sheet (builder 2f09c716, page ff6035ca, resume-log.html 70a10942, data files byte-equal, lock paper LOCK-PAGES-RL-1.md fbb83d9d, claims 2b886c0f PASS), applied on the tree uncommitted, sent as RL-PAGES-DONE; VERIFIED + checkpoint 39fa12f7 (MON-PAGES-RL-2); NEXT when pages.css v2 lands (owner bug: bar vanishes narrow, tab click scrolls the tab row away): rebuild on v2 on an export, same claims + 700 px check, send RL-PAGES-V2-DONE before applying; DONE 2026-11-16 MON-PAGES-RL-3: rebuilt on v2, page a0e8b51e 449,019 B, resume-log 8bfc0310, probe PASS 375/700/1280, applied on the tree, the monitor verifies and checkpoints; MON-PAGES-RL-4 ruled the budget: at most 0.6 MB measured and 2,500 landing elements, archive page as the next lever; rule written under (b)); MON-291-SUCC-R13 2026-11-16: LAB-TRANSPORT-001 draft 1a693123 answered NO (manifest pins the runner; add research/MANIFEST.json to allowedPaths), rest YES; expected manifest after the swap d7c3facf, 325 files OK, bridge-commit a2482753 stays, sent MON-291-SUCC-R13-2; revised draft b3fc1a0e answered YES, six acceptance commands pass on the swapped export; USAGE STOP 2026-11-16 (weekly 98 %): no new work until the monitor's RESUME, 2026-11-22 04:00 local; open on resume: RL-23 attempt 2 intake of the v2 pre-period delivery (after the pace-hold RESUME), the LAB-SYNC-002 packet after LAB-TRANSPORT-001 merges, the next full page build under the 0.6 MB rule

**The note of 2026-11-17 (replaced on 2026-11-18), unchanged:** 2026-11-17, ACTIVE for light work by day on the monitor's word (handover 15, a new session on this account; the heavy share stays paused by day, a night run needs a filed queue and LAB-NIGHT-GO): R13 main 25b11c5d (LAB-SYNC-001, PR 5), the local clone unfetched at 2e977f4f; RL-23 attempt 2 collecting under PREREG v4 2bbd9728 with evaluator a2aeed82, the gated evaluation once at the stop 2026-11-26 or earlier when every post unit is complete; LAB-SYNC-002 rides slot 292 on branch codex/lab-sync-002 from 25b11c5d after a fetch word and LAB-TRANSPORT-001's adoption PR, carrying pages.css, glossary-families.md and a regenerated manifest; the research page budget is 0.6 MB measured and 2,500 landing elements; 2026-11-17 MON-RL-H15-RESUME: the v2 pre-period delivery 0a720805 ingested by digest and check (ACCEPTED, delivery log in run-001), rule I applied (the progress view is generated by the builder; this file trimmed to the resume block and the last ten entries, older text in research/resume-log-archive.md) and rule J applied (minutes and tokens in the register's effort cell, tokens owed by the monitor's meter); next: one message a day, post-period deliveries by check only

## Superseded status notes

- STATUS: STANDING BY (owner, 2026-11-06, via the monitor: experiments wait for arranged inputs; no searches or
  fetches until an experiment needs one; weekly usage the reason). Resume point: 22 experiments closed and reported
  through RL-M36; the procedure and progress documents in place (RL-M37); nothing in flight. On the monitor's word:
  follow research/progress/README.md's procedure per scope, starting with the scope whose input arrives.
  REPOSITORY (owner proposal 2026-11-06, in the lab's chat): a lab repository for PRs and gpt-astra issues; the
  lab's proposal and three owner questions in RL-M38; the migration plan on paper in
  research/reads/REPO-MIGRATION-PLAN.md (draft 1); the owner decided (2026-11-06): gpt-astra = another LLM provider's GitHub App with read and
  issue-opening rights; verifier-numbered like the other sessions; public; repository created as
  <owner>/mas-harness-research-lab (RL-M40 relayed); the repository is R13 (kind meta), registered by R00 at slot 282 with MET-VERIFY-007 and carried
  by bundle v7; the page build must link into the repository (or drop tree links) before the bridge mirror form;
  nothing committed or pushed before the bundle and the monitor's word (plan draft 2, section 3a).
  Earlier the same day: ACTIVE. OWNER DIALOG (2026-11-06, in the lab's chat box): work as a research team by the
  procedure observe / hypothesise / collect data / design and test / report and prove; one progress document per scope
  for the owner (research/progress/README.md and S1..S6, kept current at every result, listed on the page); deep
  search permitted for "what others have done so far" (the session's web search and fetch tools; sources by identifier
  and digest; every fetch reported to the monitor; nothing from the records in a query); charter section 1a records it;
  RL-M37 told the monitor. RL-19 (H-24 grounding step) RUN and CLOSED: UNRESOLVED as preregistered (24 of 29
  figures found mechanically, 28 of 29 by hand; Harness-Bench's "more than 5,000 trajectories" not in its text).
  RL-20 (H-25 TopologySpec half) RUN and CLOSED on the fresh c1b838be export (tar 79fb0d22, in the lab scratch):
  H-25a PASS (52/52 vectors), H-25b FAIL as preregistered (21/22; the accepted edit a no-op on a one-node topology);
  two classes unexpressible in the form. RL-21 (H-26 contract-text half) RUN and CLOSED: PASS under the
  creator-linkage operationalisation (the authority records: one creator per published path, every change names its
  creator); the authority map and the trace half stay BLOCKED. Twenty-one experiments. The monitor's GO for H-23 (paper)
  followed (RL-M35 reply); RL-22 (H-23 coordinator half: a clean-room board state machine from MAS-RA-004's README
  section A2, run on the 32 transcript and 11 binding vectors; VERIFY's ledger binding declared un-modelled) has
  RUN and CLOSED: UNRESOLVED as preregistered (38 of 43 vectors from the README alone; the concurrency scope and the
  two outside models are the points to ask the author); RL-M36 sent. Twenty-two experiments. NEXT: nothing light is
  READY without an input; the monitor arranges inputs (R10 transcript export for H-29; owner run plan for H-33; R12
  oracle run for H-34) when needed; H-02's shadow half waits for MET-PERF-047; a corrected coordinator machine is a
  new id if the monitor wants it. This session's context is near its limit: resume from here after compaction.
  Earlier (the STOP of 2026-11-06 early): RL-18 CLOSED and reported (RL-M30); RL-19 then not started: no PREREG; the only thing done was an instrument
  trial (a standard-library text extraction over the five held papers) that ran slowly and was stopped at the order;
  its outcome is unknown and nothing was recorded; the five held files stay by digest in the lab scratch. On the
  monitor's resume word: RL-19's PREREG (figure check of RS-1/2/3 against the five held papers; decide the extraction
  method first: a stdlib extractor if the trial shows digits, else page reads), its review, run; then the fresh
  c1b838be architecture export for H-25/H-26 (approved to follow without a new word). Earlier the same day: ACTIVE
  since the monitor's RESUME after the 5-hour reset. RS-3 received from the owner in the lab session (2026-11-05,
  "Academic Papers for Planeon Roadmap.md", sha256 930f89a0d252f948b5a393044007e4b8e87174f6617d4cad586fa9eea63ab840,
  745,965 B with 62 embedded images): read in `research/reads/RD-ACADEMIC-PAPERS-LAB-READ.md`; register H-32..H-35
  added (all BLOCKED); the second-tier fetch ask restated with its identifiers (MAS-ProVe now arXiv 2602.03053);
  no copy kept; nothing fetched. RL-17 (H-27 replay half) RUN and CLOSED: FAIL as preregistered (deterministic; C3
  reproduces; duplicates refused; stale replays refused by holder/state, UNRESOLVED on the version clause; the log
  does not replay merges through a fresh board). RL-18 (H-31) RUN and CLOSED: FAIL as preregistered on expressibility (the manifest form
  needs a positive token budget; a simulation has none), the lab's gate reproducing all 85 contract vectors, agreement
  7 of 9; RL-18-PROPOSAL in the report. NEXT (the monitor's standing word, light, PREREG review first): RL-19 (the
  five held papers' figures checked against RS-1/2/3), then the fresh architecture export at c1b838be for H-25/H-26. RL-15 (H-30) RUN and CLOSED: FAIL as preregistered (the
  expected class): attributed recall 10 of 18, 0 false positives; the process rule (status change without an update
  entry) and the digest rule are not covered by build_roadmap's validators; RL-15-PROPOSAL (two candidate validators)
  in the report, for the visionary through the monitor. Five review rounds under v5 1e8dfc4a; the run used a scratch
  copy of roadmap/ at bridge fce8245b only. RL-16 (H-02 cost-model half) RUN and CLOSED: PASS (attested share
  re-derived; equal-load growth 9.34 s per slot [5.73, 13.50]; the 5/10/20 percent table at cadence 10); two review
  rounds under v2 8788236b. Sixteen experiments run. NEXT (light, by the lab's score): H-25 (static checker over the
  TopologySpec vectors), H-26 (one writer per governed state, contract-text half), H-27 (replay on the b4bbea79
  export), H-31 (MAS-RA-002's gate on the CONF-MAS ledgers); each needs an export or the RL-03/RL-04 scratch export
  (kept) and a PREREG review first. The shadow-period half of H-02 waits for MET-PERF-047. Earlier today: ACTIVE since the monitor's MON-RL-RESUME
  relay (2026-11-05, after the usage reset). RL-M23 (re-opened,
  standing by) and RL-M24 (the design read) sent to the monitor. Done on resume, in the MON-RL-M22 order: (1) the
  lab's (a)-(e) design read, v2 after the owner supplied both roadmap files in the lab session:
  `research/reads/RD-ROADMAP-LAB-READ.md`; RS-1 = RS-MEMO-RDROADMAP (sha256 checked against the recorded value before
  reading); RS-2 = a second, new owner-supplied document "Academic Evidence, Prioritisation and Agent-Executable
  Research Programme", sha256 5b30977bfef178e097728c37618983b1f0d6273b99e5c2c6e2150d9a50b4441e (60,459 B, 505 lines),
  proposed to the visionary as RS-MEMO-RDACADEMIC, OWNER_SUPPLIED; no copy kept of either (MON-RL-M21). (2) the
  visionary's register suggestions reconciled (read section 8): register columns stream / P/E / outside RS-1 /
  outside RS-2, rows H-25..H-31, milestones M-G1..M-G4; charter edits (PREREG review step 1a, evaluator rule, ECU in
  the run-plan form, 60/25/15 by queue class, six reportable-result gates). (3) the seven-source fetch list restated
  with RS-2's identifiers as the lab's own ask: `research/reads/FETCH-ASK-2026-11-05.md`; nothing fetched.
  Condition (v) and Q-CC2-4 read for R00 and the visionary: `research/reads/CC2-CONDITION-V-LAB-READ.md` (adopt (v)
  bounded; N_shadow (a) one cadence, 10 slots; 15 s reader cap; disagreement classes A/B/C restart the count).
- FETCHES (owner "The 5 identified lines (Recommended)", second tier "Not now"): six GETs done, five held (F2, F4a, F4b,
  F5, F6), F7 a bot-challenge page, never retried; record `research/reads/FETCH-RECORD-2026-11-05.md`; files by digest
  in the lab scratch only.
- RL-14 (H-28 observational half): RUN 2026-11-05 under PREREG v4 02ef7761 after reviews 1-3 FAIL and review 4 PASS
  (charter step 1a, first use): UNRESOLVED as preregistered (rho +0.124, clustered interval [-0.413, +0.358], n 23);
  run-001 bcfa5c1b, RESULTS 93f2bc9c; inputs pinned at bridge 46c7d6e2 and extracted at that commit because two lane
  files had moved on by the run. CLOSED under this id.
- NEXT (light, no GO needed, by the lab's score): RL-15 H-30 (scratch copy of roadmap/ only); RL-16 H-02 cost model
  T(N); then H-25, H-26, H-27, H-31 halves. Each gets PREREG-REVIEW.md before its run. The H-02 shadow-record
  experiment waits for MET-PERF-047's first shadow verify.
- PAUSE HISTORY: PAUSED 2026-11-04/05 by MON-RL-PAUSE at weekly 61 percent; resumed as above. Thirteen experiments run (RL-01..RL-13); every one has PREREG, run record(s),
  RESULTS in the verdict-ledger form and a REPORT; nothing committed (the monitor's checkpoint folds research/**
  and this file). Both scratch exports (RL-03's conformance-labs tests/mas at b4bbea79; RL-07's harness-onion
  architecture at afee03b9, with the chain, cost-report, host-interface, gate-channel, ledger, run-manifest and
  run-events subtrees extracted) stay in the lab scratch until the monitor's word; move to the Trash, never rm.
- OWNER DECISION (2026-11-05, given directly in the lab session: "Yes, on resume"): the owner-supplied document
  "R&D Roadmap for MAS-Harness / Planeon" (markdown, 42792 bytes, sha256 61fa9041f2399f52..., kept by the owner; the lab holds no copy
  yet) is applied on resume as a design read to the visionary through the monitor: (a) potential and effort scores per
  register hypothesis, recomputed from our records; (b) its four decision gates as register milestones tied to H-02,
  H-06, H-12, H-17; (c) independent review of every PREREG before its run (RL-10's clause slip is the case); (d) its
  ECU compute unit and 60/25/15 split for the run-plan form; (e) six candidate hypotheses (static workflow checking,
  one authoritative writer per governed state, concurrency/replay correctness, typed memory and handoff, gate
  interleaving, a seeded-inconsistency benchmark for the roadmap build). Its dates, staffing figures and citations
  stay as reported, not reproduced. Filing (MON-RL-M21): no second copy; lock 29 at 279's merge records it as research
  source RS-MEMO-RDROADMAP by full sha256, OWNER_SUPPLIED; the visionary's read is visionary/RD-ROADMAP-READ.md 5836de7f
  and its lock-29 staging visionary/LOCK29-RD-D1.md f0264b57 (not read by the lab under the pause).
- FIRST ITEMS ON RESUME, in the order of MON-RL-M22 (owner: "what research-lab said is more important than what
  visionary said"): (1) the lab's (a)-(e) design read above, first and leading; (2) the visionary's section-2 register
  edits (stream and outside-rank columns, milestones M-A2..A4, H-25, the H-09 note, the runner/evaluator split in
  research/README.md) weighed as input and reconciled to the lab's read where they differ, the visionary reconciling its
  roadmap notes to the lab's read before they apply; (3) the seven-source fetch list as the lab's own ask, approved
  through the monitor.
- LIVING PAGE (owner 2026-11-05, built under the pause as the owner's direct ask; location research/ confirmed by the
  owner, "Keep under research/"): research/research.html, rendered by
  research/build_research.py from the register, every experiment folder, the charter and this block, with
  research/research.json (the data record, sha256 prefix per source) and research/history.json (a snapshot when counts
  or verdicts change). Rule: rebuild after every RESULTS or REPORT is written and at every RL-M milestone, scan the
  three outputs, name the page digest in the milestone message; the monitor's checkpoint carries them with research/**. The owner's "Yes, on resume" sets what is done on resume; the
  resume word itself comes from the monitor after slot 279 merges.
- On resume: (1) read this block and the register's RL rows; (2) the only READY items without an experiment are
  H-23 (clean-room implementation sketch of the topology/coordination contracts against their vectors; paper) and
  H-24 (the crosswalk method note; paper); (3) BLOCKED items wait on their named roadmap items; (4) H-07b gets
  arms when a K 8 PERF packet's verifies exist; (5) RL-02's oracle side and finding identity wait on the
  DECISION-LEDGER-001 / REVIEW-RECORD-SERIES-001 notes; (6) counterexamples 1-17 wait on a host-interface amendment.
- RL-13 (H-22): PREREG 2f7a6389, MAPPING 1bc341c2, run-001 d4113a19 (two logged repairs per instance), RESULTS bc0ee3b8 PASS with
  two unresolved checks (one contract positive refused by the lab's checker; the pinned conventions unverified),
  REPORT dcb63e6c. CLOSED.

- RL-01 (H-07): PREREG v1.1 db893373; RESULTS bb670fd6 (v2, supersedes d1977cc2), REPORT 5f6af501. H-07a PASS by gate
  (load drives; C vs K collinear, unresolved). H-07b UNRESOLVED: I3 (R00's K 6/8/6 at bd882493, summary sha256
  85ab23bf, relayed figures only) is one K 8 run, non-comparable. CLOSED unless R00 runs more arms.
- RL-02 (H-09): v2 RESULTS 226bd62d UNRESOLVED (no oracle record; ids carry the round). Proposals ruled by the
  visionary (MON-RL-M6): RL-02 (a) finding identity → REVIEW-RECORD-SERIES-001 scope, gate material, owner approval;
  RL-02 (b) oracle block → DECISION-LEDGER-001 note. CLOSED until those land.
- RL-05 (H-03): FAIL as stated; P_t proposed → DECISION-LEDGER-001 note. CLOSED.
- RL-03 (H-19 first clause): PASS (RESULTS 213d27e6, REPORT aa5ddd1a; runs 001-003 on GO-RL03-1/2/3): the four breach
  rows and the 15 arm pairs reproduce exactly on pin b4bbea79 (export 90fdfe4d in the lab scratch, kept for RL-04).
  CLOSED.
- RL-04 (H-13 + H-19 second clause): RUN on GO-RL04 (640 runs, 8 s, point by point; script 01d4e4d4, the frozen
  b6d585e4 plus raw paired differences in the output, disclosed in run-001 e1bcd872). RESULTS 9c9116c4 (overall UNRESOLVED
  for H-13a by input; H-13b PASS by gate; H-19 second clause PASS as 'lower than advisory', 'vanish' false), REPORT
  5fbc3a25. Finding: the whole leasing effect is the DECENTRALIZED family's; CENTRAL shows none and pays about 30
  percent makespan for leases. RL-04-PROPOSAL ruled (visionary via MON-RL-M9; not a roadmap shift, not gate material; dated notes at lock
  29 at 279's merge): MAS-STRATEGY-001 (leases required where claims are peer-to-peer, optional under one
  coordinator), MAS-RA-004 (the contract mandates leases in both modes; a topology-conditional successor would be
  CONTRACT material through R00; claimOverlap 0 in all 640 leased runs is the safety evidence), MAS-RA-010-F
  ('vanish' measured as bounded). Register rows H-13 and H-19 carry the ruled wording. CLOSED. The
  scratch export is kept until the monitor confirms R12 needs nothing more; then Trash.
- RL-06 (H-10): RUN light (MON-RL-M8 go-ahead): PREREG 301c2783, run-001 c2d49f64, RESULTS 49802c4e (H-10a PASS: 3.1 merges a
  day, verify median 743 s per merge, 2 review rounds; H-10b FAIL as preregistered: a keyword taxonomy over MON ids
  leaves 70 percent OTHER, the ids are incident-specific), REPORT 42bfbc07. CLOSED; a text-level v2 only with the
  monitor's permission to classify rule lines (counts only).
- RL-07 (H-01): RUN light on the architecture export 948a20fa (afee03b9) with the four evaluator modules (v1 1ec76480,
  v2 23fe723a, v3 29483ec3, safe_yaml 99c67356; MON-RL-M10b/c), run 002 on harness-onion's .venv interpreter (PyYAML)
  read-only. PREREG 67617917 (v1.2), runs c8b5eb39 / 870361ca, RESULTS acf365ff PASS on the published vectors (116 of 116) and the
  identity rule's evidence; unresolved: live-chain step rule and equivalence not replayed, P3's 'oldest layer' not
  fixed by the vectors (input for R00: add the refusing slot to pin-refusal vectors). REPORT 69758154. CLOSED.
- RL-08 (H-08): RUN light on the cost report inside the RL-07 export (MON-RL-M10b ruling, MON-RL-M11 go-ahead):
  PREREG 1e085298, run-001 859332ff, RESULTS 59d261c7 UNRESOLVED (H-08a no refusal history; H-08b between bounds: top-decile
  shares 0.34 files / 0.31 layers, Gini about 0.5; argv 63 = 0.86 of verify CPU, descriptive), REPORT 3c99a158. CLOSED.
- RL-09 (H-18): RUN light on the export's published records (MON-RL-M13 GO; inputs listed first, accepted):
  PREREG 4387dbff, run-001 0837ee60, RESULTS aa69f568 FAIL as preregistered on paths 18-28 (5 covered, 4 uncovered: gate-rule
  paths A3/C4/C6 and a cgroup search; 2 untestable; 1-17 not enumerated anywhere published, per the monitor's search),
  REPORT 81d2cf84 with RL-09-PROPOSAL (each counterexample names its enforcing family; H-18 widened to the gate-channel
  contracts), to relay. CLOSED; a v2 with the gate-channel and admission records as a fifth family is a new id.
- RL-10 (H-04): RUN light (MON-RL-M14): PREREG 9e5db1c5, run-001 d1bd456d, RESULTS 023591f8 FAIL as preregistered (C2 clause 2 was
  scoped per ledger, the rule is per claim; per claim the composition holds: 7/7 ledger refusals and 13/13 native
  refusals agree with the shared five-level order; both maps total), REPORT 1a999a40. CLOSED; a per-claim restatement is
  a new id only on the monitor's word.
- RL-11 (H-18 widened, MON-RL-M15 GO; R10's cited ids MON-RL-M16; the visionary's cells MON-RL-M17 as expected
  state): PREREG b06eabdb, run-001 28cbcd62, RESULTS b6d7d416 UNRESOLVED (no path uncovered; 10 of 11 covered, 24 not joinable
  by token, 28 by a README mention only; cells agree), REPORT b2acd25f with the W03 note inputs (MON-RL-M19 routing correction applied) (closed by join / missing
  clause per path). CLOSED.
- RL-12 (H-04 per claim, MON-RL-M18 GO): PREREG d1763b97, run-001 f6cda7ff, RESULTS 72d2060f PASS (7/7 per claim, 2 vacuous;
  13/13 native), REPORT eba7fd47; disclosed as a restatement of RL-10's post-hoc reading. CLOSED.
- Twelve experiments run (RL-01..RL-12). READY register items without an experiment: H-22/H-23/H-24 (paper).
- READY register items without an experiment after RL-11: H-22/H-23/H-24 (paper).
- Not committed: the monitor folds `research/**` and this file into its checkpoints.

## Entries older than the last ten

- 2026-11-07 (owner's direct word in this session's chatbox, the channel the owner rule allows): "there is nothing
  pushed in our research-lab github repo. we should record our research related works (codes, documents, any
  artifacts, etc.) into this repo. so the gpt-astra can read the repo and open issue record on it that we can track
  and fix". Done the same day: a clone of `mas-harness-research-lab` beside the other repositories; `research/**`
  exported byte for byte from bridge commit a67b90a5 (git archive, 230 files), plus the root `README.md` (layout,
  manifest check, how to file an issue, rules), `LICENSE` (the canonical Apache-2.0 text, c71d239d), `.gitignore`,
  `research/tools/make_manifest.py` and `manifest_check.py` (stdlib; `planeon.research.manifest/v1`; the check
  refuses missing, unlisted or changed files, symlinks, bytecode and `.github`) and `research/MANIFEST.json`
  (235 files, bridgeCommit a67b90a5). Scans before the push: privacy_scan 0/0/0/0 over 236 files, no handle, no
  home paths, no symlinks, no `.github`. Pushed as the first commit on `main`: cc92594d6daa, 236 tracked files;
  issues are enabled. CONSEQUENCE for LAB-REPO-001 (draft 4, 5cfe26ab): the Tree contract's "main before the PR =
  the owner's LICENSE-only commit", the route's file-set anchor and the rollback line no longer hold, since R13's
  main is populated. Pending the monitor's ruling (RL-M46): (a) re-key the packet on the populated main (file set =
  head's name-status against cc92594d; the packet then adds the ci transport, the remaining tools and the YES
  record only), or (b) R13 leaves the packet route. No draft 5 until the ruling; nothing else changed. Issues
  filed on R13 reach the lab through the monitor (owner's issue-tracking rule).
  MON-RL-R13-MAIN (same day): the push is checked by API and stands as the owner's direct word; the (a)/(b)
  question and the open points (direct pushes before v7, when the ruleset goes on) are with the visionary, then
  the owner. UNTIL THAT RULING: no further pushes to R13 and no draft 5; issue_poll already covers R13.
  MON-RL-R13-FREEZE (same day): the owner ruled "Freeze until v7", the visionary (a): R13 main stays at cc92594d
  until v7 serves R13 (recorded as the owner's initial commit); branches only, no push to main, a further push
  only on the owner's word through the monitor and each re-keys the packet; LAB-REPO-001 re-keys on that base
  (head adds only the packet's files, MANIFEST.json M, rollback "main returns to cc92594d"); App install and
  ruleset main-verify together at v7's install, before 284's PR. Draft 5 GO on paper: DONE as
  `research/reads/LAB-REPO-001-PACKET-DRAFT.md` de12ac97 (YAML sha256 88159c5f; 27 replacements: objective,
  allowedPaths + .gitignore, Tree/Manifest/Page-check/Route/v7 contracts, deliverables, sixth command =
  research/tools/page_check.py, evidence, rollback, plan tree + .gitignore and reviews/, C7, D, E, F). Lab
  reading flagged as Q-LAB-6 (applied with the recommended (a)): the three page files are M too, since the data
  record enumerates research/tools and research/reads. REPO-MIGRATION-PLAN.md got a status note (cf6eb2a1).
  Sent as RL-M48; ACCEPTED (MON-RL-DRAFT5): de12ac97 with YAML 88159c5f as the future route key; Q-LAB-6 RULED (a).
  The draft is not re-edited for the ruling (its digest is the accepted one). NEXT: the final freeze before v7's c2 (a new runner digest or a push to main = a new named
  delta), then the YES before 284's c2; section-D work on the monitor's word; paused otherwise.
- 2026-11-07 (MON-RL-ISSUES, the owner's word relayed by the monitor, verbatim): "issue-tracking task of yours should
  include the [mas-harness-research-lab] repository. we should share the issues with our research-lab session and ask
  its acceptance of action (full, partial or rejected) and expect him to take actions or plan them as codebase changes
  or roadmap changes". Standing task, allowed while paused: the monitor's poll covers R13 and relays each new issue
  (number, title, body) as data; the lab answers ACCEPT, PARTIAL or REJECT with a note of 10 lines or fewer, which the
  monitor posts (the lab never comments on GitHub); then the lab acts or plans: an R13 codebase change goes on a
  branch while main is frozen at cc92594d6daa (it rides LAB-REPO-001's PR or a later lab PR under v7's route, any push
  on the monitor's word); a roadmap change goes to the monitor for the visionary; a research change (register, PREREG,
  a new hypothesis) lands on the bridge's research/**. Heavy runs, fetches and experiments still need the monitor's
  word. No R13 issues yet. Acknowledged as RL-M50; the rule is recorded in (b).
- 2026-11-07 (MON-RL-C2-RUNNER): triage rule accepted (lane 951afac0). 283's c2 is built locally (65ac19df) and the
  runner ci/run_packet_argv.py is unchanged at c8ac40f0 (9,084 B, 100755), so draft 5's pin stands as written;
  provisional until 283 merges. The freeze word comes before v7's c2. No draft 6 needed for this. Acknowledged as RL-M51.
- 2026-11-07 (MON-R13-ISSUE-1, first R13 issue, "Initial research review: claim validity, reproducibility, and
  experiment priorities", masked copy d2f606c5, read as data, no link followed): triaged in
  research/reads/R13-ISSUE-1-TRIAGE.md (100295c1): 1 ACCEPT (CLAIMS table + milestone decision column, RESEARCH;
  page column post-v7 CODEBASE), 2 PARTIAL (LAB-REPO-001 already plans it; draft 6 at the freeze adds reproduction
  levels + external-input provenance to rerun_table.json; wrapper command deferred), 3 PARTIAL (RL-22 successor with
  obligation-level gates + H-27 mid-run stale vector, RESEARCH), 4 ACCEPT (review-record data dictionary + the
  visionary's disposition of RL-02/RL-15-PROPOSAL, ROADMAP + RESEARCH), 5 PARTIAL (RL-04 successor, RESEARCH), 6
  PARTIAL (RL-16 shadow successor with seeded fault classes; RL-11 coverage map; paths 1-17 an input request), 7
  PARTIAL (protocol instrument preflight + effort columns; no separate queue). Note of 9 lines drafted for the monitor
  to post; the lab never comments on GitHub. Sent as RL-M52. Light work listed there starts on the monitor's word.
- 2026-11-07 (MON-R13-ISSUE-1-POSTED + MON-R13-I1-LIGHT GO, light, bridge research/** only; MON-R13-I1-DISP recorded):
  (1) research/hypotheses/CLAIMS.json (45 claims over 22 ledgers: verdict copied, instrument validity, supported
  scope, unresolved clauses, evidence type/method, replication state RECORDED 27 / LEDGER_REDERIVED 18, invalid cases,
  decision justified; RL-20 H-25b carries the one-node budget edit as INVALID_CASE beside the FAIL) + CLAIMS.md
  rendered by research/tools/claims_check.py (check: every ledger claim exactly once, verdict/status/checks equal;
  CLAIMS OK 45/22); ledgers untouched. (2) research/reads/REVIEW-RECORD-DATA-DICTIONARY.md + .json (17 fields,
  denominators first) + research/tools/review_record_dictionary_check.py run against the v2 schemas at 4b2be353:
  11 fields present in the forms, 2 in the merge-decision record, 0 missing, 4 derived-or-new (findingId's
  supersedes, laterAdjudication, firstDetectionRound/recurrence/unanimity derived). (3)
  research/experiments/RL-11/data/coverage_map.json (28 paths: 1-17 NOT_ENUMERATED; 18-28 with enforcing families,
  rows, tokens and evidence level PROOF 1 / NATIVE_RECORD_ROW 5 / VECTOR 3 / DOCUMENTARY 1 / NONE 18 incl. 24; derived
  from join_results.json; RL-11's frozen files unchanged). (4) README section 2: step 1b instrument preflight (from
  RL-23), the claims-table rule under step 3, step 6 effort/decision columns; REGISTER: two experiment columns (22
  rows, n/r where unrecorded) and a milestone column "decision the verdicts justify" (M-G1..G4); builder parses
  both (counts unchanged). MON-R13-I1-DISP recorded in the register: H-09 (RL-02-PROPOSAL DISPOSED at lock 29: part
  1 a REVIEW-RECORD-SERIES-001 clause, part 2 a DECISION-LEDGER-001 note; H-09a/c/d UNRESOLVED-by-input) and H-30
  (RL-15-PROPOSAL ACCEPTED VIS-RL15, builder change staged before lock 40; re-run 18 + 3 on the monitor's word,
  RL15-D1). MAS-RA-004 README inputs: not needed before R00's next packet. RL-19's data/claims.json stays frozen (the
  claim-level context rule went into README 1b instead). Bridge changes since cc92594d listed in
  research/reads/BRIDGE-CHANGES-SINCE-CC92594D.md for draft 6; the two manifest tools exist on R13 main and not yet
  on the bridge (section-D copy, on the monitor's word). Nothing committed; no push to R13. Sent as RL-M53.
- 2026-11-07 (MON-RL15-RERUN-GO, light): RL-15's 18 seeds + 3 controls on the lock-40 builder 690cff6a (roadmap.json
  a365a8f6), base = git-archive export of roadmap/ at bridge ded99886 (35 files, as tracked) in the lab scratch, frozen
  tools rl15_mutate.py b35e6009 / rl15_eval.py bbe2877c, seed 20261105, CPython 3.12.4, load about 39. STOPPED on a
  miss, as instructed; nothing written under experiments/RL-15 (outputs kept in scratch). Attempt A (work copy not
  named roadmap/ under a parent): precondition failed, the v2 paper-file validator resolves paper paths from the
  repo root, so the baseline refused; invalid, layout only. Attempt B (work copy as <parent>/roadmap): baseline
  clean; seeded refused 17 of 18, attributed 13 of 18 (run-001: 14 and 10); per class [attributed, refused, n] M1
  3/3/3, M2 3/3/3, M3 2/3/3, M4 1/3/3 (run-001 0/2/3), M5 2/3/3, M6 2/2/3 (run-001 0/0/3); controls refused 1 of 3.
  Misses: (i) M6's third instance (a secondary paper's digest, no file in the bridge) BUILT, which the PREREG said
  no file comparison can catch, so 18 of 18 was unreachable by design; (ii) control "updates" refused by the new
  date rule (an update entry without a UTC offset): the frozen benign control is malformed under lock 40's form, a
  false positive by the frozen gate (FAIL region) and an instrument-preflight case; (iii) unattributed refusals:
  M3 "factor keys" (no B2 token), M4 W03 refused first by a different validator (W05 BLOCKED with nothing blocking
  it), M4 CHAIN-COMPACTION-002 refused by the new process rule but its "updates entry" words fall beyond the frozen
  120-character capture (W04's shorter message attributes), M5 "unknown codebase reference" (no token). The two new
  validators work for what a file comparison can catch (M4 2 of 3 by the rule, M6 2 of 3). Waiting for the monitor's
  disposition: record as run-002 under the frozen gate (FAIL region by the control), or a v2 under a new id with an
  offset-bearing control, a longer message capture and the secondary-paper instance declared uncatchable. RL-M54.
- 2026-11-07 (MON-RL15-M54-RULED (c) + MON-RL15-D1-RESTATED, light): (1) RL-15 run-002 recorded under the frozen
  tools and gate: runs/run-002.md, data/rl15_runs_002.json a60da422, data/rl15_runs_002a_invalid_layout.json 4153a89b
  (attempt A), data/rl15_gate_002.json (frozen evaluator: FAIL region by the control refusal; names run-001 by
  construction); PREREG, RESULTS, REPORT unchanged; register RL-15 row and CLAIMS RL-15 decision updated. (2) RL-15b
  as a new id against the visionary's erratum (17 of 18 refused, the secondary-paper instance builds by design,
  older rules run first, new rules M4 >= 2 of 3 and M6 2 of 2 by tag, controls 0 of 3 with offsets): tools
  rl15b_mutate.py 865d5754 (same seed 20261105 = run-002's targets, whole-message capture, tag/older-rule
  attribution, layout assertion, uncatchable instance excluded from the denominator) and rl15b_eval.py 2d6c349b;
  PREREG v1 FROZEN e5a75db2 (R7 dependence declared); preflight step 1b PASS (P0 layout + baseline, P1 21 edits all
  change bytes, P2 evaluator known answers with denominator 17, P3 positive/negative controls, P4 tag beyond 120
  chars; 3 builds; PREFLIGHT.md; addendum after review note 3: M4 = 1 reads UNRESOLVED, a zero-refusal class reads
  FAIL); blind review 1 PASS, five non-blocking notes handled in PREREG-REVIEW.md. No RL-15b run (waits for the
  monitor's word). Scans 0/0/0/0 on every new file; no bytecode. Bridge-changes list regenerated. RL-M55.
- 2026-11-07 (MON-RL15B-RUN-GO, light): RL-15b RUN and CLOSED: fresh export of roadmap/ at HEAD 8df395a5 (identical
  to the pinned ded99886; builder 690cff6a asserted, manifest 620799a0 = the PREREG's pin), 22 builds in 15.2 s at
  load about 25 beside R00's heavy job; PASS as preregistered: 17 of 17 catchable refused and attributed (lock-40
  tags 4: M4 2 of 3 by the process rule, M6 2 of 2 by the digest rule; older rules 13, the third M4 by "is BLOCKED
  with nothing blocking it"), unattributed 0, crashed 0, the uncatchable secondary-paper instance built, controls 0
  of 3 (the offset-bearing entry builds); equals the erratum's expectation instance by instance. run-001 af1e9122,
  data f445e3c1, RESULTS d1810a57 (RL-15b-RESULTS-v1, H-30b SUPPORTED), REPORT 5a7ddc20 (review notes 1, 2, 4, 5
  handled in the record and the report). Register: RL-15b row RUN, H-30 status names RL-15b PASS; CLAIMS row H-30b
  added (46 claims over 23 ledgers). No re-run; verdict recorded as it came. Sent as RL-M56; the monitor relays to
  the visionary. Nothing committed; no push to R13.
- 2026-11-08 (owner's word in the lab session: "Meta-review pass", after the lab's read of the co-scientist blueprint;
  light, bridge research/** only): one meta-review over the blind PREREG reviews (step 1a applies from RL-14: 10
  experiments, 21 rounds, 9 FAIL rounds; 80 findings = 13 blocking, 65 notes, 2 pre-run stops), tabulated by the
  review-record dictionary's fields plus theme and detector: research/reads/PREREG-REVIEW-META-REVIEW-001.md
  ee75767f (F1-F10, C1-C5), data .json c38e88c1, tables -TABLES.md 26b9a759 generated by
  research/tools/prereg_review_meta.py 8415ebc2 (--check re-parses the review files; META-REVIEW OK). Findings:
  blocking power on R2 6 / R3 4 / R1 3, none on R4-R7; first-round FAIL 5 of 5 (RL-14..18) then 0 of 5 (RL-19..22,
  RL-15b); 20 of 21 rounds returned exactly 3 notes (quota); themes T4 instrument 15 (never blocking; both pre-run
  stops RL-15 and RL-21 found by the lab, not the reviewer), T7 report 14, T1 gate 13, T3 pin 11, T2 scope 8 (6
  blocking); RL-20's note 1 foresaw the one-node case; RL-17 r2 note 1 applied to the run without a v3 (slip, no
  verdict depended on it); the series is context-separated only (custody no, same model family). README section 2
  6046110c, from RL-23: step 1 author self-check (ordered gate, declared narrowing, full pins with commit, instruments
  checked by script, constants with digest); 1a every note found and none required, a gate-changing note is a new
  version even at PASS, three separation fields in the record; 1b (v) existence and computability, (vi) review-named
  edge cases in the preflight; step 4 five standing report items. No verdict, ledger or register row changed; no
  roadmap item touched. Bridge-changes list regenerated b9cc7e2b (A 41, M 4 + pages). Scans 0/0/0/0 on every new
  or changed file; no bytecode. Sent as RL-M57. Nothing committed; no push to R13.
- 2026-11-08 (MON-283-MERGED-LAB: 283 MERGED, harness-onion main e515f0b8, PR 239, verify 1009 s; GO light for the
  LAB-REPO-001 freeze, draft 6, before v7's c2): DONE on the bridge, `research/reads/LAB-REPO-001-PACKET-DRAFT.md`
  draft 6 e603aa24 (YAML sha256 92a41264, 20,007 B, the lines between section A's fences; 88159c5f at draft 5
  de12ac97). Changes: a Draft 6 paragraph; inputs re-digested (charter 6046110c, register 57f55f4a, migration plan
  cf6eb2a1, triage 100295c1; bridge HEAD 8fdb94b5); the Tree contract's sets widened to the packet's 12 files plus the
  bridge's 41 adds (53 A) and the manifest, the 3 page files and the 4 modified bridge files (8 M); a new
  Bridge-changes contract enumerating the 41 A and 4 M paths and freezing the set (any other add, delete or rename
  before B' is a named delta); the Evaluator contract widened by R13 issue 1 recommendation 2 (level LEDGER_REDERIVED,
  RAW_REPRODUCED, INDEPENDENT_REPLICATION or RECORDED on every entry; externalInputs source, commit, sha256,
  availability, retrieval on RECORDED entries; the PREREG argument by the ledger's prereg digest, RL-11's versioned
  case); the runner pin c8ac40f0 (9084 B, 100755) named as main e515f0b8's runner and no longer provisional, confirmed
  by digest-string equality against the monitor's word only (the lab's platform checkout holds main 4b2be353 and no
  object e515f0b8; no fetch word); the Route clause's set wording (53 A, 8 M); deliverables and evidence counts
  (manifest 288 = the base's 235 + 53; prereg_check 23 folders, reviews 10 of 23; rerun 23 entries, 10
  LEDGER_REDERIVED with RL-15b, 13 RECORDED); sections B, D (RL-15b's argv, the freeze note), E (runner CONFIRMED;
  Q-LAB-7 the new YAML digest as the frozen key, recommended (a) applied) and F. Unchanged byte for byte against draft
  5, checked by script: the six argv arrays, offlineExecution, prefetchCommands, allowedPaths, id, repository, branch,
  rollback, warmSourceAccess, sourceReuse, predecessors; the YAML parses (16 keys, 11 contracts, 6 deliverables, 6
  evidence lines). The YAML file sits in this session's scratch at the same digest; R00 writes it from section A.
  Bridge-changes list regenerated faf29889 (one row changed, the draft's own digest; A 41, M 4 plus pages). Scans
  0/0/0/0 on the draft, the YAML and the list; no bytecode. Sent as RL-M58. Nothing committed; no push to R13; R13 main
  cc92594d. NEXT: R00 builds v7 against YAML 92a41264; the lab's section-D work (the five tools, the two manifest-tool
  copies, the YES record and its review record) on the monitor's word; the YES before 284's c2; paused otherwise.
- 2026-11-08 (MON-LAB-D6-OK: draft 6 verified, runner c8ac40f0 byte-checked by the monitor at PR 239's head 6ef5d5a7 =
  main e515f0b8's tree; Q-LAB-7 accepted, v7's c2 keys the route to YAML 92a41264; GO light for section D on the bridge
  only): DONE. (1) The two manifest tools copied from R13 main cc92594d byte for byte: research/tools/make_manifest.py
  bb536406 and manifest_check.py 5511aeec, mode 755; the changes list no longer carries them (neither A nor M). (2) The
  five acceptance tools, standard library, counts only, problem lines CODE:path: research/tools/prereg_check.py 16001f66
  (9,815 B), rerun_results.py 284ca154 (10,821 B), rerun_table.json 29dfb885 (33,601 B; 23 entries, 10 LEDGER_REDERIVED
  with the evaluator argv, evaluator and PREREG digests from each ledger's evidence, 13 RECORDED with a one-line reason
  and externalInputs built from each ledger's evidence entries: IN_TREE paths, OWNER_HELD exports of harness-onion
  afee03b9 and conformance-labs b4bbea79 by 40-hex commit, one UNPUBLISHED relayed summary), privacy_check.py de3bd1b6
  (4,238 B; the platform's four hit classes mirrored from scripts/review_record.py at 4b2be353; RESEARCH_NAME_DIGESTS
  loader), page_check.py 374a4c60 (2,528 B; imports build_research.py by path, stubs the lane reader and the bridge
  commit, compares the record minus generatedAt/lane/bridgeCommit, checks every enumerated tool and read is a manifest
  key); ci/zero_bill_scan.py c71c55a6 (2,173 B) in this session's scratch, since the lab writes nothing outside
  research/** on the bridge (it goes onto the R13 branch with the transport copies). (3) Check runs on a staging tree in
  scratch (a local clone of R13 at cc92594d, the bridge's research/** overlaid, the three transport copies from the
  4b2be353 export and zero_bill_scan.py under ci/, the manifest regenerated with bridgeCommit = bridge HEAD 8fdb94b5,
  nothing committed): zero_bill_scan clean (exit 0, no output); MANIFEST OK 285 files (288 minus the runner, the YES
  record and its review record, which come later); PREREG OK 23 folders, 10 reviewed, 0 records; RERUN OK 23 entries
  (LEDGER_REDERIVED 10 byte for byte, RECORDED 13, 0 and 0); PAGE OK 23 experiments, 44 tools, 19 reads; PRIVACY OK 283
  files, 0 hits, with and without the unpublished name table (4 digests loaded locally). Name-status of the staged head
  against cc92594d: A 50, M 8 (the frozen 53 A minus the three later files; the 8 M exact). Negative controls, each
  restored after: a flipped ledger byte -> LEDGER_DIFFERS:RL-19; a review record with a wrong briefSha256 ->
  RECORD_BRIEF_MISMATCH and a valid one counted; an edited research.json -> RECORD_DIFFERS:counts; a seeded e-mail ->
  HIT:README.md emails=1; a changed file -> MANIFEST FAIL; seeded .github, symlink, bytecode and a hosted-runner token
  -> four zero-bill lines. (4) Two findings. (a) RL-01: the register's frozen column named v1 f0bdb2f7, but no v1 file
  exists anywhere in the bridge history (PREREG.md was amended in place to v1.1 db893373 before the first commit, a
  lapse before the kept-versions rule); prereg_check refused it as written; the row now keeps v1.1 db893373 in the
  frozen column and records the lapse and the digest in the state column (REGISTER.md 1a4effd8; no verdict, ledger or
  claim changed). (b) Q-LAB-8: the Privacy contract's set ("the manifest's file set plus README.md, LICENSE and ci/")
  includes the pinned transport copy ci/warm-source-isolation.sh, whose own isolation logic matches /private, /tmp,
  /Users and /home as path shapes (3 hits by the contract's own rule), so the frozen YAML's wording would fail the
  command under the verifier. privacy_check.py as written excludes the four pinned transport copies (fixed by digest in
  the Transport contract) and scans every other ci/ file; the YAML's Privacy contract needs the same words, a named
  delta with a new digest, applied only on the monitor's word (the draft and YAML are untouched). (5) Bridge-changes
  list regenerated d978ad7e (A 46 = the 41 bridge adds plus the five packet tools, M 4 plus pages). Scans 0/0/0/0 on
  every new or changed file; no bytecode; TMPDIR in scratch. Sent as RL-M59. Nothing committed; no R13 commit or push;
  R13 main cc92594d. NEXT: the monitor's word on Q-LAB-8 (then the YAML delta and a page rebuild), R00's built packet
  for the YES record and its review record (the last two A files), the branch with ci/ on the monitor's word.
- 2026-11-08 (MON-LAB-Q8-RULED: RL-01 correction accepted; Q-LAB-8 ruled (a); R00 holds v7's R13 route key for the new
  digest): DONE, draft 6.1 as a NAMED DELTA over draft 6 with one change inside the YAML, the Privacy contract's set
  ("plus README.md, LICENSE and the lab's own ci/ files; the four pinned transport copies are fixed by digest in the
  Transport contract and not scanned"). `research/reads/LAB-REPO-001-PACKET-DRAFT.md` f06fd72f (draft 6 was e603aa24);
  YAML sha256 8ae5c7fd (20,123 B; was 92a41264), extracted by the same rule; a unified diff of the two extractions shows
  exactly one contract line removed and added (line 127), checked by script; the fixed fields (six argv arrays,
  offlineExecution, prefetchCommands, allowedPaths, id, repository, branch, rollback) still equal draft 5's; the YAML
  parses. Outside the YAML the draft records section D's state (section D bullet), the RL-01 correction and Q-LAB-8 as
  RULED (section E), and section F names the 6.1 digest. Page rebuilt; bridge-changes list regenerated a592baf5 (the draft's
  M row); staging six commands re-run; scans 0/0/0/0. Sent as RL-M60. Nothing committed; no R13 commit or push. NEXT:
  R00's built packet keyed to 8ae5c7fd for the YES; the R13 branch with ci/ and the YES record on the monitor's word.
  MON-LAB-61-OK (same day): verified by the monitor's own extraction (draft f06fd72f, YAML 8ae5c7fd, 20,123 B); R00 keys
  v7's R13 route to it; THE FREEZE: no further YAML change without a named delta through the monitor. PAUSED until R00's
  built packet; then the R13 branch with ci/ and the YES record, each on the monitor's word. Acknowledged as RL-M61.
- 2026-11-08 (MON-LAB-284-F; GO light): R00's contract review for slot 284 (MET-REGISTRY-001, the meta packet that
  registers R13 and publishes LAB-REPO-001 at K = 1) found section F of the packet draft expecting three things VIS-284
  rules out: the reuse edit in C3, an in-place edit of chain-product-packets/rule.json (C5) and the YES's name check
  against rule.json. VIS-284: the Phase-0 inventory stays frozen at 13 and reuse is unchanged; a SUCCESSOR registration
  rule record allows mas-harness-research-lab from slot 284, with rule.json, v2 and v3 byte-equal; R13 is kind meta in
  the registry with releaseSet: EXCLUDED. Draft 6.2 (paper only, outside the YAML): section F amended to the rulings
  (C1, C2, C4, C6 and C3 without reuse; registration kind meta + releaseSet EXCLUDED; the name by the successor record;
  rule.json, chain_identity_v2.py and chain_identity_v3.py absent from the PR's changed paths; no rule.json name check),
  a pointer at the head of section C, a Draft 6.2 paragraph. The YAML block re-extracted by script: 20,123 B, sha256
  8ae5c7fd unchanged (lines 81-258 of the draft untouched); draft sha256 07fa5d08 (6.1 was f06fd72f). Page rebuilt;
  scans 0/0/0/0. Sent as RL-M62. Nothing committed; no R13 commit or push. The YES on R00's c1 comes on the monitor's word.
  MON-LAB-62-OK (same day): draft 6.2 verified (07fa5d08; the monitor's own YAML extraction 8ae5c7fd, 20,123 B); section C's
  pointer kept. VIS-284-CR1 (C1-3): a successor FUNCTION beside the record (binds v2 by V2_SHA256, reads the slot split from
  the record; the record's extends block names the function's digest). Draft 6.3 (paper, outside the YAML): section F adds
  the function as a new changed path, the record naming its digest, the name admitted only from slot 284; v2/v3/rule.json
  stay absent from the changed paths. YAML re-extracted 8ae5c7fd, 20,123 B; draft sha256 f68f61a7. Page rebuilt; scans
  0/0/0/0. Sent as RL-M63. The YES on R00's c1 waits for the monitor's word.
- 2026-11-08 (MON-LAB-284-YES; GO light): R00's c1 of slot 284 (MET-REGISTRY-001) committed locally: Harness-Engineering commit
  212d6343 (tree 279fbdef, parent e515f0b8 = main, branch codex/met-registry-001-r13-registration, 18 files: 4 A, 14 M). Read
  only through git archive of 212d6343 and of its parent into scratch (never in place), the two exports compared. Section F
  (draft 6.3) run by script (scratch f_check.py 126f6fe3; counts and digests only): F0-F9, F11, F12 PASS (YAML 8ae5c7fd byte
  for byte; plan 13 bc19f6a5 = section B; roots equal; schema ea815cda 14 names + releaseSet enum; registry 5a817d8e entry
  kind meta/EXCLUDED; readiness 059a8975 live 14 / Phase-0 13 / 295, validate_reuse unchanged; rule.json 5e6e6821, v2
  23fe723a, v3 29483ec3 byte-equal and absent from the changed paths; README af021909 rows 294/295; successor function
  3fa99c89 + record c3c4b8ee, extends digests equal, allowed_names 283 -> 12 names, 284 -> 13, tampered function refused;
  runner c8ac40f0 byte-equal to e515f0b8's, mode 755; RERUN OK 23 (10/0/0/13); YAML rule checks against c1's schema and
  runner); F10 PENDING (MET-REGISTRY-001.yaml + register block at c2). One check slip on the lab's side (F3-C1 matched every
  releaseSet key) corrected and re-run, disclosed. Written: research/reads/LAB-REPO-001-YES.md 3af085ec (9,584 B) and
  research/reviews/LAB-REPO-001-yes-r1.json 8dd36ef1 (8,394 B; v2, kind = the YES record, briefSha256 = its sha256,
  subject = the c1 commit/tree, base = e515f0b8, rulesSha256 = draft 6.3 f68f61a7, wrapperSha256 null, verdict YES_AT_C1);
  prereg_check: 23 folders, 10 reviewed, 1 records OK; negative control (zeroed briefSha256) refused. Bridge-changes list
  regenerated 804c3515 (A 48 + 5 ci = 53 A, M 7 + manifest = 8 M, the frozen set). Page rebuilt; scans 0/0/0/0 over the
  six new or changed files. Sent as RL-M64. Nothing committed; no R13 commit or push. NEXT: YES round 2 at c2 (F10) and
  the R13 branch with ci/, each on the monitor's word.
  MON-LAB-YES-C1-OK (same day): YES at c1 accepted (13 PASS, F10 pending c2); the records YES.md 3af085ec and yes-r1.json
  8dd36ef1 committed on the bridge at checkpoint 6302bdc0; the F3-C1 false-FAIL disclosure noted. Round 2 (F10) runs on R00's
  c2 on the monitor's word once c2 exists; the R13 branch with ci/ after 284's merge, also on the word. PAUSED. Acknowledged
  as RL-M65.
  MON-LAB-284-ARGV (same day; VIS-284-ARGV, GO light text only): slot 284's registration design changed: architecture/
  repositories.yaml and the three release files (release/evidence-policy.yaml, fixture-release-set.yaml, repos.lock.json)
  stay BYTE-EQUAL (eight of the verifier's 64 inherited commands read them live); R13 is registered in a new SUCCESSOR
  REGISTRY RECORD that 284 owns, read through one composition reader; releaseSet EXCLUDED lives in that record. Draft 6.4
  (sha256 7a48e79c, from 6.3 f68f61a7; 7 text replacements through the C1-6 channel, outside the YAML, which re-extracts
  to 8ae5c7fd, 20,123 B): a draft-6.4 paragraph; section C items 2 and 5 amended in place (the old text kept as "before
  draft 6.4"); the C pointer names VIS-284-ARGV; section F now checks the registry and release files byte-equal (absent
  from the changed paths), the successor registry record present with R13's row (kind meta, releaseSet EXCLUDED) and the
  composition reader returning 14, and lists the readiness edits as C1, C4, C6, C2's ADR line and C3 without reuse. The
  round-1 YES record on c1 stands as a record of c1 (not edited: it is committed at 6302bdc0 and round 2 supersedes it
  on the rebuilt c2). Changes list regenerated 585210e9 (A 48 + 5 ci = 53 A, M 7 + manifest = 8 M, unchanged set); page
  rebuilt (research.html 1fb47a35, research.json 693aee39, history.json d3797697 unchanged); scans 0/0/0/0 over the five
  changed files and this lane file. Scratch f_check.py is NOT yet updated: the record's and the reader's paths are R00's
  and are read from the rebuilt c2's export at round 2. Sent as RL-M66. Nothing committed; no R13 commit or push.
  MON-LAB-284-YES2 (2026-11-09; GO light): the lab's second YES pass on R00's rebuilt c2 e22e75a1a83b8e24a7e990119dfabb0eccd28878
  (tree 4c040d5d, parent c1 7ad428ec, base e515f0b8; branch codex/met-registry-001-r13-registration; 297 changed paths by the
  monitor, 14 A + 281 M seen by the pruned walk + 2 closed). Draft 6.5 (sha256 6974b279, from 6.4 7a48e79c; 7 text
  replacements through the C1-6 channel, outside the YAML, re-extracted to 8ae5c7fd, 20,123 B): section F amended for
  VIS-284-LPORACLE-2 (language-placement.json + ADR 0010 byte-equal; R13's placement row in the successor placement record
  with its schema; C2's ADR line in ADR 0001) and for validate_reuse.py's one count line 293 -> 295 (checked by diff);
  eleven byte-equal files named; the successor registry record and the reader (registry_rows / placement_rows, 14 each)
  named by path; Q-LAB-9 (record form: the frozen YAML binds the review record's file name to its round and names
  -r1.json only, so the second pass is written IN PLACE at the two frozen paths with round 1 on the new subject; a -r2.json
  would be a 54th A path = a YAML delta) and Q-LAB-10 (c2 leaves schemas/repositories.schema.json byte-equal and readiness's
  EXPECTED_REPOSITORIES at 13, as MET-REGISTRY-001's contract 1 states under VIS-284-ARGV, which the monitor's relay did not
  name; F reads C1/C3 accordingly) both answered (a) under the owner delegation, open to overrule. Read route: git archive of
  e22e75a1 and of e515f0b8 into fresh scratch dirs, compared through ops/tools/r00/kit/pruned_walk.py; the reader and the
  successor function imported from the export and run in scratch with tampered-pin negative controls (both refuse); F9 and
  prereg_check by the YAML's own argv on the bridge (RERUN OK 23; PREREG OK 23 folders, 10 reviewed, 1 records). Result 20
  PASS, 0 FAIL, 0 PENDING (scratch f_check2.py b88c8218). Slip disclosed: the first F15 run hashed the placement record's
  source spans at their display-only `lines` (BR-TT-1) and FAILed; corrected to a digest search inside the section (the
  second span sits at line 1604 against display lines 1598: a NOTE finding for R00). Records rewritten in place:
  research/reads/LAB-REPO-001-YES.md 835be39e (14,353 B) and research/reviews/LAB-REPO-001-yes-r1.json 9f582542 (13,008 B;
  round 1 on subject c2, base e515f0b8, rulesSha256 = draft 6.5, two NOTE findings, two questions, seven disclosures); the
  round-1 files (3af085ec / 8dd36ef1 on 212d6343) are superseded and live in the bridge history at 6302bdc0. Changes list
  regenerated 5fcbde75 (A 48 + 5 ci = 53 A, M 7 + manifest = 8 M, unchanged set); page rebuilt (research.html 81590c8b,
  research.json a245307d, history.json d3797697 unchanged); scans 0/0/0/0 over the seven changed files and this lane file.
  Bridge HEAD seen 46a4f0cb. Sent as RL-M67. Nothing committed; no R13 commit or push. NEXT, on the monitor's word: at the
  final head (D5a oracle, identity, ci/ weights, outside F) re-check F's inputs light by re-hash; the R13 branch with ci/
  after 284's merge.
  MON-LAB-284-YES2-OK (same day): the second YES pass at c2 e22e75a1 is accepted; the monitor read draft 6.5 6974b279, the
  YAML block 8ae5c7fd (20,123 B), YES.md 835be39e and yes-r1.json 9f582542 from disk. Q-LAB-9 (a) stands (records in place
  at the frozen paths, round 1 on the new subject, the superseded pass in history; no YAML delta). Q-LAB-10 (a) stands as
  the VIS-284-ARGV reading (schema and EXPECTED_REPOSITORIES at 13, the successor record's schema admits R13, composed rows
  14); the monitor notes it to the visionary at lock 46. The span NOTE is confirmed: R00 fixes the placement record's
  display lines as c3, so its digest 333aad7d changes. At the final head, on the monitor's word, the lab re-runs F14/F15
  light, re-hashes the other F inputs and updates the record digest in section F's text. PAUSED. Acknowledged as RL-M68.
  MON-LAB-284-FINAL (2026-11-09; GO light): the final-head pass on R00's c8 a641e7bb82085cd49e1863c241d5f0ebb84e33d0 (tree
  323c61bc, parent 608a225d, base e515f0b8; 300 changed paths by the monitor = 16 A + 284 M; the pruned walk sees 16 A + 282
  M + 2 closed; since c2: c3 span fix, c4 placement clause, c5 D5a oracle + identity, c6/c7 ci/ weights + catalog reader
  list, c8 conftest gc.freeze()). Export by git archive into a fresh scratch dir; all 20 F checks re-run by scratch
  f_check3.py 4c90ddd6 (F5, F10, F14, F15 as agreed; the rest as the re-hash): 20 PASS, 0 FAIL. Digests confirmed:
  unchanged LAB-REPO-001.yaml 8ae5c7fd, plan bc19f6a5, registry record 9c129674 / schema b2d07238, placement schema
  26c4e874; changed MET-REGISTRY-001.yaml 455cd736 (300 allowedPaths), rule record 4405e9da (extends names the function
  e8635f23), function e8635f23 (clause parameter), placement record 17fc67ef (display lines 1604: the c2 NOTE resolved),
  authority b47b2309; the eleven F13 files + the runner c8ac40f0 byte-equal to the base. The D5a oracle test is a closed
  path: counted by the walk, never read. Draft 6.6 (sha256 3037ea86, from 6.5 6974b279; 4 text replacements outside the
  YAML, re-extracted to 8ae5c7fd): a 6.6 paragraph, the F heading, and a final-head sentence at the end of F naming those
  digests. Records rewritten in place (Q-LAB-9 (a) standing): YES.md 96e5797a (14,169 B) and yes-r1.json 2034e6a4
  (11,558 B; subject c8, round 1, rulesSha256 = draft 6.6, no findings, two ruled questions, six disclosures); the c2 pass
  (835be39e / 9f582542) and round 1 (3af085ec / 8dd36ef1) stay in the bridge history. prereg_check PREREG OK 23 folders, 10
  reviewed, 1 records. Changes list regenerated 29cac1df (A 48 + 5 ci = 53 A, M 7 + manifest = 8 M, unchanged set); page
  rebuilt (research.html f1171c5c, research.json 0a4fa438, history.json d3797697 unchanged); scans 0/0/0/0 over the seven
  changed files and this lane file. Bridge HEAD seen a1239080. Sent as RL-M69. Nothing committed; no R13 commit or push.
  NEXT, on the monitor's word after 284's merge: the R13 branch with ci/ (three transport copies from the 4b2be353 export,
  the runner c8ac40f0 from the e515f0b8 export, scratch ci/zero_bill_scan.py c71c55a6), manifest regenerated at B', page
  rebuilt; never a push to main.
  MON-LAB-284-FINAL-OK (same day): the final-head YES on c8 is accepted (20/20); the monitor read draft 6.6 3037ea86, the
  YAML block 8ae5c7fd (20,123 B), YES.md 96e5797a and yes-r1.json 2034e6a4 from disk. 284's c8 dry run is 1,144.62 s, tier
  3, so it waits for the owner's 284-D2 at good morning: the recommended route keeps the head at c8 and the lab's record
  stands; a changed head brings a light re-hash on the monitor's word. The R13 branch with ci/ comes after 284's merge, on
  the word. PAUSED. Acknowledged as RL-M70.
  MON-LAB-284-MERGED (2026-11-09; GO light for the R13 step): 284 merged (harness-onion main 98d1f6f1, PR 240, verify 64/64 in
  1,058 s); LAB-REPO-001 8ae5c7fd published in the chain; the final-head YES on c8 stands. Branch
  codex/lab-repo-001-repository-bootstrap created in the local R13 clone from main cc92594d (clean, 236 tracked); the
  bridge's research/** overlaid from `git archive 415cf244 research` (B' candidate); ci/ from the exports with modes:
  verify-offline.sh 778cb0fa 755, warm-source-isolation.sh f717f62f 644, network_canary.py 1be4a837 755 (4b2be353 export),
  run_packet_argv.py c8ac40f0 755 9,084 B (e515f0b8 export), zero_bill_scan.py c71c55a6 755 (scratch); manifest regenerated
  (288 files, bridgeCommit 415cf244; 30a3d649 at this state). Name-status vs cc92594d: 53 A, 8 M, 0 D, as the Tree
  contract. Six commands from the clone root: zero_bill silent; MANIFEST OK 288; PRIVACY OK 285 files 0 hits (0 digests
  loaded; 4 loaded with RESEARCH_NAME_DIGESTS set, 0 hits); PREREG OK 23/10/1; RERUN OK 23; page_check FAIL
  RECORD_DIFFERS:reads: the bridge's research.json (built at the final-head step BEFORE gen_changes rewrote the changes
  list) carried the list's old digest 5fcbde75 against 29cac1df in the tree. Fix on the bridge: page rebuilt after the list
  (research.html 010a3955, research.json 15c4ca55, history.json d3797697 unchanged; every reads/tools digest in
  research.json now equals the tree, 0 stale; scans 0/0/0/0). The bridge needs the monitor's checkpoint for that rebuild
  (B'); then: re-overlay research/ from B', make_manifest --bridge-commit B', the six commands, commit; the push on the
  monitor's word. Branch left staged, uncommitted. Reported as RL-M71. Rule recorded in memory: gen_changes BEFORE
  build_research at every milestone.
  MON-LAB-R13-CKPT (same day): the fix is right (the monitor read research.html 010a3955 and research.json 15c4ca55 on the
  bridge working tree); the slip is noted and closed; the memory rule stands. No checkpoint while the visionary holds lock
  46; the monitor checkpoints when the lock returns and sends B'. Then exactly: re-overlay research/ from B'; manifest
  --bridge-commit B'; the six commands; commit; report head, tree, name-status, MANIFEST digest, scans; the push only on
  the word. The Co-Authored-By trailer is fine for R13. Stay staged and uncommitted; touch no other bridge file.
  Acknowledged as RL-M72.
  MON-LAB-R13-B (same day; GO light): B' = bridge 3b573074c3d2ede716116fc1973be06b510715a3 ("lock 46 applied ...; lab page
  fix"; research.json 15c4ca55; LAB-REPO-001 IN_PROGRESS in the roadmap). The five steps run exactly: research/ re-overlaid
  from `git archive 3b573074 research`; make_manifest --bridge-commit 3b573074 (288 files; MANIFEST sha256
  833a0fa81f12c6be396306428e600f7da5d629bef7318e6b27d3ed9f4443d00b); the six commands from the clone root ALL PASS
  (zero_bill silent; MANIFEST OK 288; PRIVACY OK 285 files 0 hits, 0 digests loaded and 4 loaded with RESEARCH_NAME_DIGESTS;
  PREREG OK 23/10/1; RERUN OK 23 = 10 LEDGER_REDERIVED + 13 RECORDED; PAGE OK 23 experiments, 44 tools, 20 reads, 7 record
  keys); the staged set checked by script against the contracts' named paths: A = the 12 packet files + the 41 bridge adds
  (53), M = manifest + 3 page files + 4 bridge modifies (8), 0 other; manifest keys = the tracked set minus the manifest
  (288 = 288). Commit on codex/lab-repo-001-repository-bootstrap: head 080513a0d62a6c5b61d3d555b6cd4246a43bcca9, tree
  ff349d616d46dcbfc9527a44240478e7bd441316, parent cc92594d; subject "LAB-REPO-001: R13 repository bootstrap over
  cc92594d"; the Co-Authored-By trailer as agreed. Ops privacy scan over ci/, MANIFEST, README, LICENSE, .gitignore:
  0 hits except warm-source-isolation.sh 3 absolute-path shapes (its own isolation logic; pinned byte for byte, Q-LAB-8).
  No bytecode. NOT PUSHED; no network. Reported as RL-M73. NEXT: the push on the monitor's word, then the PR (verifiable
  under bundle v7's first-packet route); R13 main stays cc92594d.
  MON-LAB-R13-PUSH (same day): the owner approved, verbatim via the monitor, "Approve push 080513a0 (Recommended)",
  head-bound to codex/lab-repo-001-repository-bootstrap at 080513a0 (tree ff349d61, parent cc92594d); the monitor checked
  the branch from disk. Done: head confirmed 080513a0 and clean; `git push -u origin codex/lab-repo-001-repository-bootstrap`
  (that one branch; remote head 080513a0); PR opened with gh against main: <owner>/mas-harness-research-lab#2, OPEN, not
  draft, title "LAB-REPO-001: R13 repository bootstrap over cc92594d"; body (scratch pr_body_r13.md, 4,909 B, privacy scan
  0/0/0/0, one coverage word "each" backed by RERUN OK 23) names the packet digest and slot 284 publication, base/head/B',
  the 53 A / 8 M set with the script check, the manifest (288, 833a0fa8), the ci/ table, the YES record 96e5797a and
  review record 2034e6a4, the 23 PREREG folders, the six commands with outputs, issue 1 PARTIAL (no closing keyword: the
  monitor posts the note), rollback, and the attribution line. Transport approval (hosted form): v7 verify_pr.py 8c75bf6a
  read only through the lab's masking reader (record_key = short(repo) + "--" + sha with short = the name after the slash;
  approval_bytes = canonical JSON, sorted keys, separators (",", ":"), ascii, of headSha/pr/repository/schemaVersion;
  accepted with or without a trailing newline; APPROVALS = the verifier's approvals directory named in v7's code, root-owned, nlink 1,
  not group/world-writable): file mas-harness-research-lab--080513a0d62a6c5b61d3d555b6cd4246a43bcca9.json, 161 B, sha256
  1ae0ca72248ee009b1300af8644b3b10e14891ca7176b62c0d1d3240b431ce18, repository = nameWithOwner read by gh (never typed),
  unplaced at <session-neutral tmp>/lab-transport-approvals/ (a copy also in the session scratch). No other network.
  Reported as RL-M74. NEXT (owner via the monitor): the verify start and the merge; then the monitor's PARTIAL note on
  issue 1; R13 main moves only by the merge.
  MON-LAB-R13-MERGED (same day): PR 2 merged on the owner's word "Merge at 080513a0 (Recommended)"; verify 6/6 in 3 s
  (check run 128945583698); R13 main 2e977f4f5a3162bd2ec3e939b9c2c16c8956a994 (tree ff349d61, the approved head's tree;
  parent cc92594d; subject "LAB-REPO-001: R13 repository bootstrap over cc92594d (#2)"); the monitor's record
  handoff/merge-decisions/2026-11-09-mas-harness-research-lab-PR2.json 692b5ba2 (digest checked). Issue 1 CLOSED with
  the monitor's note (recommendation 2's planned parts shipped: PREREG 23/10, RERUN 23 with 10 re-derived, the read-only
  page check; the wrapper command deferred; recommendations 1 and 3-6 as triaged). Lab: `git fetch origin main` (the
  monitor's named step) and `git merge --ff-only 2e977f4f` on the local clone's main (tree equals 080513a0's: yes; 289
  tracked files); the merge recorded here and in the register; page rebuilt; scans. From here later R13 packets branch
  from 2e977f4f; the first-packet route is retired; each push, heavy run or fetch needs the monitor's word; the paused
  research rounds resume only on the word. Acknowledged as RL-M75.
- 2026-11-09 (MON-R13-ISSUES-3-4; the owner's issue-tracking rule; light, no run, no push): issues 3 ("P1: Validate
  RL-15b's fixed case set before allowing PASS") and 4 ("P2: Make future pre-run stops observable before evaluating the
  protocol changes") fetched read-only with the two approved commands (JSON; author login and repository owner masked
  before any read; masked copies 9135ba21 / c228ee03 in the lab scratch). Triaged in research/reads/R13-ISSUES-3-4-TRIAGE.md
  (33247a00). Issue 3 ACCEPT: the evaluator 2d6c349b reads its denominators and control count from the run record, pins no
  case set, drops zero-sized classes from the FAIL test and never reconciles rows with counts (confirmed by reading lines
  21, 27-30, 35; nothing executed); the committed record f445e3c1 is complete and self-consistent by read-only recount
  (21 unique cases, 18 + 3, every count equal to its recount), so the H-30b PASS stands as a description of that data.
  Action on the monitor's word: companion validator research/tools/rl15b_validate.py (frozen case set, class counts,
  the one exclusion, three controls, field consistency, counts recomputed; VALID / INVALID / INCOMPLETE, never PASS) +
  experiments/RL-15b/data/rl15b_validation.json and VALIDATION.md with provenance; README 1b (vii) acceptance boundary +
  C1 pinned denominators from RL-23; CLAIMS H-30b and the register row qualified; evaluator, ledger, report untouched.
  Issue 4 PARTIAL: the collector 8415ebc2 knows stops for RL-15 and RL-21 only (STOP_ANCHORS, lines 102-110) and walks
  only folders with PREREG-REVIEW.md (line 115). ACCEPTED: OUTCOME.json per attempt (form
  planeon.research.experiment-outcome/v1: stage reached, COMPLETED_NO_STOP / STOPPED / PENDING, stop stage, cause,
  detector, caught / escaped / false-block class, evidence sha256; written from RL-23 on, backfilled RL-14 to RL-22), a
  successor collector over every registered RL id failing on absent outcomes with the 001 snapshot preserved; the
  candidate hypothesis as H-36 BLOCKED on five reviewed experiments with denominator, ascertainment, comparator
  (RL-19 to RL-22), margin and the three outcomes fixed first. PLANNED, not scheduled: the masked paired comparison of
  old and revised protocol on frozen PREREG variants (heavy slot + separate reviewer custody) as a future RL id. Notes
  of 7 and 6 lines drafted; the monitor posts them. No roadmap item touched. Page rebuilt after this entry (digests in
  the milestone message); scans 0/0/0/0 over the triage, this lane file and the three page files. Sent as RL-M77. The
  light work (issue 3 items 1-3, issue 4 items 1-3, the README text) starts on the monitor's word. Builder fix at this rebuild:
  research/build_research.py's Resume-header regex stopped at the first ")" and failed on this header's nested
  parentheses, so the page had shown "Lab ACTIVE" with an empty Resume block since the 2026-11-09 header; the header
  now reads to the line's last ")" (status PAUSED again). Disclosed in RL-M77.
- 2026-11-09 (MON-R13-3-4-GO; light GO for the issue 3 and 4 remediation, not a research round; bridge research/** only;
  interpreter the profile CPython 3.12.14, -I -B; no network, no R13 commit or push): ISSUE 3 DONE. Frozen case set
  experiments/RL-15b/data/rl15b_case_set.json 35525dd9 derived from RL-15 run-002 (a60da422; 21 identities, 18 seeded of
  which 17 catchable, 3 controls); companion validator research/tools/rl15b_validate.py 31ae73e4 (V1-V8: identities,
  duplicates, rows per class, catchable flags and the declared exclusion, row types, field consistency, counts recomputed
  from rows, the ledger's scores and E1 binding; VALID / INCOMPLETE / INVALID, never a verdict): the committed record
  f445e3c1 is VALID 8 of 8 (data/rl15b_validation.json 05276597). Acceptance boundary research/tools/rl15b_boundary.py
  4e86669a: five deterministic mutations (drop class M1, drop controls, stale counts, duplicate case, missing case): the
  frozen evaluator 2d6c349b PASSES ALL FIVE, the validator rejects all five (INCOMPLETE 3, INVALID 2); table
  data/rl15b_boundary.json 1f722721; copies and evaluator outputs in the lab scratch (rl15b_boundary/). VALIDATION.md
  3fcb0514. CLAIMS.json 89a5f87a (H-30b instrumentNote + supportedScope qualified; CLAIMS OK 46 over 23; CLAIMS.md
  14e7328b); README 9442e6f8 (C1 pinned denominators; 1b (vii) acceptance boundary; 1c outcome record); register a244815e
  (RL-15b row and H-30 status notes; header cell "first step | stream" split as the rows already were; H-36 added).
  Evaluator, ledger, run record and report untouched. ISSUE 4 DONE (items 1-3): research/tools/outcome_record.py
  3556e846 (form planeon.research.experiment-outcome/v1; backfill / add / check) wrote OUTCOME.json for all 23 folders
  from their records: 25 attempts, 23 COMPLETED_NO_STOP, 2 STOPPED (RL-15 attempt 1 under v3 cda3e838, GATED_RUN,
  LAB_RUN, ESCAPED_TO_GATED_RUN; RL-21 attempt 1 under v1 73c96e89, PREFLIGHT, LAB_PREFLIGHT, CAUGHT_BY_PREFLIGHT;
  superseded PREREG.vN.md files give the full digests), 0 PENDING, 0 defective; research/tools/outcome_collect.py
  c5a53de8 over the register's ids: 23 ids, absent 0, first-round PASS 5 of 10 reviewed first attempts; --from RL-23 an
  empty valid cohort; the 001 meta-review snapshot and prereg_review_meta.py untouched. H-36 registered BLOCKED with
  denominator, ascertainment, comparator RL-19 to RL-22, margin to fix before the first cohort record, the three
  outcome classes; the masked paired protocol comparison in its first-step cell as a future RL id (heavy slot +
  reviewer custody). OUTCOME digests: RL-01 57574927, RL-02 01697638, RL-03 2bce2715, RL-04 fe01a061, RL-05 c4ecb1a9, RL-06 eb3c1ce4, RL-07 1359477c, RL-08 fa78794d, RL-09 dff25517, RL-10 9617721a, RL-11 eeb0d440, RL-12 c7cbecad, RL-13 0b7904b7, RL-14 e6807e24, RL-15 b60b1364, RL-16 a01b90c3, RL-17 5c030b6b, RL-18 ef6cf428, RL-19 27f23c8e, RL-20 64ee7c6b, RL-21 88e0cd0e, RL-22 3ceedcdb, RL-15b 5cddedad. Page rebuilt
  after this entry (digests in RL-M78); privacy scan 0/0/0/0 and no path shapes over every new or changed file.
  Nothing committed; the monitor checkpoints the bridge; the R13 PR later on the owner's word. Sent as RL-M78.
  MON-R13-3-4-OK (same day): digests verified by the monitor (case set, validator, validation, boundary tool and table,
  outcome_record, outcome_collect, the 23 OUTCOME files, lane file 3c084bb5, page aae16160); bridge checkpoint 3651fb6a
  carries them (status clean); privacy scan of the added lines 0 hits. R13 issues 3 and 4 stay OPEN until the lab PR
  lands, which waits for the owner's word. Research rounds paused. STANDING BY.
- 2026-11-09 (MON-048-LAB-READ; light, paper only, rounds paused): R00's DESIGN_048 rev 1 (715a4be8, 197 lines) read
  whole for Q-048-1 (an authored class-other edit to an attested file under condition (v)). Lab read
  research/reads/DESIGN-048-Q1-LAB-READ.md (9c795426): ruling (b) demote with countEffect neutral, under C1 (the ten
  clean verifies include one demotion-free verify and one verify with an authored demotion on a live head; a dry run
  serves if no packet edits an attested file), C2 (a demoted layer's outcome change is never neutral: explained by the
  hunks or class A, restart), C3 (records name demoted layers, authority entries, live seconds, the attested fraction;
  RL-14's dataset gains a demoted column), C4 (bundle v8 recomputes the deselected set as attested minus sample minus
  layers with a changed declared input, from the ledger and the live files, never from the G1 record; vector 19
  amended). (b) keeps G1's trust argument sound with C4. Note on Q-048-4: end the period no earlier than three clean
  shadow verifies after the rewrite that produces G1's ledger, no restart. Page rebuilt; scans 0/0/0/0. Sent as RL-M79.
  MON-048-OWNER (same day): the owner adopted the lab's read (9c795426): OQ-048-1 = "(b) Demote, with C1-C4"; OQ-048-2 =
  "(a) 048 at 299" (the rewrite at 296, three clean shadow verifies after it, 048 at 299). RL-14's dataset gains the demoted
  column (C3) when that work resumes. Rounds paused; STANDING BY.
- 2026-11-09 (MON-C286-Q2; light, paper only, rounds paused): CONTRACT_286 r1' (f23460f3, 408 lines) section 3.11 read
  for Q-C286-2 (countEffect of an explained outcome change on a demoted layer). Lab read
  research/reads/CONTRACT-286-QC2-LAB-READ.md (557fa451): COUNT when the explanation is checked causally, RESTART
  otherwise. The contract's statement check (outcomeStatements naming layer, path, nodes + a class-other hunk) shows
  intent, not cause: an undeclared input edited in the same packet would pass it (the gap C2 named). Isolation check
  E1: scratch copy of the head with every changed declared input of the layer restored to base bytes, the differing
  nodes re-run; all recorded outcomes return = explained, count; else class A, restart. Statement still required; E1 in
  the shadow verify when 286 carries it, else a recorded light step before the verify is credited (countEffect "pending
  isolation"); record fields per event; vector 17c splits into 17c (isolation PASS) and 17d (FAIL). Page rebuilt;
  scans 0/0/0/0. Sent as RL-M80.
- 2026-11-09 (MON-286-E1-READ; light, paper only, rounds paused): non-author read of R00's isolation tool
  isolate286.py (6ecd8c7a, 178 lines) against E1 (CONTRACT_286 r3 19c3b7c2 section 3.11 + C1-6 closure; the lab's read
  557fa451). Self-test only: 8/8 OK under the profile interpreter -I -B. Lab read
  research/reads/ISOLATE286-E1-LAB-READ.md (61090ac6): FINDINGS, not PASS. Blocking: A1 the recorded-outcome mapping
  (overall over phases) and the restored-outcome mapping (pytest -rA words; SKIPPED lines carry no node id) are not one
  function, so skips and xfails read FAIL falsely, and the record collapses phases where the contract says per phase;
  A2 the restored set is taken from the record's restoredPaths without checking each path is a declared input of the
  layer (an extra path masks an undeclared cause = false PASS). Conditions: B1 ledger at head unverified against the
  record's ledger digest; B2 allowlist parsed from head bytes; B3 event form assumed (statement/nodes/live keys).
  Form: C1 canonical record-line form for the binding digest; C2 schemaVersion extra, labReadSha256 unchecked. Minor:
  path traversal in restoredPaths, asserts under -O, refusals write no record, xdist serial pin, node-digest
  convention. Read bound to tool 6ecd8c7a; a revised tool needs a new read. Page rebuilt. Sent as RL-M81.
- 2026-11-09 (MON-286-E1-REREAD; light, paper only, rounds paused): re-read of isolate286.py v2 (7a03e62c, 467
  lines; v1 kept 6ecd8c7a) against E1 and the reader it pairs with at c1b f70f6518 (git show of _start/_statement/
  _finish/_record/naming_authority/pin_normalised, the writer's node line, the root conftest's print; never a working
  tree). Self-test only: 33/33 OK (profile interpreter -I -B). Lab read research/reads/ISOLATE286-E1-LAB-READ-V2.md
  (3058efff): PASS for the first credited use. A1 agrees() = the reader's _finish rule over per-phase report.outcome
  triples on both sides; A2 restored set derived from the ledger's layer vs writingCommit, must equal restoredPaths;
  B1 ledger named by the record's naming authority + event ledgerSha256; B2 allowlists head vs writingCommit; B3 the
  reader's 11 event members validated; C1 canonical line = the conftest's print; C2 schemaVersion + 64-hex lab digest;
  minors closed. Notes N1-N6: r4 text (members ledgerSha256/refusal/schemaVersion, canonical form, refusal = FAIL,
  PIN-LINE-LIMIT), PIN-LINE-LIMIT narrow and conservative, two prefixed lines (hand the JSON line), dry-run record
  form, VPY unbound to uv.lock, cache writes. Bound to tool 7a03e62c. Page rebuilt. Sent as RL-M82.
- 2026-11-10 (MON-SC-D1-F; standing rule, no run): the owner adopted the visionary's self-critique corrections
  (SC-D1 (a); visionary/SELF-CRITIQUE.md 79067647). Correction F for the lab: the lab's heavy share (RD-D1's
  60/25/15 heavy-queue split) is paused until one deployable runs end to end; the lab repository and its register
  stay. This partly reverses RD-D1; research rounds were already paused, so nothing changes today. Still allowed:
  light issue fixes and the paper reads the monitor requests. The R13 PR carrying the issue 3/4 fixes still waits
  for the owner's word. Recorded here; page rebuilt; acknowledged as RL-M83.
- 2026-11-10 (owner's direct word in this session's chatbox: a comprehensive, complete and concise self-criticism of
  the lab's R&D decisions; light, paper only, no run, no network, no subagents): research/reads/LAB-SELF-CRITIQUE.md
  (8cf22653, 147 lines), in the form of the visionary's SC-D1. Evidence from research.json f56c987e, CLAIMS.json, the
  register, this file, meta-review 001 and the three issue triages. Verdict: a complete, auditable record at near-zero
  compute that has not changed anything the product does. Twelve criticisms (C1 breadth over depth, C2 document-set
  hypotheses, C3 expected FAILs preregistered, C4 consumption unwatched, C5 design reads added chain mechanism, C6
  in-house review custody, C7 reactive protocol growth, C8 late then over-built publication, C9 unused heavy split, C10
  stale progress view, C11 own cost unmeasured, C12 own null result not acted on). Corrections A-K proposed for the
  owner (proposed label SC-D2; option (a) recommended). No verdict, claim or register entry changed. Page rebuilt.
  Sent as RL-M84.
- 2026-11-10 (MON-SC-D2; light, paper only, no run): the owner adopted the lab's corrections, verbatim "(a) All A-K
  (Recommended)"; LAB-SELF-CRITIQUE 8cf22653 checkpointed (4d136150). Applied as lab rules: research/README.md
  (section 2 freeze and custody paragraph, 1a pointer, section 3 SC-D2 bullet), research/hypotheses/REGISTER.md
  (experiments table F column filled for all 23 rows: CONSUMED 6, INPUT 10, NONE 7, digests n/r until the next
  visionary lock; rules section appended), this file (SC-D2 RULES block above the OPENED bullet). D (the monitor
  briefs blind reviewers) and K (one monitor message a day unless a GO or a ruling is needed) in force now; I and J
  on resume; SC-D1 F still pauses the heavy share. Page rebuilt. Landed digests sent as RL-M85 (today's one message
  under K; RL-M83 and RL-M84 preceded it).
- 2026-11-12 (owner's direct word in this session's chatbox: "how can we benefit from this repo" with the Agent
  Laboratory repository URL, then "Fetch and record"; light, one fetch, no run): one read-only GET of the repository
  page, pinned in the read's fetch record (AL-1: HTTP 200, 304,076 bytes, sha256 6b76db5f, default-branch head
  d9017d90, fetched 2026-11-12T01:41:44Z); nothing else fetched (no clone, no paper, no sub-page); the fetched copy
  stays in the session scratch. Read research/reads/AGENT-LABORATORY-LAB-READ.md (6d86b6af, 85 lines): ruling = a
  method reference and a later workload, not a component. U1 the three-reviewer rubric as the second reviewer family
  in the monitor's PREREG brief (rule D); U2 a per-phase, per-model cost table as the shape of rule J's columns; U3
  phase checkpoints with resume as the form of rule I's progress view; U4 a candidate release-gate hypothesis (a
  multi-agent research pipeline as a tenant workload fails closed at the egress policy, logged, resumable) NOT
  registered until R14's doubles exist and a heavy slot opens (rules A and B; SC-D1 F); non-use as a component or an
  adoption baseline; recommendation to the visionary: no roadmap item, no codebase record (SC-D1 A and D). Options
  (a) recommended. Page 3fb018c4 / e6846f89 / 29fd8b20 (27 reads); scans 0/0/0/0, no e-mail or clone address
  reproduced. RL-M86 = today's one monitor message (rule K). Rounds paused; heavy share paused under SC-D1 F.
- 2026-11-12 (MON-RL-M86; owner verbatim "Method reference only (Recommended)" for Agent Laboratory: index entry only,
  no roadmap item, no codebase record, U1-U3 inside the lab's process, U4 unregistered, no further fetch; and "Prepare
  the R13 PR (Recommended)" = GO to prepare, light): branch codex/lab-sync-a2482753 created in the local R13 clone from
  main 2e977f4f (= origin/main); research/** overlaid from `git archive a2482753 research` (the bridge's committed
  checkpoint; the uncommitted Agent Laboratory read and page rebuild are NOT in it, by the monitor's count of 37 new and
  8 changed); MANIFEST regenerated (--bridge-commit a2482753e831..., 325 files, 62c8725e). Six commands from the clone
  root, all PASS: zero_bill silent; MANIFEST OK 325; PRIVACY OK 322 files 0 hits (4 name digests loaded); PREREG OK
  23/10/1; RERUN OK 23 (LEDGER_REDERIVED 10, RECORDED 13); PAGE OK 23 experiments, 48 tools, 26 reads, 7 record keys.
  Name-status vs main: 37 A, 9 M (8 + MANIFEST), 0 D, no path outside research/; branch research/ identical to the
  bridge tree minus MANIFEST (blob-by-blob). Bridge privacy_scan over the 46 changed files 0/0/0/0; local paths 0.
  Committed with the trailer: head 9992d1755f71edc2ac25eacd8aceff9f06a76af7, tree 2112241e, parent 2e977f4f. PR body
  drafted in the session scratch (r13pr/pr_body.md) with a counted claims script (11 claims PASS; coverage words
  backed; no closing keyword; scans 0). NOT PUSHED; no gh pr create. Reported as RL-M87 (a GO report, outside rule
  K's daily message). Next, each on the monitor's word: the push; the verify (never during a harness-onion verify); the
  owner approves the head and the merge; issues 3 and 4 stay open until the monitor's note.
- 2026-11-12 (MON-RL-R13-PUSH-GO; owner verbatim "Approve push 9992d175 (Recommended)", head-bound): approval line
  (the owner's words + the full head sha) added to the PR body, claims re-run with a 12th claim, 12/12 PASS, body
  8e8f3c89 (2,237 B), scans 0/0/0/0, no closing keyword. Pushed exactly 9992d1755f71edc2ac25eacd8aceff9f06a76af7 to
  refs/heads/codex/lab-sync-a2482753; PR <owner>/mas-harness-research-lab#5 OPEN, not draft, base main, title "Lab sync at
  bridge a2482753: issue 3 and 4 remediation, outcome records, reads, SC-D2 rules"; refs/pull/5/head read back = 9992d175
  (EQUAL). Transport-approval file in PR 2's hosted form (canonical JSON of headSha/pr/repository/schemaVersion; repository
  = nameWithOwner read by gh): record_key mas-harness-research-lab--9992d175...json, 161 B, sha256 4694ddcb, pr 5, unplaced
  at <session-neutral tmp>/lab-transport-approvals/ (copy in the session scratch); install line sent to the monitor for
  the owner's sudo. Network: the push, gh pr create/view, gh repo view, two ls-remote reads; nothing else; gh output
  masked. Reported as RL-M88. NEXT: the owner installs the file; the verify on the monitor's word (never during a
  harness-onion verify); the merge is the owner's; issues 3 and 4 stay open until the monitor's note; R13 main moves only
  by the merge; the Agent Laboratory read rides the next sync.
- 2026-11-12 (MON-RL-R13-VERIFY-GO, then MON-RL-R13-ROUTE): the owner installed the transport file (root:wheel 0644,
  4694ddcb); the verify of PR 5 at 9992d175 was REFUSED before launch (check run 130916760063, 2 s): "harness-onion main
  has 0 packets naming this repository with the PR's head branch; exactly one is required". SLIP: the lab's RL-M87
  assumption (ordinary hosted route = no new packet) was wrong; LAB-REPO-001.yaml line 150 means each later lab PR needs
  its own harness-onion packet naming the repository and the head branch and inheriting the six commands. Owner, verbatim
  "Ride slot 288 (Recommended)": R00 adds a lab-sync packet (repository mas-harness-research-lab, branch
  codex/lab-sync-a2482753) to slot 288. PR 5 stays OPEN at 9992d175; no push, no rebase; the installed file stays valid
  for that head. Sent R00's inputs through the monitor as RL-M89: repository, branch, head/tree/base, PR 5, allowedPaths
  ["research/"] with the 37 A / 9 M / 0 D set spelled out, predecessors ["LAB-REPO-001"] (R00's call), prefetchCommands
  [], the six offlineAcceptanceCommands and the offlineExecution block verbatim from LAB-REPO-001, expectedEvidence =
  the six outputs at this head, rollback = revert, the transport-file binding. MON-RL-M89-OK: the same fields written as one JSON file for R00,
  LAB-SYNC-288-inputs.json (4,286 B, sha256 e4125198, mode 0444, beside the transport files in the session-neutral tmp
  folder; scan 0/0/0/0; RL-M90). NEXT: 288 merges; the verify on the
  monitor's word; the merge is the owner's. Rule for every later sync: ask R00 for the packet BEFORE the push word.
- 2026-11-12 (MON-CONV-1; no reply, C2): factory conventions C1-C8 adopted as a standing block above (file sha256
  61c9c0cf, 20 lines, digest checked before reading). First use: C3 headers and C1 files from the next message; C6 on
  PR 5's merge (review rounds used 0 lab-authored; heavy-run seconds 0; scope-to-merge wall time from MON-RL-M86's GO).
- 2026-11-12 (MON-LAB-FACTORY-1; owner "all these trials can be a good hypothesis and data for research-lab"): protocol v1
  for an observational study of the factory trials H1-H8, on paper, landed as research/reads/FACTORY-STUDY-PROTOCOL-v1.md
  (sha256 6c0e8f61, 198 lines; brief 7325ba8f, 24 lines, digest checked before reading; sources handoff/FACTORY-IMPROVEMENTS.md
  0bc476b1 and FACTORY-CONVENTIONS.md 16f7ffd1 at bridge 3e1db1bb). H-37..H-44 as falsifiable statements with thresholds and
  guards, pre/post periods and minimum n, declared confounders, the aggregate form planeon.research.factory-aggregates/v1
  (aggregates only, monitor-produced; never transcripts, the usage store or the lane table), an ordered gate, light compute
  only, options (a) adopt as RL-23 PREREG v1 with H-37..H-44 (Recommended) / (b) H-37, H-38, H-40 only / (c) a read. Nothing
  registered, nothing frozen, no delivery opened until the ruling, the blind review (rule D) and the evaluator preflight.
  Page rebuilt (research.html a184245a, research.json 84a2a5c5); scans 0/0/0/0. Sent as RL-M91 (this stream takes the C7
  paper slot; rule B's order queues behind it on the owner's word). NEXT: the owner's option; two slot-288 constants from
  the monitor (lost-detail slips, minutes per step) before the freeze, or the fallback guards in section 4 apply.
- 2026-11-12 (MON-LAB-FACTORY-2; owner verbatim "Adopt all eight (Recommended)"): RL-23 PREREG v1 FROZEN as
  research/experiments/RL-23/PREREG.md (sha256 467c636c, 215 lines) from the draft read 6c0e8f61; the only changes: the two
  slot-288 constants the monitor delivered (minutes per step 22.2 over 25 reports 09:58-18:50, 532 min; lost-detail slips 0
  over four compaction events) pinned in section 4 with the measure's window narrowed to scope -> last report before PACKET
  r1 (H-42's window, so the interim value is final and post slots are measured alike; the monitor's full-slot figure at
  288's merge is descriptive), H-44's thresholds fixed (18.87 min, 0 slips), a producer digest pin per delivery (section 6),
  section 11 as the registration record, section 13 the author's self-check (4 of 4 input digests resolve by script).
  Register d3aeb9bc: H-37..H-44 READY (empirical, observational; S2 (X); 3/1) and the RL-23 row (v1 467c636c; effort 35 /
  n/r / 0; F NONE); OUTCOME.json 71c70d11 attempt 1 at REVIEW, PENDING (H-36's cohort opens); outcome_collect pending 1,
  defective 0. Page rebuilt (research.html 5188540d, research.json a2ac9b6e, history.json 219bbac7, snapshots 31); scans
  0/0/0/0. prereg_check on the bridge: 3 expected problems on RL-23 (LEDGER_MISSING, REPORT_MISSING, REVIEW_MISSING), so the
  next R13 sync's acceptance set fails until the folder completes or the checker learns the PENDING state; told the monitor
  first (detector rule), proposed the pending-folder rule plus a self-test vector, patch on its word. Sent as RL-M92.
  NEXT: the monitor briefs the blind reviewer from 467c636c (rule D); on PASS the evaluator and its known-answer fixture
  (preflight 1b (ii)-(v)) before the pre-period delivery is opened; a review note that moves a gate region makes v2.
- 2026-11-12 (MON-LAB-FACTORY-3; option (a) approved with three conditions): research/tools/prereg_check.py patched
  (sha256 54ddffc7, 305 lines, from 16001f66): a folder whose OUTCOME.json last attempt is PENDING is accepted only when
  PREREG.md's sha256 equals the outcome record's digest and its prefix is the register row's pin, the folder holds no
  RESULT, LEDGER or REPORT file at all (rglob, name tokens), and any review of that digest reads PASS (the lab's stricter
  addition); `--self-test` builds the three vectors in temporary trees (PENDING accepted; PREREG digest not the pin,
  refused with PENDING_PIN_MISMATCH + FROZEN_DIGEST_MISSING; a stray RESULTS.json, refused with PENDING_STRAY_FILE):
  SELFTEST OK 3 vectors. Full tree: "PREREG OK: 24 folders (1 pending), 10 reviewed, 1 records" (the OK line now carries
  the pending count; LAB-SYNC-002's expectedEvidence must quote the new form). Regression on a scratch copy without
  RL-23: 23 folders (0 pending), 10 reviewed, 1 records under both tool versions. Page rebuilt (research.html 0f81be4f,
  research.json 33e6b135); scans 0/0/0/0. The patch reaches R13 only in the next LAB-SYNC packet (branch
  codex/lab-sync-002, the monitor's word); PR 5 unchanged at 9992d175. Effort: 15 min. Sent as RL-M93. The blind
  reviewer is running from 467c636c (one round, cap 2); the monitor relays the verdict; the monitor checkpointed the
  RL-23 files (bridge b18f8e1c). NEXT: on PASS, the evaluator and fixture; on FAIL, v2.
- 2026-11-12 (MON-LAB-FACTORY-4; blind review r1 of v1 467c636c, file sha256 3ecd616c, 31 lines, digest checked:
  CHANGES_REQUIRED, 1 MAJOR, 11 MINOR, 7 NOTE): PREREG v2 FROZEN as research/experiments/RL-23/PREREG.md (sha256 969489d7,
  270 lines; v1 kept as PREREG.v1.md). All findings taken as worded except RV1-16 (slip guard kept on the median, the total
  reported descriptively); the MAJOR adds the later-found-defect guard to H-41 and H-42 and "Guard: none" to H-37 and H-39;
  region 5 now names each guard's comparator; the stop rule no longer truncates post windows; 288 is transitional for H-40;
  H-44 thresholds declared absolute; fidelity, changes[] and "baseline partly treated" rows; windows[] at account level,
  slot kind, dryC2Runs, both producer digests held fixed; the lab's spot-check of one post slot against the bridge step
  notes; closure table in section 14. PREREG-REVIEW.md (e6d9c2d3, 43 lines) carries review 1 as FAIL with the custody,
  context and model-family fields (model family asked of the monitor); OUTCOME.json (1eddb82b) attempt 1 continues on v2
  with reviewRounds 1, verdict FAIL (the backfill convention: rounds accumulate per attempt, RL-15 took three); register
  607bc143 (pins v1 467c636c, v2 969489d7; H-37..H-44 texts aligned; effort 35 + 30 min). prereg_check OK 24 (1 pending);
  outcome check 0 defective; page rebuilt (research.html ccda3fb5, research.json 73e9cf34); scans 0/0/0/0. Review r2
  (delta-scoped, the last) on the monitor's launch. NEXT: on PASS, the evaluator and fixture; a note that moves a gate
  region after r2 would make v3 only on the monitor's word (C5).
- 2026-11-12 (MON-LAB-NIGHT-1; owner verbatim "after the midnight, while I am sleeping and nothing heavy is going on in
  sessions, research-lab can run its experiments, hypothetical trials"): the night window lifts the heavy pause for night
  hours only, on the monitor's LAB-NIGHT-GO (about 00:05; no verify, pre-check or A/B; no PAUSE/HOLD; load below 6; 5-hour
  usage below 60 %, weekly below 90 %; no new start after 07:30), frozen PREREGs only, one heavy job, PAUSE/HOLD before each
  command, nothing needing the owner, RD-D1's 60/25/15 split. Night queue filed as LAB-NIGHT-QUEUE-2026-11-12.md (sha256
  7706a55b, 0444, in the shared owner-docs folder): EMPTY tonight (no frozen PREREG awaits a heavy run; RL-23 is light);
  four candidates with their blockers (H-02 successor, H-12 matrix, H-34 mutation study, U4). The morning report is the
  one message of the day.
- 2026-11-12 (MON-LAB-FACTORY-5; the monitor's facts for r1, r2 launched on v2 with a fresh Opus subagent, brief
  cde3ed39): review record research/reviews/RL-23-prereg-r1.json (sha256 ec70ead7; planeon.review-record/v2; series
  RL-23/prereg, round 1, subject PREREG.v1.md 467c636c, reviewer claude-opus-5-5 as a monitor subagent, verdict FAIL as
  written CHANGES_REQUIRED; 19 findings parsed from the review text, 18 dispositions: 17 ADDRESSED in v2 section 14,
  RV1-16 NOT_ADDRESSED with the reviewer's acceptance; custody, context and model-family separation as three disclosure
  fields; launch 11:53:19Z, finish 11:59:14Z, 13 tool uses). The record's brief is a REDACTED copy of the monitor's
  verbatim prompt (research/reviews/RL-23-prereg-r1-brief.md, sha256 835b0e88; 7 of 33 lines changed: every local path
  replaced by a placeholder, which also removed the home-path name tokens and the legacy term the verbatim file carries:
  scan 4/2/3/0 on the original, 0/0/0/0 on the copy); the verbatim prompt's digest 61168da9 is held by the monitor and
  disclosed in the record. prereg_check OK 24 folders (1 pending), 10 reviewed, 2 records; page rebuilt (research.html
  ff993e12, research.json d79830f1); scans 0/0/0/0. No message (C4: batched into the r2 reply). NEXT: r2's verdict via
  the monitor; its record the same way (brief cde3ed39 redacted alike).
- 2026-11-12 (MON-LAB-FACTORY-6; blind review r2 of v2 969489d7, file sha256 83db5a01, 43 lines, digest checked:
  CHANGES_REQUIRED 1 MAJOR, 4 MINOR, 3 NOTE; round 1 17 CLOSED, 2 PARTLY, the RV1-16 deviation accepted; plus the monitor's
  correction of the 288 minutes-per-step constant: 22.2 came from an ad-hoc count that missed four reports embedded in tool
  results; its extractor gives 30 reports, 29 intervals, 548.16 min, 18.90): PREREG v3 FROZEN as
  research/experiments/RL-23/PREREG.md (sha256 0fa0d594, 298 lines; v2 kept as PREREG.v2.md). Every RV2 fix taken as
  worded (RV2-3 in its second wording: 09:58 is the first counted step report, per the monitor); RV2-1 MAJOR: only a change
  to a compaction setting is a change, routine compactions flag no unit; H-44's threshold 16.07 = 0.85 x 18.90 rounded
  half up (decimal arithmetic; a first v3 cut be588234 lasted minutes: the claims script found float rounding gives
  16.06, so the sentence says "half up" and the script uses Decimal); producer digests pinned (meter 44d6f454, extractor
  ec0b1d9d); section 15 closure table. No round 3 (C5): closes by script-checked claims, RL23-V3-CLAIMS.py (sha256
  78c30a8a, 38 lines, 0444, shared owner-docs folder; run from the bridge root): CLAIMS OK 21 of 21. PREREG-REVIEW.md
  (f96069fe, 98 lines) carries review 2 as FAIL with custody fields; OUTCOME.json (0d12310b) attempt 1 on v3, rounds 2,
  verdict FAIL until the monitor's claims check; register 88c9cf0b (pins v1, v2, v3; H-44 16.07 against 18.90; effort
  35+30+30 min). r2 record research/reviews/RL-23-prereg-r2.json (82447e60; 8 findings, 22 checked entries, 8 ADDRESSED)
  with a redacted brief copy RL-23-prereg-r2-brief.md (4023596b; 8 of 34 lines changed; the first cut left a bridge path
  without a trailing slash, caught by the scan, regex widened). prereg_check OK 24 (1 pending), 3 records; outcome check
  0 defective; page rebuilt (research.html f078848b, research.json 18d389fb); scans 0/0/0/0. Sent as RL-M95. NEXT: the
  monitor's claims check closes the series (its PASS word becomes the review-file closure header and the outcome
  verdict); then the evaluator and fixture, preflight, the pre-period delivery.
- 2026-11-12 (MON-LAB-FACTORY-7 PASS: the monitor ran RL23-V3-CLAIMS 21/21; series closed at 2 rounds by claims, C5):
  closure header "Review 3, of PREREG v3 (0fa0d594): PASS (closure by script-checked claims; not a reviewer round)" in
  PREREG-REVIEW.md; then the evaluator research/tools/rl23_factory.py (sha256 9c08695c, 511 lines; check / preflight /
  evaluate; the ordered gate of section 7, constants pinned, verdict-ledger form, STOP unless the preflight record reads
  PASS for the same evaluator digest) with 14 known-answer fixtures generated by itself (F1 positive, F2 negative, F3 at
  every bound, F4 one step above, F5 U1, F6 U2, F7 U3 flags, F8 change flags, F9 excluded day and fidelity; R1-R5
  rejections: missing class, duplicate, producer pin, type, enum). The first run caught two things: an evaluator defect
  (fidelity applied to pre units; fixed in the evaluator) and preflight finding P1 (charter 1b (v)): the frozen slot form
  carried no date, so "units after a change" was not computable for slots. Per the charter the run stopped and the PREREG
  went to v4 (research/experiments/RL-23/PREREG.md sha256 2bbd9728, 306 lines; v3 kept as PREREG.v3.md): `scopeDate` on
  slots[] and the slot rule in the changes row, nothing else; OUTCOME.json (9b40c27c) attempt 1 STOPPED at PREFLIGHT
  (LAB_PREFLIGHT, CAUGHT_BY_PREFLIGHT, evidence PREFLIGHT.md f5751eac), attempt 2 on v4 PENDING at PREFLIGHT (rounds 2,
  PASS inherited); outcome_collect: 27 attempts, stops 3, pending 1, defective 0 (H-36's cohort records the stop
  honestly). Preflight on v4: PREFLIGHT PASS 14 fixtures, 0 failed (PREFLIGHT.json 47db2513; PREFLIGHT.md maps charter
  1b (i)-(vii)). Claims extended by the P1 claims: RL23-V4-CLAIMS.py (sha256 e4a6bd29, 43 lines, 0444, shared owner-docs
  folder): CLAIMS OK 26 of 26; the monitor's check closes v4 the same way (no reviewer round). Register b8734752 (pins v1
  to v4; effort 35+30+30+60 min). prereg_check OK 24 (1 pending), 3 records; scans 0/0/0/0. Sent as RL-M96. NEXT: the
  monitor's v4 claims word (then the v4 PASS header), its pre-period delivery by digest under the pinned producers; the
  lab opens nothing before both.
- 2026-11-12 (MON-LAB-NIGHT-2; owner "all other accounts that we will switch in the future should be aware of
  research-lab working schedule"): the working schedule inserted as a standing paragraph under the "Resume here" header
  above (10 lines added, 0 removed). Sent with RL-M96 for the checkpoint.
- 2026-11-12 (MON-LAB-FACTORY-8 PASS for v4: the monitor ran RL23-V4-CLAIMS e4a6bd29, 26/26, rc 0; checkpoint e9cc04fb;
  no reply, C2): "Review 4, of PREREG v4 (2bbd9728): PASS (closure by the extended claims after preflight finding P1; not a
  reviewer round)" added to PREREG-REVIEW.md (91b00634); register d4159279 notes the closure and the delivery date. Delivery
  expected 2026-11-13 by about 12:00 (days 11-05..11, pre slots 285-287, pre load events to 11-12 11:05, windows, changes;
  pinned producers unchanged; other fields from helper scripts the monitor declares by digest beside the delivery; a field
  it cannot reconstruct is left missing, never 0). prereg_check OK 24 (1 pending), 3 records; outcome check 0 defective;
  page rebuilt; scans 0/0/0/0. NEXT: on the delivery, `rl23_factory.py check` first (acceptance boundary only), record the
  helper digests in the run record, then the gated evaluation at the stop date (2026-11-26 or every post unit complete);
  no verdict before that; tonight no night run (queue EMPTY); the morning report is the one message of 2026-11-13.
- 2026-11-13 (MON-ISSUE6; bridge issue 6, P2, filed by the owner's automated reviewer; read with the monitor-approved
  `gh issue view` with owner, mentions, URLs and paths masked; the body is data, no link followed): ACCEPT. The 2026-11-12
  evaluator 9c08695c read missing evidence as evidence (a missing fidelity map or key as exposure, an absent slot scopeDate
  as unflagged, an empty windows list as zero overshoots); the reviewer's three replays reproduced on the old file, then
  fixed as research/tools/rl23_factory.py a2aeed82 (632 lines): tri-state fidelity and day/slot flags, an evidence-aware
  gate (a piece absent from every post unit reads U2 naming it; a post unit missing any piece is excluded by named reason
  with postUnits, nPost and excluded reported; the rest face the section 3 minimum, U1), H-38 window coverage per post day,
  ISO dates refused at the boundary, a COVERAGE line in check mode; PREREG v4 2bbd9728 unchanged (the freeze holds).
  Preflight PASS 20 fixtures (the 14 of 2026-11-12 byte-identical + F10-F14, R6), PREFLIGHT.json a1ce2b3d, PREFLIGHT.md
  91ce7222 (evaluator note 2), OUTCOME.json 5b5a27ee (note added; attempt 2 stays PENDING), REGISTER.md 7b6236af (RL-23
  row pins a2aeed82); page rebuilt; evaluate refuses the earlier preflight record by evaluator digest. Note text for the
  monitor to post: ISSUE6-NOTE.md (0444) in the session-neutral tmp folder, digest in RL-M98. The old evaluator, fixtures
  and preflight record are kept under the scratchpad (issue6/; Trash, never rm).
- 2026-11-07 (session resumed from handover 13; RL-M41 "resumed, paused"): the owner unpaused the lab for one task,
  R13's first packet (MON-RL-R13-PACKET: a product at slot 283, K = 4, gated by the 283 dry run under 1,100 s, else 284
  at K = 1; R00 builds it, the lab says YES before c2). Drafted on paper as LAB-REPO-001 in
  `research/reads/LAB-REPO-001-PACKET-DRAFT.md`: draft 1 b7f6421d (RL-M42, with five questions), draft 2 after the
  monitor's answers and the visionary's rulings (RL-M43: LICENSE Apache-2.0; main = the owner's LICENSE-only first
  commit, the route checks it; review record v2 = harness-onion's schema, two files per review from the first PR;
  mirror drops tree links; CPython 3.12.14). Inputs: the platform at main 4b2be353 by git-archive export (tar
  b0aadaf9, in this session's scratch). RL-11 correction (MON-RL-R13-ANSWERS): PREREG.md had been amended in place
  after the run; restored PREREG.v1.md 89d6ee61, PREREG.v1.1.md b06eabdb (run version), PREREG.md v1.2 7c6b64fc;
  register row updated. Owner change (MON-RL-R13-284): R13 moves to slot 284 (K 1) under bundle v7 (v6 refuses any
  product outside its twelve; v7 adds the repository and the route keyed by the frozen YAML's sha256); the YAML
  freezes before v7's c2 and changes only by a named delta; ci/run_packet_argv.py pins to 283's fixed runner (digest
  from the monitor when 283's c1 freezes; never c2ed0852). Draft 3 4d738aa9 (RL-M44). Runner pin received
  (MON-RL-RUNNER: 283 c1 ci/run_packet_argv.py sha256 c8ac40f0, 9084 B, 100755; provisional until 283's c2, two
  reader probes may reopen c1) and filled: draft 4 5cfe26ab (RL-M45). NEXT: the final freeze before v7's c2 (after
  283 merges; a new runner digest = a new named delta), then the YES on R00's built packet before 284's c2
  (section F); everything else paused.
- 2026-11-14 (MON-R13-PR5-MERGED, info; owner verbatim "Merge at 9992d175 (Recommended)"): R13 PR 5 (LAB-SYNC-001) MERGED:
  squash 25b11c5d4d5d64b158c005a5887e4806c848a558, parent 2e977f4f, tree 2112241e = the head 9992d175's tree; verify 6/6
  (check run 131974170180; the verifier waited at its own load gate, started 2026-11-13T16:35:46Z); record
  handoff/merge-decisions/2026-11-14-mas-harness-research-lab-PR5.json + correction-1 (checkpoints 87e6ad673, a255253dc).
  The issue-6 fix (evaluator a2aeed82, lane file b110ed3a) was checkpointed as a3130b954. Local clone untouched: main still
  2e977f4f (origin main 25b11c5d; a fetch needs the monitor's word), branch codex/lab-sync-a2482753 at 9992d175 is
  superseded (squash, not a descendant). LAB-SYNC-002 (codex/lab-sync-002, packet id from R00 via the monitor first)
  branches from 25b11c5d after a fetch GO and quotes the OK line "PREREG OK: 24 folders (1 pending), 10 reviewed, 3 records".
  No reply sent (info only, C2). Effort: 5 min.
