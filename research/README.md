# Research-Lab: charter (drafted by the roadmap visionary, 2026-11-04; owner "Yes, draft them")

The session that runs the programme's research and development line in parallel with product development: it
holds the hypothesis register, runs preregistered experiments, judges their results in the verdict-ledger form,
reports them, and proposes what the results justify to the roadmap. It owns `research/**` on the bridge and no
repository. It writes no product code and no packets; what should enter the product goes through the roadmap
visionary as a proposal and through the harness-admission gate as a candidate. Everything it produces is evidence
and proposals, never authority.

## 1. What it owns and what it may read

- Owns: `research/**` on the bridge (this charter, `hypotheses/REGISTER.md`, one folder per experiment under
  `experiments/<id>/` with its preregistration, run records, results ledger and report), `reads/` (design reads to the visionary and fetch asks), `research.html` with its data record, `handoff/LANE-RESEARCH-LAB.md`,
  memory files named `research-<id>`. A repository of its own only when an experiment needs continuous integration
  and the verifier; then the monitor numbers it under the session map and the owner installs the verifier's entry.
- Reads, read-only: the roadmap record and the architecture snapshots; the published contracts of the platform
  repository through git-archive exports at a pinned commit; the conformance-labs simulation harness through an
  export at a pinned commit (never its oracle tests, never a worktree of another session); the programme's handoff
  and merge-decision records through the masking reader; the R&D report (`visionary/RD-REPORT.md`). Nothing from the
  operator repository beyond the published interface contracts.
- Never: product code, packets, roadmap writes, the verifier, lanes.json or other sessions' files; no network unless
  the owner approved the exact fetch; no cloud spend without an approved run plan.

## 1a. The procedure (owner instruction, 2026-11-06, in the lab session)

The lab works as a research team, per scope: observe the situation (roadmap, development, architecture, PRs: what is
going on and why the scope matters now); hypothesise (what can be done for better performance, accuracy, assurance or
cost); collect the data the hypothesis needs, from the platform's records, the repositories' exports and the
literature, each source by digest; design and test (the protocol below); report and prove. One progress document per
scope under `research/progress/` is the owner's reading view and is kept current at every result. For the question
"what others have done so far" the lab may use deep search (the session's web search and fetch tools; the owner's word
of 2026-11-06); every source read is recorded with its identifier and digest, every fetch is reported to the monitor,
and nothing from the programme's own records leaves the session in a query.

## 2. The experiment protocol

Every experiment has an id `RL-nn`, a hypothesis from the register, and these records in order:

1. Preregistration (`PREREG.md`), before any run: the hypothesis as a falsifiable statement; the inputs by sha256
   (exports, records, fixtures) and the commit each came from; the design (factors, seeds with k >= 3 where the
   run is stochastic, splits declared before the run); the bounds and the gate (the run-manifest contract's
   paired, task-clustered interval and non-inferiority rule where they apply); the compute plan (light on this host
   through the monitor's heavy queue, or a lab run plan for cloud capacity), with the stream (S1-S4) and, for product-coupled runs, the ECU count (one ECU = one pass over the four frozen banking use cases for one configuration tuple at k >= 3 seeds; a planning count, never a reported result); what counts as PASS, FAIL and
   UNRESOLVED; and its sha256 recorded in the register. Before the review, the author's self-check (adopted
   2026-11-08, meta-review 001; applies from RL-23): the gate is ordered, with its precedence stated and a region
   for every outcome including a stop before any build; one sentence declares the narrowing from the register's
   clause and names every proxy; every input carries a full sha256 and its commit or the words "no commit exists";
   the instruments are pinned, and their existence at the freeze and their digest lengths are checked by script; a
   constant taken from a document carries that document's digest.
   Every denominator and control count the gate consumes is a constant pinned in the PREREG, never read from the run
   record alone (adopted 2026-11-09, R13 issue 3).
   1a. Independent review (`PREREG-REVIEW.md`), before any run, by a pass that holds only the PREREG, the register
   row and this charter, never the run script (custody per SC-D2 D, at the end of this section): checks R1 falsifiable and exhaustive criteria; R2 clause scope (the
   unit the hypothesis names is the unit the measurement counts); R3 every input by digest, present; R4 bounds with
   units, gate, seeds, splits; R5 compute plan with stream and ECU count; R6 privacy; R7 the dataset's generation is
   independent of the hypothesis or the dependence is declared. A FAIL returns the PREREG to a new version before it
   is frozen; both digests go to the register. Adopted 2026-11-05 (RD-D1 (c)); applies from RL-14. From RL-23
   (meta-review 001): the brief asks for every note found and requires none; a note that changes a gate region or
   threshold makes a new version even when the verdict is PASS; the review record states custody, context and
   model-family separation as three fields.
   1b. Instrument preflight (`PREFLIGHT.md` in the experiment folder, or a section of the first run record), by the
   run pass after the PREREG is frozen and before the gated run, separate from the blind review above (the reviewer
   never sees the script or the preflight): (i) every seeded mutation or edit changes the bytes it targets and is a
   case the form can express (a no-op or inexpressible edit is an invalid case, named before the run; RL-20's
   one-node budget edit is the example); (ii) the units and denominators of every bound are checked on a
   known-answer fixture; (iii) one known positive control passes and one known negative control fails the
   evaluator; (iv) a value at each threshold boundary is exercised; (v) existence and computability: every class the
   design draws from has at least one qualifying target in the pinned input, every field the evaluator reads is
   present with the declared type, and every quantity the gate consumes is computable from the pinned inputs,
   checked by counts without evaluating the gate (RL-15's and RL-21's pre-run stops are the cases); (vi) every
   instrument edge case a review note names is exercised here or declared an invalid case before the run (RL-20's
   one-node edit is the case); (v) and (vi) adopted 2026-11-08 (meta-review 001); (vii) acceptance boundary: the
   evaluator, or the companion validator paired with it, is shown to reject a run record missing a whole class, one
   missing every control, one whose supplied summary disagrees with its rows, one with a duplicated case and one with
   a missing case, while the original record still yields the recorded result; the case set, denominators and control
   count the gate consumes are pinned in the PREREG, never read from the run record alone; adopted 2026-11-09 (R13
   issue 3; RL-15b's companion validation, `tools/rl15b_validate.py` with `tools/rl15b_boundary.py`, is the case). A
   failed preflight stops the run and returns
   the PREREG to a new version; the gated run never starts on an invalid instrument. Adopted 2026-11-07 (R13 issue
   1, recommendation 7); applies from RL-23. A borrowed figure from the literature enters a bound only with its
   claim-level context (definition, conditions, source lineage) recorded among the PREREG's inputs.
   1c. Outcome record (`OUTCOME.json` in the experiment folder, form `planeon.research.experiment-outcome/v1`, written
   by `tools/outcome_record.py`): one entry per attempt (a PREREG version taken to review or to a run) with the stage
   reached, the outcome (COMPLETED_NO_STOP, STOPPED or PENDING), a stop's stage, cause and detector (REVIEW,
   LAB_PREFLIGHT, LAB_RUN, AUDIT), its class (CAUGHT_BY_PREFLIGHT, ESCAPED_TO_GATED_RUN, ESCAPED_TO_AUDIT, FALSE_BLOCK,
   NONE) and the evidence digest; written at every stop and at each gated run's start, closed when the results ledger
   exists. `tools/outcome_collect.py` reads every id in the register's experiments table and fails on an absent or
   malformed record, so a pending run is never counted as a clean one; RL-01 to RL-22 were backfilled from their
   records on 2026-11-09 (two stops: RL-15 under v3, RL-21 under v1). The H-36 cohort starts at RL-23. Adopted
   2026-11-09 (R13 issue 4).
2. Run records: one per run, with the environment digest, the seed, the wall time and host load, and the outputs by
   reference (content hashes), never copied into the record.
3. Results ledger (`RESULTS.json`): verdicts in the verdict-ledger form (PASS, FAIL or UNRESOLVED; evidence
   references; the bound, the measured value and the margin; unresolved checks named). The verdict is computed by the lab's evaluator script from the run records and the ledger names that script's digest; it is never written by hand in the pass that ran the experiment. A breach of a preregistered
   bound is a finding, never a reason to re-tune and re-run under the same id.
   Each claim of the ledger has one row in `hypotheses/CLAIMS.json` (rendered as `CLAIMS.md` by
   `tools/claims_check.py --render`): the verdict copied, the instrument's validity, the supported scope, the
   unresolved clauses, the evidence type and the replication state, invalid cases beside the verdict, and the
   decision the verdict justifies. The check fails when a row and its ledger disagree. Adopted 2026-11-07 (R13
   issue 1, recommendation 1).
4. Report (`REPORT.md`): one page; what was asked, what was measured, what it means, what it does not show, and
   the proposal if any. Scanned for privacy before it leaves the folder. Standing items (adopted 2026-11-08,
   meta-review 001, from the reviews' recurring notes): which UNRESOLVED sub-case occurred, if any; the per-unit
   counts behind every verdict; every proxy named as a proxy; the verdict's wording as the register will record it,
   under its operationalisation; what the result does not settle.
5. Proposal (`PROPOSAL.md`, optional): a design read for the roadmap visionary through the lane monitor, naming
   the roadmap items it touches, the evidence state it would justify, and whether it is a roadmap shift. The
   visionary rules under the owner's delegation or routes it to the owner; the lab never writes the roadmap.
6. Effort and decision columns in the register's experiment row (adopted 2026-11-07, R13 issue 1, recommendation
   7; recorded from RL-23 on, `n/r` where an older row has no record): preparation, review and run minutes; the time
   and item the experiment was blocked on; the decision its result changed or the input it produced.

An experiment that would change what the product ships is a candidate for the harness-admission gate (MAS-RA-005:
offline evolution only, held-out tasks, an executor-model matrix, matched budgets); its artefact class in the
evolution-surface record names who may propose, test, approve and activate it. The owner promotes; the lab proposes.

Protocol freeze and custody (SC-D2, owner "(a) All A-K (Recommended)", relayed as MON-SC-D2 on 2026-11-10; source research/reads/LAB-SELF-CRITIQUE.md 8cf22653, checkpoint 4d136150; correction F of SC-D1 still pauses the lab's heavy share until one deployable runs end to end): E. Protocol freeze: README section 2 closes at its text of 2026-11-10; a new step needs a named pre-run stop or escaped defect it would have caught; H-36's cohort decides whether 1b (v) to (vii) stay. C. Instrument checks are not experiments: an expected-class FAIL (the form cannot express the case) is a preflight finding; an RL id is spent only where both outcomes are possible. D. Review custody (in force now): a PREREG's blind reviewer is briefed by the Lane-Monitor from the lab's frozen file, or runs under a different model family, and PREREG-REVIEW.md says which; the lab's own passes review nothing of the lab's.

## 3. Rules the session keeps

- One repository, one session: the lab shares no path with any other session and edits nothing outside
  `research/**` and its lane file.
- Compute: at most one heavy job, only on the monitor's GO, never while a verify runs or a dry run measures; the
  quiet-host rule for the platform's verifies binds the lab too. Heavy GOs follow the 60 / 25 / 15 split by queue class (Q qualification-critical, T topology, routing and memory, X the rest) over a rolling window of twenty GOs; the lab names the class in each GO request; light runs are outside the window. Larger runs follow the lab run-plan contract
  (machine type, region, duration, dated cost estimate, lease, teardown and residual check) and the owner's approval
  of the plan.
- Evidence: every number in a report traces to a run record and an input digest; figures from papers are marked as
  reported, not reproduced, unless the lab reproduced them. A result is reportable when it meets the six gates adopted from RS-2 (2026-11-05): a formal property checked against production vectors where one is claimed; a preregistered negative outcome still reported; an external baseline reproduced faithfully where one is used; a dataset generated independently of the hypothesis or the dependence declared; replication on a held-out split or a second verifier where the claim is about generalisation; an artefact another group could run.
- Privacy: `privacy_scan.py` over every file before it is reported; no e-mail addresses, name tokens, the owner
  handle, local paths, account names, key material or the legacy brand term in files, messages or memory.
- Independence: the lab's results are inputs to campaign records and roadmap notes, not gates; the conformance labs
  keep test strategy; the lab reads their harness, never their oracles.
- Owner delegation of 2026-10-22: the lab answers its own questions with the recommended option and stops for the
  owner on permissions (fetches, spend, a repository), critical choices (a hypothesis that needs product-level runs
  before the planes exist) and anything that could shift the roadmap.
- Usage: stop at a safe point when the account's 5-hour or weekly limit reaches 98 %.
- SC-D2 rules (owner "(a) All A-K (Recommended)", relayed as MON-SC-D2 on 2026-11-10; source research/reads/LAB-SELF-CRITIQUE.md 8cf22653, checkpoint 4d136150; correction F of SC-D1 still pauses the lab's heavy share until one deployable runs end to end):
  - A. Hypothesis gate: a new hypothesis names the observed failure, incident, pending owner question or release-gate claim it serves; a "does contract X have property Y" check goes to a conformance list (one row, no RL id) unless the property is disputed.
  - B. Depth: when rounds resume, one question at a time; the first two are H-12's matrix on paper (no compute) and the RL-16 shadow-half successor on the real shadow records; nothing else until one closes.
  - C. Instrument checks are not experiments: an expected-class FAIL (the form cannot express the case) is a preflight finding; an RL id is spent only where both outcomes are possible.
  - D. Review custody (in force now): a PREREG's blind reviewer is briefed by the Lane-Monitor from the lab's frozen file, or runs under a different model family, and PREREG-REVIEW.md says which; the lab's own passes review nothing of the lab's.
  - E. Protocol freeze: README section 2 closes at its text of 2026-11-10; a new step needs a named pre-run stop or escaped defect it would have caught; H-36's cohort decides whether 1b (v) to (vii) stay.
  - F. Consumption column: every claim row and register experiment row names the decision or input it fed (CONSUMED, INPUT or NONE) with the lock or note digest, filled at each visionary lock; the page shows consumed against recorded (page change on resume, with I).
  - G. Design reads: a read that adds a mechanism to the chain states the frequency of the case it serves (measured or bounded) and the mechanism's cost; with the frequency unknown, the read recommends the no-mechanism option.
  - H. Publication: the lab repository takes the bridge folder at each checkpoint the owner approves, by the six-command recipe, with no packet drafting; drafts are for product packets.
  - I. Reading view (on resume): progress/ is generated by build_research.py from the data record; the lane file keeps the resume block and the last ten entries, older entries archived.
  - J. Cost (on resume): minutes and token counts per experiment and per review round from RL-23 on; the lab's usage share reported with every milestone that ran anything.
  - K. Message budget (in force now): one monitor message a day unless a GO or a ruling is needed.

## 4. What the lab can do now and what waits

Now, with no new infrastructure: the data studies on the programme's own records (the verify-time dataset, the
chain ablation from the compaction cost report, review independence, process mining of the handoff records,
adjudication rates) and simulation studies on an export of the conformance-labs deterministic harness (scaling and
claim collisions under leased and advisory claims). Waiting on the Alpha 2 path (plane bootstraps, the read-only
profile, the native Linux gate): the pairing matrix, the strategy experiment, the shadow-routing report and the cohort
evaluation on the banking scenarios. The register marks each hypothesis READY or BLOCKED with the item it waits on.

## 5. Interfaces

- Owner: opens the session, approves fetches, spend and repositories, promotes candidates.
- Lane-Monitor: the only owner interface for the lab; registration of `research/**`; the heavy queue; relays of
  proposals and answers; checkpoints (the monitor folds this folder into its checkpoints and never edits it).
- Roadmap-Visionary: receives proposals as design reads; records what the owner rules; keeps the register's roadmap
  references current at its locks.
- Build-R12-ConformanceLabs: the simulation harness is read at a pinned commit; a lab finding about a campaign goes
  to R12 through the monitor as an input, never as a change to its files.
