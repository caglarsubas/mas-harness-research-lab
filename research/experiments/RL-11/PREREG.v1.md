# RL-11 preregistration: the widened allowlist join (H-18 as widened per MON-RL-M15)

Status: FROZEN v1 (2026-11-05, light; MON-RL-M15 GO; MON-RL-M16 adds R10's cited inputs). New id for the widened
join; RL-09 (4387dbff) stands as the four-family result. Integrity check before the freeze, disclosed: the fifth
family's file list and sizes, each vector file's section names and id shapes, the count of files mentioning the
tokens A3, C4, C6, prog_run and "dir search" (names only), and the presence of R10's fourteen cited transcript ids
in the v1-v3 gate-channel vectors (all present in v3; T90 absent from v1). No join was computed before the freeze.

## 1. Hypothesis (falsifiable)

H-18 widened: the union of the kernel-level records (seccomp rows, SELinux matrix rows, descriptor sets, T04
proofs) and the gate-channel contracts covers every effect path the threat model names, with a finite residual list.
Universe U = counterexamples 18-28 (1-17 UNRESOLVED-by-input, as RL-09). Families: S, M, D, T as in RL-09 (same
rules); G = the gate-channel and admission records (every vector with an id and intent text in i05-gate-channel
v1-v4, admission-semantics v2-v4, i07-policy-write v1-v3; the authorities and READMEs as text rows; the
artifact-edge registry v12 and the edge-record v9/v12 authorities as text rows); R = R10's statement relayed by the
monitor (MON-RL-M16): the cited transcript ids per path, matched to G rows by id.

Token rule, widened for this id: tokens are taken from the whole counterexample text (statement and requirement),
not only the "Required:" sentence: clause tokens (P2, A3, S4, C4, C6, I07, v2, T0x), backticked identifiers, and
upper-case operation or state names of two or more letters joined by underscores or standing alone in capitals
(WRITE_OBJECT, CREATE, ARM, HELD, ADMITTED_BEFORE_INVALIDATION, CSR, RBAC), excluding the generic W01. A row covers
a path when its text (id, intent, expect, refusal, statement, ref, source line) contains a token, or when R cites
its id for the path. Residual as in RL-09 (the amendments' residuals; the specification's 6.3 and 8), plus R10's
stated gaps (the C4 stamp-equality branch declared unreachable and vectored through C2 only; no T04 proof for 28)
recorded as named residual statements.

Gate: PASS when every path in U is covered by at least one row of any family or is RESIDUAL; FAIL when a path is
neither; UNRESOLVED when a path yields no token. Per path the report names the covering family and, where none
covers, the missing clause for the next amendment (the W03 note). Documentary join, as RL-09.

## 2. Inputs

- The seven four-family files of RL-09 (`data/inputs_four_families.txt`, unchanged digests).
- The twenty-one fifth-family files (`data/inputs_fifth_family.txt`), all inside the architecture export 948a20fa.
- R: MON-RL-M16 (R10 read at 2908a12d): 18 / A3 → T28, T31, T30, T90 (+ urgent path T27); 21 / C6 → T25 (+ restart
  tests, not in the export); 22 / C4 → T05, T13, T39, T43 (certificate), T06 (request), T04 (stamp-none), closed by C2
  via T02, T03; 28 → no T04 proof names A17, A18 or A38; kernel rows exist in matrix v4.

## 3. Compute, criteria, privacy

Light: `research/tools/rl11_join.py` (stdlib, `python3 -I -B`), seconds. Criteria as in section 1. Outputs hold
path numbers, tokens, row ids and counts; scanned before reporting.
