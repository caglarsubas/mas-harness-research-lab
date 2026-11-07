# RL-09 report: the allowlist join (H-18), 2026-11-05

**Asked.** Does the union of seccomp rows, SELinux matrix rows, descriptor sets and T04 proofs cover every effect
path the threat model names, with a finite residual list?

**Measured.** From harness-onion's published architecture records at main afee03b9: the host-interface
specification's enumerated counterexamples 18-28 (each with a "Required:" sentence naming the mechanism), joined
by citation and clause token to the 69 seccomp duties (v5), the 214 SELinux assertions (v4), the 23 items and
obligations of the HS53 and HE5 amendments, and the 8 rows among them that name T04. Counterexamples 1-17 are
counted by the plan record but enumerated in no published record (the monitor confirmed by a names-only search), so
they are UNRESOLVED-by-input. The join is documentary: a row covers a path when it cites the path's lines or one of
its required clause tokens.

| path | required mechanism (tokens) | covering rows | status |
|---|---|---|---|
| 18 | admission rule A3 | none | UNCOVERED |
| 19 | S4, RefuseManualStart, containment boolean | 1 seccomp, 8 SELinux; residual named | COVERED |
| 20 | P2 name_connect | 9 SELinux, 1 amendment (T04) | COVERED |
| 21 | connection rule C6 | none | UNCOVERED |
| 22 | connection rule C4 | none | UNCOVERED |
| 23 | (no token: "refusal; writer ...") | not attempted | UNRESOLVED |
| 24 | (no token: "profile ...") | not attempted | UNRESOLVED |
| 25 | AF_UNIX connectto | 7 SELinux, 1 amendment (T04) | COVERED |
| 26 | P2, P4 | 3 SELinux | COVERED |
| 27 | v2 (generic token; weak) | 1 seccomp, 3 amendment; residual named | COVERED (weak) |
| 28 | cgroup dir search, prog_run | none | UNCOVERED |

**Verdict: FAIL as preregistered** (RESULTS.json). Four of the eleven enumerated paths are covered by no row of any
of the four record families, and two could not be joined. The pattern of the uncovered four is the finding: their
required mechanism is the effect gate's own admission or connection rule (A3, C4, C6) or a cgroup directory search,
which kernel allowlists, the MAC matrix and the descriptor amendments do not state. The threat model's effect paths
are not all kernel paths, so a union of kernel-level records cannot cover them. The residual list is finite and
recorded (two amendment residuals; the specification's open items).

**What it means.** H-18 as worded picks the wrong closure: the covering set needs a fifth family, the gate-channel
and admission-semantics contracts (I05 v4, the admission semantics v2), which the lab did not include because the
hypothesis names four. With them the join may well close on 18-28; that is a v2 under a new id, not a re-run.

**What it does not show.** Nothing about paths 1-17; nothing semantic (a citing row may not enforce what is
required); path 27's coverage rests on a generic token; the token extraction misses two paths whose requirement is
stated in prose. The export's version choice (v5 seccomp, v4 matrix, HS53 and HE5 amendments) is the current one;
older versions were not joined.

**Proposal.** RL-09-PROPOSAL, a design read for the visionary through the monitor, small and not a roadmap shift: a
note on the threat-model record that each counterexample's "Required:" sentence should name the record family that
enforces it (kernel allowlist, MAC matrix, descriptor amendment, gate rule), so that coverage becomes a checked
join rather than a documentary one; and the register's H-18 should read "the union of the kernel-level records and
the gate-channel contracts".
