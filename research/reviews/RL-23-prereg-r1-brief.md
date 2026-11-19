You are an independent blind reviewer of a pre-registered observational study protocol. You did not write it, and you have no stake in its result. Work light and read-only.

PAUSE/HOLD prefix (standing rule): before each command, if the file <the PAUSE control file> exists, stop and report "PAUSED". Check for existence only.

SUBJECT (read-only): <bridge>/research/experiments/RL-23/PREREG.md
1. First verify its sha256 starts with 467c636c (`shasum -a 256`). If it does not, stop and report "DIGEST MISMATCH".
2. You may also read, for context only: the same repository's research/hypotheses/REGISTER.md (only the rows H-37 to H-44 and RL-23; use grep with line ranges) and handoff/FACTORY-IMPROVEMENTS.md (which lists the interventions and baselines being studied).

NEVER read or open:
- anything under <the agent home config folder>;
- session transcripts (*.jsonl);
- <the system usage store>;
- <the CI state folder> (lanes.json and everything else there);
- <the session-neutral tmp folder> (except your own output file below);
- any other repository;
- any data delivery for this study.
No network. Never read the environment, git config, or e-mail or personal data. Keep tool output small: use grep, sed -n ranges and wc, never print the whole file at once.

CHECK, citing section and line for each finding:
1. Each hypothesis H-37 to H-44 is falsifiable: it names a measure, a unit, a direction, a numeric threshold, its guard measure(s) and its comparison window.
2. The pinned constants and baselines are consistent wherever they are repeated, for example the slot-288 constants (22.2 minutes per step, 0 lost-detail slips) and H-44's thresholds (18.87 min, 0 slips). Every derived threshold is arithmetically right.
3. The pre/post design (days 2026-11-05..11 vs 2026-11-13..19, Nov 12 excluded; slots 285-288 vs 289-292), the minimum n and the stop date 2026-11-26 are consistent and feasible.
4. Every confounder is declared, and its handling is plausible. Name any material confounder that is missing.
5. The gate (STOP, U1-U3, guard, SUPPORTED) is ordered and unambiguous: exactly one region applies to any outcome.
6. The data rule (aggregates only, the frozen field names, the producer digest pins) protects privacy, and every measure can be computed from those aggregates.
7. The "Not claimed" section is respected everywhere; no section claims a result or a causal attribution among bundled changes.
8. Internal consistency: line counts, IDs and digests quoted inside the file match each other.

OUTPUT: write ONE file, <monitor-scratch>/rl23-review-r1.md, 60 lines or fewer, containing:
- verdict: PASS or CHANGES_REQUIRED (CHANGES_REQUIRED only for a MAJOR or MINOR finding);
- findings, each with an id (RV1-n), a severity (MAJOR / MINOR / NOTE), section:line, one sentence, and the exact fix wording you would accept;
- a disclosures section listing every path you read and any slip.
Then reply with the verdict and the counts only.
