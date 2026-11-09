# RL-15b preregistration: the seeded-inconsistency benchmark restated for the lock-40 roadmap builder (H-30)

Status: FROZEN v1 (2026-11-07, light; the monitor's ruling MON-RL15-M54-RULED (c) and the visionary's restated
expectation MON-RL15-D1-RESTATED, "ERRATUM to RL15-D1", folded into lock 41). A new id that names RL-15: RL-15's
PREREG v5 (1e8dfc4a), run-001, RESULTS.json and REPORT.md stand unchanged; RL-15 run-002 (2026-11-07, frozen tools
and gate on the lock-40 builder; `experiments/RL-15/runs/run-002.md`, data a60da422) is the record this restatement
corrects for its three instrument defects. First experiment under charter step 1b (instrument preflight).

Researcher degrees of freedom, declared (R7): the lab knows run-002's draws, messages and counts; the seed is kept
at 20261105 so the targets are the same instances the visionary's expectation names, and the expected counts below
are taken from that expectation, not chosen after this run. The older rules' wordings used for attribution were read
from run-001's and run-002's refusal messages (the validators' own words), never from the builder's source. The lab
read the lock-40 builder's two tag strings from the visionary's erratum.

## Hypothesis

H-30 restated (claim H-30b): on the lock-40 roadmap builder (690cff6a), every catchable seeded inconsistency
instance of the register's classes (dangling dependency; status against evidence state; score drift; a status
change without an update entry; a stale snapshot digest) and the lab's added class (a stale reference) is refused;
every refusal is attributed to a named rule, either a lock-40 rule by its tag ("(RL-15 v1)", "(RL-15 v2)") or the
older rule of `load()` that ran first; the lock-40 rules refuse at least 2 of the 3 M4 instances and both catchable
M6 instances; and no benign control edit is refused.

## Design

- Unit: one build of the work copy after exactly one edit of its `roadmap.json`; refused = the build exits non-zero
  and its last stderr line starts with `roadmap.json:`; crashed = non-zero without that prefix. The whole last stderr
  line is captured (RL-15 captured 120 characters, which cut the new process rule's attributing words for long ids).
- Base: a git-archive export of the bridge's `roadmap/` at commit ded99886 (35 tracked files) in the lab scratch;
  `build_roadmap.py` sha256 690cff6ac379da3deec621e21f614f43709ba673fe5715f6d650e196916d4901; `roadmap.json`
  a365a8f6248fd616497e43d4c95caf9ad37d6930de719ce9f6dbdc3a640ca1d6; base manifest digest (the tool's recomputation
  over the 35 files) 620799a075851f28bb7ab8966c93ecac418b19c9688ea4fe57cf2615dda03f89. The bridge's `roadmap/` is
  never built or edited.
- Layout: the work copy is `<parent>/roadmap/`, re-created from the base before every build, TMPDIR set to its
  parent; the lock-40 paper-file rule resolves a paper's recorded path from the repository root (RL-15 run-002
  attempt A failed this precondition). The tool refuses any other layout.
- Seeded edits: 6 classes x 3 instances = 18 drawn with seed 20261105 from the qualifying sets of this
  `roadmap.json` (the same instances as RL-15 run-002): M1 dangling dependency; M2 a DONE item's evidence state set
  to PLANNED; M3 a benefit factor out of scale, at zero, or removed; M4 an open item whose evidence state is already
  consistent with DONE has its status set to DONE with no update entry; M5 an unknown harness key, an unknown
  codebase id, a duplicated item id; M6 a research source's digest malformed (63 hex), a paper's digest replaced
  while its file is unchanged, a secondary paper's digest replaced. The third M6 instance is declared UNCATCHABLE
  before the run: a secondary paper names no file (34 of the 45 carry a digest, none a file), so no file comparison
  can refuse it; it is applied and reported descriptively and excluded from every denominator. Catchable denominator
  17.
- Controls: 3 benign edits a correct validator must accept: a description extended by one sentence; a dated update
  entry appended with a UTC offset (`2026-11-07T23:00:00+08:00`; lock 40's date rule requires an offset and all 280
  live entries carry one, so RL-15's offset-less control was an instrument defect); a title extended by a marker.
- Attribution, over the whole message: NEW when the message carries a lock-40 tag; OLDER when, with no tag, it
  matches one of the older rules' wordings fixed here: "unknown dependency"; "is DONE but its evidenceState is";
  "rating <factor> out of range"; "factor keys"; "harnesses needs"; "unknown codebase reference"; "duplicate item
  id"; "is BLOCKED with nothing blocking it" (a side effect of an M4 status change that unblocks another item;
  `load()`'s rules run before the lock-40 rules, so such an instance is refused there first and attributed there, as
  the erratum states). A refusal with neither is UNATTRIBUTED.
- Measures (recorded by the tool, `data/rl15b_runs.json`): qualifying targets per class; per instance the exit
  code, refused / crashed / built, the whole message, catchable, attribution (new rule, older rule or none); counts:
  catchable refused, attributed, by new rule (per class for M4 and M6), by older rule, unattributed, the uncatchable
  instance's outcome, controls refused (any non-zero exit), crashes.
- Minimum effect of interest: a class is covered when all its catchable instances are refused and attributed; the
  lock-40 rules are shown working when their tags account for at least 2 of 3 M4 and 2 of 2 catchable M6 refusals.
- Gate, evaluated in this order by `tools/rl15b_eval.py` (regions disjoint and exhaustive):
  - precondition: the unmodified copy builds (exit 0) and the layout is `<parent>/roadmap/`; otherwise UNRESOLVED
    (no verdict on the builder);
  - PASS when all 17 catchable instances are refused, 0 are unattributed, the new rules account for at least 2 M4
    and 2 M6 refusals, and 0 of 3 controls exit non-zero;
  - FAIL when any class has no catchable instance refused, or at least 1 control exits non-zero (a false positive),
    or neither new rule refuses anything;
  - UNRESOLVED otherwise (a catchable instance built or crashed, an unattributed refusal, or a new-rule count
    below the expectation), the instances named.
- Expected outcome, from the erratum (the lab's prediction before the run): PASS, with seeded refused 17 of 17
  catchable (18 of 18 minus the declared uncatchable instance, which builds), new rules M4 2 of 3 (the third M4
  instance refused first by the older "is BLOCKED with nothing blocking it" rule), M6 2 of 2, older rules 13,
  unattributed 0, controls 0 of 3. Named most-likely departure: an UNRESOLVED by one unattributed refusal if a
  validator's wording differs from the fixed list; that would be a finding about the wording list, recorded, not a
  re-tune under this id.
- Compute plan: light (22 builds, under 10 s on this host), on the monitor's word, stream S2 (the lab's own
  instrument), 0 ECU; no network; `python3 -I -B`; TMPDIR in the lab scratch; no bytecode left.
- Privacy: the tool copies no item text; the output carries item ids, field names, exit codes, the validators'
  messages and wall times; `privacy_scan.py` over every file before it is reported.

## Instrument preflight (charter step 1b), before the blind review and the gated run

Run by the lab on the scratch base, recorded in `PREFLIGHT.md` with its outputs under `data/preflight/`:
- P0 layout and precondition: the work copy is `<parent>/roadmap/` and the unmodified copy builds (exit 0); the
  tool refuses a work copy not named `roadmap`.
- P1 expressibility: each of the 21 edits, applied to a fresh copy, changes `roadmap.json`'s bytes (no no-op); the
  uncatchable instance is listed as such.
- P2 units and denominators: the evaluator on four synthetic outputs returns PASS (17/17, new rules 2/2, controls
  0), FAIL (a control refused), FAIL (neither new rule fires), UNRESOLVED (one unattributed refusal); the catchable
  denominator reads 17 in each.
- P3 known controls: one positive control (a dangling dependency seeded on an item outside the drawn targets) is
  refused with "unknown dependency"; one negative control (the offset-bearing update entry) builds with exit 0.
- P4 boundaries: a synthetic message of more than 120 characters with the tag at its end is read as NEW (the
  whole-message capture); the tag strings match the erratum's exactly.
- A failed preflight returns this PREREG to v2; the gated run never starts on an invalid instrument. The preflight
  is not the gated run: it builds the baseline and the two known controls only (3 builds).

## Inputs by sha256

| input | sha256 |
|---|---|
| mutation tool `tools/rl15b_mutate.py` | 865d57542506e327968d69c9989aefd5a0f489ba3c07b55bfc1daec9c4a60205 |
| evaluator `tools/rl15b_eval.py` | 2d6c349b221ce54e563d595a295746084f1b38a654055b862fdb831da14392de |
| roadmap/build_roadmap.py at ded99886 (lock 40) | 690cff6ac379da3deec621e21f614f43709ba673fe5715f6d650e196916d4901 |
| roadmap/roadmap.json at ded99886 | a365a8f6248fd616497e43d4c95caf9ad37d6930de719ce9f6dbdc3a640ca1d6 |
| base manifest (35 files, the tool's recomputation) | 620799a075851f28bb7ab8966c93ecac418b19c9688ea4fe57cf2615dda03f89 |
| RL-15 PREREG v5 (lineage) | 1e8dfc4a03dd9ba771282060fa13643fb4bee51c1f209e32e5e723731a51e77f |
| RL-15 run-002 output (the corrected record's data) | a60da42246cfd5880ed024fc551591fb3e5fab6c8ced94d40a592bdbc8a47d7e |

## Records

`PREREG.md` (this, frozen; digest in the register), `PREFLIGHT.md` + `data/preflight/`, `PREREG-REVIEW.md` (the
blind review, holding only this PREREG, the register row and the charter), `runs/run-001.md`,
`data/rl15b_runs.json`, `RESULTS.json` (written by the evaluator), `REPORT.md`.
