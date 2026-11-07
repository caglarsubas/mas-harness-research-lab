# RL-06 report: process mining of the programme's records (H-10), 2026-11-05

**Asked.** Can throughput and cost per packet be read from the handoff and merge-decision records (H-10a)? Does the
incident-to-rule corpus form a stable taxonomy (H-10b)?

**Measured.** The 47 merged records (2026-10-21 to 2026-11-04) through the lab's allowlist extractions; the
verifier's 27 harness-onion check runs; the 17 handoff markdown files read by script for MON identifiers and the
word "rule" only (1,012 distinct identifiers; a rule subset of 111 that appear on a line with the word "rule").
The category keyword lists were fixed in PREREG v1 before any classification.

**H-10a: PASS.** Coverage 0.94 (47 of 47 with a date and a verify time, 44 with a review count). Throughput:
3.1 merges per day over 15 days; by ISO week, bridge / hosted: W43 12 / 8, W44 9 / 12, W45 (partial) 3 / 3. Cost:
verify wall time per merged record median 743 s (5.8 s for hosted repositories' light verifies up to 1,116 s), per
harness-onion run median 929 s (726 to 1,205); review rounds per merged record median 2 (1 to 8).

**H-10b: FAIL as preregistered.** Of the 111 rule identifiers, 70 percent fall in OTHER (bound for FAIL: above 40
percent); the categories that do match are COMPUTE 21, PRIVACY 5, MERGE 3, BRIEFS 2, FILES 1, SESSION 1. Only 25
rule identifiers are slot-bound, below the 40 the stability split needed, and of the 13 in the later half only 4
fall in a category seen earlier. The finding is about the corpus, not the keyword lists: the identifiers' named
segments name the incident (a slip, a file, a check, a packet step), not a class of incident. A taxonomy needs the
rule text, which is a different design (v2 under a new id, with the monitor's permission to classify rule lines,
counts only) and was not attempted here.

**What it means.** The programme's cadence is measurable from its own records at the precision the records allow:
about three merges a day across the lanes, with the bridge repository's verifies the dominant cost at a quarter
hour each and two review rounds the norm. Whether its rules form a stable taxonomy is not answered by their names.

**What it does not show.** No cost in tokens or wall time per packet build (not in the records the lab can read);
throughput mixes packets, errata and contract merges; the rule subset detection (a line with the word "rule") is
coarse; the lab's prior exposure to rule names shaped the keyword lists, as disclosed.

**Proposal.** None as a roadmap read. A v2 design (text-level rule classification) is the lab's own follow-up if
the monitor allows reading rule lines for classification; otherwise H-10b stays where it is.
