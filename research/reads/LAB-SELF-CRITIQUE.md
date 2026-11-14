# Self-criticism of the Research-Lab's R&D decisions (SC-D2), 2026-11-10

Owner request (chatbox, 2026-11-10): a comprehensive, complete and concise self-criticism of the lab's R&D decisions
about the agentic harness platform. Method: the lab's own data record (research.json f56c987e: 36 hypotheses, 23
experiments, 29 runs), the claims table (46 rows), the register, the lane file (7bcd23e3), meta-review 001 and the
three R13 issue triages, read by script and by hand; no run, no network, no subagents. Every number below comes from
those records; opinions are marked. The visionary's self-critique (SC-D1, 79067647) judged the decision to open the lab
and its heavy share (its C6, correction F); this document judges the decisions made inside the lab's charter, which
are mine.

## 0. Verdict

In seven days the lab produced a complete, auditable experimental record at near-zero compute: every verdict derives
from a pinned input by a named script, every claim has a row, every report says what it does not show. It has not yet
changed anything the product does. Its results are mostly checks of contracts and records the programme wrote about
itself; the hypotheses that would measure the harness as a harness (effect on the banking use cases, strategy
switching, routing, cohorts) are blocked on a product that does not run, and I did not design them on paper while
waiting. Speed, breadth and process were my choices; depth, independence from my own framing, and coupling to a
running system were not, and the first three were bought with the last three. The form of the record I would keep;
the hypothesis mix, the review custody, the publication route and the protocol's growth I would change now.

## 1. Evidence

| Measure | Value | What it says |
|---|---|---|
| Hypotheses | 36: 20 with an experiment, 1 READY, 15 BLOCKED | 15 wait on product items that do not exist yet |
| Stream S1 (qualification-critical, 60 % of the heavy share) | 12 hypotheses: 8 BLOCKED, 4 run | the stream given most compute has the least runnable work |
| Heavy GOs requested by the lab | 0 (29 runs, all light) | the split allocated compute that was never asked for |
| Experiment dates | 23 experiments 2026-11-04 to 07; 22 inside three days | breadth over depth |
| Verdicts | PASS 8, FAIL 8, UNRESOLVED 7 | |
| FAIL composition | 4 "as preregistered" (RL-15, RL-17, RL-18, RL-20), 1 my clause-scoping error restated as PASS (RL-10 to RL-12), 3 substantive negatives (RL-05, RL-06, RL-09) | half the FAILs were foreseen before the run |
| Claims by evidence type | documentary 22, empirical 13, simulation 11 | half the evidence is reading documents |
| Claims by instrument validity | VALID 12, VALID_WITH_LIMITS 24, INVALID 4, NONE 3, DESCRIPTIVE 2, UNDERPOWERED 1 | a quarter of the claims rest on a limited or absent instrument |
| Decisions changed by results | 1 reviewed roadmap-builder change (RL-15 proposal, lock 40); 0 product-code changes; about 6 notes and inputs; 2 proposals ruled not gate material or disposed | evidence delivered, little consumed |
| Product uptake of design reads | condition (v): N_shadow 10, 3/N, 15 s cap; Q-048-1: (b) with C1 to C4; Q-C286-2: the E1 check, now a 467-line tool, a contract section and two lab reads | all of the lab's product influence is on chain machinery |
| Register effort and decision columns | 0 of 23 rows | the lab measured the programme's cost per packet (RL-06) and never its own |
| Blind PREREG reviews | 21 rounds, 10 experiments; 13 blocking findings (scope 6, pinning 4, gate 3); 20 of 21 rounds returned exactly three notes | the review found form |
| Pre-run stops | 2, both found by the lab's tooling, 0 by the review | the review never saw an instrument |
| External review (R13 issues) | 3 issues, 3 accepted at least in part, each naming a defect the in-house review missed | |
| Protocol | README 153 lines, section 2 is 82; 7 preflight sub-steps and an outcome record adopted 2026-11-07 to 09, each within a day of a finding; the hypothesis that tests them (H-36) is blocked | patched reactively, untested |
| Tools and text | 37 experiment scripts, 11 process tools; 316 files, about 7,000 lines of prose, 5,500 of Python | |
| Publication | nothing in the lab repository until the owner noticed (2026-11-07); then six drafts and sub-revisions of a 602-line packet, about 20 of 83 milestones, merged 2026-11-09 | three of seven days on plumbing |
| Owner's reading view (progress/) | last updated 2026-11-06; two results, one meta-review and three issues since | not kept current as the charter says |
| Milestone messages | 83 in seven days, through one relay | about twelve a day |
| RL-14 (the programme's own working method) | rho +0.12, interval -0.41 to +0.36, n 23; descriptive signs opposite | no evidence yet that typed records reduce slips |

## 2. Criticisms

C1. I chose breadth. Twenty-two experiments in three days, each a light pass over records the lab already held. Each
is a real check and each is small; none took a second day. The question that would have taken a week (H-12, the harness
effect against the model effect) stayed blocked, and I did not design its matrix on paper, which its register row names
as the first step.

C2. I let documents set the hypothesis set. Thirty-five of 36 hypotheses carry a section and a score from the three
owner-supplied syntheses; at most six (H-07, H-09, H-10, H-28, H-30, H-36) start from something observed to go wrong in
the programme. The rest ask whether our own contracts have the properties we wrote into them, and such checks pass
by construction at a high rate (RL-07 116 of 116, RL-20 52 of 52, RL-21 4,335 of 4,335). A result that cannot surprise
is a test, not research.

C3. I preregistered FAILs I expected. RL-15, RL-17, RL-18 and RL-20 record FAIL "as preregistered" because the gate sat
where a known limitation of the form would fall. The ledger stays honest and the verdict says nothing new; the
information was the form's limit, known before the run. Those belonged in a preflight, and the ids in what I did not
know.

C4. I did not watch consumption. Forty-six claims, no product change, one builder change, the rest notes; two proposals
ruled not gate material. The charter is right that the lab has no authority. But no register row records the decision
its result fed (the claims table's decision field came after issue 1), so the near-zero ratio was invisible to me until
today.

C5. My design reads added mechanism to the chain. The three reads the product took up each add rules to the verifier
and chain machinery: the shadow period, the demotion conditions, the E1 isolation check. On Q-C286-2 I ruled count with
E1 over restart, which bought a 467-line tool, a contract revision and two lab reads for a case I wrote "should be rare"
and never estimated. The visionary's C4 (machinery in the critical path) applies to me as co-author. Opinion: restart
was the cheaper rule and I argued past it.

C6. Review custody was mine. The blind PREREG reviews were passes briefed from this session; custody, context and
model-family separation were not recorded until meta-review 001 required them. Yield: 13 blocking findings, all on
form; none on instruments, which caused both pre-run stops and the acceptance-boundary defect the external reviewer
found (issue 3). I asked R00 for a non-author read of its tool while my own experiments had none.

C7. I patched the protocol after every finding. Seven preflight sub-steps and an outcome record entered the charter
between 2026-11-07 and 09, each within a day of an issue, none tested; the hypothesis that would test them (H-36) needs
five experiments the pause forbids. The lab now has 11 process tools against 37 experiment scripts and a six-command
publication recipe. Ceremony is cheaper to add than to remove, and I only added.

C8. Publication was late, then over-built. Nothing reached the lab's repository until the owner noticed; I then drafted
the bootstrap as a product-grade packet through the full admission chain: six drafts, about 20 milestones, three of the
lab's seven days. A push of the bridge folder with its manifest on day one, hardened later, would have given the
external reviewer three more days of material and found issue 3 sooner.

C9. The heavy split was planning without a plan. I co-designed the 60/25/15 split and the compute unit; the lab
requested no heavy GO, and the favoured stream has 8 of 12 hypotheses blocked. The owner has paused the share (SC-D1 F);
the accurate statement is that it was never used.

C10. The owner's reading view went stale. progress/ stopped on 2026-11-06 while the lane file grew past 750 lines and 83
milestones. I kept the record the monitor needs and not the one the owner asked for.

C11. My own cost is unmeasured. RL-06 measured the programme's throughput and verify cost; the lab recorded no minutes
and no tokens per experiment or review round, and the effort columns apply only from RL-23. The two usage pauses (weekly
61 % on 2026-11-04 and 05, the 98 % stop on 2026-11-09) are the only cost signal, and both came from outside the lab.

C12. I did not act on my own null result. RL-14 found no evidence that typed, digest-pinned handoff records reduce
resume slips (interval spanning zero at n 23, descriptive signs opposite). Since then I added two typed record forms
(CLAIMS, OUTCOME) and more structure to the lane file. UNRESOLVED is not a refutation, but it was a reason to stop adding
structure until measured; I read it as a reason for more.

## 3. What I would keep

The preregistration-then-ledger form with script-derived verdicts and the claims table. The export and privacy
discipline (pinned exports, never an oracle, scans before anything leaves). One-page reports with "what it does not
show". RL-01, RL-03 and RL-16 with the condition (v) read as the model of a result that fed a decision. The external
issue channel, which found what the internal review did not.

## 4. Corrections proposed (owner decision, proposed label SC-D2)

- A. Hypothesis gate: a new hypothesis names the observed failure, incident, pending owner question or release-gate claim
  it serves; "does contract X have property Y" checks go to a conformance list (one row, no RL id) unless the property is
  disputed.
- B. Depth: when rounds resume, one question at a time; the first two are H-12's matrix on paper (no compute) and the
  RL-16 shadow-half successor on the real shadow records; nothing else until one closes.
- C. Instrument checks are not experiments: an expected-class FAIL (the form cannot express the case) is a preflight
  finding; an RL id is spent only where both outcomes are possible.
- D. Review custody: a PREREG's blind reviewer is briefed by the monitor from the lab's frozen file, or runs under a
  different model family, and the record says which; the lab's own passes review nothing of the lab's.
- E. Protocol freeze: section 2 closes at its current text; a new step needs a named pre-run stop or escaped defect it
  would have caught; H-36's cohort decides whether (v) to (vii) stay.
- F. Consumption column: every claim row and register row names the decision or input it fed with the lock or note
  digest, filled at each visionary lock; the page shows consumed against recorded.
- G. Design reads: a read that adds a mechanism to the chain states the frequency of the case it serves (measured or
  bounded) and the mechanism's cost; with the frequency unknown, the read recommends the no-mechanism option.
- H. Publication: the lab repository takes the bridge folder at each checkpoint the owner approves, by the six-command
  recipe already in place, with no packet drafting; drafts are for product packets.
- I. Reading view: progress/ is generated by build_research.py from the data record so it cannot go stale; the lane file
  keeps the resume block and the last ten entries, older entries archived.
- J. Cost: minutes and token counts per experiment and per review round from RL-23 on; the lab's usage share reported
  with every milestone that ran anything.
- K. Message budget: one monitor message a day unless a GO or a ruling is needed.

Options: (a) adopt A to K (Recommended); (b) adopt the hypothesis and review corrections only (A, B, C, D, G); (c)
record the critique, change nothing.

## 5. Scope of this document

It criticises decisions made inside the lab's charter; the decisions to open the lab, give it a repository and a heavy
share are the visionary's C6 and correction F and are not re-judged here. No verdict, claim row or register entry is
changed. The owner's own instructions (the procedure of 2026-11-06, the issue-tracking rule, the pause) are named where
they interact with mine, not judged. Nothing here changes before the owner's word through the monitor.
