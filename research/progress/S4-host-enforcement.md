# S4: host enforcement completeness and the evidence algebra

**Observe.** The native profile composes seccomp allowlists, a SELinux matrix, descriptor sets and T04 proofs per
role, with gate-channel contracts beside them; Alpha 2 waits on native Linux qualification. Why now: the literature
says the primitives are mature and the risk is compositional completeness.

**Hypotheses.** H-18 (the union of the kernel-level records and the gate-channel contracts covers every effect path
of the threat model, with a finite residual); H-04 (the verdict ledger's evidence rule and the host record's evidence
classes compose into one algebra).

**Data.** The architecture export at afee03b9: allowlists, matrix, host-interface amendments, threat statements, the
verdict-ledger and native-profile records; the visionary's coverage cells; R10's cited transcripts.

**Experiments.** RL-09 (11 enumerated paths: 5 covered, 4 need the gate's own rules, 2 untestable; paths 1-17 not
enumerated anywhere published); RL-11 (widened to the gate channel: 10 of 11 covered, 24 not joinable by token);
RL-10 (clause mis-scoped per ledger: FAIL as preregistered); RL-12 (per claim: the composition holds 7 of 7; native
refusals 13 of 13 agree).

**Results and proof.** Coverage is nearly complete where the records enumerate paths, and the gap is enumeration
itself (counterexamples 1-17); the evidence algebra holds per claim with one five-level order and total maps.

**Next.** A host-interface amendment that enumerates paths 1-17 (named for R10 through the monitor); the first native
run as the case study (H-20) when CONF-LINUX-001 exists.
