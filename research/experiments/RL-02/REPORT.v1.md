# RL-02 report: review independence (H-09), v1, 2026-11-04

**Asked.** Do review rounds and the independent oracle find different findings (H-09a)? Does the verifier refuse a
measurable fraction of PASS_FOR_PUSH heads (H-09b)? Do carried notes become later findings (H-09c)?

**Measured.** 105 review rounds over 25 series (10 packets, 5 designs, 10 contracts) of 12 Build-R00 item groups from
about slot 268 to 279, exported masked by the monitor (J1, sha256 a1a4b237), joined on the 8-character head to the
verifier's check-run summaries (I2). 104 rounds entered; 1 junk row dropped by the preregistered rule (PREREG v1
bbb53d0b). J1 holds per-round counts (findings, major, minor, note, disclosures), verdicts, form, ruling, duration
and interruptions; it holds no finding identities and no oracle verdicts.

**Verdict: UNRESOLVED** (RESULTS.json). H-09a and H-09c were declared UNRESOLVED-by-input before the run: the test
needs finding-level records with the oracle's verdicts, which this export does not carry. H-09b is UNRESOLVED by
its preregistered head count: 11 heads received PASS_FOR_PUSH, 9 were matched to a verify run, 1 was refused (the
capped run of PR 232; its later pass is the same head), fraction 0.11 with a Wilson interval of 0.02 to 0.44, below
the 40-head bound for a verdict.

**What the rounds show (descriptive, not gated).**

| round index | rounds | median findings | CHANGES_REQUIRED | rounds with at least one finding |
|---|---|---|---|---|
| 1 | 28 | 6 | 0.71 [0.53, 0.85] | 0.96 [0.82, 0.99] |
| 2 | 24 | 2 | 0.42 [0.24, 0.61] | 0.71 [0.51, 0.85] |
| 3 | 17 | 3 | 0.53 [0.31, 0.74] | 0.76 [0.53, 0.90] |
| 4 and later | 35 | 3 | 0.60 [0.44, 0.74] | 0.94 [0.81, 0.98] |

Rounds at index 2 and later still carry at least one finding in 0.83 of cases (63 of 76; 0.73 to 0.90). Full-form
rounds have a median of 4 findings and 0.64 CHANGES_REQUIRED; delta-form rounds 2 and 0.46. Median round duration
is 1,170 s (maximum 9,071 s); 12 rounds carried an interruption; every ruling is KEEP. The longest series is a
design at 27 rounds; the median series is 3 rounds in every kind.

**What it means.** Between-round independence looks real at the count level: a second, third or later reviewer
of the same subject keeps finding something, and the first round's median of 6 is not the whole set. That is a
candidate for a gated test in v2 (a bound on the later-round fraction), not a verdict here. Nothing can be said
about the oracle's independence from the rounds, which is H-09's main claim.

**What it does not show.** No oracle overlap (H-09a); no note tracing (H-09c); H-09b on 9 heads is a point, not a
rate; packets before slot 268 and every other lane's records are absent; counts cannot distinguish a finding found
twice from two findings.

**Proposal.** None as a roadmap read. A v2 (declared in PREREG v1) needs, through the monitor: (1) a finding-level
masked export of the same series with per-finding kind, severity, status and the round that raised it, plus the
oracle's per-packet verdicts and test counts where the review records carry them; (2) the other lanes' review
records in the same form if the lab is to say anything beyond R00. The lab asks for (1) first and runs v2 on it.
