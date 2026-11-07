# RL-11 report: the widened allowlist join (H-18 widened), 2026-11-05

**Asked.** With the gate-channel contracts added as a fifth family, does the union cover every enumerated effect
path of the threat model (counterexamples 18-28), with a finite residual list?

**Measured.** RL-09's four kernel-level families (69 seccomp duties, 214 SELinux assertions, 23 amendment items and
obligations, the T04 rows among them) plus the fifth family from the same export: 1,541 vector rows of the
effect-gate channel (I05 v1-v4), the admission semantics (v2-v4) and the policy-writer channel (I07 v1-v3), with
their READMEs, authorities, the artifact-edge registry and the edge-record authorities as text rows; and R10's
cited transcript ids (via the monitor), all fourteen found in the v3 gate-channel vectors. The token rule was
widened to the whole counterexample text before the run.

| path | status | strongest covering rows |
|---|---|---|
| 18 admission rule A3 | COVERED | 5 cited transcripts (T28, T31, T30, T90, T27); many G rows via generic tokens |
| 19 containment restart | COVERED | 1 seccomp, 8 SELinux |
| 20 leftover kubeconfig | COVERED | 9 SELinux, 1 amendment (T04), 8 G |
| 21 connection rule C6 | COVERED | cited T25; G rows |
| 22 connection rule C4 | COVERED | 8 cited transcripts (certificate, request, stamp-none; C2 via T02, T03) |
| 23 I07 WRITE_OBJECT kind | COVERED | 9 G rows, 2 seccomp, 1 SELinux |
| 24 aggregated ClusterRole | UNRESOLVED | no token under the widened rule; not joinable |
| 25 datastore restore | COVERED | 6 seccomp, 7 SELinux, 2 amendment (T04) |
| 26 CSR approval | COVERED | 3 SELinux, 18 G |
| 27 CAP_SYS_ADMIN reader | COVERED | 22 G, 3 amendment, 1 seccomp, 1 SELinux (v2 generic) |
| 28 cgroup O_PATH detach | COVERED (documentary) | one README mention only; no vector, row or proof |

**Verdict: UNRESOLVED** (RESULTS.json): no path is uncovered, one path (24) cannot be joined by any token its text
yields, so the gate is inconclusive rather than PASS. Against the visionary's expected cells (MON-RL-M17) the join
agrees: 18 and 21 pinned by vector, 22 closed by the model through C2's flush with only T02 and T03 vectored, 28
declared and not pinned. The widening works: the four paths RL-09 could not cover are the four the gate-channel
vectors do cover.

**For the W03 note.** Paths 18, 19, 20, 21, 22, 23, 25, 26, 27: closed by join (18, 21, 22 on R10's cited
transcripts; 22 by the model with C2 vectored only). Path 28: documentary only; missing a T04 proof id and the
SELINUX-MATRIX-V6 rows (the routing already named). Path 24: missing a clause token or operation name for the
aggregation-controller requirement, so the next host-interface amendment can give it one. Open cells carried from
R10 and the visionary: the admission-v4 Q12/Q13 replay for A3; C6's tombstone half; the C4 stamp-equality branch
(unreachable by the model; the StampMismatch unit test goes to R10's next effect-gate packet (crates/effect-gate, the HE-005 series)); the new I05 supplementary vectors
via R00.

**What it does not show.** Nothing about 1-17; nothing semantic; the G family's large row counts for 18 and 27
come from generic tokens (CREATE, RBAC, v2) and are weak, the cited transcripts are the strong rows; 28's coverage
is a README sentence.

**Proposal.** None beyond RL-09's (each counterexample names its enforcing family), which the visionary has.
