# S3: the multi-agent coordination contracts

**Observe.** The platform's multi-agent runtime is contracts first: TopologySpec and the coordinator board (MAS-RA-004),
the run manifest and distribution gate (MAS-RA-002), the verdict ledger (MAS-RA-001), run events (MAS-RA-003), and the
conformance labs' simulation campaigns (CONF-MAS-001..005) with their ledgers. Why now: the literature says more
agents often hurt; the contracts bound topology by design; whether they are correct, replayable and implementable by
others decides B3's publishability and the admission gate.

**Hypotheses.** H-19 (the campaign's breaches reproduce; leases bound duplicated work); H-13 (scaling changes sign
by task shape; leases reduce duplication); H-22 (the contracts are interchange formats); H-27 (replay correctness);
H-31 (the campaign ledgers fit the run-manifest form); H-25 (a static checker over TopologySpec); H-26 (one writer
per governed state); H-23 (implementable by another runtime).

**Data.** The conformance-labs export at b4bbea79 (the harness, 13 classes, 32 seeds, ledgers); harness-onion's
architecture at afee03b9 and c1b838be (records, schemas, 85 + 95 vectors, 114 authority records).

**Experiments.** RL-03 (breaches reproduce exactly); RL-04 (640 runs: leasing's effect is the decentralized family's,
duplicates 23-63 percent under advisory claims, zero overlap when leased); RL-13 (the three contracts emit from the
schemas); RL-17 (deterministic 416 of 416; duplicates refused; the log does not replay merges through a fresh board);
RL-18 (the lab's gate reproduces all 85 run-manifest vectors; the arms study cannot be a manifest: token budget
minimum 1; agreement 7 of 9 with per-class bounds); RL-20 (a second TopologySpec implementation reproduces 52 of 52;
cycles, unreachable nodes and budget escapes are refused by the record; writers and effect paths are unexpressible);
RL-21 (one creator per published path, every change built on it); RL-22 (a README-only board machine reproduces 38 of
43; the concurrency scope and two outside models are what to ask the author).

**Results and proof.** The contracts are deterministic, their vectors reproduce from the records alone, and two
of them have been re-implemented clean-room; replay safety rests on durable state, not the event log; the paired gate
and per-class bounds answer different questions; a simulation has no token budget.

**Next.** The mid-run stale-version vector (R12); the fault-class half of H-27 (DATA-CORRECTNESS-001); the strategy
envelope when its record exists; the authority map from the creator-and-basis graph.
