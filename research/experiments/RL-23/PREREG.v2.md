# RL-23 PREREG v2 (frozen 2026-11-12, after blind review r1): an observational study of the factory trials H1 to H8

Asked by the monitor (MON-LAB-FACTORY-1; owner: "all these trials can be a good hypothesis and data for
research-lab"). Paper only, no run, no network, no heavy step. This is the lab's one open paper stream (C7); the
rule B order (H-12's matrix, then the RL-16 successor) queues behind it on the owner's word of 2026-11-12. The
document is a PREREG in the charter's form (README section 2, frozen text of 2026-11-10; no new protocol step is
added). Adopted by the owner on 2026-11-12 (verbatim, relayed as MON-LAB-FACTORY-2: "Adopt all eight (Recommended)")
from the draft research/reads/FACTORY-STUDY-PROTOCOL-v1.md (sha256 6c0e8f6106d4e3b1a3d1f8f0924577033526962c6a44b8406855ebdd15c95673).
Version 1 (sha256 467c636c74e8a60a674b6a5ec5a1967c26ccee711c22278cdbf930c15666cffe) differed from the draft only by the two pinned
slot-288 constants in section 4, the H-44 thresholds they fix, the producer pin in section 6, section 11's registration
record and section 13's self-check. Version 2 closes blind review r1 (sha256 3ecd616c393b8da610c49cc42d449195cd6abf9b73692dcc667f7dfd9e56f6c8,
CHANGES_REQUIRED: 1 MAJOR, 11 MINOR, 7 NOTE) as section 14 records; no delivery was open at either freeze. No aggregate
file is opened before the blind review reads PASS and the evaluator's preflight passes.

Inputs, all by full sha256 and commit:

| input | sha256 | commit |
|---|---|---|
| the monitor's study brief, LAB-FACTORY-STUDY-BRIEF.md (24 lines) | 7325ba8fb7553d2fb5924d9295e46e69dfe0a521862c4ad5976f15a9661c435b | no commit exists (0444 file in the session-neutral tmp folder) |
| bridge handoff/FACTORY-IMPROVEMENTS.md (interventions, dates, baselines) | 0bc476b1cfc8e63338b7271306f805f40c5c0ff23666d957dcaa05f2b461a0b7 | bridge 3e1db1bb |
| bridge handoff/FACTORY-CONVENTIONS.md (C1 to C12 texts) | 16f7ffd1359110ba06ad6235f0294cb84bf6948fc31e500efab78ad6f3c618ce | bridge 3e1db1bb |
| research/README.md (the charter; section 2 is the protocol) | 608eaf26d1ba78616830a1b2e10e9a0237ad22235cee2f4e0ddee9207fe383af | bridge 3e1db1bb |

Every fixed baseline number below is copied from those two bridge files or the brief, except the two slot-288 constants
pinned in section 4 from MON-LAB-FACTORY-2; the pre medians of H-37, H-39 and H-40 are computed by the evaluator from
the pre-period delivery under the pinned producer digests. The gate never reads a baseline from a run record.

## 1. What is studied and why now (hypothesis gate, rule A)

The monitor changed how the factory works on 2026-11-12 in eight ways, each after an observed cost. The study asks
whether the measures the monitor named moved, by how much, and whether the guard measures (defects found later,
stop-line overshoots, lost detail) stayed flat. It is observational: no unit was assigned at random, the changes
were bundled, and every verdict reads "consistent with", never "caused by".

| H | intervention (source: FACTORY-IMPROVEMENTS.md step) | observed cost it serves |
|---|---|---|
| H1 | C1 to C4 and C9 message and context conventions (step 2, step 9; sent to ten lanes 2026-11-12) | the token baseline of 2026-11-11: cost = calls x context; the monitor 872 calls a day at 262 to 445K mean context |
| H2 | adaptive usage watch (step 1, 2026-11-12 ~11:10) | about 144 watch calls a day, about 16 percent of the monitor; the 2026-11-12 17:29 overshoot (81 to 100 percent in 20 minutes after a six-session fan-out) |
| H3 | Spotlight exclusion of the workspace and the tmp folder (step 3, owner, 2026-11-12 ~11:05) | load 15 to 20 after worktree creation and pushes; 11.65 / 11.76 / 13.54 at the 10:13 checkpoint, 5.21 / 10.14 / 12.68 right after (inside the excluded 11:05 to 12:00 purge window; not a result) |
| H4 | review-round cap 2 with fast checks before round 1, C5 (step 4; rule to R00 at slot 288) | slot 287: eight review cycles, about a day from scope to merge |
| H5 | dry c2 at the contract stage, C10 (step 11; from slot 289) | slot 288: 5 c2 builds |
| H6 | pre-approved GO chains, C11 (step 12; from slot 289) | slot 288: about 16 rulings, about 8.5 hours from scope to PACKET r1 |
| H7 | shape matrix for machinery, C12 (step 13; from slot 289) | slot 288: the v2.5 reader repair inside a product slot, 4 MAJOR across 2 rounds |
| H8 | R00 auto-compact at 50 percent of the window (step 14; the owner types the setting at slot 289's start) | R00 745 calls at 487K mean context in slot 288; slot 288 took about four times the usual cycles |

## 2. Hypotheses (falsifiable statements, as the register would record them)

- H-37 (H1): on full post days the monitor's API calls per message handled and its mean context per call are both
  at most 0.75 of the pre-period medians. Guard: none; the report states that no guard is tested.
- H-38 (H2): on every full post day the usage watch makes at most 50 API calls, and no post 5-hour window ends in an
  unconfounded stop-line overshoot (section 4).
- H-39 (H3): the pooled median 1-minute host load over verify-start events and post-push events (within 10 minutes
  after a push or worktree creation), without other-app load, is at most 0.70 of the pooled pre median; each kind is
  also reported separately. Guard: none; the report states that no guard is tested.
- H-40 (H4): every review series in every post slot (289 to 292) closes in at most 2 rounds, and later-found defects
  per slot (post median) do not exceed the pre median of slots 285 to 287.
- H-41 (H5): committed c2 builds per post slot (median) are at most 3, and later-found defects per post slot (median)
  do not exceed the pre median of slots 285 to 287 (section 4).
- H-42 (H6): rulings waited on per post slot (median) are at most 10, scope-to-PACKET-r1 wall time (median) is at
  most 6.0 hours, and later-found defects per post slot (median) do not exceed the pre median of slots 285 to 287
  (section 4).
- H-43 (H7): no post product slot contains a machinery repair, and machinery MAJOR findings per post slot (median)
  do not exceed 4 (slot 288).
- H-44 (H8): R00's mean context per call over post slots (median) is at most 365K tokens, mean minutes per step from
  scope to PACKET r1 (median) is at most 18.87 minutes, and lost-detail slips per slot (median) do not exceed 0. The
  thresholds 365K and 18.87 are absolute constants fixed at the first freeze from the rounded baselines 487K and 22.2
  (0.75 and 0.85 of them); section 7's raw-values rule applies to post values and to ratios of medians.

Narrowing from the owner's words: "benefit" is read as the monitor's own named measure per step, nothing wider.
Proxies: "message handled" stands for relay work (H-37); "rulings waited on" stands for coordination cost (H-42);
"lost-detail slip" stands for compaction harm (H-44); "later-found defect" stands for review quality (H-40). Each is
a proxy and is reported as one.

Manipulation checks: H-38's watch-call primary, H-40's rounds primary and H-44's context primary are largely fixed
by the intervention settings (the hourly watch, the cap, the compaction point); the report labels them manipulation
checks. H-40's cap is read over every series here, although the bridge's step 4 caps contract series by default.

## 3. Design

Before-and-after comparison on three unit types, with the intervention date fixed by the bridge file and a
transitional unit excluded. No randomisation, no model fitting, no p-values: medians, minimum and maximum, and the
count of post units that beat the pre median (the sign count) are reported for every measure.

| unit | pre period | excluded | post period | minimum n for a verdict |
|---|---|---|---|---|
| calendar day (H-37, H-38) | 2026-11-05 to 2026-11-11, the days the monitor's meter can rerun over its own transcripts (at least 3) | 2026-11-12 (partial day; interventions landed mid-day) | 2026-11-13 to 2026-11-19 | 3 pre and 3 post full days |
| load event (H-39) | events from 2026-11-05 00:00 to 2026-11-12 11:05 local that the verifier log and the checkpoint Host lines hold | events on 2026-11-12 between 11:05 and 12:00 (the purge of old index entries) | events after 2026-11-12 12:00 | 8 pre and 8 post events, each side with at least 3 verify starts |
| chain slot (H-40) | slots 285, 286, 287 | slot 288 (transitional: the cap reached R00 inside it and its rounds were seen at the freeze) | slots 289 to 292 | 2 pre and 3 post slots with per-series round counts |
| chain slot (H-41 to H-44) | slot 288 (single-slot baseline); 287's counts, if reconstructed, are descriptive only | none | slots 289 to 292 | 3 post slots (H-43: 3 post product slots); the defect guards of H-41 and H-42 use H-40's pre slots 285 to 287 |

Days run from 00:00 to 24:00 local time of the host, the clock the meter and the logs share. A slot belongs to the
post period by its number, whatever day it runs on. The study stops at 2026-11-26 or, if earlier, when every
declared post unit is complete (2026-11-19 ended, the last post slot at PACKET r1, every post slot's 7-day issue window
closed); reaching the minimum n does not stop collection. A slot whose 7-day window is open at the stop has
`postMergeIssues7d` missing. What has not reached its minimum at the stop is UNRESOLVED, sub-case U1.

## 4. Measures and their definitions

Every measure comes from an aggregate file the monitor produces (section 6). Denominators and fixed pre values are
constants pinned here; the pre medians of H-37, H-39 and H-40 are computed by the evaluator from the pre-period
delivery; where the brief gives a range, the pre value is the monitor's single per-day figure in that delivery.

| measure | definition | unit | pre constant |
|---|---|---|---|
| calls per message handled | monitor API calls on the day divided by cross-session messages sent plus received by the monitor that day | ratio | from the pre-period days (median) |
| mean context per call | the meter's mean input context per API call for the monitor on the day | tokens | median of the pre days (2026-11-11: within 262K to 445K as the brief reports) |
| watch calls | API calls attributed by the meter to usage-watch firings on the day | count | 144 (2026-11-11) |
| stop-line overshoot | a 5-hour window whose usage at the USAGE STOP message, or at the reset if no STOP was sent, exceeded 95 percent | event | one on 2026-11-12 (confounded: a six-session fan-out at 81 percent) |
| confounded overshoot | an overshoot whose window saw a fan-out of 3 or more sessions started at or above 60 percent | event | the 2026-11-12 case |
| start load | the 1-minute load average the verifier log prints at verify start | load | pre events (median) |
| post-push load | the 1-minute load of the first checkpoint Host line within 10 minutes after a push or worktree creation | load | 11.65 at the 2026-11-12 10:13 checkpoint (one of the pre events) |
| other-app load | the monitor's flag on an event when another workload (containers, a local model) ran | boolean | excluded events |
| rounds per series | review rounds a named series used in the slot (contract, source, reader, PACKET, paper) | count | 287: 8 cycles over its series (pre slots 285 to 287 by delivery) |
| later-found defects | oracle failures after the series closed plus PACKET MAJOR findings plus issues opened on the merged slot within 7 days | count | pre slots (median) |
| c2 builds | committed c2 builds the slot took before PACKET r1; C10's uncommitted dry c2 is not counted and is recorded as `dryC2Runs` | count | 5 (288) |
| rulings waited on | monitor rulings the build lane waited on between scope and PACKET r1 | count | about 16 (288) |
| scope to PACKET r1 | wall hours from the scope message to PACKET r1 | hours | about 8.5 (288, the brief; the step-report span is 8.87 h) |
| machinery repair | a change to chain readers, class rules or kit tools made inside a product slot | count | 1 (288, the v2.5 reader) |
| machinery MAJOR | MAJOR findings against machinery files in the slot | count | 4 (288) |
| R00 context | the meter's mean input context per API call for R00 over the slot's days | tokens | 487K (288; 745 calls) |
| minutes per step | mean wall minutes between consecutive step reports of the build lane from the scope message to the last report before PACKET r1 launches (the window of H-42's wall time); a step report is a build-lane message to the monitor carrying the slot's packet id or lane-milestone id; the first interval starts at the scope message | minutes | 22.2 (288: 25 reports from 09:58 to 18:50 local on 2026-11-12, a 532-minute span, 24 intervals; delivered by the monitor as MON-LAB-FACTORY-2 before this freeze; the monitor's full-slot figure at 288's merge is descriptive only) |
| lost-detail slip | a case the monitor records where the build lane re-established a fact from before a compaction and a ruling or a round was spent on it | count | 0 (288: four compaction events on 2026-11-12, no recorded case; delivered by the monitor as MON-LAB-FACTORY-2 before this freeze) |

## 5. Confounders declared, and how each is handled

| confounder | recorded as | handling |
|---|---|---|
| slot complexity (K, parts, machinery present) | shape fields per slot | post slots are compared to pre slots of the same shape class where one exists; otherwise the verdict carries the tag "unmatched shape" |
| account switches and limit resets | count per day and per slot | a day or slot with a switch is kept and flagged; a hypothesis whose post units are all flagged is UNRESOLVED, sub-case U3 |
| concurrent fan-outs | count of fan-outs of 3 or more sessions per day and per window | defines the confounded overshoot (H-38); reported beside H-37 |
| the owner's working hours | share of the slot's wall time inside the owner's windows | reported beside H-42; no adjustment |
| host load from other applications | boolean per load event | events flagged are excluded from H-39 |
| intervention fidelity (the setting typed, the GO chain issued, the dry c2 run, the convention in force) | `fidelity` {h1 to h8: true or false} per day and per slot | a unit without its intervention is excluded from that hypothesis and counted in the report |
| other changes inside the post window (improvement steps 5 to 8, new conventions, model or effort changes, monitor session restarts that reset context per call, compactions) | dated `changes[]` {date, kind} | units after a change are flagged; all post units of a hypothesis flagged gives U3 |
| slot 288 partly exposed to H1 to H4 (all landed during it on 2026-11-12) | none | H-41 to H-44 carry the tag "baseline partly treated" |
| regression to the mean after slot 288 | none | named as a threat (section 9); the single-slot baselines H-41 to H-44 carry the tag "single baseline" |
| the bundles (C1 to C9, the watch and Spotlight landed within hours; H5 to H8 all start at slot 289) | none | H-37 to H-39 cannot be separated from each other, nor H-41 to H-44; each verdict names its bundle |

## 6. Data rule and the aggregate file (frozen form)

The lab receives aggregates only, produced by the monitor from its meter, the verifier log, the checkpoint Host
lines and its own notes, as 0444 files named by path and sha256 in a monitor message. The lab never reads session
transcripts, the system usage store or the lane table; lane step notes are read through the bridge. Numbers and
identifiers only: dates, slot numbers, session role names, series names; no message text, no handles, no paths.

Form `planeon.research.factory-aggregates/v1`, one JSON object per delivery:

- `schemaVersion`, `producedAt` (date), `period` {`from`, `to`}, `clock` ("host-local"), `producer` {`meterSha256`,
  `extractSha256`}: the monitor's meter and its log extractor by digest.
- `days[]`: `date`, `session` (role name), `calls`, `messagesHandled`, `meanContextTokens`, `weightedMtok`,
  `watchFirings`, `watchCalls`, `accountSwitches`, `fanOuts3Plus`, `fidelity` {`h1`, `h2`, `h3`: true or false}.
- `windows[]` (account level): `windowEnd`, `usageAtStop` (percent), `fanOut3PlusStartUsage` (the percent at which a
  fan-out of 3 or more sessions started inside the window, or null).
- `changes[]`: `date`, `kind` (improvement step, convention, model or effort change, monitor restart, compaction).
- `loadEvents[]`: `at` (date and time), `kind` (verify-start, push, worktree), `load1`, `load5`, `load15`, `otherAppLoad`.
- `slots[]`: `slot`, `kind` (product or machinery), `shape` {`k`, `parts`, `machinery`}, `fidelity` {`h4` to `h8`},
  `c2Builds`, `dryC2Runs`, `series[]` {`name`, `rounds`}, `rulingsWaited`,
  `scopeToPacketR1Hours`, `laterDefects` {`oracleFailures`, `packetMajor`, `postMergeIssues7d`}, `machineryRepairs`,
  `machineryMajor`, `r00Calls`, `r00MeanContextTokens`, `stepMinutesMean`, `lostDetailSlips`, `accountSwitches`,
  `fanOuts3Plus`, `ownerWindowShare`.

A missing field is a missing measure, never a zero. The producer digests pin the monitor's instruments, which live in
the monitor's folder and are never read by the lab: the evaluator refuses a delivery whose `meterSha256` or
`extractSha256` differs from the first delivery's, and the register row records both digests when the first delivery
arrives. The producer is also the intervening party, and slips, rulings waited on and other-app flags are its labels:
for one post slot the lab spot-checks the delivered rulings-waited-on and step-report counts against the bridge's lane
step notes and reports the agreement beside the verdicts (a report item, not a gate input). Files delivered before the freeze are recorded by digest and
not opened. The evaluator is written after the freeze, in the standard library, run with the isolated interpreter,
and preflighted on a known-answer fixture before it reads a delivery (charter 1b: units and denominators, one
positive and one negative control, a value at each threshold, every field present with its type).

## 7. The gate (ordered; the first region that applies decides)

1. STOP before any analysis: the PREREG is not frozen, or its blind review (rule D, briefed by the monitor) has not
   read PASS, or the evaluator's preflight has not passed. Nothing is computed.
2. UNRESOLVED U1: the hypothesis has fewer units than section 3's minimum at the stop date.
3. UNRESOLVED U2: a measure the hypothesis consumes is missing from every post delivery.
4. UNRESOLVED U3: every post unit of the hypothesis carries a confounder flag that section 5 sends to U3.
5. NOT SUPPORTED (guard): the hypothesis's guard measure breaches the comparator stated in section 2 (H-38 overshoot;
   H-40, H-41 and H-42 defects; H-43 machinery MAJOR; H-44 slips): H-38 zero unconfounded overshoots in post windows;
   H-40 to H-42 post median at most the pre median of slots 285 to 287; H-43 post median at most 4; H-44 post median
   at most 0. Pre-period overshoots are reported descriptively. H-37 and H-39 have no guard.
6. SUPPORTED: every primary threshold in section 2 holds on the post median (or on every post unit where the
   statement says "every").
7. NOT SUPPORTED otherwise.

Thresholds are exact: "at most 0.75" is post median divided by pre median less than or equal to 0.75, computed
on the raw values, never on rounded ones. Each verdict is reported with its per-unit values, the sign count, the
confounder table of section 5 and its tags ("unmatched shape", "single baseline"). Eight hypotheses are read as
eight separate verdicts; no family-wise claim is made and no verdict is promoted to a causal one.

## 8. Compute plan

Light only, on this host, outside the heavy queue: one evaluator run per delivery, seconds. Stream S2 (X). No ECU
(not product-coupled). The monitor's own interim reports (2026-11-13 and 2026-11-14 09:05) are operational reports
to the owner, not this study's analysis; the study's verdicts are computed once, at the stop date, after the freeze.

## 9. Threats to validity, named now

Bundled interventions (H1 to H3 landed within hours of each other, H5 to H8 all start at slot 289); single-slot
baselines for H-41 to H-44; regression to the mean after an unusually slow slot 288; sessions know they are measured;
slot shapes differ between periods; the meter's attribution of calls to the watch is the monitor's own labelling;
the owner's hours and account switches move the day-level measures; a short post window of seven days and four
slots. A SUPPORTED verdict therefore means "the named measure moved as the monitor expected, with the declared
confounders listed", and nothing more. A NOT SUPPORTED verdict is reported in full (charter section 3, the
negative-outcome gate).

## 10. Effort and cost (rule J)

Paper: this window. Evaluator and fixture: one light pass after the freeze. Review: one monitor-briefed blind round,
cap 2 (C5). Heavy-run seconds: 0. Expected report size: one page plus the per-unit tables.

## 11. Registration (what the owner's word made)

The owner adopted option (a) on 2026-11-12. This text is frozen as `experiments/RL-23/PREREG.md` v1 with its
digest in the register's RL-23 row; H-37 to H-44 are registered (kind empirical, observational; section "factory
process (RS-1 methodology; owner word 2026-11-12)"; stream S2 (X); status READY, first delivery pending); the
outcome record's first attempt is written at stage REVIEW, outcome PENDING (H-36's cohort starts here); the monitor
briefs the blind reviewer from this file (rule D); the evaluator and its known-answer fixture are written after this
freeze and preflighted before the first delivery is read; the monitor's first delivery may cover the pre period at
once, since the meter reruns over past days. A review note that changes a gate region or a threshold makes a new version: v2 is that version, frozen on 2026-11-12
after review r1; review r2 is delta-scoped and the last (C5).


## 12. Not claimed

No result, no direction of any measure after 2026-11-12, no statement about which of the bundled changes would
carry an effect, and nothing about steps 5 to 8 of the improvement plan, which are on hold and not studied.

## 13. Author's self-check at the freeze (charter step 1, from RL-23)

- The gate is ordered with its precedence stated and a region for every outcome, including a STOP before any
  analysis (section 7).
- One sentence declares the narrowing from the owner's words and names every proxy (section 2).
- Every input carries a full sha256 and its commit or the words "no commit exists" (the table above); checked by
  script at the freeze: 4 of 4 input digests are 64 hex and resolve to a present file with that digest.
- Instruments: the lab's evaluator is written after the freeze and its digest goes to the ledger; the monitor's meter
  and extractor are pinned per delivery by `producer` (section 6).
- Every constant taken from a document carries that document's digest (the baselines, FACTORY-IMPROVEMENTS.md
  0bc476b1); the two slot-288 constants delivered by the monitor (22.2 minutes per step, 0 slips) are pinned in
  section 4 with their delivery named, and the gate reads them from this file, never from a run record.
- At the v2 freeze, re-checked by script: the three bridge inputs resolve at commit 3e1db1bb to their pinned digests
  (3 of 3) and the brief to its digest; the review r1 file's digest matches the monitor's message (MON-LAB-FACTORY-4).

## 14. Closure of blind review r1 (sha256 3ecd616c; CHANGES_REQUIRED: 1 MAJOR, 11 MINOR, 7 NOTE)

| finding | disposition | where in v2 |
|---|---|---|
| RV1-1 MAJOR, no defect guard on H-41 and H-42 | taken as worded | section 2 (H-41, H-42 gain the defect guard; H-37, H-39 state "Guard: none"); section 7 region 5 |
| RV1-2 guard comparator ambiguous | taken as worded | section 7 region 5 |
| RV1-3 stop rule could truncate post windows | taken as worded | section 3 |
| RV1-4 slot 288 transitional for H-40 | taken as worded | section 3 (H-40 row); section 4 (rounds row) |
| RV1-5 rounded thresholds vs raw-values rule | taken as worded | section 2 (H-44) |
| RV1-6 H-43 guard baseline | taken as worded (both files) | section 2 (H-43); section 3 (H-41 to H-44 row); register H-43 unchanged |
| RV1-7 fidelity, other changes, 288 partly treated, bundles | taken as worded | section 5 (three rows, bundle row); section 6 (`fidelity`, `changes[]`) |
| RV1-8 windows at account level, slot kind | taken as worded | section 6 (`windows[]`, `kind`); section 3 (H-43 minimum) |
| RV1-9 extractor digest held fixed | taken as worded | section 6 |
| RV1-10 baseline sentence | taken as worded | the sentence after the inputs table; section 4 opening |
| RV1-11 dry c2 not a c2 build | taken as worded | section 4 (c2 row); section 2 (H-41); section 6 (`dryC2Runs`) |
| RV1-12 pooled load median, pre window start | taken as worded | section 2 (H-39); section 3 (load row) |
| RV1-13 NOTE early-result reading | taken | section 1 (H3 cell) |
| RV1-14 NOTE 8.5 h source | taken | section 4 (scope row) |
| RV1-15 NOTE manipulation checks | taken | section 2 (last paragraph) |
| RV1-16 NOTE slip guard on the median | kept as registered: the median form matches the other guards; the total over post slots is reported descriptively | section 2 (H-44), section 9 |
| RV1-17 NOTE "names as voiding" | taken | section 7 region 4 |
| RV1-18 NOTE producer is the intervening party | taken as suggested | section 4 (first interval); section 6 (lab spot-check) |
| RV1-19 NOTE checks passed | none needed | none |

Review r2 is delta-scoped to these changes and is the last round (C5); wording or citation notes after it close by
script-checked claims, not a new round.
