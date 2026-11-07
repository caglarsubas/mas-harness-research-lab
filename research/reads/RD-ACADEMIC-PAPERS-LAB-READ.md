# Research-Lab read of the third owner-supplied document: "Academic Literature Crosswalk and Empirical Synthesis for the MAS-Harness and Planeon R&D Architecture" (RS-3), 2026-11-05

Status: v1, written the day the owner supplied the file in the lab session ("a papers deep-search report of Gemini for you to use for updating our roadmap of research implementation, leveraging potential gaps in the fields"). The lab keeps no copy; the file is recorded by digest. Nothing here is a roadmap write: the register (the lab's) is updated; roadmap items are the visionary's, through the monitor.

| source | title (as the file states it) | sha256 | size | lines, words | status |
|---|---|---|---|---|---|
| RS-3 | "Academic Literature Crosswalk and Empirical Synthesis for the MAS-Harness and Planeon R&D Architecture" (file name "Academic Papers for Planeon Roadmap.md") | 930f89a0d252f948b5a393044007e4b8e87174f6617d4cad586fa9eea63ab840 | 745,965 B | 316, 7,202 | NEW; proposed to the visionary as research source RS-MEMO-RDPAPERS, OWNER_SUPPLIED, advisory |

What the file is: a synthesis written over RS-1 and RS-2 (its works-cited entries 1 and 2 are those two files) plus 55 web sources; it repeats RS-1's and RS-2's scores for the 22 lines unchanged (both scales, side by side) and adds per-track tables of papers with venues, identifiers and "key empirical baselines", a works-cited list with URLs, and 62 embedded images (figures, not read; about 685 KB of the file). Every figure below is "as reported by RS-3"; the lab has read none of the papers except the five the owner approved on 2026-11-05 (F2, F4a, F4b, F5, F6), and has not yet compared RS-3's figures with those five texts (a later, light task: RL-19 candidate, section 5).

## 1. What RS-3 adds beyond RS-1 and RS-2

- Identifiers the earlier files lacked: MAS-ProVe (ICML 2026, arXiv 2602.03053, OpenReview UoM3G7nKr0; the first fetch list's F1 had none); the independent PREreview of VeriHarness (Zenodo 10.5281/zenodo.23180223); Concordat (arXiv 2610.37461v2) and Yu et al. (arXiv 2610.19372) beside AgentLTL; Ekstazi (ISSTA 2015), RTS++ (ICST 2019) and the 2023 semantics-aware RTS paper as the regression-test-selection baseline for A1; Styx (VLDB Journal 2026, DOI 10.1007/s00778-026-00971-x; SIGMOD 2025) for D1; SAFER (ICLR 2026, arXiv 2510.10193, OpenReview kJmLmOvwLC) for D2; Lineage-Driven Fault Injection for D3; the authors of the oversight study (Narayanan and Feigh) and its abstract page.
- Reported figures that sharpen hypotheses: VeriHarness (34 percent of unanimous claims wrong; the modal answer right 47 percent; 74 percent of disputed claims hold a correct candidate; selection +4.4/+4.1 points, with revision +6.2/+6.4; the PREreview's 3-5x compute cost and "correlated-error floor"); MAS-ProVe (few-shot trajectories give zero gain over zero-shot judging; summarised context beats raw trajectories); Kim et al. (260 configurations; +80.8 to -70.0 percent; the 45 percent single-agent threshold; a linear predictor over coordination metrics picks the best architecture in 87 percent of held-out cases); Zhou et al. (the variance ceiling and the precision-optimal repeat count); AgentLTL's three constraint types (ordering, call presence, entity grounding) and Yu et al.'s drop in gate interventions from 39.2 to 8.8 percent of trajectories; MPBench (nine vulnerabilities, four write channels; average attack success 50.46 percent; 66.67 percent under aggressive compaction into system prompts against 34.25 percent with tool-gated retrieval); HarnessOpt-Bench (111 runs; held-out partitions must stay inaccessible); Agentproof (linear-time structural checks, witness traces under a second to 5,000 nodes); Ekstazi (32-54 percent less test time by file dependencies); SAFER (Clopper-Pearson feasibility bounds for abstention; abstention 5.1 to 0.74 percent); Narayanan and Feigh (dependent agent workflows mask cascading errors; high-workload reports 22 against 30 percent; low abstraction saves 1.59 s and corrects nothing).
- A programme shape: pin five code and data archives into the crosswalk first (VeriHarness, the Nature MI archive, Agentproof with AgentLTL, SAFER, MAS-ProVe with MAST); shadow-only for compaction and routing; the same 60/25/15 split; seven publication clusters.

## 2. Mapping to the register (where each paper lands, and what it changes)

| RS-3 paper or finding (as reported) | register hypothesis | what the lab takes |
|---|---|---|
| Ekstazi, RTS++, semantics-aware RTS (A1) | H-02 | a second comparison arm for the shadow period: an Ekstazi-style file-dependency selection over argv 63's test files, computed from the input sets MET-PERF-047's writer captures (D3 (a)); the lab names it for R00; no lab run now |
| in-toto, SLSA (A1, E1) | H-01, H-06 | baselines already in the crosswalk; nothing new |
| Groll et al.; Afzali et al. (A2) | H-03, H-09 | the three-variable rule for H-09 (custody, context, model family) is now backed by a named "correlated-error floor"; H-09's design adds a model-family column when the review records carry one |
| Bala et al.; interrupted time series (A3) | H-10 | H-10 v2's design: rule effectiveness by interrupted time series, counts only, on the monitor's permission |
| VeriHarness; PREreview; MAS-ProVe (B1) | H-11, H-09 | H-11's measurement on the campaign ledgers gets the three figures as reported baselines (34 / 47 / 74 percent) and the 3-5x cost caveat; a new candidate H-32 below |
| Harness-Bench; Zhou et al. (B2) | H-12, H-31 | the precision-optimal repeat count enters H-12's matrix design and H-31's gate reading (k >= 3 against the variance ceiling), once F4b is read |
| Kim et al. (B3) | H-13, H-14 | the 45 percent threshold and the linear coordination predictor as candidate selection rules to test on the simulation harness (H-13a's missing task family remains R12's) |
| AgentLTL; Yu et al.; Concordat (B4) | H-29 | H-29's vectors become the three constraint types (ordering, call presence, entity grounding) over the R10 gate transcripts; the intervention-rate figure is a reported baseline |
| MPBench (B5) | H-28 | the harness half's case classes: the four write channels and the compaction-without-source-filtering vulnerability; a new candidate H-33 below on the programme's own compaction |
| HarnessOpt-Bench; MIPRO; Promptbreeder (B6) | none yet | MAS-RA-005's admission gate already requires the inaccessible held-out split; a note for the visionary, no hypothesis |
| Agentproof; the EMNLP survey (B7) | H-25 | H-25's violation classes align with Agentproof's (dead end, unreachable exit, human-gate bypass) and its witness-trace requirement; F2 is held and will be read for RL-20 |
| Anjali et al.; Alhindi and Hallett (C1) | H-18 | the usability finding supports treating allowlists as reviewed contracts; no change |
| MAST; TOGBench (C2) | H-19, H-09 | TOGBench's mutation-tested oracles: a candidate H-34 below on the conformance labs' own oracle sidecars |
| Saltzer and Schroeder; South et al. (C3) | H-26 | H-26's trace half adds revocation vectors (a revoked authority refuses later writes) |
| Styx; Jepsen; LDFI (D1, D3) | H-27 (fault half) | the parity-vector design for the fault half: crash, replay, paused lease, clock skew, worked backward from lineage invariants; BLOCKED on DATA-CORRECTNESS-001 as before |
| SAFER and its exchangeability caveat (D2) | H-15 | H-15's report columns add abstention calibration and a distribution-shift check; still BLOCKED |
| Nweke and Yeng (E1) | H-06 | the explicit missing-evidence state is RELEASE-EVIDENCE-001's NOT_RUN / BLOCKED cell; no change |
| Mitchell et al.; Narayanan and Feigh (E2) | DESIGN-UX-001 (item note) | a new candidate H-35 below on lineage surfacing; the three measures stand |

## 3. Candidate hypotheses added to the register (H-32..H-35), each READY on paper or BLOCKED on a named item

- H-32 (B1, S1 Q): on the programme's own review records, claims that every review round accepted unanimously are later refuted by the verifier or a later round at a non-zero rate, and disputed claims hold the later-confirmed reading more often than the unanimous ones. Inputs: the review records through the masking reader and the verifier's refusals after PASS_FOR_PUSH (RL-02's table); BLOCKED on REVIEW-RECORD-SERIES-001 for finding identity, as H-09. The reported 34 / 74 percent figures are the comparison, as reported.
- H-33 (B5, S3 T): the programme's own handoff compaction filters sources: a weak-signal fact seeded into a lane file's free text does not reach the next resume block's pinned facts, while a digest-pinned fact does. A sessions experiment: BLOCKED on an owner-approved run plan (it needs live sessions); the observational half (which facts in resume blocks carry a pin, RL-14's typedness) is done.
- H-34 (C2, S1 Q): the conformance labs' oracle sidecars catch seeded mutations of the candidate code at a rate the author-written suites do not (TOGBench's method). Inputs: R12's non-oracle tests on the export and a mutation set; the oracle files are never read, so the lab can only pose the mutations and ask R12, through the monitor, to run the oracle side; BLOCKED on that arrangement.
- H-35 (E2, S4 X): surfacing inter-agent lineage (which claim depended on which) in the operator shell reduces missed cascading errors without raising workload, against a trace-only shell. BLOCKED on PRODUCT-SHELL-001's integrated flows; the three measures (time to correct intervention, severity-weighted misses, workload) are RS-2's and RS-3's.

## 4. The fetch ask, second tier, restated with RS-3's identifiers (the lab's own ask, through the monitor; nothing fetched)

The owner ruled the second tier "Not now (Recommended)" on 2026-11-05. RS-3 changes one thing: F1 (MAS-ProVe) now has an exact identifier, arXiv 2602.03053, so it can be approved as one GET like F2 when the owner wants it. The rest stays not now, listed so the identifiers are on record: PREreview of VeriHarness Zenodo 10.5281/zenodo.23180223; AgentLTL arXiv 2607.02599; Yu et al. arXiv 2610.19372; Concordat arXiv 2610.37461; SAFER arXiv 2510.10193; Styx DOI 10.1007/s00778-026-00971-x; VeriHarness arXiv 2610.00972; MAST (NeurIPS 2025 proceedings page); Ekstazi (ISSTA 2015, author page); Nweke and Yeng DOI 10.1109/ACCESS.2026.3665991. The oversight study (F7) stays not held: its publisher host answered the approved GET with a challenge page and is never retried; RS-3 names an abstract page on the same host, which the lab does not request.

## 5. Next light steps the lab proposes (each with a PREREG review first)

1. RL-19: read the five held papers and check RS-1/RS-2/RS-3's reported figures against their texts (a figure-grounding check in the crosswalk's own form: claim, page, verified or corrected), light, no network.
2. H-25 on a fresh architecture export at c1b838be (the monitor's order), with Agentproof's classes beside the lab's.
3. H-29's three constraint types once the monitor exports the R10 gate transcripts masked.

## 6. What this read does not do

It copies no date, staffing or compute figure as the programme's; it rates no roadmap item; it reads no paper RS-3 cites beyond the five already held; it treats RS-3's figures as reported until RL-19 checks them.
