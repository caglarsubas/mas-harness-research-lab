# RL-19 report: the syntheses' figures against the five held papers (H-24, the grounding step on a second corpus)

**Asked.** Are the figures the three owner-supplied syntheses (RS-1, RS-2, RS-3) attribute to the five papers the
owner approved for fetching found in those papers' own text, at a rate of at least 90 percent? Preregistered as v1
(317c3088), reviewed once (PASS; `PREREG-REVIEW.md`). 29 claims fixed before any search (`data/claims.json`).

**Measured.** Run-001 6163a225; data 0a881349; RESULTS a211b180. The extractor found 24 of 29 claims (0.828): by paper,
Agentproof 6 of 6, Harness-Bench 3 of 5, the repeated-running paper 4 of 5, the Nature Machine Intelligence article
6 of 6, the memory-poisoning paper 5 of 7; by synthesis, RS-3 24 of 29, RS-2 9 of 11, RS-1 0 of 1. The five not found:
"more than 5,000 trajectories" (Harness-Bench), "ten backends" (Harness-Bench), "16 models" (repeated running),
"four memory write channels" and "nine structural vulnerabilities" (memory poisoning).

**Verdict: UNRESOLVED as preregistered** (82.8 percent, between the 70 percent FAIL line and the 90 percent PASS
line).

**Hand pass, descriptive (review 1 note 1).** Of the 24 FOUND claims, 22 have a specific pattern (a decimal, a
percentage, a comma number or a name) whose context shows the synthesis's meaning: VERIFIED. Two short patterns
matched by coincidence first ("15" on an author line; "5,000" with an empty context) but are VERIFIED by the
first-page read of 2026-11-05 (the abstract states 15 temporal policies and graphs up to 5,000 nodes). Of the five
NOT_FOUND, four are the extractor's loss of word spacing in three PDFs, and the first-page reads of 2026-11-05 show
each figure as the syntheses state it: seven harnesses with ten backends; 16 models on 99 problems with two prompts
and five runs; four memory write channels and nine structural vulnerabilities. One claim is NOT VERIFIED: "more than
5,000 trajectories" for Harness-Bench (RS-1, RS-2 and RS-3 all state it); the paper's abstract gives 300 tasks, seven
harnesses and ten backends, and its text names 6,864 sampled runs; no figure of 5,000 appears. The syntheses' figure
may paraphrase the total runs; it is not in the text as stated. By hand: 28 of 29 claims verified, 1 not.

**What it means.** The three syntheses report the five papers' figures faithfully with one exception, which all
three share (RS-2 and RS-3 cite RS-1 as a source, so one misreading travelled). The mechanical rate (82.8 percent)
is bounded by the lab's extractor, not by the syntheses: a space-aware extraction would have found four of the five
misses. The grounding method of the crosswalk (claim, pattern, context, verification by read) works on this corpus
with a stdlib extractor plus first-page reads; a full repeat needs either a better extractor or page reads for every
specific claim.

**What it does not show.** Nothing about the figures the syntheses attribute to papers the lab does not hold (the
second-tier list, MAS-ProVe, VeriHarness and the rest); nothing about the syntheses' interpretations, only their
numbers; the hand pass is the lab's reading of first pages, not of every paper in full.

**Proposal.** None as a roadmap read. For the crosswalk (F1): when the five papers enter it as OWNER_SUPPLIED
secondary papers, their figures can be marked verified at the claim level from this record, except Harness-Bench's
"more than 5,000 trajectories", which should be carried as "as reported by the syntheses, not found in the text". A
space-aware extractor is a new id if the lab repeats the step on more papers.
