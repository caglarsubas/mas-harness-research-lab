# Research-Lab progress by scope (the owner's reading view; kept current at every result)

Owner instruction (2026-11-06, in the lab session): work like a research team following a scientific procedure, keep a
progress document per scope the owner can read, and use deep search when the question is "what others have done so
far". The procedure the lab follows, per scope:

1. Observe: what is going on in the roadmap, the repositories, the architecture and the PRs, and why this scope matters now.
2. Hypothesise: what could be done for better performance, accuracy, assurance or cost (the register's H-rows).
3. Collect: the data the hypothesis needs, from the platform's own records, the repositories' exports and the literature
   (digest-pinned; outside sources through deep search, recorded with their identifiers).
4. Design and test: a preregistration, an independent review of it, the run, a verdict in the ledger form.
5. Report and prove: a one-page report with what was measured, what it means and what it does not show; proposals to the
   roadmap visionary through the lane monitor.

| scope | question | document | experiments so far |
|---|---|---|---|
| S1 | How much does re-proving the whole history cost, and what does the signed checkpoint buy? | `S1-history-chain.md` | RL-01, RL-07, RL-08, RL-16; the condition (v) read |
| S2 | Do reviews, the oracle and the verifier find different things, and does the programme's own process leave a measurable trace? | `S2-review-and-process.md` | RL-02, RL-05, RL-06, RL-14 |
| S3 | Are the multi-agent contracts (topology, board, run manifest, ledgers) correct, replayable and implementable by another runtime? | `S3-coordination-contracts.md` | RL-03, RL-04, RL-13, RL-17, RL-18, RL-20, RL-21, RL-22 |
| S4 | Is the host's enforcement complete and is its evidence one algebra? | `S4-host-enforcement.md` | RL-09, RL-10, RL-11, RL-12 |
| S5 | Can the programme's planning and literature records be checked by script? | `S5-records-as-data.md` | RL-15, RL-19 |
| S6 | What have others done, and what does it change in our hypotheses? | `S6-literature.md` | the RS-1/RS-2/RS-3 reads, the five held papers, the fetch asks |

Every document has the same six sections (Observe, Hypotheses, Data, Experiments, Results and proof, Next) and names
the records by digest. The living page `research/research.html` lists these documents beside the experiments.
