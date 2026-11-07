# RL-15 report: a seeded-inconsistency benchmark for the roadmap build (H-30)

**Asked.** Do the roadmap build's validators refuse every seeded inconsistency class of the register (dangling
dependency; status against evidence state; score drift; a status change without an update entry; a stale snapshot
digest) and the lab's added class (a stale reference), naming the seeded edit, and refuse none of three benign
control edits? Preregistered as v5 (1e8dfc4a) after four failed reviews and one instrument stop (v1 56b2829f, v2
532b08a3, v3 cda3e838, v4 cf9fe7a9; `PREREG-REVIEW.md`). Everything ran on a pristine copy of `roadmap/` at bridge
commit fce8245b in the lab scratch; the bridge's `roadmap/` was never touched.

**Measured.** 22 builds in 7.7 s (run-001 87f4ad62; data ed7ce16d; RESULTS 050c553c). The unmodified copy builds clean (exit
0, 0.81 s). Of the 18 seeded edits, 14 were refused by the build and 10 of those refusals carried a token specific to
the seeded edit; 0 of 3 controls were refused or crashed; no build crashed. Precision 10 of 14 refusals (0.714). Per
class, attributed / refused / seeded: M1 dangling dependency 3 / 3 / 3 ("unknown dependency"); M2 status against
evidence 3 / 3 / 3 ("is DONE but its evidenceState is PLANNED"); M3 score drift 2 / 3 / 3 (the out-of-range factors
by "rating B2 out of range"; the removed factor refused as "factor keys", a refusal that names neither `benefit` nor
`B2`, so unattributed by the preregistered rule); M4 status change without an update entry 0 / 2 / 3 (two edits
refused for a different reason, "X is BLOCKED with nothing blocking it": closing the item unblocked a dependent whose
status the record still said BLOCKED; the third built clean; no refusal mentions an update entry); M5 stale
reference 2 / 3 / 3 (the unknown codebase refused as "unknown codebase reference", unattributed by the token rule);
M6 stale snapshot digest 0 / 0 / 3 (a 63-character source digest, a replaced seed-paper digest with the file
unchanged on disk, and a replaced secondary-paper digest all built clean).

**Verdict: FAIL as preregistered.** Two classes have 0 of 3 attributed refusals, M4 and M6, which is the FAIL
region; the PREREG named FAIL through M4 as the expected class and said an all-18 PASS was unreachable because M6's
third instance can be caught by no file comparison. FAIL here is the ordinary outcome of a benchmark, not a
near-miss of PASS: the validators cover the shape rules (M1, M2, M3, M5) and do not cover the process rule (M4) or
the digest rule (M6).

**What it means.** The build checks what it can see in one file: ids, dependency closure, status against evidence
state, factor ranges and keys, harness and codebase references, duplicate ids. It does not check that a status
change is accompanied by a dated update entry (the diff against the last snapshot records the change; it never
refuses it), and it does not check the research section's digests against anything, neither their length nor the
copied paper files. Two of M4's refusals show a different, useful rule firing: closing an item exposes dependents
whose BLOCKED status is stale. The attribution rule was strict by design: two refusals that did catch the seeded edit
("factor keys", "unknown codebase reference") are counted as unattributed because their words name neither the field
nor the seeded value; the descriptive count without that rule is 14 of 18.

**What it does not show.** Nothing about validators the lab did not seed; three edits per class; one record; the
validators and the record share an author, so the four covered classes may reflect that author's own habits. The
digest class was seeded on research-source digests, the only digest-bearing fields of the record; the architecture
snapshots live in another file the build reads but the lab did not mutate.

**Proposal.** RL-15-PROPOSAL, a design read for the visionary through the monitor, not a roadmap shift: two
candidate validators for build_roadmap, each a data check of the kind it already runs, (1) refuse a status change
against the last snapshot that no update entry dated on or after the snapshot names (M4), and (2) refuse a
research-section digest that is not 64 hexadecimal characters, and, where a file under `research/papers/` is named,
one that does not match that file (M6); plus the observation that closing an item should also be refused while a
dependent still says BLOCKED, which the build already does. Whether these enter the builder is the visionary's call
under the owner's delegation; the lab writes no roadmap.
