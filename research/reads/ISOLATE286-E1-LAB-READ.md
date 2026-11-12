# Research-Lab read of R00's isolation tool isolate286.py (E1) before its first credited use, 2026-11-09

Asked by the monitor (MON-286-E1-READ; light, paper only, rounds paused) as the non-author reader named by
CONTRACT_286 r3 section 3.11 (MON-286-CR1 (3)). Inputs: the lane tool `TOOLS r00/slot286/isolate286.py` (sha256
6ecd8c7a, 178 lines, both confirmed), CONTRACT_286 r3 (19c3b7c2, 671 lines) section 3.11 and the C1-6 closure in
section 12, and the lab's own read CONTRACT-286-QC2-LAB-READ.md (557fa451). Run: the tool's `--self-test` only, under
the profile interpreter with `-I -B`: `ISOLATE286 SELF-TEST 8/8 OK`, exit 0, no file written. No other run, no network,
no read of the reader's code, of the repository tree or of any file beyond the tool and the contract. This read is
bound to tool digest 6ecd8c7a; a revised tool needs a new read (light).

## 1. Verdict: FINDINGS, not PASS

The tool's shape is E1's: a git-archive export of the record's head (MON-SCRATCH-COPY), the head checked against the
record's headSha, each restored path's base blob confirmed by digest before it is written, node collection after the
restore (so a removed or renamed node is collected from the base test file, the case the lab's read expected), only
the named nodes run, serially, under the runner's allowlisted names with TMPDIR under the output directory, PASS only
when every node's restored outcome equals its recorded one, an empty node set FAIL, a node missing from the ledger or
from the run never equal to anything, environment values digested, the record's members as the closure lists them,
and the record bound by headSha and the record line's digest. Two findings make the instrument give wrong answers on
cases the contract names, so the first credited use waits for them; three are trust conditions the tool should
enforce rather than assume; the rest are minor.

## 2. Findings that block the first credited use

- **A1, the two outcome mappings are not one function (false FAIL).** The recorded outcome is `overall()` over the
  ledger's per-phase outcomes (setup skipped = skipped, any failed = failed, else passed); the restored outcome is a
  word parsed from `pytest -rA`'s short summary, whose SKIPPED lines carry a location and reason and no node id (the
  self-test pins exactly that). So a node whose recorded or restored outcome is a skip can never match: recorded
  skipped and restored skipped reads "not run", FAIL; a `pytest.skip()` inside the test body (setup passed, call
  skipped) is "passed" on the ledger side and "not run" on the run side, FAIL; XFAIL maps to skipped on the run side
  and to passed on the ledger side, FAIL. Every such case is a false restart, and the pass-turned-skip the lab named as
  the likely explained event is one of them when it is checked from the other direction. The contract's record member
  is also "the outcome per phase in each" of recorded, live and restored; the tool writes one collapsed word. Fix: one
  function over per-phase data on both sides, and per-phase triples in the record. The per-phase data of the restored
  run can come from a verbose run parsed per node id, from a junit file, or from the head's own reader hooks (which
  compute live per-phase outcomes for the shadow record and would compute them for the scratch run by the same code).
- **A2, the restored set is taken from the record, not derived (false PASS possible).** E1 restores every changed
  declared input of the layer and nothing else. The tool writes every `restoredPaths` entry of the record's event
  after confirming its base digest, but never checks that the path is one of the layer's attested inputs in the
  ledger, nor that the list is complete. An extra path that is not a declared input would restore an undeclared cause
  too and read PASS where E1 says class A; a missing changed declared input only produces a false FAIL. Fix: derive
  the set as the layer's attested inputs whose blob at the head differs from the blob at `writingCommit`, require it to
  equal the record's list (paths and digests), and refuse on any difference. The ledger and git are already in hand.

## 3. Trust conditions the tool should enforce

- **B1, the ledger is read from the head tree unverified.** `architecture/chain-checkpoint/record.json` at the head
  supplies `writingCommit`, the layer's test file and every recorded outcome. Nothing binds those bytes to the ledger
  the verify compared against. Fix: compare the file's sha256 with the ledger digest the shadow record names (or the
  attested digest) and write it into the isolation record.
- **B2, the environment allowlist comes from the head's bytes.** `CHILD_ENVIRONMENT_ALLOWLIST` is parsed from the
  scratch copy's `ci/run_packet_argv.py`, which the packet under verify may have edited. Fix: parse the same name at
  `writingCommit` (or the verifier's pinned runner) and refuse when the two lists differ, unless that path is itself a
  restored declared input.
- **B3, the event's form is assumed, not checked.** The tool reads `slot`, `kind`, `nodes`, `restoredPaths[{path,
  baseSha256}]` and `statement` from the reader's event and `layers.<slot>.live` keyed by a 12-hex prefix; the
  contract states the isolation record's members, not this event's, and the self-test's event has no `statement`
  (main would stop on it with a traceback, not a message). Fix: pin the event's exact members in a vector 41/42 fixture
  and validate them before any export, with one refusal message each.

## 4. Binding and record form

- **C1, the record line's canonical form.** `shadowRecordLineSha256` is the digest of the prefix, one space and the
  stripped JSON body, a reconstruction rather than the line's bytes. Any other party computing "the sha256 of the
  shadow record line" must use the same form, or the PASS credits nothing. Fix: state the canonical form in section
  3.11 (the tool's is fine) and have the reader print exactly it.
- **C2, members.** `schemaVersion` is written beside the closure's list ("exactly these members"); pin it in the
  contract. `labReadSha256` is recorded as typed, unchecked; require 64 hex. Per-phase forms per A1.

## 5. Minor

- A `restoredPaths` path is joined to the scratch directory as given; a path with `..` or a leading slash would write
  outside it. Refuse non-normalised or absolute paths and any path not in the head tree.
- The output-directory checks are `assert` statements; under `-O` they vanish. Use explicit checks.
- Every refusal is a `SystemExit` before any record is written, so a refused isolation leaves only the message; the
  count rule then rests on the deadline. State in 3.11 that a refusal is a FAIL for the count, or write a record.
- Serial execution is by one pytest process; if the head's pytest configuration adds xdist options, pass `-p no:xdist`
  (or `-n 0`) to keep the contract's "serial".
- Node digests are taken as sha256 of the node id line `--collect-only -q` prints; the ledger writer's convention
  must be the same (a mismatch only refuses, "differing nodes are not collected"). Nodes whose ids contain spaces do
  not match the summary regex's `\S+`.

## 6. What the self-test covers

Parsing the record line behind noise, selecting the event, `overall()` on three phase patterns, the summary regex on
a PASSED, a FAILED and a SKIPPED line, and `decide()` on a pass, a fail and an empty set. It does not exercise the
export, the restore, the collection, the binding digest, the environment, the record's members or any refusal path.

## 7. Not claimed

No claim about the reader's event form, its live-outcome keys or the ledger writer's node-digest convention beyond
what the tool assumes; no scratch run; no read of CONTRACT_286 outside sections 3.11 and 12; nothing about the verify
time of E1.
