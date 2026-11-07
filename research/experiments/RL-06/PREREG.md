# RL-06 preregistration: process mining of the programme's records (H-10)

Status: FROZEN v1 (2026-11-05, light; the monitor's MON-RL-M8 "go ahead"). This file's sha256 goes into the
register. Integrity check before the freeze, by script and counts only: 17 handoff markdown files hold 1,012
distinct identifiers of the form MON-<segments> (719 named, 293 slot-bound), 153 lines carry such an id and a
date; the extracted merge-decision rows carry a date and a verify time on 52 of 53 and a review count on 44 of
47 merged records. No category was assigned before the freeze. The category keyword lists below are written from
the lab's general knowledge of the programme's rule names, which is disclosed as prior exposure.

## 1. Hypotheses (falsifiable)

- H-10a (measurable): throughput and cost per packet can be read from the records. PASS when at least 80 percent
  of merged records carry a decision date, a verify wall time and a review-round count, and the three series below
  are produced; FAIL otherwise.
- H-10b (stable taxonomy): the incident-to-rule corpus forms a stable taxonomy. Unit: a distinct MON identifier in
  the handoff files; the rule subset = ids that appear on at least one line containing the word "rule" (any case).
  Category = the first keyword group matched in the id's named segments, in the order of the table below; ids
  matching none are OTHER. Time order: slot-bound ids by their slot number; named ids are undated and are used for
  the distribution only. Gate: PASS when (a) OTHER holds at most 25 percent of the rule subset, and (b) among
  slot-bound rule ids in the later half of slots, at least 90 percent fall in a category already present in the
  earlier half; FAIL when OTHER exceeds 40 percent or (b) is below 70 percent; UNRESOLVED otherwise or when fewer
  than 40 slot-bound rule ids exist.

| category | keywords (segment match, whole segment) |
|---|---|
| PRIVACY | PRIVACY, HANDLE, PATH, PATHS, SCRUB, MASK, MASKED, NAME, NAMES, HASH, HASHES, REDACT, EMAIL, URL, TOKEN |
| COMPUTE | HEAVY, LOAD, GO, HOLD, PAUSE, VERIFY, DRY, PRECHECK, OLLAMA, QUIET, SLOT, CAP, TIMEOUT |
| BRIEFS | BRIEF, BRIEFS, KIT, KITS, REVIEWER, REVIEW, PIN, PINS, STOP, CLASSIFIER, QUOTING, GLOB |
| FILES | SCRATCH, TRASH, BASETEMP, TOOLS, COPY, LINK, LINKS, SYMLINK, CHAIN, SNAPSHOT, EXPORT |
| MERGE | PUSH, MERGE, PR, HEAD, APPROVAL, TRANSPORT, BUNDLE, ORDER, PUBLISH, RESUME |
| SESSION | USAGE, CLEAR, HANDOVER, SESSION, SESSIONS, COMPACTION, CHECKIN |
| OTHER | none of the above |

## 2. Inputs

| input | source | pin | state |
|---|---|---|---|
| K1 `handoff/*.md` (17 files) at the bridge's working tree of 2026-11-05 | the bridge | per-file sha256 recorded in the run record | read by script for MON ids and the word "rule" only; no line is printed |
| I1 rows (`RL-01/data/I1_rows.tsv` 6c5a1c58) and RL-05 rows (`RL-05/data/predicate_rows.tsv` dd4f5600) | the lab's allowlist extractions of the merge-decision records | PINNED | throughput and cost fields |
| I2 (808bf769) | RL-01 | PINNED | verify wall time per harness-onion run |

## 3. Design

- Series: merges per ISO week by repository class; verify seconds per merged record (I1 elapsed) and per
  harness-onion run (I2); review rounds per merged record (RL-05 n_reviews); medians and ranges.
- Taxonomy: counts per category for all ids and for the rule subset; the split of slot-bound rule ids at the median
  slot; the fraction in (b). Deterministic; no seeds.

## 4-6. Compute, criteria, privacy

Light: `research/tools/rl06_process.py` (stdlib, `python3 -I -B`), seconds. Criteria as above. Outputs hold counts,
category names, slot numbers, dates and medians; no id text other than category names leaves the script; scanned.
