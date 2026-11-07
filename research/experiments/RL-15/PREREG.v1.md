# RL-15 preregistration: a seeded-inconsistency benchmark for the roadmap build (H-30)

Status: FROZEN v1 (2026-11-05, light; the monitor's RESUME word: "Continue RL-15 (H-30) ... light, on a scratch copy of roadmap/ only, with PREREG-REVIEW first"). This file's sha256 goes into the register. The experiment never touches the bridge's `roadmap/`: a pristine copy of that directory was made in the lab scratch (the base), a sibling work copy is re-created from the base before every build, and the mutation tool refuses a base path that is not in the scratch.

Integrity check before the freeze, by counts only: the copied record holds 206 items (statuses BLOCKED, DONE, HISTORICAL, IN_PROGRESS, READY, WAITING_OWNER; evidence states CONTRACT_ADOPTED, IMPLEMENTED, PLANNED; benefit and effort as four factors each, `[value, reason]`), 272 dated update entries and a research section; the build script `build_roadmap.py` (993 lines, 17 functions) checks the record in its `load()` function through 28 calls of its `fail()`, which raises SystemExit with a message starting `roadmap.json:`; the architecture builder it calls afterwards reports failures but never blocks the build. One baseline build of the unmodified copy exited 0 in 0.82 s with nothing on stderr (the precondition; recorded again in the run record). No seeded build was run before the freeze.

Researcher degrees of freedom, declared: the five mutation classes below were fixed from the register's H-30 row before the lab read anything of the build script; after that the lab read the script's docstring, its function names, the form of `fail()` and the count of checks, and the record's key shapes (never the conditions of the 28 checks), to make each seeded edit well-formed JSON of the right shape. The record itself was written by the roadmap visionary's locks for the programme's own planning, independently of this hypothesis (R7). Dataset and validators share an author (the visionary session); this benchmark measures their agreement, not an outside standard.

## 1. Hypothesis (falsifiable)

H-30: the roadmap build's validators refuse every seeded inconsistency class (dangling dependency; status against evidence state; score drift; a status change without an update entry; a stale reference) on a scratch copy of the record, and refuse none of three benign control edits.

- Unit: one build of the work copy after exactly one edit of its `roadmap.json`; refused = the build process exits non-zero and its last stderr line starts with `roadmap.json:` (the validators' own form). A warning with exit 0, including anything the architecture builder prints, is not a refusal.
- Seeded edits, 5 classes x 3 instances = 15, targets drawn with seed 20261105 from the items that qualify:
  M1 dangling dependency: append an unknown id to an item's `dependsOn` (3 items).
  M2 status against evidence state: a DONE item's `evidenceState` set to PLANNED (3 items).
  M3 score drift: one benefit factor set to 7 (above the 1-5 scale); one set to 0 (below it); one factor key removed (3 items).
  M4 status change without an update entry: a READY item's status set to DONE with `updates` untouched (3 items).
  M5 stale reference: an unknown harness key added to an item's `harnesses`; an unknown codebase id in an item's `codebases`; an item appended as an exact duplicate of an existing one (duplicate id).
- Controls, 3 benign edits that a correct validator must accept: a description extended by one sentence; a dated update entry appended; a title extended by a marker.
- Measures: per class, refused of 3; recall = seeded refused / 15; false positives = controls refused / 3; the first 120 characters of each refusal message (the validator's words) and the wall time per build.
- Minimum effect of interest: a class is "caught" when at least one of its three instances is refused and "covered" when all three are; the hypothesis says every class is covered, and the lab would act (propose a validator) only on a class the build does not catch at all.
- Gate (regions disjoint and exhaustive over refused counts in 0..15 and control refusals in 0..3, given the precondition):
  PASS when all 15 seeded edits are refused and 0 controls are refused.
  FAIL when any class has 0 of 3 refused (a class the validators do not catch), or when at least 1 control is refused (a false positive).
  UNRESOLVED when every class has at least 1 refused but fewer than 15 in all are refused, with 0 controls refused (partial coverage inside classes; the uncaught instances are named), or when the baseline build of the unmodified copy does not exit 0 (precondition failed).
- Expected outcome class, stated in advance: M4 is the class most likely to be uncaught, since a missing update entry is a process rule rather than a shape rule; the lab expects UNRESOLVED or FAIL through M4 and says so now.
- Confounds, named: the validators and the record share an author, so a caught class may reflect that author's habits rather than a general rule; three instances per class are few; the seeded edits are the lab's operationalisation of each class, and another operationalisation could be caught differently. A PASS says the named edits are refused, nothing about edits of other kinds.

## 2. Inputs (pinned)

The base copy was taken from the bridge at commit fce8245b, where every file below is unmodified (clean in the working tree at the copy). The builds read these files from the copy only.

| input (as copied to the lab scratch) | sha256 |
|---|---|
| `roadmap/roadmap.json` | 0ac9f4764720510a043f3f7f33ca4be85a9df2618de21327db4d2d331d0e5c8c |
| `roadmap/history.json` | d0c4240649d0a538e338b093b851926ccea1cf226e4c99c4bf0e2a3f2813f8af |
| `roadmap/build_roadmap.py` | f08843e49507de6bb9034cff96fccd876b0391f66c260c5a36371d42d26d46be |
| `roadmap/build_architecture.py` | 88b233a8fe309889f6cccee5e5ceb24fee766d9a114c20072b6f62704606bdfb |
| `roadmap/architecture-sources.json` | adb28271c40d4060a5ecbaac5a0ec36e917d42c26840ec12840d0f30f85c995e |
| `roadmap/evolution-surface.json` | 52161855243bf902cbbe59d94cccdfd5c24ed71046d3cb62c283f501c31c7140 |
| `roadmap/harness-reference.json` | 90505aee326b3d33108a4fdc657250d649b8f1af16f3f437c43199b500d23753 |
| `roadmap/release-profile.json` | 8ab42038c78eab7fdd792ff7847b8cbe302d7b6a59c1b73e875e288d01e3c885 |
| `roadmap/sessions.json` | 29d38f7f611e19704f8526c66d404d1e210b2a6a9397fb8aec51ca21b6959671 |
| `roadmap/tech-stack.json` | dacc82c19dc0117e38e67b5aa45eacc1f5ee240bab502ecea22833f7f436e546 |

The record is read by the mutation tool as JSON and written back as JSON; no item text is printed or copied into the output, which holds the class, the target item id, the exit code, the refusal message's first 120 characters and the wall time per build.

## 3. Design and compute (the lab's instruments, frozen)

- Mutation tool `tools/rl15_mutate.py`, sha256 35b1bae07245eac1d6d9c93bc31869e66259c81860c535a8697aa340c53a76fc: resets the work copy from the base before every build, applies one edit, runs `build_roadmap.py` in the work copy with `python3 -I -B`, classifies the result, writes `data/rl15_runs.json` (an output). The lab's instrument, on the bridge working tree, no commit of its own (the monitor's checkpoint commits `research/**`), custody by this 64-character sha256 checked by script at the freeze. A change after this freeze is a new PREREG version.
- Evaluator: `tools/rl15_eval.py`, written before the run and frozen by sha256 in the run record (its digest is named in the ledger); it reads `data/rl15_runs.json`, applies the gate and writes `RESULTS.json` in the verdict-ledger form. The run pass writes no verdict by hand.
- Compute: light, this host, standard library, about 19 builds of under 1 s each; deterministic (the seed fixes the targets; the build is deterministic); no GO needed; stream S4, queue class X; no ECU (not a product-coupled run).
- Privacy: `privacy_scan.py` over every file of the folder before the report; the output's refusal messages are the validators' own words and are scanned like everything else.

## 4. What is PASS, FAIL, UNRESOLVED

As the gate in section 1. A FAIL or UNRESOLVED is recorded as the finding; no re-tuning of the edits, the classes or the gate under this id; a different operationalisation of a class is a new id that names this one.
