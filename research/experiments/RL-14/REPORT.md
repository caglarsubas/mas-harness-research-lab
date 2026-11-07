# RL-14 report: typed resume blocks and the new rule identifiers that follow them (H-28, observational half)

**Asked.** Are resume blocks that pin their referents by digest and line number followed by fewer new monitor rule
identifiers per day than blocks that do not? Preregistered as v4 (02ef7761) after three failed independent reviews
(v1 714effc6, v2 3b81a007, v3 941653de; `PREREG-REVIEW.md`), the first experiment under charter step 1a. Inputs:
the seven lanes' own handoff files at bridge commit 46c7d6e2 (eight files by rule, one with no blocks), pinned by
sha256 and extracted at that commit for the run.

**Measured.** 40 resume blocks, 33 windows, 23 with at least one day (run-001 bcfa5c1b; data c142ef60; RESULTS
93f2bc9c). Exposure X ranged from 0.09 to 4.96 pins per 100 words (median 2.54), with 3,592 distinct digest
prefixes and 39 line pins matched over the 40 blocks (36 blocks typed); X had no ties. Outcome Y: 30 new MON
identifiers fell inside the 23 windows; 11 windows had none (16 tied Y values). Window lengths: eight of 1 day,
thirteen of 2, one of 3, one of 4. Windows per cluster: LANE-PARALLEL 10, LANE-R00-HARNESS-ONION 5, LANE-R03 3,
LANE-R04 2, LANE-R11 2, LANE-DESIGN-UX 1.

**Verdict: UNRESOLVED as preregistered.** Spearman rho = +0.124; the file-clustered 95 percent bootstrap interval
is [-0.413, +0.358] (1,000 of 1,000 resamples defined). The sub-case is "the interval reaches the minimum effect of
interest (-0.30) but PASS is not met": the lower bound -0.413 does not exclude the MEI, so the result is not FAIL,
and the point estimate has the wrong sign, so it is not PASS. This is the outcome class the PREREG named as most
likely for 23 windows in 6 clusters. Sensitivity: digests-only rho = +0.117, the same picture. Descriptive median
split: windows opened by above-median-typedness blocks had a median of 1.0 new identifiers per day against 0.0 for
the rest (11 against 12 windows).

**What it means.** On the programme's own records there is no evidence that more pinned resume blocks are followed
by fewer monitor rules; the sign of every descriptive number points the other way, and the PREREG's reverse-direction
confound is the simplest reading: the monitor's rules prescribe pinning, and the most active lane (LANE-PARALLEL, 10
of 23 windows) both pins most and receives most rules. The hypothesis is not refuted by this gate, because the
interval still reaches the minimum effect of interest, but the observational half cannot support a pinning rule.

**What it does not show.** Nothing about causes: no adjustment for lane activity, window length (mostly 1-2 days,
so Y is coarse) or the reverse direction. The proxy counts every new monitor identifier addressed to the lane, not
slips; a text-level proxy needs the monitor's permission and is a new id. The harness half of H-28 (state recovery
after a forced restart; a poisoned observation cannot grant a permission) is untouched and waits on
RELIABILITY-CAMPAIGN-001; the memory-poisoning paper the owner approved (F6) is its input.

**Proposal.** None as a roadmap read. For the register: H-28's observational half is UNRESOLVED and closed under
this id; a v2 with a slip proxy classified from rule text is a new id, only on the monitor's permission. For the
charter: the four-round review cost about one hour of session work and found three real defects (the outcome's
double counting, the unpinned inputs, the undefined statistic); the step stays.
