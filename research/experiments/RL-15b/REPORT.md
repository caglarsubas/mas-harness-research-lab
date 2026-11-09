# RL-15b report: the seeded-inconsistency benchmark restated for the lock-40 roadmap builder (H-30)

**Asked.** On the lock-40 roadmap builder (690cff6a), is every catchable seeded inconsistency instance of the
register's classes and the lab's added class refused, each refusal attributed to a named rule (a lock-40 rule by its
tag, or the older rule of `load()` that ran first), with the lock-40 rules refusing at least 2 of 3 M4 and both
catchable M6 instances, and no benign control refused (H-30b)? Preregistered as v1 (e5a75db2) against the design
authority's restated expectation (ERRATUM to RL15-D1), with the instrument preflight of charter step 1b (PASS,
`PREFLIGHT.md`) and one blind review (PASS, five non-blocking notes, `PREREG-REVIEW.md`). The new id that corrects
RL-15 run-002's three instrument defects: the offset-less control, the 120-character capture and the instance no
file comparison can catch. Everything ran on a fresh export of `roadmap/` at bridge HEAD 8df395a5 (identical to the
pinned ded99886) in the lab scratch; the bridge's `roadmap/` was never touched.

**Measured.** 22 builds in 15.2 s at host load about 25 (run-001 af1e9122; data f445e3c1; RESULTS d1810a57), 25 light
builds with the preflight. The unmodified copy builds clean (exit 0, 3.64 s). Of the 17 catchable seeded edits, 17
were refused and all 17 attributed: 4 by the lock-40 tags (M4 2 of 3 by the process rule, M6 2 of 2 by the digest
rule) and 13 by an older rule of `load()` (the third M4 instance by "is BLOCKED with nothing blocking it", the rule
that runs first, as the erratum said). The declared uncatchable instance, a secondary paper's digest with no file to
compare, built. 0 of 3 controls exited non-zero; no build crashed. Precision 17 of 17 refusals (1.000).

**Verdict: PASS** (RESULTS.json): all 17 catchable instances refused and attributed, the new rules at the expected
counts (M4 2, M6 2), 0 controls refused; every number equals the preregistered expectation.

**What it means.** Both lock-40 validators do what RL15-D1 asked for what a file comparison can catch: a status
change to DONE with no update entry dated on or after it is refused, and a research digest that is malformed or
disagrees with its file is refused, each with a tagged message that names the item or source. RL-15's FAIL stands as
the record of the builder before lock 40 (M4 0 of 3, M6 0 of 3 attributed); RL-15 run-002 stands as the record of
the frozen instrument's three defects on the patched builder; RL-15b is the clean statement on a corrected
instrument.

**What it does not show.** A PASS here confirms the design authority's reading of RL-15 run-002 on a corrected
instrument rather than a fresh prediction: the targets, the messages and the counts were known before this PREREG
was written and the expectation was transcribed from the erratum (declared under R7; review note 5). Nothing about
validators the lab did not seed; three edits per class, one record, one roadmap.json; the secondary-paper digest
class stays uncaught by design (no file to compare; 34 of the 45 secondary papers carry a digest and none a file);
the older rules' wordings are the lab's fixed list, so a differently worded refusal would have read as unattributed
(none did); a crashing control would have been scored as a false positive (none crashed; review note 2).

**Proposal.** None as a roadmap read. For the visionary (through the monitor): RL15-D1's expectation as restated
by the erratum is met instance by instance; the RL-15b report enters as a research source by digest when the
visionary records it. A secondary paper's digest could only be checked against a file the bridge holds, which is a
scope choice for the roadmap's research record, not a builder defect.
