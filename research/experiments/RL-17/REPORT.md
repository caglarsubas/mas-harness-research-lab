# RL-17 report: replay correctness on the exported simulation harness (H-27, replay half)

**Asked.** On the conformance labs' simulation harness at b4bbea79: are runs deterministic (H-27a); does the
committed REPLAY_STALE class row reproduce (H-27b); are duplicated and stale (reordered) board operations refused
after a run (H-27c); and does the recorded operation sequence, replayed through a fresh board, reproduce the claim
and merge answers, the register's own clause (H-27d)? Preregistered as v2 (77015690) after one failed review (v1
15939132; `PREREG-REVIEW.md`). The fault-class half of H-27 is a later id (BLOCKED on DATA-CORRECTNESS-001).

**Measured.** Run-001 35f3d6a9; data f5fe694a; RESULTS 7f8a3356. 13 classes x 32 seeds. H-27a: 416 of 416 run pairs
byte-identical. H-27b: C3's class row equal to the committed one (result PASS, no differing key). H-27c: 70,169
duplicate replays, all answered DUPLICATE_ID, none changed state; 39,795 stale replays (versioned operations with a
fresh id and the original expectedVersion, posed at the deadline tick), none accepted, none changed state, but none
answered STALE_VERSION: 30,504 were refused as NOT_HOLDER and 9,291 as MERGED. H-27d: 0 of 416 runs replayed the
claim and merge sequence identically through a fresh board; the first divergence was at a MESSAGE in 384 runs and at
a VERIFY in 32; every VERIFY replay (10,082) raised inside the board; agreement by kind: RELEASE 109 of 113, ACQUIRE
6,149 of 8,095, RENEW 17,686 of 25,223, ASSIGN 2,045 of 3,349, MERGE 817 of 9,461, MESSAGE 32 of 20,388, VERIFY 0.

**Verdict: FAIL as preregistered, with one claim UNRESOLVED.** H-27a PASS; H-27b PASS; H-27c UNRESOLVED by the
preregistered rule (every stale replay was refused, but by the holder and state checks that run before the version
check, so the version rule itself was not shown; the lab expected STALE_VERSION and says so); H-27d FAIL, the
outcome class the PREREG named: the board is not a pure function of its operation stream. An exception in the
fresh-board replay counted as a divergence (review 2 note 3), and FAIL took precedence.

**What it means.** The exported harness is deterministic and its committed replay class reproduces; its board
refuses every duplicate before any other check and refuses every late versioned operation, though by holder and
merge state rather than by version at the deadline tick. The register's clause fails for a reason the design
predicts: the board reads the workers, the coordinator, the artefacts and the task-pass state for verification and
merge, so the effect log alone cannot replay merges through it. Replay safety in this harness rests on durable
simulation state, not on the log, which is the D1 question (RS-1 and RS-3: "replay safety often depends on durable
tool-side state"). The claim operations that need no such state (RELEASE, most ACQUIRE and RENEW) replay; VERIFY
and MERGE do not.

**What it does not show.** "The coordinator" is represented by `Board.apply` (the harness's coordinator board);
"reordered" is the stale-version late arrival, not a permuted log: both are proxies, declared. The stale vector was
posed at the deadline tick, after leases had expired, so the holder check fired first; a vector posed mid-run
(before expiry) would reach the version check and is a new id. Nothing about the production coordinator (R04/R08),
only the labs' simulation of the contracts.

**Proposal.** None as a roadmap read. Two inputs: for R12 through the monitor, the stale-version vector mid-run
(a new id, RL-17 names it) and the observation that the board's refusal order is holder, state, then version; for
the visionary's DATA-CORRECTNESS-001 and D1 notes, that log replay through the board needs the durable state the
board consults, so the replay contract should name that state as an input, not only the event log.
