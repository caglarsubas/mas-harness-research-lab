# Research-Lab re-read of R00's isolation tool isolate286.py v2 (E1) before its first credited use, 2026-11-09

Asked by the monitor (MON-286-E1-REREAD; light, paper only, rounds paused) after R00 revised the tool against the lab's
read of v1 (ISOLATE286-E1-LAB-READ.md, 61090ac6; v1 kept as isolate286.v1.py, 6ecd8c7a). Inputs: the lane tool
`TOOLS r00/slot286/isolate286.py` v2 (sha256 7a03e62c, 467 lines, both confirmed); CONTRACT_286 r3 (19c3b7c2)
section 3.11 and the C1-6 closure (the tool cites an r4, which is not in the contract folder; the lab read r3); and,
as the monitor allowed, the reader it pairs with at c1b (commit f70f6518 of the perf049 repository, read with
`git show` at that commit, never a working tree, never an oracle): `ci/chain_checkpoint.py`'s `_start`, `_statement`,
`_finish`, `_record`, `naming_authority`, `pin_normalised` and its constants, the writer's node-digest line, and the
root `conftest.py`'s record-line print and report hook (grep-limited lines). Run: the tool's `--self-test` only, under
the profile interpreter with `-I -B`: `ISOLATE286 SELF-TEST 33/33 OK`, exit 0, nothing written under TOOLS. No other
run, no network. This read is bound to tool digest 7a03e62c; a revised tool needs a new read.

## 1. Verdict: PASS for the first credited use, with notes on the contract text and the operating procedure

Every finding of the v1 read is closed in the tool's bytes and each closure matches the reader it pairs with:

- **A1 closed.** `agrees(recorded, observed)` is the reader's rule in `_finish` (observed exists and equals the
  recorded value on every phase the ledger recorded); both sides are per-phase outcomes from `report.outcome` per
  `report.when` (the conftest's hook for the verify, the in-memory plugin for the restored run), so a setup skip, a
  `pytest.skip()` in the body and an xfail are the same words on both sides. The record keeps per-phase triples for
  recorded, live and restored; a node not run is None and never agrees.
- **A2 closed.** The restored set is derived from the ledger's layer (validator, authority, test file, inputs) as the
  files whose blob at the head differs from the blob at `writingCommit`, each base blob required to hash to the
  ledger's digest, and must equal the event's `restoredPaths` in paths and digests (the reader's `_changed` lists the
  same files: every attested file whose live digest differs, demoted and cascade-replayed alike). An extra or missing
  path, or a differing digest, refuses.
- **B1 closed.** The ledger at the head must be named by the shadow record's naming authority (the same rule as the
  reader's `naming_authority`: `newFiles` or `changedFiles[...].afterSha256`) and equal the event's `ledgerSha256`,
  which the reader sets from the bytes it compared against; the exported ledger is checked again after the archive.
- **B2 closed.** The allowlist is parsed at the head and at `writingCommit`; a difference refuses unless the runner is
  itself a restored attested file, in which case the base list applies.
- **B3 closed.** The event's eleven members are exactly the reader's (`_statement` plus `seconds` from `_finish`),
  validated with their forms before any export; the nodes run are the reader's differing nodes (a subset of the
  statement's), sorted and distinct; the shadow record's `recorded` per node must equal the ledger's.
- **C1 closed.** The canonical form `PREFIX + " " + json.dumps(record, sort_keys=True)` is byte-for-byte what the
  root conftest prints; the digest is over those UTF-8 bytes, and a non-canonical line refuses.
- **C2 closed.** `schemaVersion` is a pinned member and the lab digest must be 64 hex.
- **Minors closed.** Restored paths are normalised, contained and never through a link; no `assert`; every refusal
  and every unforeseen fault writes a FAIL record naming it (type name only for a fault); `-n 0` when the head's
  pytest configuration adds xdist options; the writer's node-digest convention is checked at `writingCommit` and node
  ids come from collection in the scratch copy.

The stated deviations (TMPDIR beside the scratch copy, `pytest.main` through `VPY -B -c`, the environment exactly the
allowlisted names present plus TMPDIR) are faithful to the closure's intent; the self-test now covers the canonical
line, the event's forms, the agreement rule, the restored-set derivation on a synthetic repository (missing, extra,
pin-line), the ledger binding, containment, the xdist pin and the refusal record.

## 2. Notes (none changes the tool's answer on a well-formed input)

- **N1, the contract text.** r4 must carry what the tool now does: the isolation record's member set gains
  `ledgerSha256`, `refusal` and `schemaVersion` beside C1-6's "exactly these members"; the canonical line form; the
  rule that a refusal is a FAIL for the count; and PIN-LINE-LIMIT with its reach (N2).
- **N2, PIN-LINE-LIMIT's reach.** The refusal fires only when the layer under isolation attests the pin-line path and
  that file's blob changed since `writingCommit`; by construction only the writing slot's own validator carries the
  pin line and is filled before the commit, so a later authored edit to that one file is the only trigger. The limit
  is narrow and conservative (FAIL, restart). Its completion, if ever needed, is to compare the base blob
  pin-normalised by the reader's own rule with the ledger digest, as the writer already does.
- **N3, two prefixed lines.** The reader's summary line and the JSON record line share the prefix; the tool takes the
  first occurrence in the file it is given and refuses when it is not JSON. The operating step must hand it the JSON
  line alone (or the tool may select the one prefixed line that parses, refusing when several do).
- **N4, dry-run records.** `dry_run_compare` writes the record as a JSON file without the prefix; when an explained
  event comes from a dry run (C1 lets a dry run serve), the line to digest is the canonical form built from that
  file's one object, and r4 should say so.
- **N5, the interpreter.** VPY is still an operator argument; the record carries the Python version and the head's
  `uv.lock` digest but nothing binds the venv to that lock. Acceptable at 286; MET-PERF-048's in-verify form removes
  the argument.
- **N6.** `-p no:cacheprovider` was dropped, so the restored run writes a pytest cache into the scratch copy; harmless.

## 3. Not claimed

No scratch run of the tool on a real record; nothing about the reader beyond the functions named above; nothing
about how often an explained event will occur in 287-296; no verify-time figure for E1.
