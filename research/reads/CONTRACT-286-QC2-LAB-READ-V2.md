# Research-Lab read of Q-C286-2, V2: the isolation check E1 does not establish that the declared edits are the cause, 2026-11-14

Asked by the monitor (MON-R13-ISSUE6; light, paper only, rounds paused). Input: R13 issue 6 (P1, body only, read through
the masked gh form; its links not followed); the lab's V1 read (research/reads/CONTRACT-286-QC2-LAB-READ.md 557fa451,
bytes unchanged, superseded here in section 2 step 3 and in the causal wording of its section 1 ruling); DESIGN-048-Q1
condition C2 (9c795426); ISOLATE286-E1-LAB-READ-V2 (3058efff). No run of any suite, no network. The lab's read prevails
on the lab's claim; a tool or contract change is the owner's process (R00's isolate286.py and CONTRACT_286 are the landed
bytes; the lab changed none of them).

## 1. Verdict: ACCEPT; the V1 claim "the change is caused by the declared edits" is withdrawn

E1 (V1 section 2 steps 1-3) restores the changed declared inputs, keeps the rest of the live tree, and credits the event
when the differing nodes return their recorded outcome. That cell shows the other changed inputs have no effect at the
base value of the declared inputs. It does not show the declared edits alone produce the live outcome: a node whose
outcome needs a declared edit D and an undeclared input U together returns the recorded outcome with D restored (U alone
does nothing) and is credited, although changing U at the live D changes the outcome. This is the missed-input case that
C2 was written to catch. The issue's table, cells (D, U) and outcome: (0,0) passed; (1,0) passed; (0,1) passed, so E1
accepts; (1,1) skipped. Per-phase agreement (setup, call and teardown identical in every cell but the call) does not
remove it. Checked offline, standard library, by research/tools/e1_control.py 374ece1b `selftest`: of the 16 outcome
functions of (D, U) over two words, 8 change the live outcome; E1 credits 4 of them, 2 wrongly (the joint cause in
either polarity); the issue's table is one of the two.

## 2. The corrected rule (a 2x2 control)

Cells per differing node, each a per-phase outcome map, under the same interpreter, environment and node identity:
recorded (the record's base), declared-only (the declared edits applied, every other changed input at its base bytes),
other-only (E1's cell: the declared inputs restored, the rest live) and live (the head). Credit (kind
"demoted-outcome-explained", countEffect count) needs other-only == recorded AND declared-only == live. Other-only !=
recorded is class A as before. Declared-only != live with other-only == recorded is the joint case: class A, restart,
under the existing process, no new class. A cell missing or not comparable (phase sets differ, a node not run) is
unresolved: no credit, countEffect pending, the state V1's procedural form already carries. Over the 2x2 the control
credits exactly the functions where the other changed inputs have no effect (the selftest's enumeration), and the
declared-only positive control stays eligible (known-answer case K2). `e1_control.py check CONTROL.json` evaluates a
four-cell control file per node and prints beside it what E1 alone would have said.

## 3. Rule G accounting (charter SC-D2 G)

Frequency: unknown. V1 expected an explained event at a merged head to be rare, and no shadow record of one exists
(287-296 not read by the lab). Cost of the added cell: one more scratch copy and one more run of the same differing
nodes, the bound E1's own cell already has; the seconds are verify time. With the frequency unknown this read adds no
mechanism to the chain: the no-mechanism option is that an explained event's countEffect stays "pending isolation"
(uncredited, the period's count does not advance on it) until a record carries the declared-only cell as well. Whether
the cell is added to R00's tool and to CONTRACT_286 is the owner's decision, with that cost stated. The lab's control
script is a known-answer reference, not a chain tool.

## 4. What this touches

No PREREG (the frozen RL-23 v4 included) and no outcome record cites E1 or Q-C286-2 (the grep over research/experiments
finds none; "E1" there is an evidence id). RL-16 (H-02, cost half, PASS) is closed and unaffected. H-02's shadow half
(the RL-16 successor, not yet registered) counts a clean period with the corrected rule: an E1-credited event without the
declared-only cell is unresolved, not clean. The roadmap's lock-286 note and R00's slot-286 claims cite V1 by digest;
V1's bytes stay. Agreement in the control covers the tested changed inputs and outcomes, not dependency completeness (an
unchanged undeclared input, or the environment, is outside it). The falsifiable claim is that the control rejects the
seeded joint cases K1 and K5 and keeps K2; the selftest holds it.

## 5. Not claimed

No reproduction of isolate286.py on a real record, no real shadow event, no claim that any credited event so far was a
joint cause (none has been credited), no verify-time figure for the extra cell, nothing on the rest of CONTRACT_286.
