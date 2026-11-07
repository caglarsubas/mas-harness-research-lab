# RL-09 preregistration: the allowlist join (H-18)

Status: FROZEN v1 (2026-11-05, light; MON-RL-M11/M12 "go ahead"). Integrity check before the freeze, disclosed:
the records' top-level structures, the specification's headings, the count and line range of its enumerated
counterexamples (18-28), the shapes of the seccomp duties' `source` citations (specification file and line) and of
the SELinux assertions' `ref` (section and clause tokens), and the count of rows carrying a clause token (22 of 69
duties; 135 of 214 assertions). No join was computed before the freeze.

## 1. Hypothesis (falsifiable)

H-18: the union of seccomp rows, SELinux matrix rows, descriptor sets and T04 proofs covers every effect path the
threat model names, with a finite residual list. Stated over the records the export holds:

- Universe U: the effect paths the host-interface specification names as counterexamples. The export enumerates
  counterexamples 18-28 (section 9 of the resolved specification, each with a "Required:" sentence); counterexamples
  1-17 are counted by the plan record (17) but not enumerated in any exported file. U = {18..28}; 1-17 are declared
  UNRESOLVED-by-input before the run.
- Covering rows, by record family: (S) seccomp duties (69 rows over 7 roles; each cites a specification line);
  (M) SELinux assertions (214; each cites a section and clause tokens, with a statement); (D) descriptor-set items:
  the host-interface amendments' DECIDED items and obligations (HS53 and HE5); (T) T04 proofs: the amendments'
  obligations and items whose text names T04.
- A row covers path N when (a) a seccomp duty's cited line lies inside N's text range in the resolved
  specification, or (b) the row's citation or statement contains a clause token of N's "Required:" sentence
  (tokens of the form P2, A3, S4, C4, C6, I07, v2, or a backticked identifier such as `name_connect`), excluding the
  generic W01 token. A path is RESIDUAL when a record's own residual entry (the amendments' `residuals`, the
  specification's section 6.3 and 8) names it or one of its tokens.
- Gate: H-18 PASS on U when every path in U is covered by at least one row or is RESIDUAL, and the residual list is
  reported in full; FAIL when a path in U is neither covered nor residual; UNRESOLVED when a path's "Required:"
  sentence yields no token (the join cannot be attempted for it). Overall H-18: the verdict on U, with 1-17
  UNRESOLVED-by-input named. This is a documentary join (citations and tokens), not a semantic proof that the rows
  enforce the requirement; the report says so.

## 2. Inputs (sha256 prefixes in `data/inputs.txt`; all inside the architecture export 948a20fa at afee03b9)

| input | file |
|---|---|
| Z1 resolved specification (counterexamples 18-28, section 9; residual sections 6.3 and 8) | host-interface-inputs/resolved/HOST_INTERFACE_SPEC.md |
| Z1' HS53 specification (the same sections after amendments; used to confirm the counterexample text is unchanged) | host-interface-amendment-hs53/HOST_INTERFACE_SPEC.md |
| Z2 seccomp allowlists v5 (roles, duties: row, rules, source) | seccomp-allowlists-v5/allowlists.json |
| Z3 SELinux matrix v4 (assertions: id, ref, statement, class, perms) | selinux-matrix-v4/matrix.json |
| Z4 host-interface amendments HS53 and HE5 (items, obligations, residuals) | host-interface-amendment-hs53/amendment.json, host-interface-amendment-he5/amendment.json |
| Z5 host-interface plan (the count of counterexamples, 17 base) | host-interface-plan.json |

## 3. Design, compute, privacy

Deterministic text join by script (`research/tools/rl09_join.py`, stdlib, `python3 -I -B`), seconds. Outputs: per
path the covering row ids by family, the residual flag, the token set; counts; no specification text beyond
the tokens and row ids leaves the script. Scanned before reporting.
