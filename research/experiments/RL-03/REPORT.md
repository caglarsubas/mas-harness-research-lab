# RL-03 report: the adversarial campaign's breaches reproduced on a pinned export (H-19, first clause), 2026-11-05

**Asked.** Do the campaign's duplicated-work breaches (classes C2, C5, C7, C9) reproduce on a git-archive export of
the conformance-labs simulation harness at a pinned commit, and are they what the committed ledger says they are?

**Measured.** The export (sha256 90fdfe4d; conformance-labs main b4bbea79, the tree of CONF-MAS-005's merge; 23
files, no oracle members) was extracted into the lab's scratch and driven through the harness's own ledger module
in memory, under three GO'd runs on the monitor's heavy slot: one timing run (4 ms per simulation), the four class
rows over the committed 32 seeds (5 s), and the arms section, three claim policies over five classes (3 s). Every
recomputed value was compared with the committed `results.json` by JSON equality.

| check | result |
|---|---|
| classes.json digest equals the ledger's classesSha256 | yes |
| C2, C5, C7, C9 rows equal the committed rows (result, gates, quantiles, whole row) | 4 of 4 |
| arms (A1-A3 over C2, C3, C4, C5, C7) equal the committed results (quantiles, totals) | 15 of 15 |
| the only failing ratio bound is duplicatedWorkRatioPpm | yes, all four |

Defended duplicated work in ppm (p50 / p95 / max; bound p95 100,000, max 250,000): C2 0 / 133,333 / 142,857;
C5 40,000 / 178,571 / 281,250; C7 0 / 142,857 / 148,148; C9 200,000 / 285,714 / 303,030. Completion and lost work
hold in all four; the controls fire in every seed; the depth checks hold.

**Verdict: PASS** (RESULTS.json): the breaches reproduce exactly, and the harness is deterministic across the
interpreter and host the lab used. The arms add the shape of the fix space: the poison back-off policy (A3) removes
C2's duplicated work entirely (0 / 0 / 0) and the renew-aware merge (A1) removes C7's; the headroom renewal (A2)
makes every class worse; the collusion class C5 stays above the p95 bound under every policy.

**What it does not show.** Nothing about larger agent counts or about leased versus advisory claims, which is
H-19's second clause and RL-04's question; nothing about the other nine classes, which were not recomputed; a
reproduction on one host, not an independent implementation.

**Proposal.** None. The result is an input for Build-R12's campaign record through the monitor: the pinned export is a
faithful, deterministic reproduction base, and RL-04 may use it.
